import numpy

def moving_average(prices, period, exponential=False):
    x = numpy.asarray(prices)
    weights = None
    if not exponential:
        weights = numpy.ones(prices)
    else:
        weights = numpy.exp(numpy.linspace(-1., 0., period))

    weights /= weights.sum()

    a = numpy.convolve(x, weights, mode='full')[:len(x)]
    a[:period] = a[period]
    return a
    