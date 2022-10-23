##### function that installs required packages #####
import pip
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])    

for package in ["asyncio","json","websockets","pandas", "seaborn", "sklearn", "explorepy", "argparse", "time", "asyncio", "numpy", "scipy", "matplotlib", "sys"]:
    import_or_install(package)
    
####################################################
import json
import websockets
import argparse
import explorepy
import time
import numpy as np
from scipy import signal
from explorepy.stream_processor import TOPICS
import matplotlib.pyplot as plt
import sys
import sklearn
from sklearn.cross_decomposition import CCA
import seaborn as sns
import pandas as pd
import asyncio


###########
# Classes #
###########


class EEG:

    def __init__(self, CHANNELS,CHANNEL_MASK, WINDOW_LENGTH, SAMPLING_RATE):
        self.CHANNELS = CHANNELS
        self.CHANNEL_MASK = CHANNEL_MASK
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

    def gather_data(self, explore,CHANNEL_MASK):
        # clear the previous window
        self.clear_stored_data()
        explore.set_channels(channel_mask=CHANNEL_MASK)
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
        b, a = signal.butter(N, [lf, hf], type_of_filter, fs=sr)
        self.stored_data = signal.filtfilt(b, a, self.stored_data)

    def notch_filter(self, notch_freq):

        """
        Applies notch filter around 50 Hz
        """
        sr = self.SAMPLING_RATE
        notch_freq = notch_freq
        quality_factor = 20.0
        # Design a notch filter using signal.iirnotch
        b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, sr)
        self.stored_data = signal.filtfilt(b_notch, a_notch, self.stored_data)

    def channel_selection(self, channel_mask):
        stored_data = np.array(self.stored_data)[channel_mask]
        self.stored_data = stored_data.squeeze()

    def channel_average(self): 
        self.stored_data = np.mean(self.stored_data, 0)
    
    def get_data(self):
        return (self.stored_data)


