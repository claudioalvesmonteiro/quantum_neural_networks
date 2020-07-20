import pandas as pd
import numpy as np

df = pd.read_csv('dataset.csv')
x_train = df.iloc[:, :-1].to_numpy()
y_train = df.iloc[:, -1].to_numpy()

data_len = len(y_train)
input_dim = x_train.shape[-1]
nb_epochs = 20
lr = 0.01

def deterministicBinarization (w):
    # This function makes a Deterministic Binarization of a given weights list
    w2 = [0] * len(w)

    for i in range(len(w)):
        if w[i] >= 0:
            w2[i] = 1
        else:
            w2[i] = -1
    
    return w2

def hardSigmoid(x):
    result = max(0,min(1,(x+1)/2))
    return result 

def stochasticBinarization(w):
    # This function makes a Stochastic Binarization of a given weights list based on the hard sigmoid function
    w2 = [0] * len(w)

    for i in range(len (w)):
        w2[i] = hardSigmoid(w[i])

    return w2

def makeBinarization(w, stochastic=True):
    if stochastic:
        return stochasticBinarization(w)
    else:
        return deterministicBinarization(w)

def runNeuron (nb_epochs, binaryWeights=False, stochastic=True):
    w = np.random.rand(input_dim) # Real weights
    wB = makeBinarization(w, stochastic) # Binarization of Real weights

    for epoch in range(nb_epochs):
        y_pred = np.zeros(data_len)
        for i, x in enumerate(x_train):

            if binaryWeights:
                out = np.sum(np.multiply(x, wB))
            else:
                out = np.sum(np.multiply(x, w))

            if out > 0:
                y_pred[i] = 1
            delta = y_train[i] - y_pred[i]

            for j in range(input_dim):
                w[j] = w[j] + (lr * delta * x_train[i][j])
            
            wB = makeBinarization(w, stochastic)

        hits = (y_train == y_pred).sum()
        print('Epoch {:d} accuracy: {:.2f}'.format(epoch + 1, (hits / data_len) * 100))

print("100 epocas, pesos reais")
runNeuron (nb_epochs=100, binaryWeights=False)

print("100 epocas, pesos binarizados deterministicamente")
runNeuron (nb_epochs=100, binaryWeights=True, stochastic=False)

print("100 epocas, pesos binarizados estocasticamente")
runNeuron (nb_epochs=100, binaryWeights=True, stochastic=True)
