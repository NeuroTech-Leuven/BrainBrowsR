# Preprocessing

Writen by: Rien Sonck

## Goal

This document aims to explain the rationale behind our preprocessing steps.

## Details

Preprocessing of electroencephalogram (EEG) usually consists of the following steps:

1. Filtering of the signal (Did we do it: Yes)
2. Downsampling the signal (Did we do it: No)
3. Re-referencing of the signal (Did we do it: No)
4. Artifact rejection (Did we do it: No)
5. Interpolation of bad channels (Did we do it: No)
6. Channel selection (Did we do it: Yes)
7. Averaging over trials (Did we do it: No)

In the following, the preprocessing steps considered in this project and several important decisions are explained in more detail.

### Signal filtering

Filtering the signal is a crucial step as Electroencephalogram (EEG) electrodes record much noise. We can distinguish four types of noise:

1. Environmental noise: this is noise picked up by EEG electrodes from electrical devices around us. These devices work on a powerline of 50 Hz (or 60 Hz).
2. Electrode noise: if an electrode is loose or has a low conductance between the scalp and the electrode, this can cause a very noisy signal.
3. User noise: noise from the users, such as muscle movement (eye blinks, jaw clenching, arm movement).
4. Brain noise: the collected brain signal is a combination of many brain processes going on at the same time. We are often only interested in one or a few brain processes. So, all the irrelevant brain processes to our application can be considered as well to be noise.

In the BrainBrowsR application, the incoming EEG signal, see Figure 1, is filtered by a notch filter at 50 Hz and a fifth-order Butterworth filter between 0.5 and 35 Hz.

![alt text](./images/unfiltered_signal.jpg)

_Figure 1: unfiltered incoming EEG signal in the frequency spectrum._

You might wonder why we still need to use a 50 Hz notch filter if we already use a 0.5-35 Hz bandpass filter. The reason is that even when using the bandpass filter, the 50 Hz powerline will still leak through the filter due to the roll-off (steepness of the transfer function) not being steep enough, see Figure 2.

![alt text](./images/filtered_signal_bandpass.jpg)

_Figure 2: filtered EEG signal using a fifth-order Butterworth bandpass filter between 0.5-35 Hz._

When combining the Butterworth filter with the notch filter, we get a cleaner signal, see Figure 3.

![alt text](./images/filtered_signal_notch_bandpass.jpg)

_Figure 3: filtered EEG signal using a fifth-order Butterworth bandpass filter between 0.5-35 Hz and a 50 Hz notch filter._

The bandpass filter range was chosen because the target frequencies and one of the harmonics of our BrainBrowsR application are between 6-18 Hz. Furthermore, this bandpass filter also removes strong EEG drifts and offsets present in frequencies < 0.5 Hz.

User noise is more challenging to get rid of. Although muscle noise is most noticeable in the range of 110-140 Hz, it will also contaminate the frequency band that we are interested in: the alpha band.
There are many movement artefact removal methods, such as principal component analysis (PCA), independent component analysis (ICA), and denoising source separation (DSS). However, these methods would take up too much time in our online system, which works with 4-second long windows. Thus, the best approach is to tell the user to be as quiet as possible when using the BrainBrowsR application.

### Downsampling the signal

Usually, EEG signals are downsampled as research-grade EEG headsets have a sampling rate of 1000 - 8000 Hz.
The more samples, the longer the processing of the signal will take. Since we only sample at 250 Hz and process only windows of ~4 seconds of data, there is no need for us to downsample the signal even more.

### Re-referencing the signal

The EEG signal is not re-referenced in our application. We use the [Mentalab headset](../headset.md), with its reference electrode placed at AFz mentioned as GND on the Mentalab headset. The AFz electrode location is a good reference location for the SSVEP paradigm since it is located away from the occipital cortex, so we do not lose signal. However, the electrode still picks up much environmental noise. Software re-referencing to another commonly used reference electrode, like Cz, would only reduce the signal-to-noise ratio of our SSVEP signal.

### Interpolation of bad channels

A high RMS value of a channel means much variability in the channel. These channels do not contain much useful information, but by interpolating them with nearby channels, we can still extract their information. We only use three channels, so the data would be useless if one or more channels were bad. Therefore this is not included in the preprocessing.

### Channel selection

Channel/electrode selection, SSVEP, is a visually evoked response such that the visual cortex is the most crucial area for our analysis. Therefore, we only use occipitally placed electrodes: O1, Oz, and O2. The electrode selection is already made on the hardware. Thus we do not need to include a channel selection in the preprocessing of the signal.

### Averaging over electrode channels

Averaging over electrode channels is another method that can drastically reduce noise. However, our classification algorithm exploits the spatial information captioned by the different electrodes, so we do not use any averaging in our preprocessing steps.

## Implementation

The implementation of the preprocessing is done using the Python programming language. You can find this code [here](../../src/data_processing/preprocessing.py). There is preprocessing class that contains the notch filter and the bandpass filter. Both are created using the [signal module from scipy](https://docs.scipy.org/doc/scipy/reference/signal.html).
The brain activity (recorded with the [Mentalab](https://mentalab.com/) headset) is read into Python by using the [explorepy](https://github.com/Mentalab-hub/explorepy) package.

## Result

With preprocessing, we can read out a signal from the headset in an online fashion and pass a clean signal to the [classification](./classification.md) code that will classify it.
