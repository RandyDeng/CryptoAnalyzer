import numpy as np

def running_avg(data, N):
    return np.convolve(x, np.ones((N,))/N, mode='valid')

def exponential_avg(data, N):
    weights = np.exp(np.linspace(-1, 0, N))
    output = np.convolve(x, weights / weights.sum(), mode='valid')[:len(data)]
    output[:N] = output[N]
    return output

def momentum_line(data, F):
    moments = np.zeros((len(data),))
    counter = 0
    last_data = 0
    for current_data in data:
        if counter == 0:
            moments[counter] = 0
        else:
            moments[counter] = moments[counter - 1] + (current_data - last_data) * F
            last_data = current_data
        counter++
    return moment
