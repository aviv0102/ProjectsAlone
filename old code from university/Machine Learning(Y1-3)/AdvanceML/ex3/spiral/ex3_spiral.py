'''
Itay Hassid 209127596   Aviv Shisman 206558157
'''

# imports:
import torch
from torch import nn, optim
from torch.autograd.variable import Variable
import matplotlib.pyplot as plt
import numpy as np
import generate_data



size_t=2

'''
goal : to transfer data from an some distrabution to data in the form of line,parbula,spirala

how: model 1 will generate data --> generator and will get feed back if his data is good (from model2)
     model 2 will be a regular classifier will be trained on generate_data_set maybe
     
output: model 1 will learn to output data like line,parab,spirala

'''
def main():
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    discriminator = DiscriminatorNet()

    generator = GeneratorNet()

    d_optimizer = optim.Adam(discriminator.parameters(), lr=0.0003)
    g_optimizer = optim.Adam(generator.parameters(), lr=0.0002)

    loss = nn.BCELoss()

    train(generator,discriminator,d_optimizer,g_optimizer,loss)

    return


'''
model 2
'''
class DiscriminatorNet(torch.nn.Module):
    """
    A three hidden-layer discriminative neural network
    """

    def __init__(self):
        super(DiscriminatorNet, self).__init__()
        n_features = size_t
        n_out = 1

        self.hidden0 = nn.Sequential(
            nn.Linear(n_features, 64),
            nn.LeakyReLU(0.001),
        )
        self.hidden1 = nn.Sequential(
            nn.Linear(64, 32),
            nn.LeakyReLU(0.001),
        )
        self.hidden2 = nn.Sequential(
            nn.Linear(32, 16),
            nn.LeakyReLU(0.001),
        )
        self.out = nn.Sequential(
            torch.nn.Linear(16, n_out),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        x = self.hidden0(x)
        x = self.hidden1(x)
        x = self.hidden2(x)
        x = self.out(x)
        return x
'''
model 1
'''
class GeneratorNet(torch.nn.Module):
    """
    A three hidden-layer generative neural network
    """

    def __init__(self):
        super(GeneratorNet, self).__init__()
        n_features = 2
        n_out = size_t

        self.hidden0 = nn.Sequential(
            nn.Linear(n_features, 16),
            nn.LeakyReLU(0.001)
        )
        self.hidden1 = nn.Sequential(
            nn.Linear(16, 32),
            nn.LeakyReLU(0.001)
        )
        self.hidden2 = nn.Sequential(
            nn.Linear(32, 64),
            nn.LeakyReLU(0.001)
        )

        self.out = nn.Sequential(
            nn.Linear(64, n_out),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.hidden0(x)
        x = self.hidden1(x)
        x = self.hidden2(x)
        x = self.out(x)
        return x

def train (generator,discriminator,d_optimizer,g_optimizer,loss):

    num_test_samples = 16
    test_noise = noise(num_test_samples)

    # Total number of epochs to train
    num_epochs = 250
    for epoch in range(num_epochs):
        print('epoch:{}'.format(epoch))
        points = generate_data.getSingle()
        for i in range(len(points)):
            N=1
            my_data = points[i,:].unsqueeze(0)

            # 1. Train Discriminator
            real_data = Variable(my_data)
            # Generate fake data and detach
            # (so gradients are not calculated for generator)
            fake_data = generator(noise(N)).detach()


            # Train D
            d_error, d_pred_real, d_pred_fake = \
                train_discriminator(discriminator,loss,d_optimizer, real_data, fake_data)

            # 2. Train Generator
            # Generate fake data
            fake_data = generator(noise(N))
            # Train G
            g_error = train_generator(discriminator,loss,g_optimizer, fake_data)

        if epoch % 100 == 0:
            display_status(epoch, num_epochs, 0, 0, d_error, g_error, d_pred_real, d_pred_fake)

    write_res(generator)
    return


def write_res(generator):
    for i in range(5):
        x=[]
        for i in range(1000):
            curr= Variable(generator(noise(1)).detach()).data.numpy()
            x.append(curr)
        x = np.stack(x)
        plt.plot(x[:,0,0], x[:,0,1], '.', label='class 1')
        plt.title('training set')
        plt.legend()
        plt.show()
    print('done')



# <------------------------------ train each model

def train_discriminator(discriminator,loss,optimizer, real_data, fake_data):
    N = real_data.size(0)
    # Reset gradients
    optimizer.zero_grad()


    # 1.1 Train on Real Data
    prediction_real = discriminator(real_data)
    # Calculate error and backpropagate
    error_real = loss(prediction_real, ones_target(N))
    error_real.backward()

    # 1.2 Train on Fake Data
    prediction_fake = discriminator(fake_data)
    # Calculate error and backpropagate
    error_fake = loss(prediction_fake, zeros_target(N))
    error_fake.backward()

    # 1.3 Update weights with gradients
    optimizer.step()

    # Return error and predictions for real and fake inputs
    return error_real + error_fake, prediction_real, prediction_fake


def train_generator(discriminator,loss,optimizer, fake_data):
    N = fake_data.size(0)

    # Reset gradients
    optimizer.zero_grad()
    # Sample noise and generate fake data
    prediction = discriminator(fake_data)
    # Calculate error and backpropagate
    error = loss(prediction, ones_target(N))
    error.backward()
    # Update weights with gradients
    optimizer.step()
    # Return error
    return error




# <---------------------------------- need to change to our dataSet

def images_to_vectors(images):
    return images.view(1, 2)


def noise(size):
    '''
    Generates a 1-d vector of gaussian sampled random values
    '''
    n = Variable(torch.randn(size, 2))
    return n

def ones_target(size):
    '''
    Tensor containing ones, with shape = size
    '''
    data = Variable(torch.ones(size, 1))
    return data

def zeros_target(size):
    '''
    Tensor containing zeros, with shape = size
    '''
    data = Variable(torch.zeros(size, 1))
    return data

def display_status( epoch, num_epochs, n_batch, num_batches, d_error, g_error, d_pred_real, d_pred_fake):

    # var_class = torch.autograd.variable.Variable
    if isinstance(d_error, torch.autograd.Variable):
        d_error = d_error.data.cpu().numpy()
    if isinstance(g_error, torch.autograd.Variable):
        g_error = g_error.data.cpu().numpy()
    if isinstance(d_pred_real, torch.autograd.Variable):
        d_pred_real = d_pred_real.data
    if isinstance(d_pred_fake, torch.autograd.Variable):
        d_pred_fake = d_pred_fake.data

    print('Epoch: [{}/{}], Batch Num: [{}/{}]'.format(
        epoch, num_epochs, n_batch, num_batches)
    )
    print('Discriminator Loss: {:.4f}, Generator Loss: {:.4f}'.format(d_error, g_error))
    print('D(x): {:.4f}, D(G(z)): {:.4f}'.format(d_pred_real.mean(), d_pred_fake.mean()))


if __name__ == '__main__':
    main()
