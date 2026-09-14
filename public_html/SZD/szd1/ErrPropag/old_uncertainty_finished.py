import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def main():
    haa_gaus, hpp_gaus, raa = [], [], []  #prepare a list of (now not yet existing) numpy arrays

    for bin in chosenBins: # fill lists according to some distribution defined in generate_random_samples
        new_haa, new_hpp, new_raa = generate_random_samples([hAA_content[bin], hpp_content[bin]], [hAA_errors[bin], hpp_errors[bin]], numSimul)
        haa_gaus.append(new_haa)
        hpp_gaus.append(new_hpp)
        raa.append(new_raa)

    histograms, edges = make_histograms([haa_gaus, hpp_gaus, raa]) # from our toy random values generate histograms (and remember the edges of their bins)
    plt.rcParams['font.size'] = 14 # prepare a fit
    fig, axs = plot_histograms(histograms, edges)

    max_values = [np.max(hists[2]) for hists in histograms] # code here - boundary values of the left / right sided fits

    try: # attempt fitting the histograms with gaussian distribution
        fits, centers = fit_histograms(histograms, edges, max_values) 

        for fit, ax, center in zip(fits, axs, centers): # to each ratio histogram plot add the fitting curve
            ax[2].plot(center[:np.argmax(gaussian(center, *fit[0]))], gaussian(center[:np.argmax(gaussian(center, *fit[0]))], *fit[0]), label = f'$\\sigma_l = {np.round(fit[0][1], 3)}$') # element selection: finds maximum value of the fit and plots the curve from left to max; *fit[0] means "call elements of fit[0] as individual parameters of the function gaussian()"
            ax[2].plot(center[np.argmax(gaussian(center, *fit[0])):], gaussian(center[np.argmax(gaussian(center, *fit[0])):], *fit[1]), label = f'$\\sigma_r = {np.round(fit[1][1], 3)}$')
            ax[2].set_yscale('log')
            ax[2].legend(loc = 'upper right')
    except: # if fitting for some reason fails, let the images be plotted without them
        print('fit not performed')
    for ax, l in zip(axs[2], ['$h_{pp}$', '$h_{AA}$', '$R_{AA}$']):
        ax.set_xlabel(l)
    fig.tight_layout() # set predefined figure borders (no overlap or redundant white space)
    plt.show() # display figure

    filename = 'RAA_plots.png'
    fig.savefig(filename)

    return 0


def make_histograms(data, binNum = 100): # expects 3 x numOfBins sets of arrays in format [haa, hpp, raa]
    histograms = [[] for _ in range(3)] # make a list of 3 empty lists
    edges = [[] for _ in range(3)] # same for edges

    for datum in data: # goes over rows of the final plot
        for i in range(3): # hard coded 3 for haa, hpp and raa histograms
            newHist, newEdges = np.histogram(datum[i], bins = binNum) # CODE HERE
            histograms[i].append(newHist) # CODE HERE
            edges[i].append(newEdges) # CODE HERE
    return histograms, edges # return two lists - triplets of histograms and triplets of edges


def plot_histograms(hists, edges): # expects triplets of histograms and triplets of edges (for each row)
    fig, axs = plt.subplots(numOfBins, 3, figsize = [12,int(numOfBins*4)]) # prepare the figure
    for hist, edge, ax_row in zip(hists, edges, axs): # ax_row is a list of axes objects (with size 3)
        for ax, h, e in zip(ax_row, hist, edge):
            ax.stairs(h, edges = e, color = 'black') # CODE HERE
    return fig, axs # returns the figure object and axes.


def generate_random_samples(mu, sigmas, num): # generate 2 gaussian distributed sets of size numSimul and their product
    gaus1 = np.random.normal(mu[0], sigmas[0], num) # code here
    gaus2 = np.random.normal(mu[1], sigmas[1], num) # code here
    ratio = gaus1 / gaus2 # code here
    return gaus1, gaus2, ratio # return the sets


def fit_histograms(histograms, edges, max_values): # fit the histogram (binned data) with the function gaussian()
    centers = [] # prepare an empty list for bin centers
    for edge_triplets in edges: 
        centers.append(find_bin_centers(edge_triplets[2])) # fill the list with center lists.

    fits = [] # prepare an empty list of fit parameters (each element containing two lists of fit values - fit[0] is left fit, fit[1] is right fit)
    for hist, center, max_value in zip(histograms, centers, max_values): # fitting loop; to limit which values are used for fitting try using the function np.where.
        fit1, pcov = curve_fit(gaussian, center[:np.argmax(hist[2])], hist[2][:np.argmax(hist[2])], p0 = [1,1,1]) # code here
        fit2, pcov = curve_fit(gaussian, center[np.argmax(hist[2]):], hist[2][np.argmax(hist[2]):], p0 = [1,1,1]) # code here
        fits.append([fit1, fit2]) # code here

    return fits, centers 
    

def gaussian(x, a,b,c): # gaussian function used for fitting
    return a * np.exp(- (x - b) ** 2 / (2 * c ** 2) )


def find_bin_centers(edges): # the function np.histogram produces bin edges. This simply converts edges to centers used for fitting
    return (edges[1:] + edges[:-1]) / 2


# 1. Bin edges (xAxis1)
xAxis1 = np.array([-100, -80, -60, -40, -20, -10, -5, -3, -1, 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 60, 70, 80, 100])

# 2. Bin content for hpp
hpp_content = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1.118516, 0.1920894, 0.007120608, 0.001577695, 0.0004146155, 0.0001296542, 4.644327e-05, 2.057404e-05, 9.958874e-06, 4.334099e-06, 1.442999e-06, 5.654266e-07, 2.407638e-07, 1.094223e-07, 3.354351e-08, 6.04691e-09, 7.423793e-10, 3.350337e-11, 0, 0, 0, 0])

# 3. Bin errors for hpp
hpp_errors = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0.0006107765, 0.0003700558, 4.49924e-05, 1.821935e-05, 7.447584e-06, 2.939223e-06, 1.155389e-06, 5.875219e-07, 1.855936e-07, 1.141886e-07, 3.0114e-08, 5.526975e-09, 2.701332e-09, 1.525211e-09, 6.343152e-10, 9.460454e-11, 2.709424e-11, 4.271672e-13, 0, 0, 0, 0])

# 4. Bin content for hAA
hAA_content = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0004135252, 0.0001128615, 5.329878e-05, 2.740152e-05, 1.417387e-05, 8.002939e-06, 3.765388e-06, 1.418623e-06, 5.724047e-07, 2.704585e-07, 1.308473e-07, 3.482406e-08, 5.969517e-09, 8.159869e-10, 1.976192e-11, 0, 0, 0, 0])

# 5. Bin errors for hAA
hAA_errors = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.06535e-06, 4.957864e-07, 3.151375e-07, 2.136749e-07, 1.451485e-07, 1.005136e-07, 5.988379e-08, 3.659272e-08, 2.201622e-08, 1.464843e-08, 9.694462e-09, 3.96629e-09, 1.470905e-09, 4.142606e-10, 1.499208e-11, 0, 0, 0, 0])


if __name__ == "__main__":

    chosenBins = [22, 23, 24] # what data will be used
    numOfBins = len(chosenBins) # how many rows of images are to be produced
    numSimul = int(1e6) # how many values are to be generated for each bin

    main()