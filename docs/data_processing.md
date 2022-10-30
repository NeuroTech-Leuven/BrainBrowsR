# Data processing

On the surface, data-processing consists of three main parts: pre-processing, classification and thresholding.

## Pre-processing

Pre-processing prepares the raw EEG-data to be usable for classification. To learn more about pre-processing, see [dedicated page](./data_processing/preprocessing.md).

## Classifcation

After the data has been pre-processed, it can be classified to see which frequency is dominant in the signal. This is described on [this page](./data_processing/classification.md).

## Thresholding

The classification method will always return a result no matter the certainty. In the case of BrainBrowsR, this is not the desired behaviour. Therefore, a threshold is implemented that only takes action when a certain threshold is surpassed. The implementation of this function can be found in [this file](../src/data_processing/thresholding.py).
