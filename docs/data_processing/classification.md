# Classification

![classification](images/classification.png)

Classification tries to find a label for the unlabeled data. In BrainBrowsR's case, we try to find the frequency of the stimulus the user is looking at. Two main implementations can be used, [canonical correlation analysis](CCA.md) and methods based on [Riemanian Geometry](riemannian.md). In our current implementation, we used CCA, which requires no training as opposed to Riemannian geometry. The results of both methods in the offline pipeline can be found on [this page](results.md).

The classifier takes the filtered EEG data from [preprocessing](preprocessing.md) as input. It then calculates a score for each of the four stimuli, and the highest score should match the stimulus the user is looking at. In our case, we have added some [thresholding](thresholding.md) to increase the accuracy of our method. This thresholding takes the scores and then calculates the action.
