# ROOT on Ubuntu

When installing CERN's ROOT framework on Ubuntu, we have two options: downloading a pre-compiled binary or using the Canonical Snap package. 

While Snap is convinient, it has limitations when working with Python virtual environments and kernels from Jupyter Notebooks, because it itself runs in a sandboxed environment. 

---

## Method 1: Pre-compiled Binary

This method involves downloading the pre-compiled ROOT binaries from CERN website. We can then hook ROOT into whichever Python interpreter is currently active.

### Installation

First, install the necessary Ubuntu system dependencies required by ROOT:

~~~bash
sudo apt-get update
sudo apt-get install -y dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
libxft-dev libxext-dev python3 libssl-dev
~~~

Next, download the latest version for Ubuntu 22.04 from the **[ROOT All Releases page](https://root.cern/install/all_releases/)**.

For Ubuntu 22.04, we have `gcc11.4` build. Here is an example using the current stable release:

~~~bash
# Navigate to your home directory
cd ~

# Download the stable release for Ubuntu 22.04
wget https://root.cern/download/root_v6.40.02.Linux-ubuntu22.04-x86_64-gcc11.4.tar.gz

# Extract the archive
tar -xzvf root_v6.40.02.Linux-ubuntu22.04-x86_64-gcc11.4.tar.gz
~~~

### Usage

To use ROOT, we must load its environment variables. Because we want to use it inside our `SZD` virtual environment, we should activate our Python environment first, and then source ROOT.

~~~bash
# Activate your Python virtual environment
source ~/path/to/SZD/bin/activate

# Source the ROOT environment script
source ~/root/bin/thisroot.sh

# Launch Jupyter
jupyter notebook
~~~

We can also open your virtual environment's activation script (`~/path/to/SZD/bin/activate`) and add `source ~/root/bin/thisroot.sh` to the very bottom. This way, ROOT is instantly available whenever we activate `SZD`.

~~~bash
# Add an empty line for readability
echo "" >> ~/SZD/bin/activate

# Add a comment explaining what it is
echo "# Automatically source ROOT environment" >> ~/SZD/bin/activate

# Add the actual source command
echo "source ~/root/bin/thisroot.sh" >> ~/SZD/bin/activate
~~~

---

## Method 2: Snap Package

The Snap package provides an isolated, containerized installation of ROOT. It bundles its own dependencies, ensuring it runs on almost any Linux distribution regardless of the host system.

### Installation

Usually:

~~~bash
sudo snap install root-framework
~~~

### Usage & Environment Integration

You can launch ROOT or its Python integration simply by calling the Snap aliases:

~~~bash
root
# or for python
pyroot
~~~


---

## Feature Comparison

Here is a breakdown of how the two methods contrast, specifically tailored for a PyROOT/Jupyter workflow:

| Feature | Pre-compiled Binary | Snap Package |
| :--- | :--- | :--- |
| **Updates** | Manual (check [all_releases](https://root.cern/install/all_releases/)) | Automatic |
| **System Modification** | Modifies current shell via `thisroot.sh` | Runs system-wide as a sandboxed app |
| **Python Virtual Envs** | Excellent: Binds directly to the active venv | Poor: Uses isolated, internal Python |
| **Filesystem Access** | Full access to your system | Restricted by Snap confinement rules |
