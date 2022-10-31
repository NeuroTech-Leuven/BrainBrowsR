# Data processing

On the surface, the data-processing pipeline consists of three main parts: preprocessing, classification and thresholding.

```mermaid
    flowchart LR;
    Headset--Noisy Signal-->Pre-processing--Clean Signal-->Classification--Scores-->Thresholding--Action-->Extension
```

## Pre-processing

Pre-processing prepares the raw, noisy EEG data to be usable for classification. It receives this data from the EEG headset and then proceeds to filter. As a result, it sends this clean signal to the classification. To learn more about preprocessing, see [dedicated page](./data_processing/preprocessing.md).

## Classifcation

After the data has been preprocessed, it can be classified to see which frequency is dominant in the signal. The input to classification is the clean signal, and the output is the scores used by thresholding. The classification is described on [this page](./data_processing/classification.md).

## Thresholding

The classification method will always return a result no matter the certainty. In the case of BrainBrowsR, this is not the desired behaviour. Therefore, a [thresholding function](./data_processing/thresholding.md) is implemented that only takes action when a certain threshold is surpassed.
The scores of each frequency are received from classification and then compared with each other and a threshold to decide whether the correlation was strong enough. The implementation of this function can be found in [this file](../src/data_processing/thresholding.py).