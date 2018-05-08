import numpy as np
import scipy
import matplotlib.pyplot as plt
import math

## Resample data uniformly.

from scipy.interpolate import interp1d


def make_uniform(distances, PSF, method='uniform'):
    if method == 'uniform':
        num_samples = 50
        num_channels = PSF.shape[1]
        PSF_uniform = np.empty((num_samples, num_channels))
        distances_uniform = np.linspace(
            distances[0], distances[-1], num=num_samples, endpoint=True)
        for i in range(num_channels):
            x = np.squeeze(distances)
            y = PSF[:, i]
            f = interp1d(x, y, kind='cubic')
            PSF_uniform[:, i] = f(distances_uniform)

    elif method == 'manual':
        INDICES_4 = np.array([-1, 0, 1, 2, 3, 4, 5, 6, 7, 9, 13, 17, 19, 20, 21, 22,
                              23, 24, 25, 27, 31, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49])
        INDICES_4 += 1
        PSF_uniform = np.zeros((len(INDICES_4), 4))
        distances_uniform = np.zeros((len(INDICES_4), 1))
        idx_uniform = 0
        for idx in range(len(INDICES_4)):
            PSF_uniform[idx, :] = PSF[INDICES_4[idx], :]
            distances_uniform[idx] = distances[INDICES_4[idx]]

    else:
        raise NotImplementedError('Unknown method', method)

    return distances_uniform, PSF_uniform


def polynomial_fitting(distances, PSF, degree=4):
    polyParams = np.polyfit(distances, PSF, degree).T
    return polyParams


def get_focus_distances(polyParams, bounds=None):
    num_colors = polyParams.shape[0]

    x0 = np.zeros(num_colors)
    for channelIdx in range(num_colors):
        f = np.poly1d(polyParams[channelIdx, :])
        if bounds is not None:
            result = scipy.optimize.minimize_scalar(
                f, bounds=bounds, method='bounded')
        else:
            result = scipy.optimize.minimize_scalar(f)
        x0[channelIdx] = result.x
    return x0


def compute_aam(polyParams, x0, alphaList):
    num_colors, degree = polyParams.shape
    degree -= 1
    AAM = np.zeros(len(alphaList))

    num_pairs = int(0.5*num_colors*(num_colors-1))
    c_ij = np.zeros((num_pairs, degree+1))
    d = np.zeros((num_pairs, 2*degree+1))
    counter = 0  # corresponds to ij pairs in vectorized form
    for i in range(num_colors):
        for j in range(i+1, num_colors):
            polydiff = polyParams[i, :] - polyParams[j, :]
            d[counter] = np.polymul(polydiff, polydiff)
            counter += 1

    for alphaIdx, alpha in enumerate(alphaList):
        counter = 0  # corresponds to ij pairs in vectorized form
        for i in range(num_colors):
            for j in range(i+1, num_colors):
                a_ij = (1 - alpha) * min(x0[i], x0[j])
                b_ij = (1 + alpha) * max(x0[i], x0[j])

                delta = 0
                for k in range(1, 2*degree+1+1):
                    delta += d[counter, k-1] * (b_ij**k - a_ij**k) / k

                AAM[alphaIdx] += 1.0 / (b_ij - a_ij) * delta
                counter += 1

    AAM /= num_pairs
    return AAM


if __name__ == "__main__":
    # Compute the AAM for varying alpha
    #         RG   RB   RN   GB   GN   BN
    B_ijs = [0.2, 0.3, 0.4, 0.2, 0.5, 0.6]
    B_ijs = [1., 1., 1., 1., 1., 1.]
    B_ijs = [0.2, 0.3, 0.2]
    #       RG   RB   GB  
    B_ijs = [1., 1., 1.]
