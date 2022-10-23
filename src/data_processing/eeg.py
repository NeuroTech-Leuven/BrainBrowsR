import time
import numpy as np
from explorepy.stream_processor import TOPICS

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