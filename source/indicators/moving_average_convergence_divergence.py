from .moving_average import *

def moving_average_convergence_divergence(prices, nslow=26, nfast=12):
    emaslow = moving_average(prices, nslow, True)
    emafast = moving_average(prices, nfast, True)
    return emaslow, emafast, emafast - emaslow