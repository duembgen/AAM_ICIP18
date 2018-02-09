import numpy as np
import scipy.io as sio

from aam import polynomial_fitting, get_focus_distances
from aam import compute_aam

SCALING = 100
NUM_ALPHAS = 51

def pipeline(IMG_SET_ID, scale=1e-5, num_colors=4, degree=5):
    path = "data/"
    dist_name = path + "distances_" + str(IMG_SET_ID) + ".mat"
    PSF_name  = path + "GaussStd2Color_" + str(IMG_SET_ID) + ".mat"
    PSF_NIR_name = path + "GaussStd2Nir_" + str(IMG_SET_ID) + ".mat"

    mat_dist = sio.loadmat(dist_name)
    mat_PSF = sio.loadmat(PSF_name)
    mat_PSF_NIR = sio.loadmat(PSF_NIR_name)

    distances = mat_dist['distancesCol']
    PSF       = mat_PSF['GaussStd2Color']
    PSF_NIR   = np.squeeze(mat_PSF_NIR['GaussStd2Nir'])
    PSF[:,3] = PSF_NIR

    assert distances.shape[0] == PSF.shape[0]
    assert distances.shape[0] == PSF_NIR.shape[0]
    print('loaded experimental data {} from {} distances and {} channels.'.format(IMG_SET_ID, *PSF.shape))


    from aam import make_uniform
    if IMG_SET_ID == 4:
        distances_uniform, PSF_uniform = make_uniform(distances, PSF, 'manual')

    if IMG_SET_ID == 7:
        distances_uniform = distances
        PSF_uniform = PSF

    x = np.squeeze(distances_uniform/1000)

    polyParams = polynomial_fitting(x, PSF_uniform, degree=degree)
    x0 = get_focus_distances(polyParams, bounds=(x[0], x[-1]))

    PSF_uniform_noisy = PSF_uniform.copy()
    PSF_uniform_noisy += np.random.normal(scale=scale*PSF_uniform, size=PSF_uniform.shape)
    polyParams_noisy = polynomial_fitting(x, PSF_uniform_noisy, degree=degree)
    x0_noisy = get_focus_distances(polyParams_noisy, bounds=(x[0], x[-1]))

    alphaList = np.linspace(0.2, 0.5, NUM_ALPHAS)

    print('computing aam with {} channels'.format(num_colors))
    AAM = compute_aam(polyParams[:num_colors, :], x0[:num_colors], alphaList)
    AAM_noisy = compute_aam(polyParams_noisy[:num_colors, :], x0_noisy[:num_colors], alphaList)

    AAM /= SCALING
    AAM_noisy /= SCALING

    AAM = np.log10(AAM)
    AAM_noisy = np.log10(AAM_noisy)

    #print('\\alpha \t & AAM (AAM noisy scale={}) \\\\'.format(scale))
    print('\\alpha \t & AAM \\\\')
    for i, (alpha, aam, aam_noisy) in enumerate(zip(alphaList, AAM, AAM_noisy)):
        if i in [0, np.floor(NUM_ALPHAS/2), NUM_ALPHAS-1]:
            relative = abs(aam_noisy - aam) / aam
            #print('{:2.2f} \t & {:8.2f} ({:8.2f}, {:2.2e}) \\\\'.format(
            #    alpha, aam, aam_noisy, relative))
            print('{:2.2f} \t & {:8.2f} \\\\'.format(alpha, aam))
