# Thresholding 

Written by: Nils Van Rompaey

## Goal
Our CCA algorithm returns a correlation (i.e. a value between 0 and 1) for each of the three frequencies that could be present in the signal. We do however require some way to discriminate between when the user is actually looking at one of the stimuli rather than just looking at the content of the Instagram post. To this end, we implemented a thresholding function. It assigns a certainty based on the correlations of the most recent epoch(s). This function should balance between two things:

+ It should ensure that as many 'positive epochs' (where the user is looking at a stimulus)' as possible are classified correctly. This can be achieved by lowering the threshold.
+ It should ensure that as few 'negative epochs' (where the user is looking at content) as possible cause an action to be taken. This can be achieved by raising the threshold.

## Implementation
The thresholding function takes into account the correlations of the current and of previous epochs. It calculates a measure of certainty for the current epoch by subtracting the second largest correlation from the largest correlation. If available, it also takes into account the previous score as $score[n] \* ( 1 + score[n-1]) + score[n-1]$

Once the certainty of a certain frequency surpasses the threshold, it causes an action to be sent to the extension. 

An example using three epochs and a threshold of 0.15 is given below. In this example, 10 Hz is selected after three epochs.

| *Correlations* | 8Hz | 10 Hz | 12 Hz |
|-|:-:|:-:|:-:|
| Epoch n-2 | 0.15 | 0.10 | 0.07 |
| Epoch n-1 | 0.08 | 0.18  | 0.04 |
| Epoch n (newest) | 0.10 | 0.16 | 0.09 | 

| *Certainty scores* | 8Hz | 10 Hz | 12 Hz |
|-|:-:|:-:|:-:|
| Epoch n-2 | 0.05 | 0 | 0 |
| Epoch n-1 | 0.05 | 0.10 | 0 |
| Epoch n (newest) | 0.05 | ***0.16*** | 0 |

The threshold and the number of previous epochs that are considered can be adjusted to optimise the trade-off mentioned [above](#goal). In doing so, the odds are reduced that a random frequency is mistakenly chosen in consecutive epochs and that an unwanted action is performed accordingly. 
