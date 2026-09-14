import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

size_true = 500
size_I = 2500
size_II = 2500

a = 0
b = 200
bins = 200

mean = 100.
std = 10.

true_gauss = np.random.normal(mean, std, size_true)
background_I = np.random.uniform(a, b, size_I)
background_II = np.random.uniform(a, b, size_II)

edges = np.linspace(a, b, bins+1)
hist_true, _ = np.histogram(true_gauss, bins=edges)
hist_I, _ = np.histogram(background_I, bins=edges)
hist_II, _ = np.histogram(background_II, bins=edges)

fig, ax = plt.subplots(1, 1, figsize=(6, 4))

hist_total = hist_true + hist_I - hist_II

#make negative values zero
hist_total = np.maximum(hist_total, 0.000001)

#y = size_true/(2.5*std) * np.exp(-(edges - mean)**2/(2*std**2))
#plt.plot(edges, y, label='Function Plot')






def gaussian_model(x, mu, sigma, amplitude):
    return amplitude * np.exp(-0.5 * ((x - mu)/sigma)**2)

# Compute bin centers
bin_centers = 0.5 * (edges[:-1] + edges[1:])


def poisson_loglike(data, expected):
    return np.sum(data * np.log(expected) - expected)
    
# here we get error via poisson approx:  sigma^2 = N    
def chi2_sum(data, expected):    
    return #  YOUR CODE HERE
    

mu_grid = np.linspace(50, 150, 201)       # means from 0–100 in steps of 0.5
sigma_grid = np.linspace(5, 20, 200)     # reasonable sigma scan

idx = np.argmax(hist_total)
amplitude_guess = hist_total[idx]

best_logL = -np.inf
best_mu = 0.3
best_sigma = 0.3

best_chiSum = np.inf
best_chi_mu = 0.3
best_chi_sigma = 0.1

for mu in mu_grid:
    for sigma in sigma_grid:
        expected = gaussian_model(bin_centers, mu, sigma, amplitude_guess)
        expected = np.maximum(expected, 0.0000000001)	#to avoid infinities in log
        logL = poisson_loglike(hist_total, expected)
        chiSum = chi2_sum(hist_total, expected)
        if logL > best_logL:
            best_logL = logL
            best_mu = mu
            best_sigma = sigma
        if chiSum < best_chiSum:
            best_chiSum = chiSum
            best_chi_mu = mu
            best_chi_sigma = sigma



#A = best_params[2]
#y = A * np.exp(-0.5 * ((bin_centers - best_params[0]) / best_params[1])**2)
#ax.plot(bin_centers, y, color='red')



print("Best MLM parameters:")
print(f"  mean    = {best_mu}")
print(f"  sigma   = {best_sigma}")
print(f"  amplitude = {amplitude_guess}")
print(f"  log‑likelihood = {best_logL}")


print("Best chi2 parameters:")
print(f"  mean    = {best_chi_mu}")
print(f"  sigma   = {best_chi_sigma}")
print(f"  amplitude = {amplitude_guess}")
print(f"  chi2 sum = {best_chiSum}")



y = amplitude_guess * np.exp(-(bin_centers - best_mu)**2/(2*best_sigma**2))

z = amplitude_guess * np.exp(-(bin_centers - best_chi_mu)**2/(2*best_chi_sigma**2))

plt.stairs(hist_total, edges)
plt.plot(bin_centers, y, color='red')
plt.plot(bin_centers, z, color='green')
plt.show()



