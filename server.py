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
        self.explore = self.connectHeadset(DEVICENAME)
        #self.eeg = EEG(CHANNELS, WINDOW_LENGTH, SAMPLING_RATE)
        #self.preprocessor = Preprocessor(SAMPLING_RATE)
        #self.cca = Classifier(freqs,n_chan,t_min,t_max,SAMPLING_RATE)

    def connectHeadset(self,deviceName):
        explore = explorepy.Explore()
        explore.connect(device_name=deviceName)
        return explore

    async def connect(self, websocket):
        for i in range(100):
            temp = input('N P L or Q :').capitalize()
            if temp == 'Q':
                break
            elif temp == 'N' or temp == 'P' or temp == 'L' or temp == 'O':
                await websocket.send(json.dumps(temp))
            else:
                print('Enter p, q, l or n ')


    async def start(self):
        async with websockets.serve(self.connect,"",8002):
            await asyncio.Future()



if __name__ == "__main__":
    ## Establish connection with the headset
    server = BrainServR()
    ## Run the websocket server
    asyncio.run(server.start())
