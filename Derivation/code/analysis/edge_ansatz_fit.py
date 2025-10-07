#!/usr/bin/env python3
"""Ansatz coefficient fitting script.

This script fits coefficients for the ansatz using optimization techniques.
"""
import numpy as np
from scipy.optimize import curve_fit

def ansatz(x, a, b):
    return a * x + b

def fit_data(x_data, y_data):
    params, _ = curve_fit(ansatz, x_data, y_data)
    return params

def main():
    x_data = np.array([1, 2, 3, 4, 5])
    y_data = np.array([2.2, 2.8, 3.6, 4.5, 5.1])
    params = fit_data(x_data, y_data)
    print(f'Fitted parameters: {params}')

if __name__ == '__main__':
    main()
