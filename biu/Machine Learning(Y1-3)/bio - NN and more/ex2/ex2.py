"""""
                    written by
name: Aviv Shisman              name: Itay Hassid 
id:   206558157                 id:   209127596
"""""

# imports:
import numpy as np
from tqdm import tqdm


# model params:
batch_size = 100
num_epochs = 35
lr = 0.001
input_layer = 1152
output_layer = 10
hidden_layer = 100
img_dim = 32
img_depth = 3


def main():

    # load data
    print('Loading data it might take a few moments...')
    trainSet = loadTrain("train.csv", "train")
    validSet = loadData("validate.csv", "validation", test=False)
    testSet   = loadData("test.csv", "test", test=True)

    # more params:
    filter_size = 5
    num_filt1 = 8
    num_filt2 = 8


    # weights and filters:
    f1 = create_filter((num_filt1, img_depth, filter_size, filter_size))
    f2 = create_filter((num_filt2, 8, filter_size, filter_size))
    w3 = create_weight_matrix((hidden_layer, input_layer))
    w4 = create_weight_matrix((output_layer, hidden_layer))
    b1 = np.zeros((f1.shape[0], 1))
    b2 = np.zeros((f2.shape[0], 1))
    b3 = np.zeros((w3.shape[0], 1))
    b4 = np.zeros((w4.shape[0], 1))

    # in case want to learn from zero un comment this and comment next 4 lines and get higher lr like 0.007
    #weights = [f1, f2, w3, w4, b1, b2, b3, b4]


    # load weights in case not want to learn
    np_load_old = np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
    weights = np.load('params.npy')
    np.load = np_load_old

    # train:

    print("LR:" + str(lr) + ", Batch Size:" + str(batch_size))
    cost = []
    for epoch in range(num_epochs):
        np.random.shuffle(trainSet)
        batches = [trainSet[k:k + batch_size] for k in range(0, len(trainSet), batch_size)]

        t = tqdm(batches)
        for x, batch in enumerate(t):

            weights, cost = one_batch_train(batch, weights, cost)
            t.set_description("Cost: %.2f" % (cost[-1]))

            if x % 4 == 0:
                acc = accuracy_on_validation(weights, validSet)
                print("\nAccuracy of a model: {}%".format(str(100.0 * acc)))
                np.save('params.npy', weights)

    # test:
    acc = accuracy_on_validation(weights, validSet)
    print("\nAccuracy of a model: {}%".format(str(100.0 * acc)))
    test(weights,testSet)

    return




'''
validation check
'''
def accuracy_on_validation(weights, validSet, conv_s=1, pool_s=2, pool_f=2):
    size = 0
    correct = 0
    [f1, f2, w3, w4, b1, b2, b3, b4] = weights

    np.random.shuffle(validSet)
    for i, ex in enumerate(validSet):
        if i == 200:
            break
        x = ex[1]
        y = np.eye(output_layer)[int(ex[0])].reshape(output_layer, 1)  # convert label to one-hot
        conv1 = convolution(x, f1, b1, conv_s)  # convolution operation
        conv1[conv1 <= 0] = 0  # ReLU

        conv2 = convolution(conv1, f2, b2, conv_s)  # second convolution operation
        conv2[conv2 <= 0] = 0  # ReLU

        pooled = maxpool(conv2, pool_f, pool_s)  # maxpooling operation

        (nf2, dim2, _) = pooled.shape
        fc = pooled.reshape((nf2 * dim2 * dim2, 1))  # flatten pooled layer

        z = w3.dot(fc) + b3  # first dense layer
        z[z <= 0] = 0  # pass through ReLU non-linearity

        out = w4.dot(z) + b4  # second dense layer

        probs = softmax(out)  # predict class probabilities with the softmax activation function

        label = np.argmax(probs)

        if (label == ex[0]):  # need label +1 IN TEST####
            correct += 1
        size += 1

    return correct / size * 1.0


'''
Test the model
'''
def test(weights, testSet, conv_s=1, pool_s=2, pool_f=2):

    outputFile = open('output.txt','w')
    [f1, f2, w3, w4, b1, b2, b3, b4] = weights

    for i, ex in enumerate(testSet):

        x = ex
        conv1 = convolution(x, f1, b1, conv_s)  # convolution operation
        conv1[conv1 <= 0] = 0  # ReLU

        conv2 = convolution(conv1, f2, b2, conv_s)  # second convolution operation
        conv2[conv2 <= 0] = 0  # ReLU

        pooled = maxpool(conv2, pool_f, pool_s)  # maxpooling operation

        (nf2, dim2, _) = pooled.shape
        fc = pooled.reshape((nf2 * dim2 * dim2, 1))  # flatten pooled layer

        z = w3.dot(fc) + b3  # first dense layer
        z[z <= 0] = 0  # pass through ReLU non-linearity

        out = w4.dot(z) + b4  # second dense layer

        probs = softmax(out)  # predict class probabilities with the softmax activation function

        label = np.argmax(probs) +1 # add 1 because 0-9

        outputFile.write(str(label)+'\n')


    outputFile.close()



    return


