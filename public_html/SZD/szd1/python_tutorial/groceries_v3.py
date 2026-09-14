import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## NOTE: this is the third way how to run python - no main function needed


# Load CSV file, automatically using the first row as column names
#df = pd.read_csv("nakup.csv")				# for comas
#df = pd.read_csv("nakup.csv", delim_whitespace=True)	# for a single break
df = pd.read_csv("nakup.csv", sep = '\t')		# for a tab space

# Optional: show the first few rows to check
print("Data preview:")
print(df.head())

# Make histogram of the second column (cena_za_jednotku)
plt.figure(figsize=(6, 4))
plt.hist(df['cena_za_jednotku'], bins=5, edgecolor='black', color='skyblue')
plt.title('Histogram – Cena za jednotku')
plt.xlabel('Cena (Kč)')
plt.ylabel('Počet položek')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
#plt.show()

# Make histogram of the third column (mnozstvi)
plt.figure(figsize=(6, 4))
plt.hist(df['mnozstvi'], bins=5, edgecolor='black', color='lightgreen')
plt.title('Histogram – Množství')
plt.xlabel('Množství (ks)')
plt.ylabel('Počet položek')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
#plt.show()


bin_edges=(0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5)
plt.figure(figsize=(6, 4))
plt.hist(df['mnozstvi'], bin_edges, edgecolor='black', color='lightgreen')
plt.title('Histogram – Množství')
plt.xlabel('Množství (ks)')
plt.ylabel('Počet položek')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
#plt.show()


plt.figure(figsize=(6, 4))
plt.hist(df['mnozstvi'], bins=6, range=(0.5, 6.5), edgecolor='black', color='lightgreen')
plt.title('Histogram – Množství')
plt.xlabel('Množství (ks)')
plt.ylabel('Počet položek')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
#plt.show()


bin_edges = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
# Extract the data
data = df['mnozstvi'].values
# Compute histogram counts
hist_counts, bin_edges = np.histogram(data, bins=bin_edges)
## actually you can avoid things you do not need using _ :
hist_counts, _ = np.histogram(data, bins=bin_edges)
_, bin_edges = np.histogram(data, bins=bin_edges)
# Show results
print("Bins:", bin_edges)
print("Counts:", hist_counts)
plt.figure(figsize=(6, 4))
## NOW we use different way how to draw a histogram; looks the same
plt.bar(bin_centers, hist_counts, width=1.0, edgecolor='black', color='lightgreen')
plt.title('Histogram – Množství')
plt.xlabel('Množství (ks)')
plt.ylabel('Počet položek')
plt.xticks(bin_centers)  # show each bin as integer
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

## NOTE:
## there is no difference between numpy array and a simple tuple of numbers; you can use both
#data = [1, 2, 3, 4, 5]
#bins_array = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
#bins_tuple = (0.5, 1.5, 2.5, 3.5, 4.5, 5.5)
#hist_array, _ = np.histogram(data, bins=bins_array)
#hist_tuple, _ = np.histogram(data, bins=bins_tuple)















