import argparse
import explorepy
import time
import asyncio
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from explorepy.stream_processor import TOPICS
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import sys


if __name__ == '__main__':
    main()
    
###########
# Classes #
###########


class EEG:

    def __init__(self, CHANNELS, WINDOW_LENGTH, SAMPLING_RATE):
        self.CHANNELS = CHANNELS
        self.WINDOW_LENGTH = WINDOW_LENGTH  # in seconds
        self.SAMPLING_RATE = SAMPLING_RATE  # in Hz
        self.WINDOW_SAMPLES = WINDOW_LENGTH * SAMPLING_RATE
        self.clear_stored_data()

    def clear_stored_data(self):
        self.stored_data = []
        for i in range(self.CHANNELS):
            self.stored_data.append(np.array([]))
        self.timestamps = []

    def read_stream(self, packet):
        # get a chunk of data
        timestamp, eeg_sample = packet.get_data()
        # store the data
        self.timestamps.append(timestamp)
        for i in range(self.CHANNELS):
            self.stored_data[i] = np.append(self.stored_data[i], eeg_sample[i])

    def gather_data(self, explore):
        # clear the previous window
        self.clear_stored_data()
        explore.stream_processor.subscribe(callback=self.read_stream, topic=TOPICS.raw_ExG)
        # will keep running until time.sleep stops.
        time.sleep(self.WINDOW_LENGTH)

    def get_data(self):
        return (self.stored_data, self.timestamps)


class Preprocessor:

    def __init__(self, SAMPLING_RATE):
        self.SAMPLING_RATE = SAMPLING_RATE

    def update_stored_data(self, stored_data):
        self.stored_data = stored_data

    def filter_band(self, low_freq, high_freq, 
                          type_of_filter, order_of_filter):
        """
        Applies a bandpass filter to the signal 
        Args:
            data: EEG signal with the shape: (N_chan, N_sample)
            lf: Low cutoff frequency
            hf: High cutoff frequency
            fs: Sampling rate
            type: Filter type, 'bandstop' or 'bandpass'
        Returns:
            (numpy ndarray): Filtered signal (N_chan, N_sample)
        """
        N = order_of_filter
        lf = low_freq
        hf = high_freq
        sr = self.SAMPLING_RATE
        b, a = signal.butter(N, [lf / (sr/2), hf / (sr/2)], type_of_filter)
        self.stored_data = signal.filtfilt(b, a, self.stored_data)

    def channel_selection(self, channel_mask):
        stored_data = np.array(self.stored_data)[channel_mask]
        self.stored_data = stored_data.squeeze()

    def channel_average(self): 
        self.stored_data = np.mean(self.stored_data, 0)

###############
# Definitions #
###############


def setup_connection():
    parser = argparse.ArgumentParser(description="online pipeline for BrainBrowsR")
    parser.add_argument("-n", "--name", dest="name", type=str, help="Name of the device.")
    parser.add_argument("-c", "--chan", dest="chan", type=int, help="number of channels")
    parser.add_argument("-w", "--win", dest="win", type=int, help="window length")
    parser.add_argument("-s", "--sr", dest="sr", type=int, help="sampling rate in Hz")
    parser.add_argument("-d", "--dur", dest="dur", type=int, help="duration to stream")
    args = parser.parse_args()
    explore = explorepy.Explore()
    explore.connect(device_name=args.name)  # Explore_849D
    CHANNELS = args.chan
    WINDOW_LENGTH = args.win
    SAMPLING_RATE = args.sr
    STREAM_DURATION = args.dur
    return (explore, CHANNELS, WINDOW_LENGTH, SAMPLING_RATE, STREAM_DURATION)

#################
# Main Pipeline #
#################


def main():
    # run command line: python online_pipeline.py -n Explore_849D -c 8 -w 4 -s 250 -d 20

    # initialize classes
    explore, CHANNELS, WINDOW_LENGTH, SAMPLING_RATE, \
        STREAM_DURATION = setup_connection()                # headset connection set up
    eeg = EEG(CHANNELS, WINDOW_LENGTH, SAMPLING_RATE)       # eeg receiver class
    preprocessor = Preprocessor(SAMPLING_RATE)              # preprocessor class

    # initialize constants
    CHANNEL_MASK = [False, False, False, True, True, True, True, True]

    # start the timer
    start_time = time.time()

    while time.time() - start_time < STREAM_DURATION:
        eeg.gather_data(explore)
        preprocessor.update_stored_data(eeg.stored_data)
        preprocessor.channel_selection(CHANNEL_MASK)
        preprocessor.channel_average()
        preprocessor.filter_band(low_freq=0.5, high_freq=35, type_of_filter="bandpass", order_of_filter=4)
        print(np.shape(preprocessor.stored_data))

    explore.disconnect()   # disconnect the headset
    sys.exit()             # shut down Python


