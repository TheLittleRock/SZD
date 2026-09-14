# https://compose.obspm.fr/eos/251

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import odeint

# physical constants in cgs units
pi = np.pi
G = 6.67430e-8
c = 2.99792458e10
Msun = 1.98847e33
MeV_fm3_to_cgs = 1.60218e33


# calculation settings

eos_file = "eos/eos_326.table"

cd_points = 300
dr = 1200

# try different interpolation methods:
# "nearest", "linear", "quadratic", "cubic"
interpolation_kind = "linear"

# try different colormaps:
# "viridis", "plasma", "inferno", "magma", "turbo"
colormap = "inferno"


class TOV:
    def __init__(self, en_arr, p_arr):
        en_arr = en_arr * MeV_fm3_to_cgs / c**2
        p_arr = p_arr * MeV_fm3_to_cgs

        sort_ind = np.argsort(p_arr)

        self.en_dens = interp1d(
            p_arr[sort_ind],
            en_arr[sort_ind],
            kind=interpolation_kind,
            fill_value="raise"
        )

        sort_ind = np.argsort(en_arr)

        self.press = interp1d(
            en_arr[sort_ind],
            p_arr[sort_ind],
            kind=interpolation_kind,
            fill_value="raise"
        )

        self.min_dens = np.min(en_arr)
        self.max_dens = np.max(en_arr)
        self.min_p = np.min(p_arr)
        self.max_p = np.max(p_arr)

    def check_density(self, dens):
        if dens < self.min_dens or dens > self.max_dens:
            raise Exception("density is outside the eos table range.")

    def tov_eq(self, y, r):
        P, m = y

        if P < self.min_p or P > self.max_p:
            return [0.0, 0.0]

        eden = self.en_dens(P)

        numerator = -G * (eden + P / c ** 2) * (m + 4.0 * pi * r ** 3 * P / c ** 2)
        denominator = r * (r - 2.0 * G * m / c ** 2)
        dPdr = numerator / denominator

        dmdr = 4.0 * pi * r**2 * eden

        return [dPdr, dmdr]

    def solve(self, c_dens, rmax=30e5, rtol=1e-5, dmrel=1e-12, dr=dr):
        c_dens = c_dens * MeV_fm3_to_cgs / c**2
        self.check_density(c_dens)

        r = np.arange(dr, rmax + dr, dr)

        P = self.press(c_dens)
        eden = self.en_dens(P)

        # initial mass of a small sphere near the stellar center
        m = (4.0 / 3.0) * pi * r[0]**3 * eden

        psol = odeint(self.tov_eq, [P, m], r, rtol=rtol)
        p_R, m_R = psol[:, 0], psol[:, 1]

        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            diff = np.divide(
                (m_R[1:] - m_R[:-1]),
                m_R[1:],
                out=np.zeros_like(m_R[1:]),
                where=m_R[1:] != 0
            )

        ind = -1

        for i, dm in enumerate(diff):
            if dm < dmrel and m_R[i] != 0:
                ind = i
                break

        if ind <= 1:
            raise Exception("stellar surface was not found.")

        M = m_R[ind - 1]
        R = r[ind - 1]

        return R / 1e5, M / Msun


# load the eos table
data = np.loadtxt(eos_file)

pressure = data[:, 3]        # pressure [MeV/fm^3]
energy_density = data[:, 4]  # energy density [MeV/fm^3]


# central density range
e_min = np.min(energy_density)
e_max = np.max(energy_density)

cd_min = 3.0 * e_min
cd_max = 0.98 * e_max

print(f"cd_min = {cd_min:.2f} MeV/fm^3")
print(f"cd_max = {cd_max:.2f} MeV/fm^3")
print(f"interpolation: {interpolation_kind}")

# initialize the tov solver

tov = TOV(energy_density, pressure)

# TASK 1:
# create an array of central densities from cd_min to cd_max.
# the number of points is stored in cd_points.

cd_grid = np.linspace(cd_min, cd_max, cd_points)

# compute stellar configurations

Pc_used = []
radii_all = []
masses_all = []