class Classifier():
    """
    methods:
    __init__()        : give initial parameters (number of channels, frequencies, ...)
    train()           : provide training data
    classify_single   : predict frequency for a single epoch (for online use)
    classify_multiple : test and visualize performance on a large dataset (for offline use)
    classify_single_regular : predict using regular CCA
    classify_multiple_regular : test and visualize performance on large dataset (for offline use)
    how to use regular CCA (example)
    cca = Classifier(freqs, n_chan, t_min, t_max, fs)
    cca.classify_single_regular(epochs[0,:,:], return_scores = False)
    how to use this class (example)
    n_train = len(epochs) // 2
    cca = CCA_extended(freqs, n_chan, t_min, t_max, fs)
    cca.train(epochs[:n_train, :, :], groundtruth[:n_train])
    cca.classify_multiple(epochs[n_train:, :, :], groundtruth[n_train:])
    make sure epochs and groundtruth do not have phase differences
    and that groundtruth contains the correct frequencies (not labels like 1/2/3)
    this code gets used in ./Dataset Arno/offline_pipeline_ECCA.ipynb and ./Dataset Arno2/offline_pipeline_ECCA2.ipynb 
    """

    def __init__(self, freqs, n_chan, t_min, t_max, fs):
        """
        Creates an object that can later be used to perform extended CCA
        Arguments:
        - freqs: a list of frequencies (e.g. [9, 11, 13, 15])
        - n_chan: number of channels/elektrodes (e.g. 4)
        - t_min: start time of an epoch (e.g. 0)
        - t_max: end time of an epoch (e.g. 2)
        - fs: sample frequency (e.g. 500)
        - n_harm: number of harmonics used for the CCA analysis (e.g. 2, seems to work the best)
        """

        self.freqs = freqs
        self.n_freqs = len(freqs)

        self.n_chan = n_chan

        self.fs = fs
        self.t_min = t_min
        self.t_max = t_max
        self.trained = False
                
    def update_number_of_samples(self, n_samples, n_harm=2):
        self.n_ts = n_samples
        
        t = np.linspace(self.t_min, self.t_max, self.n_ts, endpoint=False)
        self.sine_templ = np.zeros((self.n_freqs, 2*n_harm, self.n_ts))
        for f_index in range(self.n_freqs):
            f = self.freqs[f_index]
            for i in range(n_harm):
                self.sine_templ[f_index, 2*i, :] = np.sin((i+1)*f*2*np.pi*t)
                self.sine_templ[f_index, 2*i+1, :] = np.cos((i+1)*f*2*np.pi*t)
        

    def train(self, train_epochs, train_ground_truth):
        """
        Creates a template of training data that can be compared
        to make better predictions later on
        Arguments:
        - train_epochs: np.array that contains the training epochs,
          dimensions (n_train, n_chan, n_ts) with n_train the number of training epochs
        - train_ground_truth: np.array that contains the frequencies associated with
          each of the training epochs, dimensions (n_train)
        """
        n_epochs = train_epochs.shape[0]
        self.train_templ = np.zeros((self.n_freqs, self.n_chan, self.n_ts))
        for f_index in range(self.n_freqs):
            f = self.freqs[f_index]
            for epoch_index in range(n_epochs):
                if train_ground_truth[epoch_index] == f:
                    self.train_templ[f_index, :, :] += train_epochs[epoch_index, :, :]

        self.trained = True

    def classify_single(self, epoch):
        """
        Classifies a single epoch making use of both 
        the trained template and the harmonic template.
        Requires that train() has already been called
        Arguments:
        - epoch: np.array with dimension (n_chan, n_ts)
        """
        if not self.trained:
            print("Cannot classify because there is no training data yet")
            return None
        begin = time.time()

        scores = np.zeros(self.n_freqs)
        for f_index in range(self.n_freqs):        
            f_sine_templ = self.sine_templ[f_index, :, :]
            f_train_templ = self.train_templ[f_index, :, :]

            cca1 = CCA(n_components=1)
            cca2 = CCA(n_components=1)
            cca4 = CCA(n_components=1)

            cca1.fit(epoch.T, f_sine_templ.T)
            cca2.fit(epoch.T, f_train_templ.T)
            cca4.fit(f_train_templ.T, f_sine_templ.T)

            S_x1, S_y1 = cca1.transform(epoch.T, f_sine_templ.T)
            S_x2, _ = cca2.transform(epoch.T, f_train_templ.T)
            S_x4, _ = cca4.transform(epoch.T, f_sine_templ.T)

            S_y2, _ = cca2.transform(f_train_templ.T, f_train_templ.T)
            S_y3, _ = cca1.transform(f_train_templ.T, f_sine_templ.T)
            S_y4, _ = cca4.transform(f_train_templ.T, f_sine_templ.T)

            correlation1 = np.corrcoef(S_x1.T, S_y1.T)[0, 1]
            correlation2 = np.corrcoef(S_x2.T, S_y2.T)[0, 1]
            correlation3 = np.corrcoef(S_x1.T, S_y3.T)[0, 1]
            correlation4 = np.corrcoef(S_x4.T, S_y4.T)[0, 1]

            scores[f_index] = correlation1**2 + correlation2**2 + correlation3**2 + correlation4**2

        #print(time.time() - begin)
        return self.freqs[np.argmax(scores)] 

    def classify_single_regular(self, epoch, return_scores=False):
        """
        Classifies a single epoch with CCA.
        Arguments:
        - epoch: np.array with dimension (n_chan, n_ts)
        - return_scores: Boolean. Setting this to True will return a list with the correlation of each frequency.
                                Setting this to False (default) will return the frequency with the highest correlation.
        """
        
        scores = np.zeros(self.n_freqs)
        for f_index in range(self.n_freqs):
            
            f_sine_templ = self.sine_templ[f_index, :, :]          
            cca1 = CCA(n_components=1)
            cca1.fit(epoch.T, f_sine_templ.T)
            S_x1, S_y1 = cca1.transform(epoch.T, f_sine_templ.T)
            correlation1 = np.corrcoef(S_x1.T, S_y1.T)[0, 1]
            scores[f_index] = correlation1

        if return_scores:
            return scores
        else:
            return self.freqs[np.argmax(scores)]        
        
    def classify_multiple(self, epochs, ground_truth, plot=True):
        """
        Classifies a large set of test data and calculates the accuracy of the predictions
        Visualizes this with a confusion matrix.
        Arguments:
        - epochs: np.array that contains the test data,
          dimensions (n_epochs, n_chan, n_ts) with n_epochs the number of epochs
        - ground_truth: np.array that contains the frequencies associated with
          each of the test epochs, dimensions (n_epochs)
        - plot: boolean to indicate whether a confusion matrix should be made (default true)
        """

        n_epochs = len(ground_truth)
        predictions = np.zeros(n_epochs)
        for epoch_index in range(n_epochs):
            predictions[epoch_index] = self.classify_single(epochs[epoch_index, :, :])

        confusion_matrix = np.zeros((self.n_freqs, self.n_freqs))
        for i in range(len(predictions)):
            y = self.freqs.index(predictions[i])
            x = self.freqs.index(ground_truth[i])
            confusion_matrix[y,x] += 1

        cm_df = pd.DataFrame(confusion_matrix, index = self.freqs, columns = self.freqs)
        accuracy = np.sum([ground_truth == predictions])/len(ground_truth)


        if plot:
            ax = sns.heatmap(cm_df, annot=True, square=True, cmap="YlGnBu")
            ax.xaxis.tick_top()
            ax.tick_params(length=5, labelsize=12)
            #plt.xlabel("accuracy: "+ str(np.sum([ground_truth == predictions])/len(ground_truth)), size=10)
            
            plt.xlabel("accuracy: {0:.2f}".format(accuracy), size=10)
            plt.ylabel("prediction", size=15, labelpad=10)
            plt.title("ground truth", size=15, pad=10)
            plt.tight_layout()
            plt.show()    

        return accuracy

    def classify_multiple_regular(self, epochs, ground_truth, plot=True):
        """
        Classifies a large set of test data and calculates the accuracy of the predictions
        Visualizes this with a confusion matrix.
        Arguments:
        - epochs: np.array that contains the test data,
          dimensions (n_epochs, n_chan, n_ts) with n_epochs the number of epochs
        - ground_truth: np.array that contains the frequencies associated with
          each of the test epochs, dimensions (n_epochs)
        - plot: boolean to indicate whether a confusion matrix should be made (default true)
        """

        n_epochs = len(ground_truth)
        predictions = np.zeros(n_epochs)
        for epoch_index in range(n_epochs):
            predictions[epoch_index] = self.classify_single_regular(epochs[epoch_index, :, :])

        confusion_matrix = np.zeros((self.n_freqs, self.n_freqs))
        for i in range(len(predictions)):
            y = self.freqs.index(predictions[i])
            x = self.freqs.index(ground_truth[i])
            confusion_matrix[y,x] += 1

        cm_df = pd.DataFrame(confusion_matrix, index = self.freqs, columns = self.freqs)
        accuracy = np.sum([ground_truth == predictions])/len(ground_truth)


        if plot:
            ax = sns.heatmap(cm_df, annot=True, square=True, cmap="YlGnBu")
            ax.xaxis.tick_top()
            ax.tick_params(length=5, labelsize=12)
            #plt.xlabel("accuracy: "+ str(np.sum([ground_truth == predictions])/len(ground_truth)), size=10)
            
            plt.xlabel("accuracy: {0:.2f}".format(accuracy), size=10)
            plt.ylabel("prediction", size=15, labelpad=10)
            plt.title("ground truth", size=15, pad=10)
            plt.tight_layout()
            plt.show()    

        return accuracy



