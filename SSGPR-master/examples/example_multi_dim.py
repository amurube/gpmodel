import sys
sys.path.append("..")
import numpy as np
from model.ssgpr import SSGPR
np.random.seed(1)  # set seed
import urllib.request
import os.path
from scipy.io import loadmat
import matplotlib.pyplot as plt

##################################################
#     Example for high dimensional data          #
##################################################

if not os.path.isfile('../data/example_data/elevators.mat'):
    print('Downloading \'elevators\' UCI dataset...')
    urllib.request.urlretrieve('https://drive.google.com/uc?export=download&id=1jhWL3YUHvXIaftia4qeAyDwVxo6j1alk',
                               '../data/example_data/elevators.mat')

# get data and process
data = np.array(loadmat('../data/example_data/elevators.mat')['data'])
num_points = 8752
dimensions = 14
X = data[:, :-1]
X = X - X.min()
X = 2 * (X / X.max()) - 1
Y = data[:, -1].reshape(-1,1)

X_train = X[:num_points,:dimensions]
X_test = X[num_points:,:dimensions]
Y_train = Y[:num_points,:]
Y_test = Y[num_points:,:]

# create ssgpr instance
nbf = 100  # number of basis functions
ssgpr = SSGPR(num_basis_functions=nbf)
ssgpr.add_data(X_train, Y_train, X_test, Y_test)
ssgpr.optimize(restarts=1, maxiter=10, verbose=True)

# predict on the test points
mu, sigma = ssgpr.predict(X_test, sample_posterior=False)

# evaluate the performance
NMSE, MNLP = ssgpr.evaluate_performance()
print("Normalised mean squared error (NMSE): %.5f" % NMSE)
print("Mean negative log probability (MNLP): %.5f" % MNLP)

plt.figure()
X_test = range(0, len(Y_test))
plt.plot(X_test, Y_test, label="Training data", color='blue')  # training data
plt.plot(X_test, mu, label="Predictive mean", color='red')  # predictive mean
plt.fill_between(X_test, (mu - 2 * sigma).flat, (mu + 2 * sigma).flat, color="#dddddd",
                    label="95% confidence interval")

print(np.hstack((mu - 2 * sigma, mu + 2 * sigma)))
plt.grid()
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("inputs, X")
plt.ylabel("targets, Y")
plt.legend(loc='lower right')
plt.show()