#!/usr/bin/env python
from distutils.command.config import config
import explorepy
import asyncio
import json
import websockets

from data_processing.eeg import EEG
from data_processing.preprocessing import Preprocessor
from data_processing.cca import Classifier


class BrainServR:

    def __init__(self) -> None:
        DEVICENAME = "Explore_849D"
        CHANNEL_MASK = "01101000"
        WINDOW_LENGTH = 2
        SAMPLING_RATE = 250
        STREAM_DURATION = 60
        FOCUS_LENGTH = 2
        THRESHOLD = 0.7
        CHANNELS = CHANNEL_MASK.count('1') # get number of active channels
        FREQS = [8,10,12,14]

        self.explore = self.connectHeadset(DEVICENAME,CHANNEL_MASK)
        self.eeg = EEG(CHANNELS, WINDOW_LENGTH, SAMPLING_RATE)
        self.preprocessor = Preprocessor(SAMPLING_RATE)
        self.cca = Classifier(FREQS,CHANNELS,0,WINDOW_LENGTH,SAMPLING_RATE)

    def connectHeadset(self,deviceName,channelMask):
        self.explore = self.connectHeadset(DEVICENAME)
        #self.eeg = EEG(CHANNELS, WINDOW_LENGTH, SAMPLING_RATE)
        #self.preprocessor = Preprocessor(SAMPLING_RATE)
        #self.cca = Classifier(freqs,n_chan,t_min,t_max,SAMPLING_RATE)

    def connectHeadset(self,deviceName):
        explore = explorepy.Explore()
        explore.connect(device_name=deviceName)
        return explore

    async def connect(self, websocket):
        scores_stored = np.zeros((FOCUS_LENGTH, len(FREQS)))
        eeg = self.eeg
        preprocessor = self.preprocessor
        cca = self.cca

        while True:
            eeg.gather_data(self.explore, CHANNEL_MASK)
       
            # preprocessing the window 
            preprocessor.update_stored_data(eeg.stored_data)
            preprocessor.notch_filter(notch_freq=50) #set notch according to region
            preprocessor.filter_band(low_freq=0.5, high_freq=35, type_of_filter="bandpass", order_of_filter=5) #bandpass ROI
            stored_data = preprocessor.get_data()
        
            # classifying the window
            n_samples = np.shape(stored_data)[1]
            cca.update_number_of_samples(n_samples)
            scores = cca.classify_single_regular(stored_data, return_scores=True)
            scores_stored = np.vstack([scores_stored,scores])
            scores_stored = np.delete(scores_stored,0,0)
            print(scores_stored)
            index = Thresholding(THRESHOLD, scores_stored)
            if Thresholding != False:
                print(index)

    async def start(self):
        async with websockets.serve(self.connect,"",8002):
            await asyncio.Future()



if __name__ == "__main__":
    ## Establish connection with the headset
    server = BrainServR()
    ## Run the websocket server
    asyncio.run(server.start())