# -----------------------------------------training--------------------------------------------
'''
training for 1 batch 
'''
def one_batch_train(batch,params,cost):
    '''
    update the parameters through Adam gradient descnet.
    '''
    [f1, f2, w3, w4, b1, b2, b3, b4] = params

    cost_ = 0
    batch_size = len(batch)

    # initialize gradients and momentum,RMS params
    df1 = np.zeros(f1.shape)
    df2 = np.zeros(f2.shape)
    dw3 = np.zeros(w3.shape)
    dw4 = np.zeros(w4.shape)
    db1 = np.zeros(b1.shape)
    db2 = np.zeros(b2.shape)
    db3 = np.zeros(b3.shape)
    db4 = np.zeros(b4.shape)


    for i in range(batch_size):
        curr = batch[i]
        x = curr[1]
        y = np.eye(output_layer)[int(curr[0])].reshape(output_layer, 1)  # convert label to one-hot

        # Collect Gradients for training example
        grads, loss = forward_backward_for_single(x, y, params, 1, 2, 2)
        [df1_, df2_, dw3_, dw4_, db1_, db2_, db3_, db4_] = grads

        df1 += df1_
        db1 += db1_
        df2 += df2_
        db2 += db2_
        dw3 += dw3_
        db3 += db3_
        dw4 += dw4_
        db4 += db4_

        cost_ += loss

    grads = [df1, df2, dw3, dw4, db1, db2, db3, db4]
    new_params = update_params(params,grads)


    cost_ = cost_/ batch_size
    cost.append(cost_)

    return new_params, cost

'''
using weights to feedforward the example trough the conv NN and then calc grads
'''
def forward_backward_for_single(image, label, params, conv_s, pool_f, pool_s):

    # get current params:
    [f1, f2, w3, w4, b1, b2, b3, b4] = params

    # forward:

    conv1 = convolution(image, f1, b1, conv_s)  # convolution operation
    conv1[conv1 <= 0] = 0  # pass through ReLU non-linearity

    conv2 = convolution(conv1, f2, b2, conv_s)  # second convolution operation
    conv2[conv2 <= 0] = 0  # pass through ReLU non-linearity

    pooled = maxpool(conv2, pool_f, pool_s)  # maxpooling operation

    (nf2, dim2, _) = pooled.shape
    fc = pooled.reshape((nf2 * dim2 * dim2, 1))  # flatten pooled layer

    z = w3.dot(fc) + b3  # first dense layer
    z[z <= 0] = 0  # pass through ReLU non-linearity

    out = w4.dot(z) + b4  # second dense layer

    probs = softmax(out)  # predict class probabilities with the softmax activation function
    loss = categoricalCrossEntropy(probs, label)  # categorical cross-entropy loss

    # back-prop:

    dout = probs - label  # derivative of loss w.r.t. final dense layer output
    dw4 = dout.dot(z.T)  # loss gradient of final dense layer weights
    db4 = np.sum(dout, axis=1).reshape(b4.shape)  # loss gradient of final dense layer biases

    dz = w4.T.dot(dout)  # loss gradient of first dense layer outputs
    dz[z <= 0] = 0  # backpropagate through ReLU
    dw3 = dz.dot(fc.T)
    db3 = np.sum(dz, axis=1).reshape(b3.shape)

    dfc = w3.T.dot(dz)  # loss gradients of fully-connected layer (pooling layer)
    dpool = dfc.reshape(pooled.shape)  # reshape fully connected into dimensions of pooling layer

    dconv2 = maxpoolBackward(dpool, conv2, pool_f,
                             pool_s)  # backprop through the max-pooling layer(only neurons with highest activation in window get updated)
    dconv2[conv2 <= 0] = 0  # backpropagate through ReLU

    dconv1, df2, db2 = convolutionBackward(dconv2, conv1, f2,
                                           conv_s)  # backpropagate previous gradient through second convolutional layer.
    dconv1[conv1 <= 0] = 0  # backpropagate through ReLU

    dimage, df1, db1 = convolutionBackward(dconv1, image, f1,
                                           conv_s)  # backpropagate previous gradient through first convolutional layer.

    grads = [df1, df2, dw3, dw4, db1, db2, db3, db4]

    return grads, loss




# -----------------------------------------forward related---------------------------------------


