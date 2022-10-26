#!/usr/bin/env python
from distutils.command.config import config
from tkinter import N
import explorepy
import asyncio
import json
import websockets
import numpy as np
from scipy import signal
import time

from src.data_processing.eeg import EEG
from src.data_processing.preprocessing import Preprocessor
from src.data_processing.cca import Classifier
from src.data_processing.thresholding import Thresholding

class BrainServR:

    def __init__(self):
        self.DEVICENAME = "Explore_849D"
        self.CHANNEL_MASK = "01101000"
        self.WINDOW_LENGTH = 4
        self.SAMPLING_RATE = 250
        self.FOCUS_LENGTH = 3
        self.THRESHOLD = 0.15
        self.CHANNELS = self.CHANNEL_MASK.count('1') # get number of active channels
        self.FREQS = [6,12,10,8]

        self.explore = self.connectHeadset()
        self.eeg = EEG(self.CHANNELS, self.WINDOW_LENGTH, self.SAMPLING_RATE)
        self.preprocessor = Preprocessor(self.SAMPLING_RATE)
        self.cca = Classifier(self.FREQS,self.CHANNELS,0,self.WINDOW_LENGTH,self.SAMPLING_RATE)

    
    def connectHeadset(self):
        explore = explorepy.Explore()
        explore.connect(device_name=self.DEVICENAME)
        explore.set_channels(channel_mask=self.CHANNEL_MASK)

        return explore

    async def connect(self, websocket):
        await websocket.send(json.dumps("test"))
        scores_stored = np.zeros((self.FOCUS_LENGTH, len(self.FREQS)))
        eeg = self.eeg
        preprocessor = self.preprocessor
        cca = self.cca

        while True:
            eeg.gather_data(self.explore)
            # preprocessing the window 
            preprocessor.update_stored_data(eeg.stored_data)
            preprocessor.notch_filter(50) #set notch according to region
            preprocessor.filter_band(0.5,35,"bandpass", 5) #bandpass ROI
            stored_data = preprocessor.get_data()
         
        
            # classifying the window
            n_samples = np.shape(stored_data)[1]
            cca.update_number_of_samples(n_samples)
            scores = cca.classify_single_regular(stored_data, return_scores=True)
            scores_stored = np.vstack([scores_stored,scores])
            scores_stored = np.delete(scores_stored,0,0)
            print(scores_stored)
            final_certainty, index = Thresholding(self.THRESHOLD, scores_stored)
            print(index)
            print(final_certainty)
            await websocket.send(json.dumps('FU'))
            if index != -1:
                await websocket.send(json.dumps(str(index)))
                scores_stored = np.zeros((self.FOCUS_LENGTH, len(self.FREQS)))
                time.sleep(4)
    async def start(self):
        async with websockets.serve(self.connect,"",8002):
            await asyncio.Future()



if __name__ == "__main__":
    ## Establish connection with the headset
    server = BrainServR()
    ## Run the websocket server
    asyncio.run(server.start())
