import math
import numpy as np
from scipy.stats import norm
from scipy.stats import poisson




mu_b = 15      # background-only MC prediction
mu_s = 5       # signal MC prediction
n_obs = 25     # experimentally measured events

#null hypothesis is that only background exists and there is no signal


# Discovery thresholds for p   (Z = 5)
discovery_pvalue = 2.91e-7


# 1) What is the expected significance?

n_exp = int(mu_b + mu_s)
#p value  - probability P(n >= n_exp | mu_b)
p_exp = poisson.sf(n_exp -1, mu_b)
# Z value corresponding to p value
Z_exp = norm.isf(p_exp) #Inverse Survival Function
print(f"Expected p-value: {p_exp:.5f}")
print(f"Expected significance Z: {Z_exp:.3f} sigma")

# 2) What is the observed significance?

#p value  - probability P(n >= n_obs | mu_b)
p_obs = poisson.sf(n_obs -1, mu_b)
# Z value corresponding to p value
Z_obs = norm.isf(p_obs) #Inverse Survival Function
print(f"Observed p-value: {p_obs:.5f}")
print(f"Observed significance Z: {Z_obs:.3f} sigma")

#3) How many times larger luminosity do I need in my experiment to announce a discovery?
discovery_Z = norm.isf(discovery_pvalue) # Z value corresponding to discovery p-value
print(f"discovery_Z: {discovery_Z}")

# we want to find scaling factor k for the experiment so that the expected significance reaches discovery_pvalue



for k in range(1, 20):
    n_exp_scaled = int(k * n_obs)
    mu_b_scaled = k * mu_b
    p_exp_scaled = poisson.sf(n_exp_scaled - 1, mu_b_scaled)
    Z_exp_scaled = norm.isf(p_exp_scaled)
    
    print(k)
    print(n_exp_scaled)
    print(mu_b_scaled)
    print(p_exp_scaled)
    
    if Z_exp_scaled >= discovery_Z:
    	print(f"Discovery p-value: {discovery_pvalue:.4e} corresponds to Z: {discovery_Z:.3f} sigma")
    	print(f"Required luminosity scaling: {k:.2f}")
    	break

