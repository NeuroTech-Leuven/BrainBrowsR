import numpy as np
###############
# Threshold #
###############
def Thresholding(threshold, data):
    Certainty = np.zeros(np.shape(data))
    for i in range(np.shape(data)[0]):
        dominant_frequency = np.partition(data[i], -2)[-1]
        second_dominant_frequency = np.partition(data[i], -2)[-2]
        Certainty[i,(np.where(data[i] == dominant_frequency)[0][0])] = dominant_frequency - second_dominant_frequency
        if i > 0:
            Certainty[i] = (Certainty[i]*(1+Certainty[i-1]))+Certainty[i-1]
    print(Certainty)
    print(threshold)
    for j in range(len(Certainty[-1])):
        if Certainty[-1,j] > threshold:
            return Certainty[-1,j], j
    
    return -1,-1


def Thresholding2(threshold, scores):
    pred = np.argmax(scores)
    scores_sorted = sorted(scores)
    if scores_sorted[-1] >= 1.3*scores_sorted[-2] and scores_sorted[-1] >= threshold:
        classify = "certain enough"
    elif not scores_sorted[-1] >= 1.3*scores_sorted[-2]:
        classify = "difference too small"
        pred = -1
    else:
        classify = "correlation too small"
        pred = -1
    return pred