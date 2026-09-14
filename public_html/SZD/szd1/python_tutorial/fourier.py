import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import numpy as np
from scipy.optimize import curve_fit


def main():
    #filename = 'weather_data.csv'
    #df = pd.read_csv(filename)
    #time = pd.to_datetime(df['utc_timestamp'])

    #fourier(time, df['CZ_temperature'].to_numpy())
    #fit_with_sine(time, df['CZ_temperature'].to_numpy())

    # random_data1D = np.random.uniform(0,1,10000)
    # values, edges = np.histogram(random_data1D, bins = 100)
    
    # plt.rcParams['font.size'] = 14
    # fig, ax = plt.subplots(figsize = [8,6])
    
    # ax.stairs(values, edges, label = 'Random Uniform data', fill = True)
    # ax.set_xlabel('Random value')
    # ax.set_ylabel('Occurance')
    # ax.legend()
    # plt.show()
    # fig.savefig('random_hist1D.png')


    gaus1 = np.random.normal(6, 0.5, [2, 5000])
    gaus2 = np.random.normal(5, 0.3, [2, 1000])

    hist1, xedges, yedges = np.histogram2d(*gaus1, bins = [20, 20])
    hist2, xedges, yedges = np.histogram2d(*gaus2, bins = [xedges, yedges])
    hist = hist1 + hist2

    plot_histogram(hist, xedges, yedges, 'x label', 'y label', '2d_histogram.png')


def plot_histogram(hist, xedges, yedges, xlabel, ylabel, filename = None):

    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(figsize = [8,6])
    hist_fig = ax.imshow(hist, extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]])
    fig.colorbar(hist_fig)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
    if filename:
        fig.savefig(filename)


def simple_plot(xdata, ydata, labels, filename, xlabel, ylabel): #function for plotting several datasets into the same image, x and ydata are expected to be lists of arrays. If only a single dataset is to be plotted, it must also be inside a list -> dataset = [dataset]

    plt.rcParams['font.size'] = 14 # changes font size
    fig, ax = plt.subplots(figsize = [8,6]) # creates a figure and a subplot object

    for x, y, l in zip(xdata, ydata, labels): # loop over several arrays at once (cuts when the first array finishes)
        ax.plot(x, y, label = l) # line plot of x and y with a label to displayed inside a legend

    ax.legend() # includes a legend in the image
    ax.set_xlabel(xlabel) # gives a name to the x axis, below analogy for y axis
    ax.set_ylabel(ylabel) # matplotlib supports latex like math type-setting

    plt.show() # displays the current figure 
    fig.savefig(filename) # saves the figure 'fig' as a png file


def fourier(time, data):
    yf = fft(data) # performs a fast fourier transform on our dataset
    xf = fftfreq(time.size, 1) # calculates the sampling frequency bins (used for plotting) based on the length of our dataset

    periods = 1 / xf / 24
    simple_plot([periods], [np.abs(yf)], ['FFT temperature'], 'fft_temperature.png', 'Period [days]', 'Amplitude [arb.]')


def sinx(x, amp, freq, phase, con):
    return amp * np.sin(2 * np.pi * freq * x + phase) + con


def fit_with_sine(time, ydata):
    xdata = np.arange(0, time.size, 1) # make hours array with step size 1 hour

    fit, pcov = curve_fit(sinx, xdata, ydata, p0 = [30, 1/(365*24), 0, 9]) # fit data with predifined sin function and initialize fitting with parameters p0, produces least squares parameters and covariance matrix
    fit_values = sinx(xdata, *fit) # inserts xdata array into our sinx function with fit parameters (the * operator calls each element of fit individually)
    #fit_values = sinx(xdata, *[30, 1/(365*24), np.pi, 9])
    
    simple_plot([xdata, xdata], [ydata, fit_values], ['data', 'fit'], 'fit.png', 'Time [hours]', 'Temperature [$^\\circ$C]')


if __name__ == "__main__":
    main()