import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def main():

    # generates 2 random arrays of size 50000 with gaussian distribution of mean value 0, sigma 1.5 and size 500000
    N = 50000
    p = 0.002
    c_p = 0.998
    apples = np.random.normal(0, 1.5, [2, N]) 
    #simple_plot([apples[0]], [apples[1]], ['Fallen apples'], None, None, "fallen_apples.png")
    

    xbins = np.linspace(-10, 10, 200)
    ybins = np.linspace(-10, 10, 200)
    # fill it to 2D histogram
    H, xedges, yedges = np.histogram2d(apples[0], apples[1], bins=(xbins, ybins))


    # Cell centres
    xc = 0.5*(xedges[:-1] + xedges[1:])
    yc = 0.5*(yedges[:-1] + yedges[1:])
    XX, YY = np.meshgrid(xc, yc, indexing='ij')
 
    
    # =====================================================
    # Integrals inside circles of radius r = 2..10, step 0.1
    # =====================================================

    r_values = np.arange(2, 10.1, 0.1)
    radius_mask = XX**2 + YY**2  # squared distance of each bin centre

    print("=== Integral inside circles ===")
    for r in r_values:
        inside = radius_mask <= r*r	# returns true/false for each bin in 2D structure
        integral = np.sum(H[inside]) / N   # fraction of points inside
        print(f"r = {r:4.1f}   integral = {integral:.5f}")
        if integral > c_p: 
        	print(f"s = {s:4.1f}   integral = {integral:.5f}")    
        	break

    # =====================================================
    # Integrals inside circles - ALTERNATIVE
    # =====================================================

    print("=== Integral inside circles ===")
    for r in r_values:
        idx = np.where(XX*XX + YY*YY <= r*r)   # returns (i_indices, j_indices)    
        integral = np.sum(H[idx]) / N   # fraction of points inside
        print(f"r = {r:4.1f}   integral = {integral:.5f}")
        if integral > c_p: 
        	print(f"s = {s:4.1f}   integral = {integral:.5f}")    
        	break

    # =====================================================
    # Integrals inside squares of side s = 4..10, step 0.1
    # =====================================================

    s_values = np.arange(4, 10.1, 0.1)

    print("\n=== Integral inside squares ===")
    for s in s_values:
        half = s/2
        inside = (np.abs(XX) <= half) & (np.abs(YY) <= half)
        integral = np.sum(H[inside]) / N   # fraction of points inside
#        print(f"s = {s:4.1f}   integral = {integral:.5f}")    
        if integral > c_p: 
        	print(f"s = {s:4.1f}   integral = {integral:.5f}")    
        	break
    
    ## ----------------------------
    ## Let's try it also for 1D radius distribution - does it agree?
    
    # calculates the radial distance of all points from the origin
    dist = (apples[0]**2 + apples[1]**2)**0.5
    # makes a histogram of those radial distances with 500 bins between minimal and maximal value
    hist, edges = np.histogram(dist, bins = 500) 
    
    # calculates where the probability of getting hit is less than 0.2 %
    safe_zone = find_safe_distance(hist, edges, len(apples[0]), 0.002)
    
    # plots the histogram. the f'...{}' format allows one to execute code inside a string, the result of the code will then be converted to string.
    plot_histogram(hist, edges, None, 'Radial distance', f'Fallen apples / {np.round(edges[1] - edges[0], 3)} m', safe_zone, "fallen_apples_hist.png") 
    


def find_safe_distance(hist, edges, size, prob):

	#YOUR CODE HERE


def plot_histogram(hist, edges, lbl, xlabel, ylabel, line_pos, filename = None):
    plt.rcParams['font.size'] = 14 # change font size
    fig, ax = plt.subplots(figsize = [8,6]) # initialize image
    # plot histogram from histogram data and bin edge values
    ax.stairs(hist, edges, label = lbl, fill = False, color = 'black')
    # draw a vertical line where falling apples are unlikely
    ax.vlines(x = line_pos, ymin = 0, ymax=np.max(hist), color = 'red', label = f'Critical value at {np.round(line_pos, 2)}')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.show()
    if filename:
        fig.savefig(filename) # save image as png file




# function for plotting several datasets into the same image, 
# x and ydata are expected to be lists of arrays. 
# If only a single dataset is to be plotted, it must also be inside a list -> dataset = [dataset]

def simple_plot(xdata, ydata, labels, xlabel, ylabel, filename = None, mk = ','):

    plt.rcParams['font.size'] = 14 # changes font size
    fig, ax = plt.subplots(figsize = [8,6]) # creates a figure and a subplot object

    for x, y, l in zip(xdata, ydata, labels): # loop over several arrays at once (cuts when the first array finishes)
        # plot with pixel size points (not a histogram) when marker is ','
        ax.plot(x, y, label = l, marker = mk, linestyle = 'None')

    ax.legend() # includes a legend in the image
    ax.set_xlabel(xlabel) # gives a name to the x axis, below analogy for y axis
    ax.set_ylabel(ylabel) # matplotlib supports latex like math type-setting
    #ax.set_aspect('equal')

    plt.show() # displays the current figure 
    if filename:
        fig.savefig(filename) # saves the figure 'fig' as a png file


if __name__ == "__main__":
    main()
