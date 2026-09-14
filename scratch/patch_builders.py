import re

# 1. Fix build_majak_notebook.py
with open("scratch/build_majak_notebook.py", "r", encoding="utf-8") as f:
    content_m = f.read()

# Fix literal \n in cell 7
old_msg_stats = 'msg_stats = (f"$N = {n_hits:,}\\\\n"\\n             f"$\\\\bar{{x}} - \\\\tilde{{x}} = {sample_mean - sample_median:+.3f}\\\\ \\\\mathrm{{km}}$")'
new_msg_stats = 'msg_stats = f"$N = {n_hits:,}$\\n" + f"$\\\\bar{{x}} - \\\\tilde{{x}} = {sample_mean - sample_median:+.3f}\\\\ \\\\mathrm{{km}}$"'
if old_msg_stats in content_m:
    content_m = content_m.replace(old_msg_stats, new_msg_stats)
    print("Fixed msg_stats in build_majak_notebook.py")

# Fix literal \n in cell 17
old_msg_contour = 'msg_contour = "Orthogonal axes\\\\nCorrelation $\\\\rho \\\\approx 0$"'
new_msg_contour = 'msg_contour = "Orthogonal axes\\n" + r"Correlation $\\rho \\approx 0$"'
if old_msg_contour in content_m:
    content_m = content_m.replace(old_msg_contour, new_msg_contour)
    print("Fixed msg_contour in build_majak_notebook.py")

with open("scratch/build_majak_notebook.py", "w", encoding="utf-8") as f:
    f.write(content_m)

# 2. Fix build_jpsi_notebook.py
with open("scratch/build_jpsi_notebook.py", "r", encoding="utf-8") as f:
    content_j = f.read()

# Position of pbox in cell 10: lower it slightly to 0.16-0.34
content_j = content_j.replace('pbox = ROOT.TPaveText(0.18, 0.18, 0.46, 0.38, "NDC")',
                              'pbox = ROOT.TPaveText(0.18, 0.16, 0.45, 0.34, "NDC")')

# Position of textstr in cell 16: lower it to 0.38
content_j = content_j.replace('ax.text(0.04, 0.48, textstr, transform=ax.transAxes, fontsize=8.8, verticalalignment="top", bbox=props)',
                              'ax.text(0.04, 0.38, textstr, transform=ax.transAxes, fontsize=8.5, verticalalignment="top", bbox=props)')

with open("scratch/build_jpsi_notebook.py", "w", encoding="utf-8") as f:
    f.write(content_j)

print("Builder scripts patched successfully!")

