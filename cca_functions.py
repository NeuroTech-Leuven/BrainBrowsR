import numpy as np
from numpy import pi, sin, cos, tan, abs
import sklearn
from sklearn.cross_decomposition import CCA
from numpy.linalg import inv, eig
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Functions
def custom_filter_band(data, lf, hf, fs, type, signal):
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
    N = 4
    b, a = signal.butter(N, [lf / (fs/2), hf / (fs/2)], type)
    return signal.filtfilt(b, a, data)


def extract_epochs(sig, sig_times, event_times, t_min, t_max, fs):
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
    epoch_list = []
    for i, event_t in enumerate(event_times):
        idx = np.argmax(sig_times >= event_t)
        epoch_list.append(sig[:, idx + offset_st:idx + offset_end])
    ts_epoch = sig_times[idx + offset_st:idx + offset_end]
    ts_epoch = ts_epoch - ts_epoch[0]
    return np.array(epoch_list), ts_epoch



def perform_CCA(epoch, frequencies, fs, n_harmonics=1):
    """
    perform CCA on single epoch
    Args:
        epoch: signal of shape (# channels x # time samples)
        frequencies: frequencies
        fs: sampling frequency 
        n_harmonics: number of harmonics, default is 1 (only base frequency)
    Returns: dictionary containing {frequency: correlation}
    """
    n_samples = np.shape(epoch)[1]
    epoch_length = n_samples/fs
    t = np.linspace(0, epoch_length, n_samples, endpoint=False)
    n_frequencies = len(frequencies)
    results = dict()

    for f in frequencies:
        template = np.zeros([2*n_harmonics+1, len(t)])
        for i in range(0, n_harmonics):
            template[2*i, :] = sin((i+1)*f*2*pi*t)
            template[2*i+1, :] = cos((i+1)*f*2*pi*t)
        template[2*n_harmonics, :] = np.random.rand(len(t))
        cca = CCA(n_components=1)
        S_x, S_y = cca.fit_transform(epoch.T, template.T)
        correlation = np.corrcoef(S_x.T, S_y.T)[0, 1]
        results[f] = correlation

    return results


def choose_best_match(scores_dict):
    """ 
    Selects highest correlation
    Args:
        scores_dict: dictionary containing {frequency: correlation} as returned by perform_CCA()
    Returns: frequency, correlation
    """
    return max(scores_dict, key=scores_dict.get), max(scores_dict.values())

def get_predictions(epochs, gt_dict, fs, groundtruth, n_harmonics=1):
    """ 
    Selects highest correlation
    Args:
        epochs: array with shape (# epochs x # channels x # time samples)
        gt_dict: dictionary containing {ground truth label: corresponding frequency}
        fs = sampling frequency
        n_harmonics: number of harmonics, default is 1 (only base frequency)
    Returns: array of shape (# epochs) containing predictions
    """
    amount_correct = 0
    n_epochs = np.shape(epochs)[0]
    predictions = []
    for i in range(0,2):
        epoch = epochs[i, :, :]
        frequencies = list(set(gt_dict.values()))
        scores = perform_CCA(epoch, frequencies, fs, n_harmonics)
        prediction = choose_best_match(scores)[0]
        gt = gt_dict[groundtruth[i]]
        if prediction == gt:
            amount_correct += 1
        # print(i,': ',scores)
        # print("ground truth: ", gt, "| classifier: ", prediction)
        # print("accuracy: ", amount_correct/(i+1))
        # print("---------------")
        predictions.append(prediction)
    # print("accuracy: ", amount_correct/(i+1))
    return predictions



def create_confusion_matrix(predictions, groundtruths, gt_dict, plot=True):
    """ 
    Create confusion matrix from predictions and ground truths
    Args:
        predictions: array containing predictions with shape (# epochs)
        groundtruths: array containing ground truth labels with shape (# epochs)
        gt_dict: dictionary containing {ground truth label: corresponding frequency}
        plot: boolean, set to True to plot confusion matrix as heatmap
    Returns: array containing confusion matrix with shape (# frequencies x # frequencies)
    """
    n_freq = len(set(gt_dict.values()))
    confusion_matrix = np.zeros((n_freq,n_freq))
    frequencies = list(set(gt_dict.values()))
    groundtruth = groundtruths.copy()
    for key, value in gt_dict.items():
        groundtruth[groundtruth == key] = value
    for i in range(len(predictions)):
        y = frequencies.index(predictions[i])
        x = frequencies.index(groundtruth[i])
        confusion_matrix[y,x] += 1

    if plot == True:
        cm_df = pd.DataFrame(confusion_matrix, index = frequencies, columns = frequencies)
        ax = sns.heatmap(cm_df, annot=True, square=True, cmap="YlGnBu")
        ax.xaxis.tick_top()
        ax.tick_params(length=5, labelsize=12)
        plt.xlabel("accuracy: "+ str(np.sum([groundtruth == predictions])/len(groundtruths)), size=10)
        plt.ylabel("prediction", size=15, labelpad=10)
        plt.title("ground truth", size=15, pad=10)
        plt.tight_layout()
        plt.show()
    
    return confusion_matrix

