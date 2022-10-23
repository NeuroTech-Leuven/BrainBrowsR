def Thresholding(threshold, data):
    Certainty = np.zeros(np.shape(data))
    for i in range(np.shape(data)[0]):
        dominant_frequency = np.partition(data[i], -2)[-1]
        second_dominant_frequency = np.partition(data[i], -2)[-2]
        Certainty[i][np.where(data[i] == dominant_frequency)[0][0]] = dominant_frequency - second_dominant_frequency
        if i > 0:
            Certainty[i] = (Certainty[i]*(1+Certainty[i-1]))+Certainty[i-1]
        for final_certainty in Certainty[-1]:
            if final_certainty > threshold*i:
                index = np.where(Certainty[-1] == final_certainty)[0][0]
                return [final_certainty, index]
            else:
                return False