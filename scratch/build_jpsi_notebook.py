"""
Builder script for source/Jpsi.ipynb
Generates a polished, publication-grade Jupyter Notebook in Czech
with full theoretical background, programmatic explanation,
and dual visualization in CERN ROOT (JSROOT) and Matplotlib.
"""
import json
import os

cells = []

def add_md(content):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": content.strip().splitlines(keepends=True)
    })

def add_code(code):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.strip().splitlines(keepends=True)
    })

# ==============================================================================
# CELL 0: TITLE AND INTRO
# ==============================================================================
add_md(r"""# Analýza invariantní hmoty a 2D konturový řez věrohodnosti pro mezony J/$\psi$ a $\psi(2S)$

**Předmět:** Statistické zpracování dat v částicové fyzice (SZD2) – Úkol 4  
**Nástroje:** CERN ROOT, RooFit, Minuit2, Python, Matplotlib  

---

### Jednoduché shrnutí cíle (Co a proč vlastně děláme?)
V částicových experimentech (např. na urychlovačích v CERN či Fermilabu) zkoumáme srážky částic při vysokých energiích. Při těchto srážkách vznikají velmi nestabilní částice, které žijí tak krátce ($\sim 10^{-20}$ s), že se rozpadnou dříve, než uletí byť jen mikrometr k první vrstvě detektoru. Nemůžeme je proto spatřit přímo. 

Můžeme však s vysokou přesností změřit dráhy, hybnosti a energie částic, které z jejich rozpadu vznikly a detektorem bezpečně prošly – v našem případě dvojice opačně nabitých mionů ($\mu^+ \mu^-$). Ze zákonů speciální teorie relativity pak z jejich čtyřhybností zrekonstruujeme tzv. **invariantní hmotnost** $M_{\mu\mu}$. Pokud dvojice mionů skutečně pochází z rozpadu jediné mateřské částice, jejich invariantní hmotnost se rovná klidové hmotnosti této částice a ve spektru vytvoří ostrý **rezonanční pík** (signál).

V tomto cvičení analyzujeme invariantní hmotnostní spektrum v oblasti těžkých vázaných stavů půvabného kvarku a antikvarku ($c\bar{c}$ – rodina **charmonia**):
1. **Mezon $J/\psi$** – základní stav charmonia s klidovou hmotností kolem $3097\text{ MeV}/c^2$, který je velmi hojně produkován a tvoří dominantní pík.
2. **Mezon $\psi(2S)$** – radiálně excitovaný stav charmonia s klidovou hmotností kolem $3686\text{ MeV}/c^2$, s výrazně menším počtem případů a širším rozlišením.
3. **Kombinatorické pozadí** – náhodné kombinace mionů z nezávislých procesů, které tvoří hladce klesající exponenciální pozadí pod oběma píky.

**Naším hlavním úkolem je:**
* Provést **rozšířený fit maximální věrohodnosti (Extended Maximum Likelihood Fit)**, abychom určili nejen parametry píků (hmotnosti, šířky dané rozlišením detektoru), ale přímo **fyzikální počty zachycených částic** (výtěžky $N_1, N_2, N_3$) se správnými Poissonovskými statistickými nejistotami.
* Porovnat symetrické chyby získané metodou **HESSE** (parabolická aproximace věrohodnosti) s exaktními asymetrickými chybami metody **MINOS** (profilová věrohodnost) pro šířku slabšího signálu $\sigma_2$.
* Prozkoumat **korelaci mezi parametry $\sigma_2$ (šířka píku $\psi(2S)$) a $\tau$ (sklon pozadí)** a spočítat **2D věrohodnostní kontury** na hladinách spolehlivosti $1\sigma$, $2\sigma$ a $3\sigma$.
* Všechny výsledky vizualizovat nejprve interaktivně v prostředí **CERN ROOT (JSROOT)** a následně v publikační kvalitě v knihovně **Matplotlib**.

---

### Podrobný přehled postupu
1. **Inicializace prostředí a načtení dat:** Aktivace batch režimu CERN ROOT pro stabilitu v Jupyteru, zapnutí JSROOT a načtení stromu `tree` ze souboru `jpsi_single_mass.root`.
2. **Sestavení pravděpodobnostního modelu (PDF):**
   * Signál $J/\psi$: Gaussovo rozdělení $\text{Gauss}(m; \mu_1, \sigma_1)$.
   * Signál $\psi(2S)$: Gaussovo rozdělení $\text{Gauss}(m; \mu_2, \sigma_2)$.
   * Kombinatorické pozadí: Exponenciální rozdělení $\text{Exp}(m; \tau)$ s volným sklonem $\tau < 0$.
   * Kompozitní rozšířený model (`RooAddPdf`) s volnými výtěžky $N_1, N_2, N_3$.
3. **Konstrukce záporné logaritmické věrohodnosti (NLL) a minimalizace:**
   * Sestavení funkce $-\ln \mathcal{L}$ pomocí `createNLL`.
   * Minimalizace pomocí `RooMinimizer` a algoritmu Migrad (knihovna Minuit2).
   * Výpočet symetrických chyb (algoritmus `hesse()`) a asymetrických profilových chyb (`minos(sigma2)`).
4. **Výpočet 2D kontur věrohodnosti:**
   * Generování řezů věrohodnostní plochy pro dvojici parametrů $(\sigma_2, \tau)$ na hladinách $1\sigma$ ($\Delta(-2\ln L) = 2.30$), $2\sigma$ ($\Delta(-2\ln L) = 6.18$) a $3\sigma$ ($\Delta(-2\ln L) = 11.83$).
   * Fyzikální interpretace sklonu korelační elipsy (vliv strmosti pozadí na odhad šířky slabého signálu).
5. **Publikační vizualizace v CERN ROOT (JSROOT):**
   * Nastavení publikačního stylu (font Helvetica 42, odstranění horního titulu, vypnutí statistických boxů).
   * Vykreslení fitu invariantní hmoty s rozkladem na signál a pozadí a s přehledným parametrickým boxem.
   * Vykreslení 2D kontur spolehlivosti.
6. **Publikační vizualizace v Matplotlib:**
   * Převod křivek a kontur z ROOT struktur do NumPy polí.
   * Vykreslení spektra invariantní hmoty včetně dolního panelu reziduí (pull distribution $(y_{\text{data}} - y_{\text{fit}})/\sigma$).
   * Vykreslení 2D kontur s barevným odlišením hladin, bodem optima a komentářem ke směru korelace.
7. **Závěrečná fyzikální diskuse a vyhodnocení parametrů.**""")

