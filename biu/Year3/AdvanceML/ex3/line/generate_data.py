import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from sklearn import datasets
import torch

def get_data(n_points, data_type):
    """
     Returns a synthetic dataset.
    """
    if data_type == 'line':
        dx = np.random.randn(n_points, 1)
        dy = dx
    elif data_type == 'par':
        dx = np.random.randn(n_points, 1)
        dy = dx**2
    elif data_type == 'spiral':
        n = np.sqrt(np.random.rand(n_points,1)) * 780 * (2*np.pi)/360
        dx = -np.cos(n)*n + np.random.rand(n_points,1)
        dy = np.sin(n)*n + np.random.rand(n_points,1)
    else:
        print('Data type not supported.')
    # normalize
    dx /= dx.max()
    dy /= dy.max()
    return np.hstack((dx,dy))


def show():
    X = get_data(1000, 'line')

    plt.plot(X[:,0], X[:,1], '.', label='class 1')
    plt.title('training set')
    plt.legend()
    plt.show()
    return
def getSingle():
    X = get_data(1000,'line')
    return torch.from_numpy(X).float()

if __name__ == '__main__':
   show()

