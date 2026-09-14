import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import numpy as np


def main():
    filename = 'weather_data.csv'
    df = pd.read_csv(filename)
    time = pd.to_datetime(df['utc_timestamp'])

    ref_times = ["1980-01-01","1990-01-01","2000-01-01","2010-01-01", "2020-01-01"] #create reference datetimes to showcase conditional operation on pandas dataframes

    xdata = [time[(time >= n) & (time < m)] for n, m in zip(ref_times[:-1], ref_times[1:])] # pandas allows conditional operation on its elements, in this case our time axis is split into 4 regions according to a decade time intervals
    ydata = [df['CZ_temperature'][(time >= n) & (time < m) ] for n, m in zip(ref_times[:-1], ref_times[1:])] # the temperature column is split with the same conditional mask
    labels = ['yrs \'80 - \'90','yrs \'90 - \'00','yrs \'00 - \'10','yrs \'10 - \'20'] # label strings for the plot legend

    simple_plot(xdata, ydata, labels, 'Date' ,'Temperature [$^\\circ$C]', 'temperature.png') #calling the plot function inside the main function
    fourier(time, df['CZ_temperature'].to_numpy())


def simple_plot(xdata, ydata, labels, xlabel, ylabel, filename = None): #function for plotting several datasets into the same image, x and ydata are expected to be lists of arrays. If only a single dataset is to be plotted, it must also be inside a list -> dataset = [dataset]

    plt.rcParams['font.size'] = 14 # changes font size
    fig, ax = plt.subplots(figsize = [8,6]) # creates a figure and a subplot object

    for x, y, l in zip(xdata, ydata, labels): # loop over several arrays at once (cuts when the first array finishes)
        ax.plot(x, y, label = l) # line plot of x and y with a label to displayed inside a legend

    ax.legend() # includes a legend in the image
    ax.set_xlabel(xlabel) # gives a name to the x axis, below analogy for y axis
    ax.set_ylabel(ylabel) # matplotlib supports latex like math type-setting

    plt.show() # displays the current figure 
    if filename:
        fig.savefig(filename) # saves the figure 'fig' as a png file


def fourier(time, data):
    yf = fft(data, n = time.size - 20) # performs a fast fourier transform on our dataset
    xf = fftfreq(time.size - 20, 1) # calculates the sampling frequency bins (used for plotting)

    periods = 1 / xf / 24
    simple_plot([periods], [np.abs(yf)], ['FFT temperature'], 'Period [days]', 'Amplitude [arb.]', 'fft_temperature.png')


if __name__ == "__main__":
    main()