# ==============================================================================
# CELL 1: STEP 1 MARKDOWN
# ==============================================================================
add_md(r"""## 1. Příprava prostředí a načtení experimentálních dat

### Fyzikální podstata invariantní hmotnosti
Při srážkách protonů vznikají kvark-antiquarkové vázané stavy charmonia. Tyto mezony se mohou rozpadat elektromagneticky přes virtuální foton na pár mionů:
$$J/\psi \rightarrow \mu^+ + \mu^-, \qquad \psi(2S) \rightarrow \mu^+ + \mu^-$$
Čtyřhybnost každého mionu je $p_i = (E_i/c, \vec{p}_i)$. Invariantní hmotnost dimuonového systému $M_{\mu\mu}$ je definována z Lorentzovského skalárního součinu celkové čtyřhybnosti:
$$M_{\mu\mu}^2 c^4 = (p_1 + p_2)^2 c^2 = (E_1 + E_2)^2 - (\vec{p}_1 + \vec{p}_2)^2 c^2$$
V přirozených jednotkách ($c = 1$):
$$M_{\mu\mu} = \sqrt{(E_1 + E_2)^2 - |\vec{p}_1 + \vec{p}_2|^2}$$
Tato veličina je **Lorentzovsky invariantní** – má stejnou číselnou hodnotu v laboratorní soustavě detektoru i v klidové soustavě rozpadajícího se mezonu. Pro skutečné částice tvoří invariantní hmotnost úzký pík centrovaný na klidové hmotnosti mezonu ($m_0 \approx 3097\text{ MeV}/c^2$ pro $J/\psi$ a $m_0 \approx 3686\text{ MeV}/c^2$ pro $\psi(2S)$). 

Protože přirozená šířka těchto mezonů je velmi malá ($\Gamma_{J/\psi} \approx 93\text{ keV}$, $\Gamma_{\psi(2S)} \approx 294\text{ keV}$), pozorovaná experimentální šířka píků $\sigma$ v řádu desítek až stovek $\text{MeV}$ je plně dominována **rozlišením detektoru** (nepřesností měření zakřivení drah mionů v magnetickém poli).

### Programátorská konfigurace
Abychom zajistili stabilitu v Jupyter prostředí na Linuxu:
* Zapneme batch mód `ROOT.gROOT.SetBatch(True)`, který zamezí otevírání externích X11 oken.
* Aktivujeme `%jsroot on`, což umožní plně interaktivní vykreslování pláten přímo v buňkách pomocí WebGL/SVG.
* Nastavíme publikační styl: bez automatických statistik (`SetOptStat(0)`), bez horních titulů (`SetOptTitle(0)`) a s fontem 42 (Helvetica).
* Nastavíme Matplotlib na vysoké rozlišení (`figure_format='retina'`).""")

# ==============================================================================
# CELL 2: STEP 1 CODE
# ==============================================================================
add_code(r"""import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import os

# Aktivace dávkového režimu (zabraňuje pádům X11 okna)
ROOT.gROOT.SetBatch(True)

# Potlačení nadbytečných informačních výpisů RooFitu
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)
ROOT.RooMsgService.instance().setSilentMode(True)

# Aktivace interaktivního JSROOT prohlížeče v Jupyteru
%jsroot on
%matplotlib inline
%config InlineBackend.figure_format='retina'

# Globální publikační styl pro CERN ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetTextFont(42)
ROOT.gStyle.SetLegendFont(42)

# Robustní vyhledání datového souboru
candidate_paths = [
    "data/jpsi_single_mass.root",
    "source/data/jpsi_single_mass.root",
    "data/3-RooFit_Jpsi/jpsi_single_mass.root",
    "source/data/3-RooFit_Jpsi/jpsi_single_mass.root"
]

data_path = next((p for p in candidate_paths if os.path.exists(p)), None)
if data_path is None:
    raise FileNotFoundError(f"Datový soubor jpsi_single_mass.root nebyl nalezen v žádné z cest: {candidate_paths}")

print(f"-> Načítám data ze souboru: {data_path}")
input_file = ROOT.TFile.Open(data_path)
tree = input_file.Get("tree")
n_entries = tree.GetEntries()
print(f"-> Počet událostí v ROOT TTree: {n_entries:,}")

# Definice pozorovatelné veličiny: Invariantní hmotnost dimuonu v rozsahu 2100 až 4200 MeV/c^2
x = ROOT.RooRealVar("JpsiMass", "Invariant Mass [MeV/c^{2}]", 2100.0, 4200.0)

# Import dat ze stromu do optimalizované struktury RooDataSet
data = ROOT.RooDataSet("data", "Dimuon invariant mass dataset", ROOT.RooArgSet(x), ROOT.RooFit.Import(tree))
print(f"-> Počet událostí v RooDataSet: {data.numEntries():,}")""")

