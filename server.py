#!/usr/bin/env python
import time
import numpy as np
import pandas as pd
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import asyncio
from email import message
import json
import websockets
# from cca_functions import *
# from online_pipeline import *

# # intialization of variables
# # set here if you are using the simulated dataset or the mentalab recorded dataset
# path = "."
# fname_data = "/csv/SSVEP1_data.csv"
# fname_markers = "/csv/SSVEP1_markers.csv"

# gt_dict = {1:9, 2:9, 3:11, 4:11, 5:13, 6:13, 7:15, 8:15}
# fs = 500  # Hz, sampling frequency
# t_min = 0  # Start time of epoch since marker (seconds)
# t_max = 2  # End time of epoch since marker (seconds)
# screen_refresh_rate = 60
# ch_names = ["O1","Oz","O2","PO3","PO4","P7","P3","Pz","P4","P8"] # list of channel names
# lf = .5    # low frequency for bandpass filtering
# hf = 100  # high frequency for bandpass filtering
# electrodes = {  # dictionary of electrode names
#     2: "Oz",
#     3: "O2",
#     4: "PO3",
#     5: "PO4",
# }

# # read in the data
# data = pd.read_csv(path + fname_data, delimiter=",")  # EEG data
# sig = data[ch_names].to_numpy().T  # EEG signals, channels by data samples
# markers = pd.read_csv(path + fname_markers)  # event markers
# # time signature of the EEG signal
# ts_sig = (data['TimeStamp'] - data['TimeStamp'][0]).to_numpy()
# # array of time signature of the markers
# ts_markers = (markers['TimeStamp'] - markers['TimeStamp'][0]).to_numpy()
# groundtruth = markers['Code'].to_numpy()  # array of marker IDs


# # Preprocessing
# # Band-pass filter
# # filt_sig = custom_filter_band(sig, lf, hf, fs, 'bandpass')
# # extract epochs based on marker IDs
# epochs, ts_epoch = extract_epochs(sig, ts_sig, ts_markers, t_min, t_max, fs)
#from data_processing.eeg import EEG
#from data_processing.preprocessing import Preprocessor
#from data_processing.cca import Classifier


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
                await websocket.send(json.dumps())
            else:
                print('Enter p, q, l or n ')
>>>>>>> Stashed changes



# n_epochs = np.shape(epochs)[0]
# frequencies = list(set(gt_dict.values()))


async def handler(websocket):
    await runningApplication(websocket)


async def runningApplication(websocket):
        # input('klik maar')
        # epoch = epochs[i, :, :]
        # scores = perform_CCA(epoch, frequencies, fs)
        # print(scores)
        # prediction = choose_best_match(scores)[0] 
        # if prediction == 9 :
        #     await websocket.send(json.dumps('N'))
        #     print("N")
        # if prediction == 11 :
        #     await websocket.send(json.dumps('P'))
        #     print("P")
        # if prediction == 13 :
        #     await websocket.send(json.dumps('L'))
        #     print("L")
        # if prediction == 15 :
        #     await websocket.send(json.dumps('O')) 
        #     print("O")      


    for i in range(100):
        temp = input('N P L or Q :').capitalize()
        if temp == 'Q':
            break
        elif temp == 'N' or temp == 'P' or temp == 'L' or temp == 'O':
            await websocket.send(json.dumps(temp))
        else:
            print('Enter p, q, l or n ')
        # time.sleep(4)


async def main():
    async with websockets.serve(handler, "", 8002):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