###############
# Threshold #
###############
def Thresholding(threshold, data):
    Certainty = np.zeros(np.shape(data))
    for i in range(np.shape(data)[0]):
        dominant_frequency = np.partition(data[i], -2)[-1]
        second_dominant_frequency = np.partition(data[i], -2)[-2]
        Certainty[i][np.where(data[i] == dominant_frequency)[0][0]] = dominant_frequency - second_dominant_frequency
        if i > 0:
            Certainty[i] = (Certainty[i]*(1+Certainty[i-1]))+Certainty[i-1]
        for final_certainty in Certainty[-1]:
            if final_certainty > threshold*i:
                index = np.where(Certainty[-1] == final_certainty)[0][0]
                return [final_certainty, index]
            else:
                return False



#####################
# Conncetion setup  #
#####################

def setup_connection():
    parser = argparse.ArgumentParser(description="online pipeline for BrainBrowsR")
    parser.add_argument("-n", "--name", dest="name", type=str, help="Name of the device.")
    parser.add_argument("-w", "--win", dest="win", type=int, help="window length")
    parser.add_argument("-s", "--sr", dest="sr", type=int, help="sampling rate in Hz")
    parser.add_argument("-d", "--dur", dest="dur", type=int, help="duration to stream")
    parser.add_argument("-c", "--chan", dest="chan", type=str, help="Channelmask as 0 off and 1 on")
    parser.add_argument("-f", "--foc", dest="foc", type=int, help="focus length for eeg buffer")
    parser.add_argument("-t", "--thres", dest="thres", type=float, help="thresholding factor")
    args = parser.parse_args()
    explore = explorepy.Explore()
    explore.connect(device_name=args.name) 
    CHANNELS = args.chan
    WINDOW_LENGTH = args.win
    SAMPLING_RATE = args.sr
    STREAM_DURATION = args.dur
    FOCUS_LENGTH = args.foc
    THRESHOLD = args.thres
    return (explore, CHANNELS, WINDOW_LENGTH, SAMPLING_RATE, STREAM_DURATION,FOCUS_LENGTH,THRESHOLD)

#####################
# Program execution #
#####################
############################
# Websocket async functions#
############################
#python online_pipeline.py -n Explore_849D -w 2 -s 250 -d 100 -c 01101000 -f 2 -t 0.6
def main():
    explore, CHANNEL_MASK, WINDOW_LENGTH, SAMPLING_RATE, \
        STREAM_DURATION,FOCUS_LENGTH,THRESHOLD = setup_connection()  
    CHANNELS = CHANNEL_MASK.count('1') # get number of active channels

    FREQS = [8,10,12,14]

    eeg = EEG(CHANNELS,CHANNEL_MASK, WINDOW_LENGTH, SAMPLING_RATE)       # eeg receiver class
    preprocessor = Preprocessor(SAMPLING_RATE)              # preprocessor class

    cca = Classifier(FREQS, n_chan = CHANNELS, t_min = 0, t_max = WINDOW_LENGTH, fs=SAMPLING_RATE)  # classifier class
    
    scores_stored = np.zeros((FOCUS_LENGTH, len(FREQS)))
    # start the timer
    start_time = time.time()
    while time.time() - start_time < STREAM_DURATION:
        eeg.gather_data(explore, CHANNEL_MASK)
       
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
    











if __name__ == '__main__':
    main()