for cd in cd_grid:
    try:
        R, M = tov.solve(cd, dr=dr)

        radii_all.append(R)
        masses_all.append(M)

        # central pressure for color plotting
        cd_cgs = cd * MeV_fm3_to_cgs / c**2
        Pc_cgs = tov.press(cd_cgs)
        Pc_mev = Pc_cgs / MeV_fm3_to_cgs
        Pc_used.append(Pc_mev)

    except Exception:
        # some central densities may not produce a valid solution.
        # these points are skipped.
        continue


Pc_used = np.array(Pc_used)
radii_all = np.array(radii_all)
masses_all = np.array(masses_all)


# TASK 2:
# find the index of the maximum mass.
# hint: np.argmax(array) returns the index of the largest value in the array.
i_max = np.argmax(masses_all)


# TASK 3:
# use i_max to split the mr diagram into stable and unstable branches.
# the stable branch goes from the beginning up to and including the maximum mass.
# the unstable branch is the part after the maximum mass.
radii_stable = radii_all[:i_max + 1]
masses_stable = masses_all[:i_max + 1]
Pc_stable = Pc_used[:i_max + 1]

radii_unstable = radii_all[i_max + 1:]
masses_unstable = masses_all[i_max + 1:]


# TASK 4:
# find the maximum mass and the corresponding radius.
M_max = masses_all[i_max]
R_at_Mmax = radii_all[i_max]


# TASK 5:
# find the radius of a neutron star with mass 1.4 solar masses.
# hint:
# create an interpolation R(M) using the stable branch.

R_of_M = interp1d(
    masses_stable,
    radii_stable,
    bounds_error=False,
    fill_value=np.nan
)

R_14 = float(R_of_M(1.4))


print(f"maximum mass: {M_max:.3f} M☉")
print(f"radius at maximum mass: {R_at_Mmax:.3f} km")
print(f"R(1.4 M☉) = {R_14:.3f} km")


# plot 1: equation of state
plt.figure(figsize=(8, 6))

plt.plot(
    energy_density,
    pressure,
    lw=2,
    label=f"interpolation: {interpolation_kind}"
)

plt.scatter(
    energy_density,
    pressure,
    s=8,
    color="black",
    alpha=0.5,
    label="eos table points"
)

# BONUS:
# try logarithmic axes:
# plt.xscale("log")
# plt.yscale("log")

plt.xlabel("energy density ε [MeV/fm³]")
plt.ylabel("pressure p [MeV/fm³]")
plt.title("equation of state p(ε)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# plot 2: MR diagram

plt.figure(figsize=(8, 6))

plt.plot(
    radii_unstable,
    masses_unstable,
    "--",
    color="lightgray",
    lw=1.5,
    label="unstable branch"
)

plt.plot(
    radii_stable,
    masses_stable,
    color="blue",
    lw=2.5,
    label="stable branch"
)

# TASK 6:
# mark the maximum mass with a red point.

plt.scatter(
    R_at_Mmax,
    M_max,
    color="red",
    s=80,
    label="maximum mass"
)

plt.xlabel("R [km]")
plt.ylabel("M [M☉]")
plt.title("mass-radius diagram")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.xlim(9, 16)
plt.show()

# plot 3: MR diagram colored by central pressure
plt.figure(figsize=(8, 6))

Pc_log = np.log10(Pc_stable)

plt.plot(
    radii_unstable,
    masses_unstable,
    "--",
    color="lightgray",
    lw=1.5,
    label="unstable branch"
)

sc = plt.scatter(
    radii_stable,
    masses_stable,
    c=Pc_log,
    cmap=colormap,
    s=30,
    label="stable branch"
)

plt.scatter(
    R_at_Mmax,
    M_max,
    color="red",
    s=80,
    label="maximum mass"
)

plt.xlabel("R [km]")
plt.ylabel("M [M☉]")
plt.title("mr diagram colored by central pressure")

cbar = plt.colorbar(sc)
cbar.set_label(r"$\log_{10}(p_c)$ [MeV/fm$^3$]")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.xlim(9, 16)
plt.show()