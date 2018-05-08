import numpy as np

plotIdx = 1

f_poly = np.poly1d(polyParams[plotIdx, :])
x = distances_uniform
y_poly = f_poly(x)

y = PSF_uniform[:, plotIdx]

plt.plot(x, y_poly, 'r^', label="y reconst")
plt.plot(x, y, 'g^', label="y")
plt.ylabel('Experimental PSF')
plt.legend()
plt.show()

plotIdx = 1

from scipy.optimize import curve_fit

def fit_PSF_func(x, L, d, f, c):
    return np.transpose(np.array(  (L * abs( 1 - d/f + d/x ) + c)  ))

x = distances_uniform
y = PSF_uniform[:, plotIdx]

#params = curve_fit(fit_PSF_func, x, y, p0=(140989., 1.055, 1.054, 2.054))
#params = curve_fit(fit_PSF_func, x, y, bounds=((0,0,0,-np.inf),(np.inf, np.inf, np.inf, np.inf)), p0=(140989., 1.055, 1.054, 2.054))
params = curve_fit(fit_PSF_func, x, y, bounds=((0,0,0,-np.inf),(np.inf, np.inf, np.inf, np.inf)), p0=(70989., 1.055, 1.054, 2.054))

simpleLensParams = params[0]
PSF_fitted = fit_PSF_func(x, *simpleLensParams) 
#PARAMS_GREEN_SET4 = [1.30744663e+05   1.12823345e+00   1.12738942e+00  -2.10215811e-01]

err_fit = np.linalg.norm(PSF_fitted - y)
plt.plot(x, PSF_fitted, 'g^', label=str(err_fit))
plt.plot(x, y, 'k^')
plt.ylabel('Experimental PSF')
plt.legend()
plt.show()


from scipy.optimize import least_squares
from scipy.optimize import leastsq

def fit_PSF_loss(opt_vector, x, y):
    L, d, f = opt_vector
    #return L * abs( 1 - d/f + d/x )
    y_fit = (L * abs( 1 - d/f + d/x ))
    diff  = y_fit.reshape((-1,)) - y
    return diff

channelIdx = 3

x = distances_uniform
y = PSF_uniform[:, channelIdx]
x0 = np.array([1, 2, 3])
params = leastsq(fit_PSF_loss, x0=x0, args=(x,y), xtol=1e-15)
simpleLensParams = params[0]

PSF_fitted = fit_PSF_loss(simpleLensParams, x, y)

plt.plot(x, PSF_fitted, 'g^')
plt.ylabel('Experimental PSF')
plt.show()
