import numpy as np
import scipy.io as sio
import scipy
import matplotlib.pyplot as plt
import math

IMG_SET_ID = 4 # 7
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
print('loaded experimental data from {} distances and {} channels.'.format(*PSF.shape))

## Resample data uniformly. 

from scipy.interpolate import interp1d

def make_uniform(distances, PSF, method='uniform'):

    distances_uniform = np.linspace(distances[0], distances[-1], num=num_samples, endpoint=True)

    if method == 'uniform':
        PSF_uniform = np.empty((num_samples, num_channels))    
        num_samples = 50
        num_channels = PSF.shape[1]
        for i in range(num_channels):
            x = np.squeeze(distances)
            y = PSF[:,i]
            f = interp1d(x, y, kind='cubic')
            PSF_uniform[:, i] = f(distances_uniform)
            
    elif method == 'manual':
        INDICES_4 = np.array([-1, 0, 1, 2, 3, 4, 5, 6, 7, 9, 13, 17, 19, 20, 21, 22, 23, 24, 25, 27, 31, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49])
        INDICES_4 += 1
        PSF_uniform = np.zeros((len(INDICES_4),4))
        distances_uniform = np.zeros((len(INDICES_4),1))
        idx_uniform = 0
        for idx in range(len(INDICES_4)):
            PSF_uniform[idx,:] = PSF[ INDICES_4[idx], : ]
            distances_uniform[idx] = distances[ INDICES_4[idx] ]

    else:
        raise NotImplementedError('Unknown method', method)

    return distances_uniform, PSF_uniform


def polynomial_fitting(distances, PSF, degree=4): 
    x = np.squeeze(0.001*distances_uniform)

    polyParams = np.polyfit(x, PSF_uniform, degree).T
    return polyParams

# In[ ]:

# Finding x0, focal distance of each color channel.
num_colors = polyParams.shape[0]

x0 = np.zeros(num_colors)
for channelIdx in range(num_colors):
    f = np.poly1d( polyParams[channelIdx, :] )
    result = scipy.optimize.minimize_scalar(f, bounds=(x[0], x[-1]), method='bounded')
    x0[channelIdx] = result.x

print(x0)


# Compute c_ij & d_ij
if __name__ == "__main__":

    num_pairs = int(0.5*num_colors*(num_colors-1))
    c_ij = np.zeros((num_pairs, degree+1))
    d = np.zeros((num_pairs, 2*degree+1))
    duo = 0 #corresponds to ij pairs in vectorized form
    for i in range(num_colors):
        for j in range(i+1,num_colors):
            polydiff = polyParams[i, :] - polyParams[j, :]
            dtest = np.polymul(polydiff, polydiff)
            #c_ij[duo, :] = polyParams[i, :] - polyParams[j, :]
            #for k in range(2*degree+1):
            #    d[duo, k] = 0
            #    for u in range(degree+1):
            #        for v in range(degree+1):
            #            if u+v == k:
            #                d[duo, k] += c_ij[duo, u] * c_ij[duo, v]
            #print(d[duo] - dtest)
            d[duo] = dtest
            duo += 1

# In[ ]:


# Compute the AAM for varying alpha
    alphaLIST = np.linspace(0.2, 0.5, 50)
    AAM = np.zeros(len(alphaLIST))

# B_ij  RG   RB   Rnum_colors   GB   Gnum_colors   Bnum_colors
    B_ijs = [0.2, 0.3, 0.4, 0.2, 0.5, 0.6]
    B_ijs = [1., 1., 1., 1., 1., 1.]
    if num_colors == 3:
        # B_ij  RG   RB   GB
        B_ijs = [0.2, 0.3, 0.2]
        B_ijs = [1., 1., 1.]

#def compute_AAM(alpha, )

    for alphaIdx, alpha in enumerate(alphaLIST):
        # Computing delta_alpha bar
        duo = 0 #corresponds to ij pairs in vectorized form
        for i in range(num_colors):
            for j in range(i+1,num_colors):
                a_ij = (1 - alpha) * min(x0[i], x0[j])
                b_ij = (1 + alpha) * max(x0[i], x0[j])

                B_ij = B_ijs[duo] 
                #B_ij = max(bandwidths[i,1], bandwidths[j,1]) - min(bandwidths[i,0], bandwidths[j,0])
                delta = 0
                for k in range(1, 2*degree+1+1):
                    delta += d[duo, k-1] * (b_ij**k - a_ij**k) / k

                AAM[alphaIdx] += B_ij / (b_ij - a_ij) * delta
                duo += 1

    AAM /= num_pairs

    plt.plot(alphaLIST, AAM, 'r^', label="y reconst")
    plt.ylabel('AAM')
    plt.xlabel('alpha')
    plt.show()

    indices = [0, 25, 49]
    print([alphaLIST[0], AAM[0]])
    print([alphaLIST[25], AAM[25]])
    print([alphaLIST[49], AAM[49]])
