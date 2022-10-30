# Canonical Correlation Analysis

Written by: Joppe Van Rumst

## Goal

Canonical correlation analysis (CCA) is a state-of-the-art classification method for SSVEP. The goal of the method is to find for each of the stimulated frequencies the optimal linear transformation such that the correlation between 2 matrices, the signal and an assumption matrix for a given frequency, is optimized. The optimized correlations between an unseen signal and the assumption matrices for all of the frequencies can then be used to determine which frequency was attended. CCA was first applied by [Lin et al.](https://ieeexplore.ieee.org/document/4203016). At that time, it outperformed the best methods for SSVEP classification, such as power spectrum density analysis.

## Methodology

### Regular CCA

In order to use CCA, two matrices of which we want to calculate their correlation are defined. In this case the first matrix is the multichannel EEG signal and the second matrix contains the assumptions. These assumptions are the fundamental frequencies of one of the different targets presented with both a sine and cosine representation.

For better accuracy, the sine and cosine representation of the harmonics of the target signal could be added to the assumption matrix.

A weighted linear combination is made from both the EEG-signals and the assumption matrix. So the weights will on one hand linearly combine the different EEG-channels into a scalar value and on the other hand combine the sine and cosine components of the target signals and harmonics. Afterwards, the weighted values are summed up to get a scalar value of the multichannel EEG signal and a scalar value of the assumptions. These weights change according to maximize the correlation between the two scalar values. This process is repeated for every target frequency, and the target with the highest correlation would be the target were the subject is gazing at.

The maths behind the method can be best explained by the following figure: from [Pan et al](https://iopscience.iop.org/article/10.1088/1741-2560/8/3/036027/meta) ![alt text for screen readers](./images/CCA_scheme.JPG "Text to show on mouseover").

In the following deriviations, three variables are defined: $M$ the number of EEG channels, $Q$ the number of samples in each time window , $N_h$ the number of harmonics being used.

As can be seen in the previous figure $X\in {\rm IR}^{M \times Q}$ is the multichannel EEG signal which contains the SSVEP response at frequency $f$, each row contains a EEG signal across time for a specific channel. For each of the frequencies, we construct a reference signal $Y_f \in {\rm IR}^{2N_h \times Q}$ is the reference signal that consist of the sine and cosine signals with frequencies including the stimulus frequency $f$ and its harmonics:

$$ 

Y_f = {\left\lbrack \matrix{
cos(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 1) \cr sin(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 1) \cr cos(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 2) \cr sin(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot 2) \cr \cdots \cr cos(2 \cdot \pi \cdot f \cdot q \cdot N_h\cdot 2) \cr sin(2 \cdot \pi \cdot f \cdot q \cdot N_h\cdot 2) \cr }\right\rbrack}
$$

The first two rows of the matrix $Y_f$ contain the signals: $$ and $sin(2 \cdot \pi \cdot f \cdot q \cdot T_s)$ and the final two rows $cos(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot N_h)$ and $sin(2 \cdot \pi \cdot f \cdot q \cdot T_s \cdot N_h)$ with $q \in \{1,2,..,Q \}$ and $T_s$ the time interval between consecutive sample points.

Now we define the weights: $W_x \in \rm IR^{M_1}$ and $W_y \in {\rm IR}^{2N_{h_1}}$ which are respectively the weighting vectors for $X$ and $Y(f)$. $X$ and $Y(f)$ are filtered by the weighting vectors to obtain a scalar value, denoted as $x = W_x^{T}X$ and $y = W_y^{T}Y(f)$. These values are called the canonical variables in the literature.

The idea of CCA is to find $W_x$ and $W_y$ such that the correlation between the filtered signals x and y are maximized. The optimalization problem:

$$
\rho (f) = \max_{W_x, W_y}\frac{E[x \cdot y^{T}]}{\sqrt{E[x \cdot x^{T}]E[y \cdot y^{T}]}}
$$

$$
\rho (f) = \max_{W_x, W_y}\frac{E[W_x^{T}X \cdot Y(f)^{T} \cdot W_y]}{\sqrt{E[W_x^{T}XX^{T}W_x]E[W_y^{T}Y(f) \cdot Y(f)^{T}W_y]}}
$$

The correlation value is saved for all the different stimulation frequencies. The one with the highest correlation value is the winner.

### Extended CCA

![Extended CCA diagram](./images/extended_CCA_diagram.JPG "Text to show on mouseover")

To explain extended CCA you first have to understand the basic principles of Individual template CCA (IT-CC).

This method was first introduced to detect temporal features of EEG signals using canonical correlation between the test data and an individual template signals $$\bar{\mathcal X}={\frac{1}{N_t}}{\sum_{h=1}^{N_t}{\mathcal X}}$$ when using code modulated visual evoked potential.

In case of SSVEP, for each target a individual template is obtained by averaging multiple training trials $\bar{\mathcal X}_n$. Now we can replace the reference signals $Y(f)$ of the standard CCA with the individual template $\bar{\mathcal X}_n$. This will give us:

$$
\rho(f)=\max{W_x,W_y}\frac{E[W_x^{T}X \cdot \bar{\mathcal X}_n^{T} \cdot W_y]}{\sqrt{E[W_x^{T}XX^{T}W_x]E[W_y^{T} \bar{\mathcal X_n} \cdot \bar{\mathcal X_n^{T}}W_y]}}
$$

Extended CCA is a combination of CCA and IT-CCA. Correlation coefficients between projections of a test set $\hat{X}$ and a individual template $\bar{\mathcal X_n}$ using CCA-based spatial filters are used as features for target identification. The three weight vectors that are used as spatial filters to enhance the SNR of SSVEP are: $W_x(\hat{X}\bar{\mathcal X})$ between test set $\hat{X}$ and the individual template $\bar{\mathcal X_n}$, $W_x(\hat{X}Y_n)$ between the test set $\hat{X}$ and sine-cosine reference signals $Y_n$ and $W_x(\bar{\mathcal X}Y_n)$ between the individual template $\bar{\mathcal X}$ and sine-cosine reference signal $Y_n$. Afterwards a correlation vector is obtained, $r_n$

$$
r_n = {\left\lbrack \matrix{r_{n,1} \cr r_{n,2} \cr r_{n,3} \cr r_{n,4}} \right\rbrack} = \left\lbrack \matrix{r(\hat{X^{T}}W_x(\hat{X}Y_n) & Y^{T}W_y(\hat{X}Y_n)) \cr r(\hat{X^{T}}W_x(\hat{X}\bar{\mathcal X_n}) & \bar{\mathcal X_n^{T}}W_x(\hat{X}Y_n)) \cr r(\hat{X^{T}}W_x(\hat{X}Y_n) & \bar{\mathcal X_n^{T}}W_x(\bar{\mathcal X_n}Y_n)) \cr r(\hat{X^{T}}W_x(\bar{\mathcal X_n^{T}}Y_n) & \bar{\mathcal X_n^{T}}W_x( \bar{\mathcal X_n}Y_n))} \right\rbrack
$$

Where $r(a,b)$ indicates the Pearson's correlation coefficient between two one-dimensional signals $a$ and $b$. For the classification an ensemble classifier is used to combine the 4 features. In practice the weighted correlation coefficient $\rho_n$ is employed for the final feature identification.

$$
\rho_n = \sum_{l = 1}^{4} sign(r_{n,l}) \cdot r_{n,l}^2
$$

Where the $sign()$ is used to retain discrimitive information from negative correlation coefficients between test set $\hat{X}$ and individual template $\bar{\mathcal X_n}$. The individual template that maximizes the weigth correlation value is selected as the reference signal corresponding to the target. [Nakanishi et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4610694/)

## Implementation

The implementation can be explained by the following flowchart.

![CCA_diagram](./images/CCA_diagram.jpg "Text to show on mouseover")

The filtered data from the preprocessing together with a template containing sine and cosine signals from one reference frequency and its harmonics is put into the CCA module. The CCA module is imported from the sklearn library [link](https://scikit-learn.org/stable/modules/generated/sklearn.cross_decomposition.CCA.html). This function returns the corresponding weighting vectors explained above. Afterwards, we apply these weighting vectors on the template and the data. Finally, we can calculate the correlation between the signals and the template, this value is stored. The process is repeated for every reference signal. The reference with the highest correlation value is picked as the winner.

The dots indicate how we could upgrade the regular CCA to the extended CCA. By adding training data to the template matrix, we could increase the accuracy of the method. This data is first averaged for each frequency while keeping the different channels separated. The final template will have dimensions (`number of frequencies x number of channels x number of samples`).