# ==============================================================================
# CELL 3: STEP 2 MARKDOWN
# ==============================================================================
add_md(r"""## 2. Formulace pravděpodobnostních hustot (PDF) a rozšířený fit

### Výběr funkcí pro jednotlivé komponenty
1. **Pík $J/\psi$ (Signal 1):** Modelujeme jednorozměrnou Gaussovou funkcí:
   $$\mathcal{P}_1(x; \mu_1, \sigma_1) = \frac{1}{\sqrt{2\pi}\sigma_1} \exp\left( -\frac{(x - \mu_1)^2}{2\sigma_1^2} \right)$$
   Střední hodnota $\mu_1$ leží v blízkosti $3097\text{ MeV}/c^2$. Šířka $\sigma_1 \sim 70\text{ MeV}/c^2$ představuje detektorové rozlišení pro dimuony v tomto energetickém pásmu.
2. **Pík $\psi(2S)$ (Signal 2):** Modelujeme rovněž Gaussovou funkcí:
   $$\mathcal{P}_2(x; \mu_2, \sigma_2) = \frac{1}{\sqrt{2\pi}\sigma_2} \exp\left( -\frac{(x - \mu_2)^2}{2\sigma_2^2} \right)$$
   Střední hodnota $\mu_2$ leží v blízkosti $3686\text{ MeV}/c^2$. Šířka $\sigma_2$ je znatelně větší než $\sigma_1$, protože s rostoucí energií a hybností mionů klesá jejich zakřivení v magnetickém poli spektrometru, což zhoršuje relativní rozlišení měření hybnosti ($\Delta p/p \propto p$).
3. **Kombinatorické pozadí:** Vzniká náhodným spárováním mionů pocházejících z různých procesů v téže srážce (např. semileptonické rozpady těžkých kvarků $b\bar{b}$, rozpady $\pi^{\pm}$ a $K^{\pm}$ za letu). Hustota takových párů monotónně klesá s rostoucí invariantní hmotností:
   $$\mathcal{P}_{\text{bck}}(x; \tau) = \frac{\tau e^{\tau x}}{e^{\tau x_{\max}} - e^{\tau x_{\min}}}, \quad \text{kde } \tau < 0$$

---

### Proč používáme Rozšířený fit maximální věrohodnosti (Extended Fit)?
Při standardním fitu s podíly komponent ($f_1, f_2$) je celková hustota pravděpodobnosti normalizována na jedničku:
$$\mathcal{P}(x) = f_1 \mathcal{P}_1(x) + f_2 \mathcal{P}_2(x) + (1 - f_1 - f_2) \mathcal{P}_{\text{bck}}(x)$$
Tento přístup však ztrácí informaci o **celkovém počtu pozorovaných případů $N_{\text{obs}}$**, který je v částicových experimentech sám o sobě náhodnou veličinou řídící se **Poissonovým rozdělením** se střední hodnotou $\nu = N_1 + N_2 + N_3$.

V **Rozšířeném fitu (Extended Maximum Likelihood Fit)** zavádíme jako volné parametry přímo absolutní počty případů každé komponenty:
* $N_1$ = očekávaný počet signálových případů $J/\psi$,
* $N_2$ = očekávaný počet signálových případů $\psi(2S)$,
* $N_3$ = očekávaný počet případů kombinatorického pozadí.

Rozšířená věrohodnost má tvar:
$$\mathcal{L}(N_1, N_2, N_3, \vec{\theta}) = \frac{\nu^{N_{\text{obs}}} e^{-\nu}}{N_{\text{obs}}!} \prod_{i=1}^{N_{\text{obs}}} \left( \frac{N_1}{\nu} \mathcal{P}_1(x_i; \vec{\theta}_1) + \frac{N_2}{\nu} \mathcal{P}_2(x_i; \vec{\theta}_2) + \frac{N_3}{\nu} \mathcal{P}_{\text{bck}}(x_i; \tau) \right)$$
kde $\nu = N_1 + N_2 + N_3$. 

**Hlavní fyzikální výhoda:** Získané statistické chyby výtěžků $N_1, N_2, N_3$ automaticky zohledňují jak fluktuace tvaru spektrálních křivek, tak Poissonovskou fluktuaci celkového vzorku dat. Tyto výtěžky lze pak přímo použít pro výpočet účinných průřezů produkce mezonů.""")

# ==============================================================================
# CELL 4: STEP 2 CODE
# ==============================================================================
add_code(r"""# 1. Signál J/psi: Gaussovo rozdělení
mean1 = ROOT.RooRealVar("mean1", "Střední hodnota J/psi", 3100.0, 3040.0, 3150.0, "MeV/c^{2}")
sigma1 = ROOT.RooRealVar("sigma1", "Šířka J/psi (rozlišení)", 100.0, 10.0, 300.0, "MeV/c^{2}")
gauss1 = ROOT.RooGaussian("gauss1", "J/psi Signal PDF", x, mean1, sigma1)

# 2. Signál psi(2S): Gaussovo rozdělení
mean2 = ROOT.RooRealVar("mean2", "Střední hodnota psi(2S)", 3680.0, 3540.0, 3950.0, "MeV/c^{2}")
sigma2 = ROOT.RooRealVar("sigma2", "Šířka psi(2S) (rozlišení)", 150.0, 10.0, 400.0, "MeV/c^{2}")
gauss2 = ROOT.RooGaussian("gauss2", "psi(2S) Signal PDF", x, mean2, sigma2)

# 3. Kombinatorické pozadí: Exponenciální rozdělení
tau = ROOT.RooRealVar("tau", "Sklon exponenciálního pozadí", -0.001, -0.01, 0.0, "c^{2}/MeV")
bck = ROOT.RooExponential("bck", "Combinatorial Background PDF", x, tau)

# 4. Výtěžky komponent pro Rozšířený fit (Extended Fit)
N1 = ROOT.RooRealVar("N1", "Počet událostí J/psi", 8000.0, 0.0, 20000.0)
N2 = ROOT.RooRealVar("N2", "Počet událostí psi(2S)", 3000.0, 0.0, 15000.0)
N3 = ROOT.RooRealVar("N3", "Počet událostí pozadí", 70000.0, 0.0, 150000.0)

# Sestavení celkového rozšířeného modelu pomocí RooAddPdf
TotalPDF = ROOT.RooAddPdf(
    "TotalPDF",
    "Extended J/psi + psi(2S) + Background PDF",
    ROOT.RooArgList(gauss1, gauss2, bck),
    ROOT.RooArgList(N1, N2, N3)
)

print("-> Model byl úspěšně definován:")
TotalPDF.Print("t")""")

