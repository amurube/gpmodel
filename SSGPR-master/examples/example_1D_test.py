import sys
sys.path.append("..")
import numpy as np
import random
from model.ssgpr import SSGPR
from utils.plots import plot_predictive_1D
from math import floor
np.random.seed(1)  # set seed

def func(x):
    """Latent function."""
    return 1.0 * np.sin(x * 3 * np.pi) + \
           0.3 * np.cos(x * 9 * np.pi) + \
           0.5 * np.sin(x * 7 * np.pi)

##################################################
#           Example for 1D data                  #
##################################################

# Generate the data
#'''
# Number of training examples
n = 10000
# Noise
sigma_y = 0.2
# Noisy training data
X = np.linspace(-1.0, 1.0, n).reshape(-1, 1)
y = func(X) + sigma_y * np.random.normal(size=(n, 1))
#'''
data = np.hstack((X,y))
#data = np.load("../data/example_data/data_1D.npy")
n = floor(0.8 * data.shape[0])
X_train = data[:n,0].reshape(-1,1)
Y_train = data[:n,1].reshape(-1,1)
X_test = data[n:,0].reshape(-1,1)
Y_test = data[n:,1].reshape(-1,1)

# create ssgpr instance
nbf = 20  # number of basis functions
ssgpr = SSGPR(num_basis_functions=nbf)
ssgpr.add_data(X_train, Y_train, X_test, Y_test)
ssgpr.optimize(restarts=2, verbose=True)

# create some prediction points
Xs = np.linspace(-1,1,100).reshape(-1,1)
mu, sigma, f_post = ssgpr.predict(Xs, sample_posterior=True, num_samples=3)
NMSE, MNLP = ssgpr.evaluate_performance(restarts=1)
print("Normalised mean squared error (NMSE): %.5f" % NMSE)
print("Mean negative log probability (MNLP): %.5f" % MNLP)

path = "../doc/imgs/example_1D.png"
#plot results
plot_predictive_1D(path=path, X_train=X_train, Y_train=Y_train, Xs=Xs, mu=mu,
                   stddev=sigma, post_sample=f_post)