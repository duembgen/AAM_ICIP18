import numpy as np
import scipy.io as sio

from aam import polynomial_fitting, get_focus_distances
from aam import compute_aam
from aam import make_uniform

NUM_ALPHAS = 51

def pipeline(IMG_SET_ID, num_colors=4, degree=5):
    ''' Calculate AAM for experimental dataset. 

    :param IMG_SET_ID: ID of dataset to be used (in this example 4 or 7)
    :param num_colors: number of color channels to consider
    :param degree: degree of polynomial fitted to the PSF curve. 

    :returns: list of considered values of alpha, and list of corresponding AAM metrics. 
    '''

    path = "../data/"
    alphaList = np.linspace(0.2, 0.5, NUM_ALPHAS)

    dist_name = path + "distances_" + str(IMG_SET_ID) + ".mat"
    PSF_name = path + "GaussStd2Color_" + str(IMG_SET_ID) + ".mat"
    PSF_NIR_name = path + "GaussStd2Nir_" + str(IMG_SET_ID) + ".mat"

    mat_dist = sio.loadmat(dist_name)
    mat_PSF = sio.loadmat(PSF_name)
    mat_PSF_NIR = sio.loadmat(PSF_NIR_name)

    distances = mat_dist['distancesCol']
    PSF = mat_PSF['GaussStd2Color']
    PSF_NIR = np.squeeze(mat_PSF_NIR['GaussStd2Nir'])
    PSF[:, 3] = PSF_NIR

    assert distances.shape[0] == PSF.shape[0]
    assert distances.shape[0] == PSF_NIR.shape[0]
    print('loaded experimental data {} from {} distances and {} channels.'.format(
        IMG_SET_ID, *PSF.shape))

    if IMG_SET_ID == 4:
        distances_uniform, PSF_uniform = make_uniform(distances, PSF, 'manual')

    if IMG_SET_ID == 7:
        distances_uniform = distances
        PSF_uniform = PSF

    x = np.squeeze(distances_uniform/1000)

    polyParams = polynomial_fitting(x, PSF_uniform, degree=degree)
    x0 = get_focus_distances(polyParams, bounds=(x[0], x[-1]))

    print('computing aam with {} channels'.format(num_colors))
    AAM = compute_aam(polyParams[:num_colors, :], x0[:num_colors], alphaList)

    return alphaList, AAM