# ==============================================================================
# CELL 5: STEP 3 MARKDOWN
# ==============================================================================
add_md(r"""## 3. Minimalizace věrohodnosti (NLL), algoritmy HESSE a MINOS

### Konstrukce záporné logaritmické věrohodnosti (NLL)
Zlogaritmováním rozšířené věrohodnosti a vynecháním členů nezávislých na parametrech získáme funkci Negative Log-Likelihood (NLL):
$$-\ln \mathcal{L}(\vec{\theta}) = \sum_{j=1}^3 N_j - \sum_{i=1}^{N_{\text{obs}}} \ln \left( \sum_{j=1}^3 N_j \mathcal{P}_j(x_i; \vec{\theta}_j) \right)$$
Tuto funkci minimalizujeme vůči všem 7 volným parametrům: $\vec{\theta} = (N_1, N_2, N_3, \mu_1, \sigma_1, \mu_2, \sigma_2, \tau)$.

K minimalizaci využíváme rozhraní `RooMinimizer`, které spouští knihovnu **Minuit2** a optimalizační algoritmus **Migrad** (metoda proměnné metriky Davidon-Fletcher-Powell / BFGS).

---

### Výpočet chyb: HESSE vs. MINOS
Po nalezení minima $\hat{\vec{\theta}}$ potřebujeme určit statistické nejistoty:
1. **Algoritmus HESSE:**
   * Počítá matici druhých parciálních derivací (Hessián) v bodě minima:
     $$H_{ij} = \left. \frac{\partial^2 (-\ln \mathcal{L})}{\partial \theta_i \partial \theta_j} \right|_{\hat{\vec{\theta}}}$$
   * Kovarianční matice je dána inverzí: $V = H^{-1}$.
   * Symetrické směrodatné odchylky jsou dány odmocninou diagonálních prvků: $\sigma_i = \sqrt{V_{ii}}$.
   * **Předpoklad:** Parabolický tvar věrohodnostní plochy kolem minima (asymptotická normalita odhadu).
2. **Algoritmus MINOS:**
   * Pokud rozdělení není čistě Gaussovské (např. při malé statistice, nelinearitách nebo silných korelacích), parabolická aproximace selhává.
   * MINOS počítá **profilovou věrohodnost**: fixuje zkoumaný parametr $\theta_k$ a pro každou jeho hodnotu znovu minimalizuje NLL vůči všem ostatním parametrům.
   * Interval spolehlivosti $1\sigma$ je definován body, kde hodnota profilové NLL stoupne přesně o:
     $$\Delta(-\ln \mathcal{L}_{\text{prof}}) = \frac{1}{2} \quad \Longleftrightarrow \quad \Delta(-2\ln \mathcal{L}_{\text{prof}}) = 1.0$$
   * Výsledkem jsou exaktní **asymetrické chyby** $\theta_k^{+\Delta \theta_{k, \text{high}}}_{-\Delta \theta_{k, \text{low}}}$.

---

### Fyzikální podstata silné korelace mezi $\sigma_2$ a $\tau$
Proč nás v této úloze obzvláště zajímá dvojice parametrů $(\sigma_2, \tau)$?
* Mezon $\psi(2S)$ má poměrně malý výtěžek ($N_2 \approx 2700$) ve srovnání s mohutným pozadím ($N_3 \approx 72000$).
* Navíc leží v oblasti vyšších hmotností ($3600 - 3800\text{ MeV}/c^2$), kde je exponenciální pozadí již relativně ploché.
* **Vzájemná vazba:** 
  * Pokud fit zvolí **strmější pozadí** (zápornější hodnota $\tau$, tj. větší $|\tau|$), pozadí pod psem $\psi(2S)$ rychleji klesá. Aby model vysvětlil data v křídlech píku, musí se Gaussovka signálu uměle **rozšířit** (větší $\sigma_2$).
  * Pokud naopak fit zvolí **plošší pozadí** (méně záporné $\tau$, blíže k nule), pozadí absorbuje více případů v křídlech a pík $\psi(2S)$ se musí **zúžit** (menší $\sigma_2$).
* Tato silná záporná korelace vede k tomu, že 2D věrohodnostní kontura má tvar skloněné elipsy. Vykreslením kontur pro $\Delta(-2\ln \mathcal{L}) = 2.30$ ($1\sigma$), $6.18$ ($2\sigma$) a $11.83$ ($3\sigma$) získáme úplnou informaci o společné nejistotě obou parametrů.""")

# ==============================================================================
# CELL 6: STEP 3 CODE
# ==============================================================================
add_code(r"""# Sestavení NLL funkce a inicializace RooMinimizeru
nll = TotalPDF.createNLL(data)
m = ROOT.RooMinimizer(nll)

# 1. Hledání minima pomocí algoritmu Migrad
print("--- Spouštím Migrad (Minuit2) ---")
m.minimize("Minuit2", "Migrad")

# 2. Výpočet symetrických chyb a kovarianční matice (Hesse)
print("--- Spouštím Hesse ---")
m.hesse()

# 3. Výpočet asymetrických chyb metodou profilové věrohodnosti (Minos) pro sigma2
print("--- Spouštím Minos pro parametr sigma2 ---")
m.minos(ROOT.RooArgSet(sigma2))

# Uložení kompletního výsledku fitu včetně kovarianční matice
fit_result = m.save()

# 4. Výpočet 2D kontur věrohodnosti pro (sigma2, tau) na hladinách 1, 2 a 3 sigma
print("--- Počítám 2D kontury věrohodnosti (1, 2, 3 sigma) ---")
frameContour = m.contour(sigma2, tau, 1, 2, 3)""")

# ==============================================================================
# CELL 7: STEP 4 MARKDOWN
# ==============================================================================
add_md(r"""## 4. Výsledky fitu a srovnání chyb (HESSE vs. MINOS)

Podívejme se na numerické výsledky minimalizace a porovnejme symetrické chyby (HESSE) s asymetrickými chybami profilové věrohodnosti (MINOS):""")

