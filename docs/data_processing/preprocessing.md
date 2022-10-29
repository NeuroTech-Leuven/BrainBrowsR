# Preprocessing

Writen by: Rien Sonck

## Goal

The aim of this document is to explain our rationale behind our preprocessing steps.

## Details

Preprocessing of electroencephalogram (EEG) usually consists out of the following steps: 
1) Filtering of the signal (Did we do it: Yes)
2) Downsampling the signal (Did we do it: No)
3) Rereferencing of the signal (Did we do it: No)
4) Interpolation of bad channels (Did we do it: No)
5) Channel selection (Did we do it: Yes)
6) Averaging over trials (Did we do it: No)

I will explain the preprocessing steps that we took in our project and explain why we took certain decisions. 

### Filtering of the signal 
Filtering of the signal is a crucial step as Electroencephalogram (EEG) electrodes record much noise. We can distinguish four types of noise: 
1) Environmental noise: this is noise picked up by EEG electrodes from electrical devices around us. These devices work on a powerline of 50 Hz (60 Hz in the US).
2) Electrode noise: if an electrode is lose or has a bad conductance between the scalp and the electrode this can cause a very noise signal. 
3) User noise: noise coming from the users themselves such as muscle movement (eye winks, jaw clenching, arm movement, ...). 
4) Brain noise: the brain signal that we collect is a combination of many brain processes going on at the same time. We are often only interested in one or a few brain processes. So all the irrelevant brain processes to our application can be considered as well to be noise. 

In the BrainBrowsR application, the incoming EEG signal is filtered by a notch filter at 50 Hz and a 5th order bandpass butterworth filter between 0.5 and 35 Hz. The reason we still need to use a notch filter is because the 50 Hz powerline noise is otherwise still leaking through our brandpass filter, since the roll-off (steepness of the transfer function) has not yet hit zero when reaching the 50 Hz. 

The reason we choose this filter is because the buttons in the BrainBrowsR application flicker at a rate between the 6 - 12 Hz (i.e., target frequencies). This filter will get rid of strong EEG drifts and offsets. 

User noise is more difficult to get rid of. Although muscle noise is most noticeable at the range of 110-140 Hz, it will also contaminate the frequency band that we are interested in: the alpha band.
There are many movement artefact removal methods such as independent component analysis (ICA), Denoising source seperation (DSS), ... but these methods take would take up to much time in a online-system. Thus, the best approach is to tell the user to be as still as possible when using the BrainBrowsR application.

### Downsampling the signal

Usually EEG signals are downsampled as research-grade EEG headset have a sampling rate of 1000 - 8000 Hz.
The more samples you have, to longer the processing of the signal will take. Since we only sample at 250 Hz and processes only 6 seconds of data at a time there is no need for us to downsample the signal even more.

### Rereferencing of the signal

The EEG signal is not being rereferenced in our application, because rereference to the Cz electrode will get rid of our signal.

### Interpolation of bad channels

### Channel selection

channel/electrode selection, SSVEP is a visual evoked response such that the visual cortex is the most important area for our analysis. This is why we select occipital channels: [add channels].

### Averaging over electrode channels

Averaging over electrode channels is another method that can drastically reduce noise but our classification algorithm make use of the different channels so we do not use any averaging in our preprocessing steps.  

## Implementation

The implementation of the preprocessing is done using the Python programming language.
The recorded brain activity with our [Mentalab](https://mentalab.com/)
headset is read into python by using the [explorepy](https://github.com/Mentalab-hub/explorepy) package,
for further information on reading in data, I refer you to our read-in data documentation (coming soon).

For the bandpass filter we use the scipy python package.
N = 4
b, a = signal.butter(N, [lf / (fs/2), hf / (fs/2)], type)
return signal.filtfilt(b, a, data)
scipy.signal.butter creates a butterworth filter which we then execute on our EEG data by using scipt.signal.filtfilt.

Channel selection we can do because we know which channel number correspond to which electrodes. For our headset configuration [add EEG electrode selection image].

## Results
