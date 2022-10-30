# Riemannian Geometry

Written by: Rochelle Aubry and Yitong Li

## Goal

Use Riemannian Geometry for BCI classification.

Riemannian geometry is a branch of differential geometry that studies smooth manifolds. The manifold of symmetric positive-definite (SPD) matrices has proved to be very useful in brain-computer interfaces (BCI), since multivariate electroencephalography (EEG) data in finite time windows can effectively be mapped as points onto this manifold through the estimation of some form of their covariance matrix.

The Riemannian minimum distance to the mean classifier is simple, fully deterministic, robust to noise, computationally efficient and prone to transfer learning. Therefore interesting to be used for BCI applications.

To do this, the paper by [Conjendo et al.](https://hal.archives-ouvertes.fr/hal-02315131/document) was used.

## Methodology

EEG data can be manipulated through their spatial covariances, then detected and classified by measuring the Riemannian distance between covariance matrices of signal epochs and covariance matrices of referenced epochs.

The covariance captures the degree of linear dependence between several random variables, i.e. how the brain signals change relatively to each other. If two signals show the same variations, they are dependent. [read more](https://hal.uvsq.fr/hal-01710089)

Covariance matrices are symmetric positive-definite (SPD) and are thus constrained to lie strictly inside a convex cone, which is the Riemannian manifold.

![alt text for screen readers](./images/riemannian_manifold.png "Text to show on mouseover")

Figure 1. Riemannian manifold. The Euclidean distance is the red dahed line (which does not consider the curvature of the space) and Riemannian distance is in plain blue and Log-Euclidean in dashed-dotted green (which follows the geodesic , therefore taking into account the shape of the space where covariance matries lie).

Picture taken from [Chevallier, 2018](https://www.researchgate.net/publication/323358565_Riemannian_Classification_for_SSVEP-Based_BCI_Offline_versus_Online_Implementations)

A Riemannian manifold is a differentiable manifold in which tangent space at each point is a finite-dimensional Euclidean space. Euclidean space is a space in any finite number of dimensions, in which points are designated by coordinates (one for each dimension) and the distance between two points is given by a distance formula [Definition](https://www.britannica.com/science/Euclidean-space).

The Euclidian distance does not consider the curvature of the space, while Riemannian distances follows the geodesic and are thus taking into account the shape of the space where covariance matrices lie.

$S_n={S\in M_n, S^T=S}$ represents the space of all $n×n$ symmetric matrices in the space of square matrices.

$P_n={P \in S_n, P>0}$ represents the set of all $n×n$ symmetric positive-definite (SPD) matrices.

The Riemannian distance $\theta_n$ between two SPD matrices $P_1$ and $P_2$ in $P(n)$ is calculated using the following formula:

$$
\theta_R(P_1,P_2)=\Vert\log({P_1}^{-1}P_2)\Vert_F=\left[\sum_{i=1}^n\log^2(\lambda_i)  \right]^{1/2}
$$

The shortest path between two points in the Riemannian space of SPD matrices is defined by the geodesic $\gamma(t)$ with $t\in [0,1]$

$$
\gamma(t)=P_1^{1/2}(P_1^{-1/2}P_2P_1^{-1/2})^tP_1^{1/2}
$$

![alt text](./images/geodesic.png "Text to show on mouseover")

Figure 2. Tangent space of the manifold M at point P, Si the tangent vector of Pi and \gamma(t) the geodesic between P and Pi.

Figure taken from [Barachant, 2010](https://hal.archives-ouvertes.fr/hal-00602700/document)

The mean of SPD matrices can be obtained by using the concept of tangent space, which is the space defined by the whole set of tangent vectors, is identified to the Euclidian space of symmetric matrices.

Using the Riemannian Log map, we first project the whole dataset in tangent space, then the arithmetic mean is computed. Finally the arithmetic mean is projected into SPD matrices using Riemannian exponential map. After a few iterations, the geometric mean SPD matrices are obtained.

## Implementation

Our implementation can be found in [here](../../src/data_processing/riemann.py). The general procedure is as follows:

```mermaid
flowchart LR;
first[Processing] --> second[Training] --> third[Prediction]
class first cssClass
```

1. **Processing**.
   Some processing of the data should be done after the preprocessing steps to accomodate the signal as required.
   Processing consists of two steps that are handled together with the function extend signal.
   First step is a **Filter bank**. The filter bank is composed of bandpass filters for each stimulation frequency that is applied. This is done using the scipy library, of which the functions [butter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html) and [filtfilt](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html) are. The EEG signal as a numpy array (`number of channels, number of samples`) is transferred to the filtered signal (`number of frequencies, number of channels, number of samples`). For the second step we **Stack the filtered signals to build an extended signal**, by modifying the array in the shape of `number of frequencies x number of channels, number of samples`. In order to compute the covariance matrices, we extract the epochs from the raw data. Noted that the shape of numpy array (epoch data) here is `number of epochs, number of frequencies x number of channels, number of samples`.
2. **Training**.
   We first **Estimate covariance matrices by using Ledoit-Wolf shrinkage estimator on the extended signal**.
   For this, the [covariance](https://pyriemann.readthedocs.io/en/latest/generated/pyriemann.utils.covariance.covariances.html#pyriemann.utils.covariance.covariances) is used.
   This function performs a covariance matrix estimation for each given input. It accepts the epoched extended signal and returns the covariance matrix.
   From this we **Estimate the centroids for MDM classification model**.
   The classification is done by [MDM](https://pyriemann.readthedocs.io/en/latest/generated/pyriemann.classification.MDM.html#pyriemann.classification.MDM), which works as follows: for each given class, a centroid is estimated according to 'riemann' metric and each data is classified into the nearest centroid. The evaluation of performance is done by cross validation (K-fold and Leave-One-Out).
3. **Prediction**.
   For new inpput data, we firstly compute the corresponding SPD matrices. We then make a prediction using the fitted model, and calculate the [euclidean distance](https://pyriemann.readthedocs.io/en/latest/generated/pyriemann.utils.distance.distance.html#pyriemann.utils.distance.distance) between the centroid and the matric. The distance is one indicator of the certainty of the classification.

## Results

The prediction result provides the class to which the new data belongs with a certainty measurement. We also visualize the performance of the classifer by confusion matrix. For example, the plot below shows the performance of prediction with accuracy 76\%.

![alt text](./images/riemann_cm.png "Text to show on mouseover")