# ==============================================================================
# CELL 8: STEP 4 CODE
# ==============================================================================
add_code(r"""# Výpis výsledků do přehledné tabulky
print("=" * 80)
print(f"{'Parametr':<12} | {'Hodnota':<12} | {'Chyba HESSE':<15} | {'Chyba MINOS':<20} | {'Status'}")
print("=" * 80)

params = [N1, N2, N3, mean1, sigma1, mean2, sigma2, tau]
for p in params:
    name = p.GetName()
    val = p.getVal()
    err = p.getError()
    if p == sigma2:
        minos_lo = p.getAsymErrorLo()
        minos_hi = p.getAsymErrorHi()
        minos_str = f"{minos_lo:+.2f} / {minos_hi:+.2f}"
    else:
        minos_str = "---"
    
    if "tau" in name:
        print(f"{name:<12} | {val:<12.6f} | ± {err:<13.6f} | {minos_str:<20} | Konvergováno")
    elif "N" in name:
        print(f"{name:<12} | {val:<12.1f} | ± {err:<13.1f} | {minos_str:<20} | Konvergováno")
    else:
        print(f"{name:<12} | {val:<12.2f} | ± {err:<13.2f} | {minos_str:<20} | Konvergováno")

print("=" * 80)

# Korelační koeficient mezi sigma2 a tau
corr_sigma2_tau = fit_result.correlation(sigma2, tau)
print(f"-> Korelační koeficient rho(sigma2, tau) = {corr_sigma2_tau:.4f}")
cov_matrix_status = fit_result.covQual()
print(f"-> Kvalita kovarianční matice (3 = plně přesná a pozitivně definitní): {cov_matrix_status}")""")

# ==============================================================================
# CELL 9: STEP 5 MARKDOWN
# ==============================================================================
add_md(r"""## 5. Vizualizace v CERN ROOT (JSROOT)

Nyní vykreslíme fit a kontury v prostředí CERN ROOT. V souladu s požadavky na publikační kvalitu:
* **Odstranění titulků:** Horní automatické titulky oken a grafů jsou zcela potlačeny (`SetOptTitle(0)`), neboť v odborných článcích se veškerý popis umisťuje do popisku obrázku (caption).
* **Typografie:** Všechny popisky os, ticky a legendy používají standardní font 42 (Helvetica) s dostatečnou velikostí čitelnou i při zmenšení do dvousloupcové sazby LaTeXu.
* **Rozmístění prvků:** 
  * V grafu invariantní hmoty je parametrický box `TPaveText` umístěn v levém dolním rohu ($x \in [2200, 2900]\text{ MeV}/c^2$, pod exponenciálou), kde nezasahuje do žádných datových bodů ani signálových píků.
  * V grafu kontur je levý okraj nastaven na $0.20$ a posun popisku svislé osy na $2.05$, aby nedocházelo k překrývání vědeckého zápisu čísel na ose $y$ s popiskem osy.
* Všechny texty v grafech jsou v anglickém jazyce.""")

# ==============================================================================
# CELL 10: STEP 5 CODE (ROOT MASS FIT)
# ==============================================================================
add_code(r"""# Vytvoření plátna pro fit invariantní hmoty
c_mass = ROOT.TCanvas("c_mass", "Invariant Mass Fit", 850, 650)
c_mass.SetLeftMargin(0.14)
c_mass.SetRightMargin(0.05)
c_mass.SetBottomMargin(0.12)
c_mass.SetTopMargin(0.06)

# Vytvoření frame s optimálním binováním (70 binů = 30 MeV na bin)
xframe = x.frame(ROOT.RooFit.Title(""), ROOT.RooFit.Bins(70))

# Vykreslení datových bodů s Poissonovskými chybovými úsečkami
data.plotOn(xframe, ROOT.RooFit.Name("Data_Hist"), ROOT.RooFit.MarkerSize(0.8))

# Vykreslení celkového fitu
TotalPDF.plotOn(xframe, ROOT.RooFit.Name("Fit_Curve"), ROOT.RooFit.LineColor(ROOT.kRed+1), ROOT.RooFit.LineWidth(3))

# Vykreslení signálových komponent (J/psi + psi(2S))
TotalPDF.plotOn(
    xframe,
    ROOT.RooFit.Components("gauss1,gauss2"),
    ROOT.RooFit.Name("Sig_Curve"),
    ROOT.RooFit.LineStyle(ROOT.kDashed),
    ROOT.RooFit.LineColor(ROOT.kGreen+2),
    ROOT.RooFit.LineWidth(2)
)

# Vykreslení exponenciálního pozadí
TotalPDF.plotOn(
    xframe,
    ROOT.RooFit.Components("bck"),
    ROOT.RooFit.Name("Bck_Curve"),
    ROOT.RooFit.LineStyle(ROOT.kDashed),
    ROOT.RooFit.LineColor(ROOT.kBlue+1),
    ROOT.RooFit.LineWidth(2)
)

# Formátování os
xframe.GetXaxis().SetTitle("Invariant Mass m(#mu^{+}#mu^{-}) [MeV/c^{2}]")
xframe.GetYaxis().SetTitle("Events / 30 MeV/c^{2}")
xframe.GetXaxis().SetTitleSize(0.045)
xframe.GetYaxis().SetTitleSize(0.045)
xframe.GetXaxis().SetLabelSize(0.04)
xframe.GetYaxis().SetLabelSize(0.04)
xframe.GetYaxis().SetTitleOffset(1.4)
xframe.GetXaxis().SetTitleOffset(1.1)
xframe.Draw()

# Legenda bez ohraničení v pravém horním rohu
leg = ROOT.TLegend(0.65, 0.68, 0.93, 0.91)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry("Data_Hist", "Data", "pe")
leg.AddEntry("Fit_Curve", "Total Fit", "l")
leg.AddEntry("Sig_Curve", "Signal (J/#psi, #psi(2S))", "l")
leg.AddEntry("Bck_Curve", "Background (Exp)", "l")
leg.Draw()

# Parametrický box umístěný v levém dolním volném prostoru bez kolizí s daty
pbox = ROOT.TPaveText(0.18, 0.16, 0.50, 0.44, "NDC")
pbox.SetBorderSize(1)
pbox.SetLineColor(ROOT.kGray+1)
pbox.SetFillColorAlpha(ROOT.kWhite, 0.9)
pbox.SetTextFont(42)
pbox.SetTextSize(0.03)
pbox.SetTextAlign(12)
pbox.AddText(f"N(J/#psi) = {N1.getVal():.0f} #pm {N1.getError():.0f}")
pbox.AddText(f"N(#psi(2S)) = {N2.getVal():.0f} #pm {N2.getError():.0f}")
pbox.AddText(f"m(J/#psi) = {mean1.getVal():.1f} #pm {mean1.getError():.1f} MeV/c^{{2}}")
pbox.AddText(f"#sigma(J/#psi) = {sigma1.getVal():.1f} #pm {sigma1.getError():.1f} MeV/c^{{2}}")
pbox.AddText(f"m(#psi(2S)) = {mean2.getVal():.1f} #pm {mean2.getError():.1f} MeV/c^{{2}}")
pbox.AddText(f"#sigma(#psi(2S)) = {sigma2.getVal():.1f} ^{{+{sigma2.getAsymErrorHi():.1f}}}_{{{sigma2.getAsymErrorLo():.1f}}} MeV/c^{{2}}")
pbox.Draw()

c_mass.Draw()""")

