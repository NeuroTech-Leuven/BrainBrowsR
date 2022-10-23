from scipy import signal
import numpy as np

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
        b, a = signal.butter(N, [lf, hf], type_of_filter, fs=sr)
        self.stored_data = signal.filtfilt(b, a, self.stored_data)

    def notch_filter(self, notch_freq):

        """
        Applies notch filter around 50 Hz

        """
        print('13')
        sr = self.SAMPLING_RATE
        notch_freq = notch_freq
        quality_factor = 20.0
        # Design a notch filter using signal.iirnotch
        print('10')
        b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, sr)
        print('11')
        self.stored_data = signal.filtfilt(b_notch, a_notch, self.stored_data)
        print('12')



    def channel_average(self): 
        self.stored_data = np.mean(self.stored_data, 0)
    
    def get_data(self):
        return (self.stored_data)
