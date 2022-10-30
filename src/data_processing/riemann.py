from time import time
import numpy as np
import pandas as pd
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import seaborn as sns
import pyriemann
from pyriemann.classification import MDM
from pyriemann.utils.covariance import covariances
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from pyriemann.utils.distance import distance
import pickle
from sklearn.model_selection import KFold, cross_val_score, cross_validate

class Processing:

    def __int__(self):
        return self

    def extendSignal(self,sig, fs,target_freqs, type):
        """Applies a filter bank and extend signal
        Args:
            signal: EEG signal with the shape: (N_chan, N_sample)
            target_freqs: list of target frequencies
            fs: sampling frequency
            type: type of filterbank
        """

        frequencies = list()
        for n,val in enumerate(target_freqs):
            values = [target_freqs[n]-0.5, target_freqs[n]+0.5]
            frequencies.append(values)

        num_channels = sig.shape[0]
        N = 4
        ex_sig = np.empty((len(frequencies), sig.shape[0], sig.shape[1]))
        for i, freq in enumerate(frequencies):
            y = np.zeros(sig.shape)
            for chan in range(num_channels):
                b, a = signal.butter(N, [freq[0] / (fs/2), freq[1] / (fs/2)], type)
                y[chan,:] = signal.filtfilt(b, a, sig[chan])
            np.copyto(ex_sig[i], y)

        n_freqs, n_channels, n_times = ex_sig.shape
        ex_sig = ex_sig.reshape((n_freqs*n_channels, n_times))
        return ex_sig


    def extract_epochs(self,sig, t_min, t_max, fs):
        """ Extracts epochs from signal
    Args:
        sig: EEG signal with the shape: (N_chan, N_sample)
        sig_times: Timestamp of the EEG samples with the shape (N_sample)
        event_times: Event marker times
        t_min: Starting time of the epoch relative to the event time
        t_max: End time of the epoch relative to the event time
        fs: Sampling rate
    Returns: a list of epochs and the time signature of each epoch
    """
        offset_st = int(t_min * fs)
        offset_end = int(t_max * fs)
        len_epoch = offset_end - offset_st
        n_epochs = sig.shape[1] // len_epoch
        epoch_list = []
        for i in range(n_epochs):
            epoch_list.append(sig[:, i * len_epoch: (i+1) * len_epoch])

        return np.array(epoch_list)


class Classification:

    def __init__(self):
        return

    def riemann_mdm(self,X,y):
        """ Make a prediction using mdm classification
        Args:
            X: EEG data
            y: labels
        Returns:
            actual labels and predictions
        """
        cov_train = covariances(X, estimator='lwf')

        mdm = MDM()
        mdm.fit(cov_train, y)

        cv = KFold(n_splits=10)

        train_score = np.empty([0],dtype=float)
        train_score = np.append(train_score,cross_val_score(mdm, cov_train, y, cv=cv))
        mean_score = train_score.mean()

        ## Save pre-trained model locally using pickle
        filename = 'mdm_model.sav'
        pickle.dump(mdm, open(filename, 'wb'))

        return train_score,mean_score


class Predict:

    def __int__(self):
        return

    def predictiton(self,X_new,y_new):
        ''' Predict label of single epoch; extendSignal() should be called before to extend both X and X_new
        Args:
            X_new: new input eeg data
        Return:
            predicted frequency
        '''

        ## Call mdm_model.sav
        filename = 'mdm_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))

        actual_classes = np.empty([0], dtype=int)
        predicted_classes = np.empty([0], dtype=int)
        dist = np.empty([0],dtype=float)

        covest = covariances(X_new,estimator='lwf')
        n_matrices,_,_ = covest.shape

        actual_classes = np.append(actual_classes, y_new)
        predicted_classes = np.append(predicted_classes,loaded_model.predict(covest))

        for k in range(n_matrices):
            if predicted_classes[k] in loaded_model.classes_.tolist():
                idx = loaded_model.classes_.tolist().index(predicted_classes[k])
                dist = np.append(dist, distance(covest[k], loaded_model.covmeans_[idx], metric="euclid"))
                print('The true frequency is ' + str(actual_classes[k]) +
                    '\nThe predicted frequency is '+str(predicted_classes[k])+'\nThe distance from the centroid is '+str(dist[k])
                      +'\n'
                      )
        return actual_classes,predicted_classes


class Plotly:

    def __int__(self):
        return self

    def plot_confusion_matrix(self,actual_classes : np.array, predicted_classes : np.array,target_names):

        '''
        Plot confusion matrix
        Args:
            actual_classes: true labels
            predicted_classes: predicted labels
            target_names: label names
        Return:
            Confusion matrix
        '''

        matrix = confusion_matrix(actual_classes, predicted_classes)

        accuracy = np.trace(matrix) / float(np.sum(matrix))
        misclass = 1 - accuracy

        plt.figure(figsize=(8,6))
        sns.heatmap(matrix, annot=True, cmap="Blues", fmt="g")

        if target_names is not None:
            tick_marks = np.arange(len(target_names))
            plt.xticks(tick_marks, target_names, rotation=45)
            plt.yticks(tick_marks, target_names)

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
        plt.show()