import numpy as np


def toPercentile(value, dataset, accuracy=0.005):
    guess = 50
    prevguess = 0

    value = float(value)
    dataset = [float(i) for i in dataset]

    while abs(prevguess - guess) > accuracy:
        nextguess = toPercentileIterative(guess, prevguess, value, dataset)

        prevguess = guess
        guess = nextguess

    return round(guess,1)


def toPercentileIterative(guess, prevguess, value, dataset):
    guess = float(guess)
    prevguess = float(prevguess)
    value = float(value)
    testval = float(np.percentile(dataset, guess))
    if testval < value:
        return guess + abs(guess - prevguess) / 2
    else:
        return guess - abs(guess - prevguess) / 2