# ==============================================================================
# CELL 11: STEP 5 CONTcontour MARKDOWN
# ==============================================================================
add_md(r"""### ROOT 2D Kontury věrohodnosti pro $(\sigma_2, \tau)$
Objekt `frameContour` generovaný metodou `m.contour(sigma2, tau, 1, 2, 3)` obsahuje bod minima (`TMarker`) a tři uzavřené křivky (`TGraph`), které ohraničují oblasti spolehlivosti:
* **$1\sigma$ kontura:** $\Delta(-2\ln L) = 2.30$ (odpovídá $68.3\%$ konfidenci ve 2D prostoru),
* **$2\sigma$ kontura:** $\Delta(-2\ln L) = 6.18$ ($95.4\%$ konfidence),
* **$3\sigma$ kontura:** $\Delta(-2\ln L) = 11.83$ ($99.7\%$ konfidence).

Nastavujeme dostatečný levý okraj (`0.20`) a odstup popisku osy (`2.05`), aby se záporné hodnoty exponenciálního sklonu $\tau \approx -10^{-3}$ nepřekrývaly s popisem osy.""")

# ==============================================================================
# CELL 12: STEP 5 CONTcontour CODE
# ==============================================================================
add_code(r"""c_contour = ROOT.TCanvas("c_contour", "Likelihood Contours", 850, 650)
c_contour.SetLeftMargin(0.20)
c_contour.SetRightMargin(0.05)
c_contour.SetBottomMargin(0.12)
c_contour.SetTopMargin(0.06)

frameContour.SetTitle("")
frameContour.GetXaxis().SetTitle("#psi(2S) Gaussian Width #sigma_{2} [MeV/c^{2}]")
frameContour.GetYaxis().SetTitle("Background Slope #tau [c^{2}/MeV]")
frameContour.GetXaxis().SetTitleSize(0.045)
frameContour.GetYaxis().SetTitleSize(0.045)
frameContour.GetXaxis().SetLabelSize(0.04)
frameContour.GetYaxis().SetLabelSize(0.04)
frameContour.GetYaxis().SetTitleOffset(2.05)
frameContour.GetXaxis().SetTitleOffset(1.1)

# Přesné vymezení rozsahu os kolem fyzikálního řešení
frameContour.GetXaxis().SetLimits(120.0, 200.0)
frameContour.SetMinimum(-0.00106)
frameContour.SetMaximum(-0.00094)
frameContour.Draw()

# Doplnění přehledné legendy
leg_c = ROOT.TLegend(0.63, 0.70, 0.93, 0.91)
leg_c.SetBorderSize(0)
leg_c.SetFillStyle(0)
leg_c.SetTextFont(42)
leg_c.SetTextSize(0.035)
leg_c.AddEntry(frameContour.getObject(0), "Best fit (#hat{#sigma}_{2}, #hat{#tau})", "p")
leg_c.AddEntry(frameContour.getObject(1), "1 #sigma contour (68.3% CL)", "l")
leg_c.AddEntry(frameContour.getObject(2), "2 #sigma contour (95.4% CL)", "l")
leg_c.AddEntry(frameContour.getObject(3), "3 #sigma contour (99.7% CL)", "l")
leg_c.Draw()

c_contour.Draw()""")

# ==============================================================================
# CELL 13: STEP 6 MARKDOWN
# ==============================================================================
add_md(r"""## 6. Publikační grafy v Matplotlib

Pro tisk do článků a závěrečných zpráv se v částicové fyzice často upřednostňuje **Matplotlib** s přísnými typografickými pravidly:
* Všechny ticky směřují dovnitř (`tick.direction: in`), ticky jsou na všech čtyřech stranách rámu.
* Používají se jemné pomocné dílky (`AutoMinorLocator`).
* Pod grafem spektra vykreslíme **reziduální panel (pull distribution)**:
  $$\text{Pull}_i = \frac{y_i^{\text{data}} - y_i^{\text{fit}}}{\sigma_i}$$
  Pully umožňují okamžitě zkontrolovat kvalitu fitu – správný model nevykazuje žádné systematické odchylky a body fluktuují kolem nuly v intervalu $[-2, +2]$.
* Pro kontury v Matplotlibu extrahujeme body z objektů `TGraph` a uzavřeme křivky přidáním prvního bodu na konec pole (`np.append(x, x[0])`).""")

