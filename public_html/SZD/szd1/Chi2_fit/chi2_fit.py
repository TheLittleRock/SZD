
import numpy as np
from scipy.optimize import curve_fit

# -------------------------
# Input data
# -------------------------
x_position = np.array([0.42, 0.38, 0.32, 0.33])
x_error    = np.array([0.06, 0.08, 0.07, 0.05])

# Fit parameter scanning range (same as ROOT example)
grid_x_size = 100
c_values = np.linspace(0.32, 0.42, grid_x_size + 1)

# -------------------------
# (1) Manual chi2 scan
# -------------------------
def chi2_value(c):
    return np.sum(((x_position - c) ** 2) / (x_error ** 2))

chi2_list = np.array([chi2_value(c) for c in c_values])

i = np.argmin(chi2_list)
min_chi2 = chi2_list[i]
best_c = c_values[i]

print("Manual fit:")
print(f"  best c = {best_c:.6f}")
print(f"  chi2   = {min_chi2:.6f}")
print()

# -------------------------
# (2) SciPy fit equivalent to ROOT TF1("[0]")
# -------------------------

# constant function for fitting
def model(x, c):
    return c

# Fake x-bin centers (ROOT would ignore x values in constant fit)
x_dummy = np.arange(len(x_position))

# Use sigma = errors → χ² fit like ROOT
popt, pcov = curve_fit(model, x_dummy, x_position, sigma=x_error, absolute_sigma=True)

c_fit = popt[0]

# Compute chi2 from the fit result
residuals = (x_position - model(x_dummy, c_fit)) / x_error
chi2_fit = np.sum(residuals ** 2)
ndf = len(x_position) - 1

print("SciPy fit (ROOT-like):")
print(f"  fitted c = {c_fit:.6f}")
print(f"  chi2     = {chi2_fit:.6f}")
print(f"  NDF      = {ndf}")
print()

# -------------------------
# Compare results
# -------------------------
print("Comparison:")
print(f"  SciPy fit:  {c_fit:.6f}")
print(f"  Manual:     {best_c:.6f}")
print(f"  Δ = {abs(c_fit - best_c):.6e}")


