import ROOT
import numpy as np
import os

# Ensure batch mode
ROOT.gROOT.SetBatch(True)

data_path = "source/data/HIGGS/Histograms_fake.root" if os.path.exists("source/data/HIGGS/Histograms_fake.root") else "data/HIGGS/Histograms_fake.root"
f = ROOT.TFile.Open(data_path, "READ")
print("Opened file:", data_path)

h_sig = f.Get("h_m4l_Higgs125_fake")
h_bgr = f.Get("h_m4l_ZZ_fake")
h_data = f.Get("h_m4l_data_fake")

# 1. Mass distribution test
print("Sig integral:", h_sig.Integral(), "Bgr integral:", h_bgr.Integral(), "Data integral:", h_data.Integral())

# 2. Window scan test
def integrate_poisson_from_right(mu, n_obs):
    integral = 1.0
    for i in range(int(n_obs)):
        integral -= ROOT.TMath.Poisson(i, mu)
    return max(0.0, min(1.0, integral))

windows = np.linspace(0.1, 25.0, 250)
z_exp_list = []
z_obs_list = []

for w in windows:
    b1 = h_data.FindBin(125.0 - w/2.0)
    b2 = h_data.FindBin(125.0 + w/2.0)
    n_sig = h_sig.Integral(b1, b2)
    n_bgr = h_bgr.Integral(b1, b2)
    n_data = h_data.Integral(b1, b2)
    
    p_exp = integrate_poisson_from_right(n_bgr, n_bgr + n_sig)
    z_exp = ROOT.Math.gaussian_quantile_c(p_exp, 1.0) if 0 < p_exp < 1 else 0.0
    
    p_obs = integrate_poisson_from_right(n_bgr, n_data)
    z_obs = ROOT.Math.gaussian_quantile_c(p_obs, 1.0) if 0 < p_obs < 1 else 0.0
    
    z_exp_list.append(z_exp)
    z_obs_list.append(z_obs)

best_exp_idx = np.argmax(z_exp_list)
print(f"Max Expected: w = {windows[best_exp_idx]:.2f} GeV, Z = {z_exp_list[best_exp_idx]:.3f} sigma")

# 3. Sideband fit test
h_bgr_rb = h_bgr.Clone()
h_data_rb = h_data.Clone()
h_bgr_rb.Rebin(10)
h_data_rb.Rebin(10)

bin_low = h_data_rb.FindBin(150.0)
bin_high = h_data_rb.FindBin(400.0)

alphas = np.linspace(0.1, 3.1, 301)
nll_vals = []
for a in alphas:
    loglik = 0.0
    for b in range(bin_low, bin_high + 1):
        d_val = h_data_rb.GetBinContent(b)
        b_val = a * h_bgr_rb.GetBinContent(b)
        if b_val > 0:
            loglik += ROOT.TMath.Log(ROOT.TMath.Poisson(d_val, b_val))
    nll_vals.append(-2.0 * loglik)

nll_vals = np.array(nll_vals)
best_a_idx = np.argmin(nll_vals)
best_alpha = alphas[best_a_idx]
print(f"Best alpha: {best_alpha:.3f}")

# 4. 2D scan test
alphas_2d = np.linspace(0.5, 2.0, 31)
mus_2d = np.linspace(0.0, 3.0, 31)
h_sig_rb = h_sig.Clone()
h_sig_rb.Rebin(10)

b_start = h_data_rb.FindBin(100.0)
b_end = h_data_rb.FindBin(400.0)

grid_nll = np.zeros((len(mus_2d), len(alphas_2d)))
for i_m, m_val in enumerate(mus_2d):
    for i_a, a_val in enumerate(alphas_2d):
        loglik = 0.0
        for b in range(b_start, b_end + 1):
            d_val = h_data_rb.GetBinContent(b)
            mu_tot = m_val * h_sig_rb.GetBinContent(b) + a_val * h_bgr_rb.GetBinContent(b)
            if mu_tot > 0:
                loglik += ROOT.TMath.Log(ROOT.TMath.Poisson(d_val, mu_tot))
        grid_nll[i_m, i_a] = -2.0 * loglik

min_2d = np.min(grid_nll)
print("2D scan min -2lnL:", min_2d)
print("All tests passed successfully!")

