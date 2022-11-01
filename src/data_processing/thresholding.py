import numpy as np
###############
# Threshold #
###############
#threshold is a vector!#

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
        if Certainty[-1,j] > threshold[j]:
            return Certainty[-1,j], j
    
    return -1,-1