'''
convultion for a single filter group, get convolution matrix
'''
def convolution(image, filt, bias, s=1):
    '''
    Confolves `filt` over `image` using stride `s`
    '''
    (n_f, n_c_f, f, _) = filt.shape  # filter dimensions
    n_c, in_dim, _ = image.shape  # image dimensions

    out_dim = int((in_dim - f) / s) + 1  # calculate output dimensions

    # ensure that the filter dimensions match the dimensions of the input image
    assert n_c == n_c_f, "Dimensions of filter must match dimensions of input image"

    out = np.zeros((n_f, out_dim, out_dim))  # create the matrix to hold the values of the convolution operation

    # convolve each filter over the image
    for curr_f in range(n_f):
        curr_y = out_y = 0
        # move filter vertically across the image
        while curr_y + f <= in_dim:
            curr_x = out_x = 0
            # move filter horizontally across the image
            while curr_x + f <= in_dim:
                # perform the convolution operation and add the bias
                out[curr_f, out_y, out_x] = np.sum(filt[curr_f] * image[:, curr_y:curr_y + f, curr_x:curr_x + f]) + \
                                            bias[curr_f]
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1

    return out


'''
maxpool - get highest value frames
'''
def maxpool(image, f=2, s=2):
    n_c, h_prev, w_prev = image.shape

    # calculate output dimensions after the maxpooling operation.
    h = int((h_prev - f) / s) + 1
    w = int((w_prev - f) / s) + 1

    # create a matrix to hold the values of the maxpooling operation.
    downsampled = np.zeros((n_c, h, w))

    # slide the window over every part of the image using stride s. Take the maximum value at each step.
    for i in range(n_c):
        curr_y = out_y = 0
        # slide the max pooling window vertically across the image
        while curr_y + f <= h_prev:
            curr_x = out_x = 0
            # slide the max pooling window horizontally across the image
            while curr_x + f <= w_prev:
                # choose the maximum value within the window at each step and store it to the output matrix
                downsampled[i, out_y, out_x] = np.max(image[i, curr_y:curr_y + f, curr_x:curr_x + f])
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1
    return downsampled


# ----------------------------------------backprop and update----------------------------------

'''
back prop for convolution filters
'''
def convolutionBackward(dconv_prev, conv_in, filt, s):
    '''
    Backpropagation through a convolutional layer.
    '''
    (n_f, n_c, f, _) = filt.shape
    (_, orig_dim, _) = conv_in.shape
    ## initialize derivatives
    dout = np.zeros(conv_in.shape)
    dfilt = np.zeros(filt.shape)
    dbias = np.zeros((n_f, 1))
    for curr_f in range(n_f):
        # loop through all filters
        curr_y = out_y = 0
        while curr_y + f <= orig_dim:
            curr_x = out_x = 0
            while curr_x + f <= orig_dim:
                # loss gradient of filter (used to update the filter)
                dfilt[curr_f] += dconv_prev[curr_f, out_y, out_x] * conv_in[:, curr_y:curr_y + f, curr_x:curr_x + f]
                # loss gradient of the input to the convolution operation (conv1 in the case of this network)
                dout[:, curr_y:curr_y + f, curr_x:curr_x + f] += dconv_prev[curr_f, out_y, out_x] * filt[curr_f]
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1
        # loss gradient of the bias
        dbias[curr_f] = np.sum(dconv_prev[curr_f])

    return dout, dfilt, dbias



'''
back prop for max pooling mat
'''
def maxpoolBackward(dpool, orig, f, s):
    '''
    Backpropagation through a maxpooling layer. The gradients are passed through the indices of greatest value in the original maxpooling during the forward step.
    '''
    (n_c, orig_dim, _) = orig.shape

    dout = np.zeros(orig.shape)

    for curr_c in range(n_c):
        curr_y = out_y = 0
        while curr_y + f <= orig_dim:
            curr_x = out_x = 0
            while curr_x + f <= orig_dim:
                # obtain index of largest value in input for current window
                (a, b) = nanargmax(orig[curr_c, curr_y:curr_y + f, curr_x:curr_x + f])
                dout[curr_c, curr_y + a, curr_x + b] = dpool[curr_c, out_y, out_x]

                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1

    return dout




