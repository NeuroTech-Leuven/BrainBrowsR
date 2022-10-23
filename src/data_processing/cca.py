import time
from sklearn.cross_decomposition import CCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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