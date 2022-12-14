# Canonical Correlation Analysis

Written by: Joppe Van Rumst

## Goal

Canonical correlation analysis (CCA) is a state-of-the-art classification method for SSVEP. The goal of the method is to find the optimal linear transformation for each of the stimulated frequencies such that the correlation between two matrices, the signal and an assumption matrix for a given frequency, is optimized. The optimized correlations between an unseen signal and the assumption matrices for all frequencies can then be used to determine which frequency was attended. CCA was first applied by [Lin et al.](https://ieeexplore.ieee.org/document/4203016). At that time, it outperformed the best methods for SSVEP classification, such as power spectrum density analysis.

## Methodology

### Regular CCA

In order to use CCA, two matrices of which we want to calculate their correlation are defined. In this case, the first matrix is the multichannel EEG signal, and the second matrix contains the assumptions. These assumptions are the fundamental frequencies of one of the different targets presented with both a sine and cosine representation.

For better accuracy, the sine and cosine representation of the harmonics of the target signal could be added to the assumption matrix.

The EEG signals and the assumption matrix make a weighted linear combination. So the weights will, on the one hand, linearly combine the different EEG channels into a scalar value and, on the other hand, combine the sine and cosine components of the target signals and harmonics. Afterwards, the weighted values are summed up to get a scalar value of the multichannel EEG signal and a scalar value of the assumptions. These weights change to maximize the correlation between the two scalar values. This process is repeated for every target frequency, and the target with the highest correlation would be the target where the subject is gazing at.

The maths behind the method can be best explained by the following figure: from [Pan et al.](https://iopscience.iop.org/article/10.1088/1741-2560/8/3/036027/meta)![alt text for screen readers](./images/CCA_scheme.JPG "Text to show on mouseover").

*Figure 1. CCA scheme. ([Pan et al., 2011]([https://www.researchgate.net/publication/323358565_Riemannian_Classification_for_SSVEP-Based_BCI_Offline_versus_Online_Implementations](https://iopscience.iop.org/article/10.1088/1741-2560/8/3/036027/meta)))*

In the following derivations, three variables are defined: $M$, the number of EEG channels, $Q$, the number of samples in each time window, and $N_h$, the number of harmonics used.

To classify SSVEP signals with CCA, we construct a CCA model $\text{CCA}_f$ per target frequency $f$. The previous figure shows that $X\in \mathbb{R}^{M \times Q}$ is the multichannel EEG signal. Each row contains an EEG signal across time for a specific channel. For each of the frequencies, we construct a reference signal $Y_f \in \mathbb{R}^{2N_h \times Q}$. This reference signal consists of a sine and cosine signal for that frequency and each of the harmonics:

$$
Y_f = {\left\lbrack \matrix{
cos(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 1) \cr
sin(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 1) \cr
cos(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 2) \cr
sin(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 2) \cr
... \cr
cos(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot N_h) \cr
sin(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot N_h) \cr
} \right\rbrack}
$$

Now we define the weights: $W_{x,f} \in \mathbb{R} ^M$ and $W_{y,f} \in \mathbb{R}^{2N_h}$ which are respectively the weighting vectors for $X$ and $Y_f$. The weighting vectors filter $X$ and $Y_f$ to obtain a scalar value over time, denoted as $x_f = W_{x,f}^\intercal X$ and $y_f = W_{y,f}^\intercal Y_f$. These values are called canonical variables in the literature.

The idea of CCA is to find $W_x$ and $W_y$ such that the correlation between the filtered signals x and y is maximized. The optimization problem:

$$\eqalign{
\rho_f &= \max_{W_{x,f}, W_{y,f}}\frac{E[x_f y_f^{T}]}{\sqrt{E[x_f  x_f^\intercal]E[y_f y_f^\intercal]}} \\
 &=\max_{W_{x,f}, W_{y,f}}\frac{E[W_{x,f}^\intercal X  Y_f^\intercal W_{y,f}]}{\sqrt{E[W_{x,f}^\intercal XX^\intercal W_{x,f}]E[W_{y,f}^\intercal Y_f Y_f^\intercal W_{y,f}]}}
}$$

The correlation value is saved for all the different stimulation frequencies. The one with the highest correlation value is the winner.

### Extended CCA

![Extended CCA diagram](./images/extended_CCA_diagram.JPG "Extended CCA diagram")

*Figure 2. Extended CCA scheme. ([Nakanishi et al., 2015](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4610694/))*

To explain extended CCA, you first must understand the basic principles of Individual template CCA (IT-CC). This method was first introduced to detect temporal features of EEG signals using the canonical correlation between the test data and individual template signals.
Here, the correlation is not calculated between the signal and precalculated template signals but between the signal and template signals determined from responses obtained in a training phase.

In the case of SSVEP, the template signal is calculated for each frequency. For a given set of $N_t$ training signal trials $\mathcal{X} = \{X_i \in \mathbb{M\times Q}\}_{i = 0 \ldots N_t}$, the template signals are $$\bar{X}_f={\frac{1}{N_{t,f}}}{\sum_f{\mathcal X}}$$ when using code modulated visual evoked potential.
Now we can replace the reference signals $Y_f$ of the standard CCA with the individual template $\bar{X}_f$, which will give us the following:

$$
\rho_f = \max{W_{x,f},W_{y,f}}\frac{E[W_{x,f}^\intercal X \bar{X}_f^\intercal W_{y,f}]}{\sqrt{E[W_{x,f}^\intercal XX\^intercal W_{x,f}]E[W_{y,f}^\intercal \bar{\mathcal X_n} \bar{X}_f^\intercal W_{y,f}]}}
$$

Extended CCA is a combination of CCA and IT-CCA. Correlation coefficients between projections of a test set $\hat{X}$ and an individual template $\bar{x}$ using CCA-based spatial filters are used as features for target identification. The three weight vectors that are used as spatial filters to enhance the SNR of SSVEP are $W_x(X,\bar{X})$ between test data $X$ and the individual template $\bar{X}$, $W_x(X, Y)$ between the test data $X$ and sine-cosine reference signals $Y$ and $W_x(\bar{X}, Y)$ between the individual template $\bar{X}$ and sine-cosine reference signal $Y$. Afterwards a correlation vector $r$ is obtained:

$$
r_f = {\left\lbrack \matrix{r_1 \cr r_2 \cr r_3 \cr r_4} \right\rbrack} = \left\lbrack \matrix{r(X^\intercal W_x(X,Y_f), Y^\intercal W_y(X,Y)) \cr r(X^\intercal W_x(X,\bar{X}_f), \bar{X}_f^\intercal W_x(X,Y_f)) \cr r(X^\intercal W_x(X,Y_f), \bar{X}_f^\intercal W_x(\bar{X}_f, Y_f)) \cr r(X^\intercal W_x(\bar{X}_f^\intercal Y_f), \bar{X}_f^\intercal W_x(\bar{X}_f, Y_f))} \right\rbrack
$$

where $r(a,b)$ indicates the Pearson's correlation coefficient between two one-dimensional signals $a$ and $b$. An ensemble classifier is used to combine the four features for the classification. In practice, the weighted correlation coefficient $\rho_n$ is employed for the final feature identification.

$$
\rho_f = \sum_{l = 1}^{4} sign(r_{f,l}) \cdot r_{f,l}^2
$$

The $sign()$ is used to retain discriminative information from negative correlation coefficients between the test trial $X$ and individual template $\bar{X}$. The individual template that maximizes the weight correlation value is selected as the reference signal corresponding to the target. [Nakanishi et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4610694/)

## Implementation

The following flowchart can explain the implementation. The code implementing this method can be found [here](../../src/data_processing/cca.py), which contains both regular CCA and extended CCA. In the current implementation, only regular CCA is used.

![CCA_diagram](./images/CCA_diagram.jpg "CCA+CCA extended implementation scheme")

*Figure 3. CCA implementation scheme.*

The filtered data from the preprocessing, together with a template containing sine and cosine signals from one reference frequency and its harmonics, is put into the CCA module. The CCA module is imported from the  [Scikit-Learn library](https://scikit-learn.org/stable/modules/generated/sklearn.cross_decomposition.CCA.html). This function returns the corresponding weighting vectors explained above. Afterwards, we apply these weighting vectors to the template and the data. Finally, we can calculate the correlation between the signals and the template. This value is stored. The process is repeated for every reference signal. The reference with the highest correlation value is picked as the winner.

The dots indicate how we could upgrade the regular CCA to the extended CCA. We could increase the method's accuracy by adding training data to the template matrix. This data is first averaged for each frequency while separating the different channels. The final template will have dimensions (`number of frequencies x number of channels x number of samples).