'''
applying momentums and rmsprop
'''
def update_params(params, grads):

    # get params
    [f1, f2, w3, w4, b1, b2, b3, b4] = params
    [df1, df2, dw3, dw4, db1, db2, db3, db4] = grads
    beta1 = 0.95
    beta2 = 0.99

    v1 = np.zeros(f1.shape)
    v2 = np.zeros(f2.shape)
    v3 = np.zeros(w3.shape)
    v4 = np.zeros(w4.shape)
    bv1 = np.zeros(b1.shape)
    bv2 = np.zeros(b2.shape)
    bv3 = np.zeros(b3.shape)
    bv4 = np.zeros(b4.shape)

    s1 = np.zeros(f1.shape)
    s2 = np.zeros(f2.shape)
    s3 = np.zeros(w3.shape)
    s4 = np.zeros(w4.shape)
    bs1 = np.zeros(b1.shape)
    bs2 = np.zeros(b2.shape)
    bs3 = np.zeros(b3.shape)
    bs4 = np.zeros(b4.shape)

    # Parameter Update using RMSprop and momentum

    v1 = beta1 * v1 + (1 - beta1) * df1 / batch_size  # momentum update
    s1 = beta2 * s1 + (1 - beta2) * (df1 / batch_size) ** 2  # RMSProp update
    f1 -= lr * v1 / np.sqrt(s1 + 1e-7)  # combine momentum and RMSProp to perform update with Adam

    bv1 = beta1 * bv1 + (1 - beta1) * db1 / batch_size
    bs1 = beta2 * bs1 + (1 - beta2) * (db1 / batch_size) ** 2
    b1 -= lr * bv1 / np.sqrt(bs1 + 1e-7)

    v2 = beta1 * v2 + (1 - beta1) * df2 / batch_size
    s2 = beta2 * s2 + (1 - beta2) * (df2 / batch_size) ** 2
    f2 -= lr * v2 / np.sqrt(s2 + 1e-7)

    bv2 = beta1 * bv2 + (1 - beta1) * db2 / batch_size
    bs2 = beta2 * bs2 + (1 - beta2) * (db2 / batch_size) ** 2
    b2 -= lr * bv2 / np.sqrt(bs2 + 1e-7)

    v3 = beta1 * v3 + (1 - beta1) * dw3 / batch_size
    s3 = beta2 * s3 + (1 - beta2) * (dw3 / batch_size) ** 2
    w3 -= lr * v3 / np.sqrt(s3 + 1e-7)

    bv3 = beta1 * bv3 + (1 - beta1) * db3 / batch_size
    bs3 = beta2 * bs3 + (1 - beta2) * (db3 / batch_size) ** 2
    b3 -= lr * bv3 / np.sqrt(bs3 + 1e-7)

    v4 = beta1 * v4 + (1 - beta1) * dw4 / batch_size
    s4 = beta2 * s4 + (1 - beta2) * (dw4 / batch_size) ** 2
    w4 -= lr * v4 / np.sqrt(s4 + 1e-7)

    bv4 = beta1 * bv4 + (1 - beta1) * db4 / batch_size
    bs4 = beta2 * bs4 + (1 - beta2) * (db4 / batch_size) ** 2
    b4 -= lr * bv4 / np.sqrt(bs4 + 1e-7)

    new_params = [f1, f2, w3, w4, b1, b2, b3, b4]
    return new_params



# ----------------------------------------------------Others-------------------------------------------------------

'''
Load train
'''
def loadTrain(dataName, setName):
    data = []
    dataFile = open(dataName, 'r')
    lines = dataFile.readlines()[:4000] # we have been told to take only 4000 first for training
    for line in lines:
        ent = np.fromstring(line, dtype=float, sep=',')
        mat = ent[1:].reshape((3, 32, 32))
        data.append((ent[0] - 1, mat))

    print('Done loading ' + setName)
    return data

'''
load validation or test
'''
def loadData(dataName, setName, test=False):
    data = []
    dataFile = open(dataName, 'r')
    if test == False:
        lines = dataFile.readlines()[:1000]  # we have been told to take only 1000 first for validation
        for line in lines:
            ent = np.fromstring(line, dtype=float, sep=',')
            mat = ent[1:].reshape((3, 32, 32))
            data.append((ent[0] - 1, mat))
    else:
        for line in dataFile.readlines():
            ent = np.fromstring(line[2:], dtype=float, sep=',') # test....
            mat = ent.reshape((3, 32, 32))
            data.append(mat)

    print('Done loading ' + setName)
    return data


'''
create filter
'''
def create_filter(size, scale=1.0):
    stddev = scale / np.sqrt(np.prod(size))
    return np.random.normal(loc=0, scale=stddev, size=size)


'''
create weight matrix
'''
def create_weight_matrix(size):
    return np.random.standard_normal(size=size) * 0.01


'''
loss
'''
def categoricalCrossEntropy(probs, label):
    return -np.sum(label * np.log(probs))


'''
softmax for prediction
'''
def softmax(raw_preds):
    out = np.exp(raw_preds)  # exponentiate vector of raw predictions
    return out / np.sum(out)  # divide the exponentiated vector by its sum. All values in the output sum to 1.


'''
return index of the largest non-nan value in the array. Output is an ordered pair tuple
'''
def nanargmax(arr):
    idx = np.nanargmax(arr)
    idxs = np.unravel_index(idx, arr.shape)
    return idxs


if __name__ == "__main__":
    main()