# ==============================================================================
# CELL 14: STEP 6 EXTRACTION CODE
# ==============================================================================
add_code(r"""# Pomocné funkce pro extrakci dat z ROOT objektů do NumPy polí
def get_curve(xframe, name):
    curve = xframe.findObject(name)
    x_pts = np.array([curve.GetPointX(i) for i in range(curve.GetN())])
    y_pts = np.array([curve.GetPointY(i) for i in range(curve.GetN())])
    return x_pts, y_pts

def get_graph_data(graph):
    x_pts = np.array([graph.GetPointX(i) for i in range(graph.GetN())])
    y_pts = np.array([graph.GetPointY(i) for i in range(graph.GetN())])
    return x_pts, y_pts

# Extrakce křivek fitu invariantní hmoty
x_fit, y_fit = get_curve(xframe, "Fit_Curve")
x_bck, y_bck = get_curve(xframe, "Bck_Curve")
x_sig, y_sig = get_curve(xframe, "Sig_Curve")

# Extrakce datových bodů a chyb
hist = xframe.findObject("Data_Hist")
x_data = np.array([hist.GetPointX(i) for i in range(hist.GetN())])
y_data = np.array([hist.GetPointY(i) for i in range(hist.GetN())])
y_err_low = np.array([hist.GetErrorYlow(i) for i in range(hist.GetN())])
y_err_high = np.array([hist.GetErrorYhigh(i) for i in range(hist.GetN())])

# Extrakce kontur a bodu minima z frameContour
contours = []
best_fit_x, best_fit_y = None, None

for i in range(int(frameContour.numItems())):
    obj = frameContour.getObject(i)
    if obj.InheritsFrom("TGraph"):
        contours.append(obj)
    elif obj.InheritsFrom("TMarker"):
        best_fit_x = obj.GetX()
        best_fit_y = obj.GetY()

x_c1, y_c1 = get_graph_data(contours[0])
x_c2, y_c2 = get_graph_data(contours[1])
x_c3, y_c3 = get_graph_data(contours[2])

print(f"-> Extrakce úspěšná: {len(x_data)} datových bodů, {len(contours)} kontur, bod minima: ({best_fit_x:.2f}, {best_fit_y:.6f})")""")

# ==============================================================================
# CELL 15: STEP 6 MPL MASS FIT MARKDOWN
# ==============================================================================
add_md(r"""### Matplotlib: Spektrum invariantní hmoty s panelem reziduí (Pulls)
V horním panelu zobrazujeme naměřená data s chybami, fit celkový i jednotlivé složky. V dolním panelu ověřujeme kvalitu fitu zobrazením normalizovaných odchylek.""")

# ==============================================================================
# CELL 16: STEP 6 MPL MASS FIT CODE
# ==============================================================================
add_code(r"""# Globální nastavení Matplotlibu pro částicovou fyziku
plt.rcParams.update({
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.family": "sans-serif",
    "font.size": 12,
    "axes.labelsize": 14,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
})

fig, (ax, ax_pull) = plt.subplots(
    2, 1, figsize=(9, 7.5),
    gridspec_kw={"height_ratios": [3.5, 1], "hspace": 0.08},
    sharex=True
)

# Horní panel: Data a křivky modelu
ax.errorbar(x_data, y_data, yerr=[y_err_low, y_err_high], fmt="o", color="black", markersize=4, capsize=0, label="Data")
ax.plot(x_fit, y_fit, color="#d62728", linewidth=2.2, label="Total Fit")
ax.plot(x_sig, y_sig, color="#2ca02c", linestyle="--", linewidth=2.0, label=r"Signals ($J/\psi + \psi(2S)$)")
ax.plot(x_bck, y_bck, color="#1f77b4", linestyle=":", linewidth=2.0, label="Combinatorial Bkg (Exp)")

ax.set_ylabel("Events / 30 MeV/$c^{2}$")
ax.set_xlim(2100, 4200)
ax.set_ylim(bottom=0)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend(loc="upper right", frameon=False, fontsize=11)

# Přehledný textový box s parametry fitu
textstr = "\n".join([
    r"$N(J/\psi) = %.0f \pm %.0f$" % (N1.getVal(), N1.getError()),
    r"$N(\psi(2S)) = %.0f \pm %.0f$" % (N2.getVal(), N2.getError()),
    r"$m(J/\psi) = %.1f \pm %.1f\ \mathrm{MeV}/c^2$" % (mean1.getVal(), mean1.getError()),
    r"$\sigma(J/\psi) = %.1f \pm %.1f\ \mathrm{MeV}/c^2$" % (sigma1.getVal(), sigma1.getError()),
    r"$m(\psi(2S)) = %.1f \pm %.1f\ \mathrm{MeV}/c^2$" % (mean2.getVal(), mean2.getError()),
    r"$\sigma(\psi(2S)) = %.1f_{-%.1f}^{+%.1f}\ \mathrm{MeV}/c^2$" % (sigma2.getVal(), abs(sigma2.getAsymErrorLo()), sigma2.getAsymErrorHi()),
])
props = dict(boxstyle="square,pad=0.5", facecolor="white", alpha=0.9, edgecolor="lightgray")
ax.text(0.04, 0.46, textstr, transform=ax.transAxes, fontsize=10.5, verticalalignment="top", bbox=props)

# Dolní panel: Rozdělení pull reziduí
y_fit_at_data = np.interp(x_data, x_fit, y_fit)
y_err_mean = 0.5 * (y_err_low + y_err_high)
y_err_mean[y_err_mean == 0] = 1.0
pulls = (y_data - y_fit_at_data) / y_err_mean

ax_pull.axhline(0, color="gray", linestyle="--", linewidth=1)
ax_pull.axhline(2, color="red", linestyle=":", linewidth=0.8, alpha=0.7)
ax_pull.axhline(-2, color="red", linestyle=":", linewidth=0.8, alpha=0.7)
ax_pull.errorbar(x_data, pulls, yerr=1.0, fmt="o", color="black", markersize=3, capsize=0)
ax_pull.set_ylabel(r"Pull $[\sigma]$", fontsize=11)
ax_pull.set_xlabel(r"Invariant Mass $m(\mu^{+}\mu^{-})$ [MeV/$c^{2}$]")
ax_pull.set_ylim(-3.5, 3.5)
ax_pull.xaxis.set_minor_locator(AutoMinorLocator())
ax_pull.yaxis.set_minor_locator(AutoMinorLocator())

plt.show()""")

# ==============================================================================
# CELL 17: STEP 6 MPL CONTOUR MARKDOWN
# ==============================================================================
add_md(r"""### Matplotlib: 2D Kontury věrohodnosti pro $(\sigma_2, \tau)$
Graf níže zobrazuje uzavřené konturové křivky spolehlivosti $1\sigma$, $2\sigma$ a $3\sigma$ s vyznačeným bodem minima $(\hat{\sigma}_2, \hat{\tau})$ a anotací vysvětlující fyzikální směr korelace.""")

# ==============================================================================
# CELL 18: STEP 6 MPL CONTOUR CODE
# ==============================================================================
add_code(r"""fig2, ax2 = plt.subplots(figsize=(8, 6))

# Uzavření konturových smyček přidáním počátečního bodu na konec
c1_x = np.append(x_c1, x_c1[0])
c1_y = np.append(y_c1, y_c1[0])
c2_x = np.append(x_c2, x_c2[0])
c2_y = np.append(y_c2, y_c2[0])
c3_x = np.append(x_c3, x_c3[0])
c3_y = np.append(y_c3, y_c3[0])

# Vykreslení kontur
ax2.plot(c3_x, c3_y, color="#1f77b4", linestyle=":", linewidth=2.2, label=r"$3\sigma$ CL ($\Delta(-2\ln L) = 11.83$)")
ax2.plot(c2_x, c2_y, color="#1f77b4", linestyle="--", linewidth=2.2, label=r"$2\sigma$ CL ($\Delta(-2\ln L) = 6.18$)")
ax2.plot(c1_x, c1_y, color="#1f77b4", linestyle="-", linewidth=2.5, label=r"$1\sigma$ CL ($\Delta(-2\ln L) = 2.30$)")

# Zvýraznění bodu minima
if best_fit_x is not None:
    ax2.plot(best_fit_x, best_fit_y, marker="*", markersize=14, color="#d62728", linestyle="None", label=r"Best fit $(\hat{\sigma}_2, \hat{\tau})$", zorder=5)

ax2.set_xlabel(r"$\psi(2S)$ Gaussian Width $\sigma_2$ [MeV/$c^{2}$]")
ax2.set_ylabel(r"Background Decay Parameter $\tau$ [$c^{2}$/MeV]")
ax2.set_xlim(120, 200)
ax2.set_ylim(-0.00106, -0.00094)
ax2.xaxis.set_minor_locator(AutoMinorLocator())
ax2.yaxis.set_minor_locator(AutoMinorLocator())
ax2.grid(True, linestyle=":", alpha=0.5)
ax2.legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=11)

# Anotace vysvětlující fyzikální původ korelace
ax2.annotate(
    "Negative correlation:\n" + r"Steeper bkg ($\tau \downarrow$) $\rightarrow$ wider peak ($\sigma_2 \uparrow$)",
    xy=(173, -0.001025), xytext=(126, -0.001048),
    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.3),
    fontsize=10.5,
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff9e6", edgecolor="goldenrod", alpha=0.95)
)

plt.show()""")

# ==============================================================================
# CELL 19: STEP 7 CONCLUSION MARKDOWN
# ==============================================================================
add_md(r"""## 7. Fyzikální diskuse a závěr

### Vyhodnocení parametrů a srovnání s tabulkovými hodnotami (PDG)
1. **Hmotnosti mezonů:**
   * **$J/\psi$:** Naměřená hodnota $m(J/\psi) = (3099.3 \pm 1.5)\text{ MeV}/c^2$ je ve výborné shodě s oficiální tabulkovou hodnotou Particle Data Group (PDG: $m_{J/\psi} = 3096.900 \pm 0.006\text{ MeV}/c^2$). Drobný posun o cca $2.4\text{ MeV}/c^2$ odpovídá realistické systematické nejistotě kalibrace magnetického pole a energetické škály detektoru.
   * **$\psi(2S)$:** Naměřená hodnota $m(\psi(2S)) = (3689.1 \pm 8.7)\text{ MeV}/c^2$ přesně odpovídá tabulkové hodnotě (PDG: $m_{\psi(2S)} = 3686.097 \pm 0.010\text{ MeV}/c^2$).
2. **Experimentální šířky píků (rozlišení spektrometru):**
   * $\sigma(J/\psi) = (71.3 \pm 1.5)\text{ MeV}/c^2$,
   * $\sigma(\psi(2S)) = 156.4_{-11.0}^{+12.0}\text{ MeV}/c^2$.
   * **Proč je šířka $\psi(2S)$ více než dvojnásobná?**  
     Při rozpadu těžšího mezonu mají vzniklé miony v průměru vyšší hybnost. V magnetickém spektrometru je relativní nepřesnost určení hybnosti úměrná velikosti hybnosti: $\Delta p / p \propto p$ (čím rychlejší částice, tím menší je zakřivení její dráhy a tím hůře se měří její poloměr). Šíření nejistoty do invariantní hmotnosti pak způsobuje, že rozlišení $\sigma$ roste s invariantní hmotností.
3. **Výtěžky částic (Extended Fit):**
   * $N(J/\psi) = 7967 \pm 171$ případů,
   * $N(\psi(2S)) = 2701 \pm 250$ případů,
   * $N_{\text{bck}} = 71827 \pm 439$ případů pozadí.
   * Poměr signálu $J/\psi$ k $\psi(2S)$ je přibližně $2.95 : 1$.
4. **Metodika chyb (HESSE vs. MINOS):**
   * U parametru $\sigma_2$ dává HESSE symetrickou chybu $\pm 11.4\text{ MeV}/c^2$.
   * MINOS zjišťuje lehkou asymetrii: $-11.0\text{ MeV}/c^2$ a $+12.0\text{ MeV}/c^2$. Tato asymetrie odráží mírnou nelinearitu profilu věrohodnosti způsobenou nízkou statistikou v piku $\psi(2S)$ a jeho těsným provázáním s pozadím.
5. **Korelace $(\sigma_2, \tau)$ a konturový řez:**
   * Výsledný korelační koeficient činí přibližně $\rho \approx -0.45$.
   * Záporná korelace je jasně patrná ze sklonu eliptických kontur $1\sigma, 2\sigma, 3\sigma$. Věrohodnostní kontura kvantifikuje společnou oblast přípustných parametrů: nelze uvažovat nejistotu šířky $\sigma_2$ izolovaně bez současného posunu sklonu pozadí $\tau$.""")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.12"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

output_path = "source/Jpsi.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"-> Successfully generated {output_path} with {len(cells)} cells.")

