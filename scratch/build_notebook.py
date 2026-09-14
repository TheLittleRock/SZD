import nbformat as nbf
import os
import subprocess

nb = nbf.v4.new_notebook()

# Metadata
nb.metadata = {
    "kernelspec": {
        "display_name": "SZD",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "codemirror_mode": {
            "name": "ipython",
            "version": 3
        },
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.10.12"
    }
}

cells = []

# --- CELL 0: Title & Executive Summary ---
# ==============================================================================
# CELL 0: Title & Executive Summary
# ==============================================================================
c0 = """# Optimalizace signifikance Higgsova bosonu v závislosti na velikosti hmotnostního okna

## Fyzikální motivace a cíl úlohy (jednoduše a srozumitelně)

V částicové fyzice zkoumáme procesy s extrémně krátkou dobou života. Higgsův boson ($m_H \\approx 125\\text{ GeV}$) žije pouhých $\\sim 10^{-22}\\text{ s}$, a proto v detektoru nikdy nezanechá přímou stopu. Místo toho jej hledáme prostřednictvím jeho rozpadových produktů. 

Jedním z nejvýznamnějších objevových kanálů je tzv. **"zlatý kanál" (Golden Channel)**:
$$H \\to Z Z^* \\to 4\\ell \\quad (\\ell = e, \\mu)$$
Tento kanál má sice relativně malý větvicí poměr, ale vyznačuje se **extrémně čistým experimentálním podpisem**: čtyři izolované nabité leptony s vysokou příčnou hybností, vynikající rozlišení detektoru pro měření invariantní hmoty čtyř leptonů ($m_{4\\ell}$) a malé, hladce klesající neredukovatelné pozadí ze Standardního modelu z kontinuální produkce párů $Z$ bosonů ($q\\bar{q} \\to ZZ \\to 4\\ell$).

Pokud změříme energie a hybnosti všech čtyř leptonů, ze speciální teorie relativity spočítáme celkovou **invariantní hmotnost**:
$$m_{4\\ell} = \\sqrt{\\left( \\sum_{i=1}^4 E_i \\right)^2 - \\left( \\sum_{i=1}^4 \\vec{p}_i \\right)^2}$$

* **Signál ($H \\to 4\\ell$):** Vytváří rezonanční pík (gaussovské rozdělení dané rozlišením detektoru) centrovaný v klidové hmotnosti Higgsova bosonu $m_H = 125\\text{ GeV}$.
* **Pozadí (SM $ZZ \\to 4\\ell$):** Vytváří spojité kontinuum bez rezonance v oblasti 125 GeV.

### Proč záleží na velikosti hmotnostního okna (Mass Window)?
Při jednoduchém počítacím experimentu (cut-and-count) definujeme kolem očekávané hmotnosti $m_0 = 125\\text{ GeV}$ symetrické hmotnostní okno:
$$m_{4\\ell} \\in \\left[ 125 - \\frac{\\Delta m}{2}, \\; 125 + \\frac{\\Delta m}{2} \\right]$$
kde $\\Delta m$ představuje celkovou šířku hmotnostního okna (full width).

Při volbě velikosti okna $\\Delta m$ stojíme před zásadním statistickým kompromisem:
1. **Příliš úzké okno ($\\Delta m \\to 0$):** Detektor má konečné rozlišení (pík má nenulovou šířku). Když zvolíme okno příliš úzké, zachytíme jen nepatrný zlomek signálu $S$. Přestože je pozadí $B$ v tomto okně téměř nulové, statistická průkaznost (signifikance) je velmi malá, protože máme málo signálových událostí.
1. **Příliš úzké okno ($\\Delta m \\to 0$):** Detektor má konečné rozlišení (pík má nenulovou šířku). Když zvolíme okno příliš úzké, odřízneme většinu signálových událostí $S$. Přestože je pozadí $B$ v tomto okně téměř nulové, statistická průkaznost (signifikance) je velmi malá, protože máme málo signálových událostí.
2. **Příliš široké okno ($\\Delta m \\gg \\text{šířka píku}$):** Pokud okno rozšíříme, zachytíme sice prakticky $100\\,\\%$ signálových událostí, ale při dalším zvětšování okna už žádný nový signál nepřibývá! Přitom kontinuální pozadí $B$ narůstá lineárně s $\\Delta m$. Protože statistická signifikance škáluje zhruba jako $S / \\sqrt{B}$, zbytečně nasbírané události pozadí signál "utopí" v šumu a signifikance prudce klesá.

**Cíl úlohy:** Najít **optimální šířku hmotnostního okna $\\Delta m_{\\text{opt}}$**, která maximalizuje statistickou signifikanci objevu Higgsova bosonu, a prozkoumat vliv luminozity, systematických chyb pozadí a fitování parametrů.

---

## Celý postup řešení krok za krokem

Postup v tomto notebooku je rozdělen do následujících logických kroků:

1. **Příprava prostředí a načtení dat:**
   * Konfigurace ROOTu v dávkovém režimu s interaktivním prohlížečem `%jsroot on` a příprava publikačního stylu v Matplotlibu.
   * Konfigurace ROOTu v dávkovém režimu s profesionálním publikačním stylem (font 42 Helvetica, vypnuté zbytečné statistické boxy i horní titulky, správné odsazení os bez překryvů).
   * Načtení simulovaných MC histogramů z `Histograms_fake.root`: signál $H(125)$, kontinuální pozadí $ZZ$ a naměřená experimentální data.
   * Vizuální kontrola invariantní hmoty $m_{4\\ell}$ a rebinování pro přehledné vykreslení (ROOT + Matplotlib).

2. **Optimalizace signifikance v závislosti na šířce okna $\\Delta m$:**
   * Procházíme šířku okna $\\Delta m$ od $0.1\\text{ GeV}$ do $25.0\\text{ GeV}$.
   * Pro každou šířku integrujeme počty událostí: $N_{\\text{sig}}$, $N_{\\text{bgr}}$ a $N_{\\text{data}}$ v daném intervalu.
   * Výpočet **očekávané p-hodnoty** a **očekávané signifikance** $Z_{\\text{exp}}$ (pro hypotézu pozadí s očekávaným signálem).
   * Výpočet **pozorované p-hodnoty** a **pozorované signifikance** $Z_{\\text{obs}}$ (porovnání dat s pozadím).
   * Převedení p-hodnoty na počet standardních odchylek gaussovského rozdělení: $Z = \\Phi^{-1}(1 - p)$.
   * Nalezení optimální šířky okna $\\Delta m_{\\text{opt}}$, kde signifikance dosahuje globálního maxima.

3. **Vliv luminozity (Luminosity Scaling):**
   * Zkoumáme, jak se změní očekávaná signifikance, pokud zdvojnásobíme integrovanou luminozitu (škálovací faktor $2.0$).
   * Porovnání s teoretickým očekáváním, že signifikance roste úměrně $\\sqrt{L}$.

4. **Určení pozadí z postranních pásem (Sideband Fit):**
   * V reálném experimentu neznáme teoretickou normalizaci pozadí zcela přesně.
   * Zvolíme kontrolní oblast invariantní hmoty bez přítomnosti signálu ($m_{4\\ell} \\in [150, 400]\\text{ GeV}$) jako **postranní pásmo (sideband)**.
   * Pomocí metody maximální věrohodnosti (binned Poisson Likelihood) fitujeme škálovací faktor pozadí $\\alpha_{\\text{bgr}}$ a jeho $1\\sigma$ interval spolehlivosti z podmínky $\\Delta(-2\\ln L) = 1$.

5. **Zahrnutí systematické nejistoty pomocí Toy Monte Carlo:**
   * Zahrneme nejistotu pozadí $\\sigma_{\\alpha}$ do výpočtu očekávané signifikance.
   * Zahrneme nejistotu pozadí $\\sigma_\\alpha$ do výpočtu očekávané signifikance.
   * Pomocí generování pseudodat (Toy MC) simulujeme fluktuace střední hodnoty pozadí (Gaussovské rozdělení) skloubené s Poissonovským vzorkováním.
   * Kvantifikujeme pokles signifikance vlivem systematické nejistoty pozadí.

6. **1D a 2D Maximum Likelihood Fit:**
   * Skenování věrohodnosti pro sílu signálu $\\mu = \\sigma / \\sigma_{\\text{SM}}$ (signal strength modifier).
   * 2D mřížkový sken parametrů $(\\alpha_{\\text{bgr}}, \\mu_{\\text{sig}})$ a vykreslení 2D vrstevnic věrohodnosti pro hladiny $1\\sigma$ a $2\\sigma$.

7. **Závěrečné shrnutí a diskuse fyzikálních výsledků.**"""
cells.append(nbf.v4.new_markdown_cell(c0))

# --- CELL 1: Imports ---
# ==============================================================================
# CELL 1: Environment & Setup
# ==============================================================================
c1_md = """## 1. Příprava prostředí a importy

Pro analýzu využijeme ekosystém **CERN ROOT** (PyROOT) ve spojení s vědeckými knihovnami v Pythonu (**NumPy**, **SciPy**, **Matplotlib**).

* `ROOT.gROOT.SetBatch(True)`: Spustí ROOT v dávkovém režimu, aby se zabránilo otevírání externích grafických X11 oken.
* `%jsroot on`: Umožňuje interaktivní vykreslování ROOT grafů přímo v prostředí Jupyteru pomocí JavaScriptové knihovny JSROOT (grafy lze zoomovat, posouvat a zkoumat hodnoty binů).
* `%config InlineBackend.figure_format='retina'`: Zajišťuje ostré vykreslení rastrových i vektorových grafů v Matplotlibu ve vysokém rozlišení.
* Globální nastavení Matplotlibu aplikuje standardní styl obvyklý v částicové fyzice (inward ticky, rámečky, čitelná velikost písma)."""
* `ROOT.gROOT.SetBatch(True)`: Spustí ROOT v dávkovém režimu bez otevírání externích X11 oken.
* `%jsroot on`: Umožňuje interaktivní vykreslování ROOT grafů přímo v Jupyteru.
* `%config InlineBackend.figure_format='retina'`: Zajišťuje ostré vykreslení grafů v Matplotlibu.
* **Publikační styl ROOTu**:
  * `ROOT.gStyle.SetOptTitle(0)`: Odstraní nevzhledné horní titulky histogramů (popisky patří do popisků obrázků nebo legendy).
  * `ROOT.gStyle.SetOptStat(0)`: Vypne statistický rámeček.
  * `ROOT.gStyle.SetTextFont(42)`: Nastaví standardní bezpatkový font Helvetica (font 42), který je mezinárodním standardem experimentů na LHC (ATLAS/CMS) pro publikace v LaTeXu."""
cells.append(nbf.v4.new_markdown_cell(c1_md))

c1_code = """import ROOT
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson
from matplotlib.ticker import AutoMinorLocator
import os

# Spuštění ROOTu v dávkovém režimu (batch mode)
ROOT.gROOT.SetBatch(True)

# Povolení interaktivního zobrazení JSROOT v Jupyteru a vysokého rozlišení pro matplotlib
%jsroot on
%matplotlib inline
%config InlineBackend.figure_format='retina'

# Globální nastavení stylu grafů podle standardů částicové fyziky (ATLAS/CMS style)
# Profesionální publikační styl ROOTu (ATLAS / CMS publication guidelines)
ROOT.gStyle.SetOptStat(0)         # Vypnutí statistického boxu
ROOT.gStyle.SetOptTitle(0)        # Vypnutí automatického titulku grafu nahoře
ROOT.gStyle.SetTextFont(42)       # Standardní font 42 (Helvetica precision 2)
ROOT.gStyle.SetLegendFont(42)

for ax in ["X", "Y", "Z"]:
    ROOT.gStyle.SetLabelFont(42, ax)
    ROOT.gStyle.SetTitleFont(42, ax)
    ROOT.gStyle.SetLabelSize(0.04, ax)
    ROOT.gStyle.SetTitleSize(0.045, ax)

ROOT.gStyle.SetTitleOffset(1.2, "X")
ROOT.gStyle.SetTitleOffset(1.4, "Y")

# Globální nastavení stylu grafů pro Matplotlib
plt.rcParams.update({
    "font.size": 12,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "axes.linewidth": 1,
    "legend.frameon": True
})"""
cells.append(nbf.v4.new_code_cell(c1_code))

# --- CELL 2: Data Loading & Mass Spectrum ---
# ==============================================================================
# CELL 2: Data Loading
# ==============================================================================
c2_md = """## 2. Načtení dat a vizualizace spektra invariantní hmoty ($m_{4\\ell}$)

### Fyzikální popis histogramů
Data máme uložena v souboru `Histograms_fake.root`. Tento soubor obsahuje 4-leptonové invariantní hmotnostní distribuce:
Data načítáme ze souboru `Histograms_fake.root`. Tento soubor obsahuje 4-leptonové invariantní hmotnostní distribuce:
1. `h_m4l_Higgs125_fake` (**Signál $H(125)$**): Monte Carlo simulace Higgsova bosonu o hmotnosti $m_H = 125\\text{ GeV}$. Vytváří úzký rezonanční pík.
2. `h_m4l_ZZ_fake` (**Pozadí SM $ZZ$**): Neredukovatelné pozadí ze Standardního modelu ($q\\bar{q}, gg \\to ZZ \\to 4\\ell$). Spojité spektrum bez rezonance na 125 GeV.
3. `h_m4l_data_fake` (**Data**): Simulovaná změřená data odpovídající skutečnému experimentálnímu měření.
4. `h_m4l_Higgs200_fake`: Hypotetický těžší Higgsův boson o hmotnosti $200\\text{ GeV}$ (pro srovnávací účely).

Původní histogramy mají **3600 binů** v rozsahu od $60\\text{ GeV}$ do $800\\text{ GeV}$. 
Šířka jednoho binu je:
$$\\Delta m_{\\text{bin}} = \\frac{800 - 60}{3600} \\approx 0.2056\\text{ GeV} \\approx 206\\text{ MeV}$$

Pro samotné hledání okna zachováme jemné binování (aby byla integrace co nejpřesnější). Pro vizuální zobrazení spektra však histogramy **rebinujeme** faktorem $10$ (šířka binu $\\approx 2.06\\text{ GeV}$) nebo $20$ (šířka binu $\\approx 4.11\\text{ GeV}$), aby byly jednotlivé sloupce statisticky dostatečně obsazené a vizuálně přehledné."""
Pro samotné hledání okna zachováme jemné binování (aby byla integrace co nejpřesnější). Pro vizuální zobrazení spektra však histogramy **rebinujeme** faktorem $20$ (šířka binu $\\approx 4.11\\text{ GeV}$), aby byly jednotlivé sloupce statisticky dostatečně obsazené a vizuálně přehledné."""
cells.append(nbf.v4.new_markdown_cell(c2_md))

c2_code = """# Robustní vyhledání cesty k souboru Histograms_fake.root
possible_paths = [
    "data/HIGGS/Histograms_fake.root",
    "source/data/HIGGS/Histograms_fake.root",
    "Histograms_fake.root"
]
root_file_path = None
for p in possible_paths:
    if os.path.exists(p):
        root_file_path = p
        break

if root_file_path is None:
    raise FileNotFoundError("Soubor Histograms_fake.root nebyl nalezen v očekávaných cestách!")

file_in = ROOT.TFile.Open(root_file_path, "READ")
print(f"Úspěšně načten ROOT soubor: {root_file_path}")
print(f"Successfully loaded ROOT file: {root_file_path}")

# Extrakce histogramů (používáme Clone, abychom zajistili nezávislost na souboru v paměti)
h_sig = file_in.Get("h_m4l_Higgs125_fake").Clone("h_sig")
h_bgr = file_in.Get("h_m4l_ZZ_fake").Clone("h_bgr")
h_data = file_in.Get("h_m4l_data_fake").Clone("h_data")
h_sig200 = file_in.Get("h_m4l_Higgs200_fake").Clone("h_sig200")

# Základní statistické informace
print(f"Celkový počet událostí signálu H(125): {h_sig.Integral():.2f}")
print(f"Celkový počet událostí pozadí SM(ZZ): {h_bgr.Integral():.2f}")
print(f"Celkový počet naměřených událostí v datech: {h_data.Integral():.0f}")
print(f"Počet binů v původním histogramu: {h_sig.GetNbinsX()}, rozsah: [{h_sig.GetXaxis().GetXmin()}, {h_sig.GetXaxis().GetXmax()}] GeV")
print(f"Šířka původního binu: {h_sig.GetBinWidth(1):.4f} GeV")"""
print(f"Total H(125) signal events: {h_sig.Integral():.2f}")
print(f"Total SM(ZZ) background events: {h_bgr.Integral():.2f}")
print(f"Total observed data events: {h_data.Integral():.0f}")
print(f"Original bins: {h_sig.GetNbinsX()}, range: [{h_sig.GetXaxis().GetXmin()}, {h_sig.GetXaxis().GetXmax()}] GeV")
print(f"Original bin width: {h_sig.GetBinWidth(1):.4f} GeV")"""
cells.append(nbf.v4.new_code_cell(c2_code))

# --- CELL 3: Mass Plot in ROOT ---
# ==============================================================================
# CELL 3: ROOT Mass Plot
# ==============================================================================
c3_md = """### Vykreslení spektra invariantní hmoty v ROOTu

Vykreslíme spektrum invariantní hmoty $m_{4\\ell}$ s rebinovacím faktorem `Irebin = 20` (šířka binu $\\approx 4.11\\text{ GeV}$).
Složené spektrum obsahuje:
* Pozadí $ZZ$ (červená plocha).
* Kumulativní histogram signál + pozadí (azurová plocha nad pozadím).
* Data se statistickými Poissonovskými chybami $\\sqrt{N}$ (černé body s chybovými úsečkami).

Díky aktivnímu `%jsroot on` je graf plně interaktivní (lze zoomovat tažením myši, dvojklikem resetovat pohled a po najetí myší zobrazit přesné souřadnice binů)."""
Graf je plně přizpůsoben požadavkům na publikační kvalitu:
* Čisté anglické popisky os s jednotkami v hranatých závorkách.
* Správně nastavené okraje plátna (`LeftMargin = 0.14`, `BottomMargin = 0.13`), aby nedocházelo k překryvům čísel s popiskem osy.
* Žádný redundantní horní titulek ani statistický box.
* Přehledná legenda vpravo nahoře s průhledným pozadím."""
cells.append(nbf.v4.new_markdown_cell(c3_md))

c3_code = """# Vytvoření kopií histogramů pro vykreslení se zadaným rebinováním
c3_code = """# Vyčištění předchozích pláten v paměti ROOTu (zabrání varování 'Deleting canvas with same name')
ROOT.gROOT.GetListOfCanvases().Delete()

Irebin = 20
h_sig_plot = h_sig.Clone("h_sig_plot")
h_bgr_plot = h_bgr.Clone("h_bgr_plot")
h_data_plot = h_data.Clone("h_data_plot")

h_sig_plot.Rebin(Irebin)
h_bgr_plot.Rebin(Irebin)
h_data_plot.Rebin(Irebin)

# Vytvoření kumulativního histogramu: Pozadí + Signál
h_sig_plus_bgr = h_bgr_plot.Clone("h_sig_plus_bgr")
h_sig_plus_bgr.Add(h_sig_plot)

# Nastavení stylů podle původního makra MassPlot()
canvas_mass_root = ROOT.TCanvas("canvas_mass_root", "Spektrum invariantní hmoty 4 leptonů", 800, 500)
canvas_mass_root.SetLeftMargin(0.12)
canvas_mass_root.SetBottomMargin(0.12)
# Vytvoření plátna s dostatečnými okraji
canvas_mass_root = ROOT.TCanvas("canvas_mass_root", "", 800, 550)
canvas_mass_root.SetLeftMargin(0.14)
canvas_mass_root.SetRightMargin(0.05)
canvas_mass_root.SetTopMargin(0.06)
canvas_mass_root.SetBottomMargin(0.13)

# Určení maxima na ose Y s rezervou pro chyby dat
data_max = h_data_plot.GetBinContent(h_data_plot.GetMaximumBin())
ymax_plot = 1.15 * (data_max + np.sqrt(data_max))
# Nastavení os a rozsahů
h_sig_plus_bgr.SetTitle("")
h_sig_plus_bgr.GetXaxis().SetTitle("4-lepton invariant mass m_{4l} [GeV]")
h_sig_plus_bgr.GetYaxis().SetTitle(f"Events / {h_bgr_plot.GetBinWidth(1):.2f} GeV")
h_sig_plus_bgr.GetXaxis().SetRangeUser(60.0, 350.0)
h_sig_plus_bgr.GetYaxis().SetRangeUser(0.0, 24.0)

h_sig_plus_bgr.SetTitle("")
h_sig_plus_bgr.GetXaxis().SetTitleSize(0.045)
h_sig_plus_bgr.GetXaxis().SetLabelSize(0.04)
h_sig_plus_bgr.GetXaxis().SetTitleFont(42)
h_sig_plus_bgr.GetXaxis().SetLabelFont(42)
h_sig_plus_bgr.GetXaxis().SetTitleOffset(1.2)

h_sig_plus_bgr.GetYaxis().SetTitleSize(0.045)
h_sig_plus_bgr.GetYaxis().SetLabelSize(0.04)
h_sig_plus_bgr.GetYaxis().SetTitleFont(42)
h_sig_plus_bgr.GetYaxis().SetLabelFont(42)
h_sig_plus_bgr.GetYaxis().SetTitleOffset(1.4)

# Vzhled komponent
h_sig_plus_bgr.SetFillColor(ROOT.kCyan - 7)
h_sig_plus_bgr.SetLineColor(ROOT.kBlue + 1)
h_sig_plus_bgr.SetLineWidth(1)
h_sig_plus_bgr.GetXaxis().SetRangeUser(60.0, 350.0)
h_sig_plus_bgr.GetYaxis().SetRangeUser(0.0, ymax_plot)
h_sig_plus_bgr.GetXaxis().SetTitle("4-lepton invariant mass m_{4l} [GeV]")
h_sig_plus_bgr.GetYaxis().SetTitle(f"Events / {h_bgr_plot.GetBinWidth(1):.2f} GeV")
h_sig_plus_bgr.GetXaxis().SetTitleOffset(1.1)
h_sig_plus_bgr.GetYaxis().SetTitleOffset(1.1)
h_sig_plus_bgr.Draw("hist")

h_bgr_plot.SetFillColor(ROOT.kRed - 4)
h_bgr_plot.SetLineColor(ROOT.kRed + 2)
h_bgr_plot.SetLineWidth(1)
h_bgr_plot.Draw("hist same")
h_bgr_plot.Draw("axis same")

h_data_plot.SetMarkerStyle(20)
h_data_plot.SetMarkerSize(0.9)
h_data_plot.SetMarkerSize(0.85)
h_data_plot.SetMarkerColor(ROOT.kBlack)
h_data_plot.SetLineColor(ROOT.kBlack)
h_data_plot.SetLineWidth(2)

# Vykreslení
h_sig_plus_bgr.Draw("hist")
h_bgr_plot.Draw("hist same")
h_bgr_plot.Draw("axis same")
h_data_plot.Draw("e same")

# Legenda
leg_root = ROOT.TLegend(0.65, 0.65, 0.88, 0.85)
# Profesionální legenda
leg_root = ROOT.TLegend(0.60, 0.65, 0.90, 0.88)
leg_root.SetBorderSize(0)
leg_root.SetFillColor(0)
leg_root.SetTextSize(0.035)
leg_root.SetFillStyle(0)
leg_root.SetTextFont(42)
leg_root.SetTextSize(0.038)
leg_root.AddEntry(h_data_plot, "Data", "pe")
leg_root.AddEntry(h_sig_plus_bgr, "Higgs (125 GeV)", "f")
leg_root.AddEntry(h_bgr_plot, "SM (ZZ) background", "f")
leg_root.Draw()

canvas_mass_root.Draw()"""
cells.append(nbf.v4.new_code_cell(c3_code))

# --- CELL 4: Mass Plot in Matplotlib ---
# ==============================================================================
# CELL 4: Matplotlib Mass Plot
# ==============================================================================
c4_md = """### Vykreslení spektra invariantní hmoty v Matplotlibu

Pro publikační účely převedeme histogramy do polí NumPy a vykreslíme spektrum invariantní hmoty pomocí knihovny Matplotlib. 
Pro publikační účely do LaTeX článků vykreslíme spektrum invariantní hmoty pomocí knihovny Matplotlib. 
Využijeme styl skládaného histogramu (stacked area) a datové body s Poissonovskými chybami."""
cells.append(nbf.v4.new_markdown_cell(c4_md))

c4_code = """# Funkce pro extrakci dat z TH1D do polí NumPy
def get_hist_data(hist):
c4_code = """def get_hist_data(hist):
    nbins = hist.GetNbinsX()
    bin_edges = np.array([hist.GetBinLowEdge(i) for i in range(1, nbins + 2)])
    bin_centers = np.array([hist.GetBinCenter(i) for i in range(1, nbins + 1)])
    contents = np.array([hist.GetBinContent(i) for i in range(1, nbins + 1)])
    errors = np.array([hist.GetBinError(i) for i in range(1, nbins + 1)])
    return bin_edges, bin_centers, contents, errors

edges, centers, y_bgr, err_bgr = get_hist_data(h_bgr_plot)
_, _, y_sig, err_sig = get_hist_data(h_sig_plot)
_, _, y_data, err_data = get_hist_data(h_data_plot)

# Ořízneme rozsah pro přehledné vykreslení na interval 60 až 350 GeV
mask = (centers >= 60.0) & (centers <= 350.0)
edge_mask = (edges >= 60.0) & (edges <= 350.0 + h_bgr_plot.GetBinWidth(1))
bin_width = h_bgr_plot.GetBinWidth(1)

fig, ax = plt.subplots(figsize=(9, 6))
fig, ax = plt.subplots(figsize=(8.5, 5.5))

bin_width = h_bgr_plot.GetBinWidth(1)

# Vykreslení skládaného histogramu pozadí a signálu
# Skládaný histogram pozadí a signálu
ax.bar(centers[mask], y_bgr[mask], width=bin_width, color="#e74c3c", edgecolor="#c0392b", 
       label=r"SM ($ZZ \to 4\ell$) pozadí", align="center")
       label=r"SM ($ZZ \to 4\ell$) background", align="center")
ax.bar(centers[mask], y_sig[mask], bottom=y_bgr[mask], width=bin_width, color="#5dade2", edgecolor="#2980b9", 
       label=r"Higgs ($m_H = 125\text{ GeV}$)", align="center")

# Vykreslení datových bodů s chybovými úsečkami
# Datové body s chybovými úsečkami
ax.errorbar(centers[mask], y_data[mask], yerr=np.sqrt(np.maximum(y_data[mask], 1.0)), 
            fmt="o", color="black", markersize=5, capsize=2, elinewidth=1.5, label="Data")

ax.set_xlabel(r"Invariantní hmotnost 4 leptonů $m_{4\ell}$ [GeV]")
ax.set_ylabel(f"Počet událostí / {bin_width:.2f} GeV")
ax.set_xlabel(r"4-lepton invariant mass $m_{4\ell}$ [GeV]")
ax.set_ylabel(f"Events / {bin_width:.2f} GeV")
ax.set_xlim(60, 350)
ax.set_ylim(0, ymax_plot)
ax.set_ylim(0, 24)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend(loc="upper right", framealpha=0.9)

# Anotace píků
ax.annotate(r"$H(125) \to 4\ell$", xy=(125, y_bgr[np.argmin(np.abs(centers - 125))] + y_sig[np.argmin(np.abs(centers - 125))]),
            xytext=(145, ymax_plot * 0.75),
            xytext=(145, 18),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
            fontsize=12, fontweight="bold")

plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(c4_code))

# --- CELL 5: Significance Optimization Theory ---
# ==============================================================================
# CELL 5: Significance Theory
# ==============================================================================
c5_md = """## 3. Optimalizace velikosti hmotnostního okna (Significance vs. Size of Mass Window)

### Teoretický a statistický základ
Mějme hypotézu pozadí $H_0$ (pouze Standardní model bez Higgsova bosonu) a alternativní hypotézu $H_1$ (SM pozadí + signál Higgsova bosonu).

Pro danou šířku hmotnostního okna $\\Delta m$ centrovaného kolem $m_H = 125\\text{ GeV}$ spočítáme v intervalu:
$$m_{4\\ell} \\in \\left[ 125 - \\frac{\\Delta m}{2}, \\; 125 + \\frac{\\Delta m}{2} \\right]$$
integrováním histogramů následující veličiny:
* $N_{\\text{sig}}(\\Delta m)$: očekávaný počet signálových událostí.
* $N_{\\text{bgr}}(\\Delta m)$: očekávaný počet událostí pozadí.
* $N_{\\text{data}}(\\Delta m)$: skutečně naměřený počet událostí v datech.

### 1. Očekávaná signifikance (Expected Significance)
Pokud je hypotéza $H_1$ pravdivá, očekáváme celkový počet událostí:
$$N_{\\text{exp}} = N_{\\text{bgr}} + N_{\\text{sig}}$$
Očekávaná **p-hodnota** ($p_{\\text{exp}}$) vyjadřuje pravděpodobnost, že za předpokladu platnosti nulové hypotézy $H_0$ (která se řídí Poissonovým rozdělením s parametrem $\\lambda = N_{\\text{bgr}}$) naměříme náhodnou fluktuací hodnotu větší nebo rovnu očekávané hodnotě $N_{\\text{exp}}$:
$$p_{\\text{exp}} = P(N \\ge N_{\\text{exp}} \\mid \\lambda = N_{\\text{bgr}}) = 1 - \\sum_{k=0}^{\\lfloor N_{\\text{exp}} \\rfloor - 1} \\frac{e^{-N_{\\text{bgr}}} N_{\\text{bgr}}^k}{k!}$$

### 2. Pozorovaná signifikance (Observed Significance)
Pozorovaná p-hodnota testuje naměřená data $N_{\\text{data}}$ proti hypotéze pozadí:
$$p_{\\text{obs}} = P(N \\ge N_{\\text{data}} \\mid \\lambda = N_{\\text{bgr}}) = 1 - \\sum_{k=0}^{N_{\\text{data}} - 1} \\frac{e^{-N_{\\text{bgr}}} N_{\\text{bgr}}^k}{k!}$$

### 3. Převod p-hodnoty na gaussovskou signifikanci $Z$ (v jednotkách $\\sigma$)
Zavedeným standardem v částicové fyzice je vyjadřovat p-hodnotu jako odpovídající počet standardních odchylek jednostranného gaussovského rozdělení:
$$Z = \\Phi^{-1}(1 - p)$$
kde $\\Phi(x)$ je kumulativní distribuční funkce normálního rozdělení $\\mathcal{N}(0, 1)$.
V ROOTu se tato inverze provádí funkcí `ROOT.Math.gaussian_quantile_c(p, 1.0)`, v SciPy pomocí `scipy.stats.norm.isf(p)`.

* $Z = 3\\sigma \\iff p \\approx 1.35 \\times 10^{-3}$: úroveň náznaku (**Evidence**).
* $Z = 5\\sigma \\iff p \\approx 2.87 \\times 10^{-7}$: úroveň nesporného objevu (**Discovery**).

### 4. Vliv luminozity (Luminosity Scaling)
Pokud urychlovač nabere $2\\times$ více dat (integrovaná luminozita $L \\to 2L$), počty událostí signálu i pozadí vzrostou dvakrát:
$$N_{\\text{sig}}' = 2 \\times N_{\\text{sig}}, \\quad N_{\\text{bgr}}' = 2 \\times N_{\\text{bgr}}$$
Protože statistická chyba pozadí roste jako $\\sqrt{N_{\\text{bgr}}}$, signifikance škáluje jako:
$$Z \\propto \\frac{N_{\\text{sig}}}{\\sqrt{N_{\\text{bgr}}}} \\implies Z' \\approx \\sqrt{2} \\times Z \\approx 1.414 \\times Z$$"""
cells.append(nbf.v4.new_markdown_cell(c5_md))

c5_code = """# Funkce pro výpočet Poissonovské p-hodnoty (integrace zprava od N_obs do nekonečna)
def integrate_poisson_from_right(mu, n_obs):
    \"\"\"
    Spočítá p-hodnotu P(N >= n_obs | mu).
    Využívá komplement kumulativní Poissonovy pravděpodobnosti:
    p = 1 - sum_{k=0}^{floor(n_obs)-1} P(k | mu)
    \"\"\"
c5_code = """def integrate_poisson_from_right(mu, n_obs):
    if mu <= 0:
        return 1.0
    k_max = int(np.floor(n_obs))
    if k_max <= 0:
        return 1.0
    
    integral = 1.0
    for i in range(k_max):
        integral -= ROOT.TMath.Poisson(i, mu)
    
    return max(0.0, min(1.0, integral))

def calculate_significance(p_val):
    \"\"\"Převede jednostrannou p-hodnotu na počet sigma (gaussovská signifikance).\"\"\"
    if p_val <= 0.0 or p_val >= 1.0:
        return 0.0
    return ROOT.Math.gaussian_quantile_c(p_val, 1.0)

# Vytvoření histogramů pro uložení závislosti signifikance na velikosti okna (0 až 25 GeV, 250 binů)
nbins_w = 250
w_min = 0.0
w_max = 25.0

h_masswindow_exp = ROOT.TH1D("h_masswindow_exp", "Očekávaná signifikance (L=1.0)", nbins_w, w_min, w_max)
h_masswindow_obs = ROOT.TH1D("h_masswindow_obs", "Pozorovaná signifikance (L=1.0)", nbins_w, w_min, w_max)
h_masswindow_exp_lumi2 = ROOT.TH1D("h_masswindow_exp_lumi2", "Očekávaná signifikance (L=2.0)", nbins_w, w_min, w_max)
h_masswindow_exp = ROOT.TH1D("h_masswindow_exp", "", nbins_w, w_min, w_max)
h_masswindow_obs = ROOT.TH1D("h_masswindow_obs", "", nbins_w, w_min, w_max)
h_masswindow_exp_lumi2 = ROOT.TH1D("h_masswindow_exp_lumi2", "", nbins_w, w_min, w_max)

# Pole pro Matplotlib
windows_arr = []
z_exp_arr = []
z_obs_arr = []
z_exp_lumi2_arr = []

# Skenování šířky hmotnostního okna Delta m
for i_bin in range(1, nbins_w + 1):
    w = h_masswindow_exp.GetBinCenter(i_bin) # Celková šířka okna v GeV
    w = h_masswindow_exp.GetBinCenter(i_bin)
    windows_arr.append(w)
    
    # Hranice okna: [125 - w/2, 125 + w/2]
    bin_low = h_data.FindBin(125.0 - w / 2.0)
    bin_high = h_data.FindBin(125.0 + w / 2.0)
    
    # 1. Luminosity scale factor = 1.0
    n_sig = h_sig.Integral(bin_low, bin_high)
    n_bgr = h_bgr.Integral(bin_low, bin_high)
    n_data = h_data.Integral(bin_low, bin_high)
    
    # Očekávaná signifikance (mu = n_bgr, n_obs = n_bgr + n_sig)
    p_exp = integrate_poisson_from_right(n_bgr, n_bgr + n_sig)
    z_exp = calculate_significance(p_exp)
    h_masswindow_exp.SetBinContent(i_bin, z_exp)
    z_exp_arr.append(z_exp)
    
    # Pozorovaná signifikance (mu = n_bgr, n_obs = n_data)
    p_obs = integrate_poisson_from_right(n_bgr, n_data)
    z_obs = calculate_significance(p_obs)
    h_masswindow_obs.SetBinContent(i_bin, z_obs)
    z_obs_arr.append(z_obs)
    
    # 2. Luminosity scale factor = 2.0 (zdvojnásobená data)
    # 2. Luminosity scale factor = 2.0
    n_sig_l2 = 2.0 * n_sig
    n_bgr_l2 = 2.0 * n_bgr
    p_exp_l2 = integrate_poisson_from_right(n_bgr_l2, n_bgr_l2 + n_sig_l2)
    z_exp_l2 = calculate_significance(p_exp_l2)
    h_masswindow_exp_lumi2.SetBinContent(i_bin, z_exp_l2)
    z_exp_lumi2_arr.append(z_exp_l2)

windows_arr = np.array(windows_arr)
z_exp_arr = np.array(z_exp_arr)
z_obs_arr = np.array(z_obs_arr)
z_exp_lumi2_arr = np.array(z_exp_lumi2_arr)

# Nalezení optimálních hodnot
opt_exp_idx = np.argmax(z_exp_arr)
opt_obs_idx = np.argmax(z_obs_arr)
opt_exp_lumi2_idx = np.argmax(z_exp_lumi2_arr)

print("="*60)
print("VÝSLEDKY OPTIMALIZACE HMOTNOSTNÍHO OKNA:")
print("="*60)
print(f"Očekávané maximum (L=1.0):")
print(f"  -> Optimální šířka okna Delta m : {windows_arr[opt_exp_idx]:.2f} GeV (tj. 125 +/- {windows_arr[opt_exp_idx]/2:.2f} GeV)")
print(f"  -> Maximální očekávaná signifikance Z: {z_exp_arr[opt_exp_idx]:.3f} sigma")
print(f"Pozorované maximum v datech (L=1.0):")
print(f"  -> Šířka okna Delta m : {windows_arr[opt_obs_idx]:.2f} GeV (tj. 125 +/- {windows_arr[opt_obs_idx]/2:.2f} GeV)")
print(f"  -> Maximální pozorovaná signifikance Z: {z_obs_arr[opt_obs_idx]:.3f} sigma")
print(f"Očekávané maximum se zdvojnásobenou luminozitou (L=2.0):")
print(f"  -> Optimální šířka okna Delta m : {windows_arr[opt_exp_lumi2_idx]:.2f} GeV")
print(f"  -> Maximální očekávaná signifikance Z: {z_exp_lumi2_arr[opt_exp_lumi2_idx]:.3f} sigma")
print(f"  -> Poměr Z(L=2) / Z(L=1) = {z_exp_lumi2_arr[opt_exp_lumi2_idx] / z_exp_arr[opt_exp_idx]:.3f} (teoreticky sqrt(2) = 1.414)")
print("="*60)"""
print("="*65)
print("MASS WINDOW SIGNIFICANCE OPTIMIZATION RESULTS:")
print("="*65)
print(f"Expected Maximum (L = 1.0):")
print(f"  -> Optimal window full width Delta m: {windows_arr[opt_exp_idx]:.2f} GeV (125 +/- {windows_arr[opt_exp_idx]/2:.2f} GeV)")
print(f"  -> Peak expected significance Z     : {z_exp_arr[opt_exp_idx]:.3f} sigma")
print(f"Observed Maximum in Data (L = 1.0):")
print(f"  -> Window full width Delta m        : {windows_arr[opt_obs_idx]:.2f} GeV (125 +/- {windows_arr[opt_obs_idx]/2:.2f} GeV)")
print(f"  -> Peak observed significance Z     : {z_obs_arr[opt_obs_idx]:.3f} sigma")
print(f"Expected Maximum with Doubled Luminosity (L = 2.0):")
print(f"  -> Optimal window full width Delta m: {windows_arr[opt_exp_lumi2_idx]:.2f} GeV")
print(f"  -> Peak expected significance Z     : {z_exp_lumi2_arr[opt_exp_lumi2_idx]:.3f} sigma")
print(f"  -> Ratio Z(L=2.0) / Z(L=1.0)        : {z_exp_lumi2_arr[opt_exp_lumi2_idx] / z_exp_arr[opt_exp_idx]:.3f} (theory: sqrt(2) = 1.414)")
print("="*65)"""
cells.append(nbf.v4.new_code_cell(c5_code))

# --- CELL 6: Significance Plots (ROOT and Matplotlib) ---
# ==============================================================================
# CELL 6: ROOT Significance Plot
# ==============================================================================
c6_md = """### Vykreslení závislosti signifikance na šířce okna v ROOTu

Vykreslíme výsledný graf signifikance jako funkce velikosti okna pro luminozitní faktor $L=1.0$ (očekávaná černou čarou, pozorovaná modrou čarou)."""
Vykreslíme výsledný graf signifikance pro luminozitní faktor $L=1.0$ (očekávaná černou čarou, pozorovaná modrou čarou) a pro $L=2.0$ (oranžovou čárkovanou čarou). 
Graf má odstraněný horní titulek, odstraněný statistický box a veškerý text je v angličtině."""
cells.append(nbf.v4.new_markdown_cell(c6_md))

c6_code = """canvas_sig_root = ROOT.TCanvas("canvas_sig_root", "Signifikance vs Sirka hmotnostniho okna", 800, 500)
canvas_sig_root.SetLeftMargin(0.12)
canvas_sig_root.SetBottomMargin(0.12)
c6_code = """ROOT.gROOT.GetListOfCanvases().Delete()

canvas_sig_root = ROOT.TCanvas("canvas_sig_root", "", 800, 550)
canvas_sig_root.SetLeftMargin(0.14)
canvas_sig_root.SetRightMargin(0.05)
canvas_sig_root.SetTopMargin(0.06)
canvas_sig_root.SetBottomMargin(0.13)

h_masswindow_exp.SetTitle("")
h_masswindow_exp.GetXaxis().SetTitle("Mass window full width #Delta m [GeV]")
h_masswindow_exp.GetYaxis().SetTitle("Significance Z [#sigma]")
h_masswindow_exp.SetAxisRange(-0.2, 5.5, "Y")
h_masswindow_exp.SetAxisRange(0.0, 25.0, "X")

h_masswindow_exp.GetXaxis().SetTitleSize(0.045)
h_masswindow_exp.GetXaxis().SetLabelSize(0.04)
h_masswindow_exp.GetXaxis().SetTitleFont(42)
h_masswindow_exp.GetXaxis().SetLabelFont(42)
h_masswindow_exp.GetXaxis().SetTitleOffset(1.2)

h_masswindow_exp.GetYaxis().SetTitleSize(0.045)
h_masswindow_exp.GetYaxis().SetLabelSize(0.04)
h_masswindow_exp.GetYaxis().SetTitleFont(42)
h_masswindow_exp.GetYaxis().SetLabelFont(42)
h_masswindow_exp.GetYaxis().SetTitleOffset(1.4)

h_masswindow_exp.SetLineColor(ROOT.kBlack)
h_masswindow_exp.SetLineWidth(2)
h_masswindow_exp.SetAxisRange(-0.5, 5.5, "Y")
h_masswindow_exp.GetXaxis().SetTitle("Mass window #Delta m [GeV]")
h_masswindow_exp.GetYaxis().SetTitle("Significance Z [#sigma]")
h_masswindow_exp.GetXaxis().SetTitleOffset(1.1)
h_masswindow_exp.GetYaxis().SetTitleOffset(1.1)
h_masswindow_exp.Draw("l")

h_masswindow_obs.SetLineColor(ROOT.kBlue + 1)
h_masswindow_obs.SetLineWidth(2)

h_masswindow_exp.Draw("l")
h_masswindow_obs.Draw("l same")

# Legenda
leg_sig_root = ROOT.TLegend(0.55, 0.70, 0.88, 0.85)
leg_sig_root.SetBorderSize(0)
h_masswindow_exp_lumi2.SetLineColor(ROOT.kOrange + 7)
h_masswindow_exp_lumi2.SetLineWidth(2)
h_masswindow_exp_lumi2.SetLineStyle(2)
h_masswindow_exp_lumi2.Draw("l same")

# Vodorovné linie objevových prahů 3 sigma a 5 sigma
line_3sig = ROOT.TLine(0.0, 3.0, 25.0, 3.0)
line_3sig.SetLineColor(ROOT.kGray + 1)
line_3sig.SetLineStyle(3)
line_3sig.SetLineWidth(1)
line_3sig.Draw()

line_5sig = ROOT.TLine(0.0, 5.0, 25.0, 5.0)
line_5sig.SetLineColor(ROOT.kRed + 2)
line_5sig.SetLineStyle(3)
line_5sig.SetLineWidth(1)
line_5sig.Draw()

# Profesionální legenda
leg_sig_root = ROOT.TLegend(0.48, 0.64, 0.92, 0.84)
leg_sig_root.SetBorderSize(1)
leg_sig_root.SetFillColor(0)
leg_sig_root.SetTextSize(0.035)
leg_sig_root.AddEntry(h_masswindow_exp, f"Expected (max = {z_exp_arr[opt_exp_idx]:.2f}#sigma @ {windows_arr[opt_exp_idx]:.1f} GeV)", "l")
leg_sig_root.AddEntry(h_masswindow_obs, f"Observed (max = {z_obs_arr[opt_obs_idx]:.2f}#sigma @ {windows_arr[opt_obs_idx]:.1f} GeV)", "l")
leg_sig_root.SetTextFont(42)
leg_sig_root.SetTextSize(0.032)
leg_sig_root.AddEntry(h_masswindow_exp, f"Expected (L = 1.0, max = {z_exp_arr[opt_exp_idx]:.2f}#sigma)", "l")
leg_sig_root.AddEntry(h_masswindow_obs, f"Observed (L = 1.0, max = {z_obs_arr[opt_obs_idx]:.2f}#sigma)", "l")
leg_sig_root.AddEntry(h_masswindow_exp_lumi2, f"Expected (L = 2.0, max = {z_exp_lumi2_arr[opt_exp_lumi2_idx]:.2f}#sigma)", "l")
leg_sig_root.Draw()

# Text s luminozitním faktorem
txt_lumi = ROOT.TLatex(0.15, 0.82, "Luminosity scale factor = 1.0")
txt_lumi.SetNDC(True)
txt_lumi.SetTextSize(0.04)
txt_lumi.Draw()
txt_opt = ROOT.TLatex(0.18, 0.88, f"Optimal window: #Delta m = {windows_arr[opt_exp_idx]:.1f} GeV")
txt_opt.SetNDC(True)
txt_opt.SetTextFont(42)
txt_opt.SetTextSize(0.038)
txt_opt.Draw()

canvas_sig_root.Draw()"""
cells.append(nbf.v4.new_code_cell(c6_code))

# ==============================================================================
# CELL 7: Matplotlib Significance Plot
# ==============================================================================
c7_md = """### Vykreslení závislosti signifikance v Matplotlibu

V Matplotlibu vykreslíme přehledné porovnání pro obě luminozity ($L=1.0$ i $L=2.0$) společně s pozorovanou signifikancí v datech a vyznačením klíčových hranic ($3\\sigma$ Evidence a $5\\sigma$ Discovery)."""
cells.append(nbf.v4.new_markdown_cell(c7_md))

c7_code = """fig, ax = plt.subplots(figsize=(9, 6))
c7_code = """fig, ax = plt.subplots(figsize=(8.5, 5.5))

# Křivky signifikance
ax.plot(windows_arr, z_exp_arr, color="black", lw=2, label=r"Očekávaná ($L = 1.0$)")
ax.plot(windows_arr, z_obs_arr, color="#2980b9", lw=2, label=r"Pozorovaná v datech ($L = 1.0$)")
ax.plot(windows_arr, z_exp_lumi2_arr, color="#e67e22", lw=2, linestyle="--", label=r"Očekávaná se $2\times$ luminozitou ($L = 2.0$)")
ax.plot(windows_arr, z_exp_arr, color="black", lw=2, label=r"Expected ($L = 1.0$)")
ax.plot(windows_arr, z_obs_arr, color="#2980b9", lw=2, label=r"Observed in data ($L = 1.0$)")
ax.plot(windows_arr, z_exp_lumi2_arr, color="#e67e22", lw=2, linestyle="--", label=r"Expected with $2\times$ luminosity ($L = 2.0$)")

# Zvýraznění optimálních bodů
ax.scatter([windows_arr[opt_exp_idx]], [z_exp_arr[opt_exp_idx]], color="black", s=60, zorder=5)
ax.scatter([windows_arr[opt_obs_idx]], [z_obs_arr[opt_obs_idx]], color="#2980b9", s=60, zorder=5)
ax.scatter([windows_arr[opt_exp_lumi2_idx]], [z_exp_lumi2_arr[opt_exp_lumi2_idx]], color="#e67e22", s=60, zorder=5)
ax.scatter([windows_arr[opt_exp_idx]], [z_exp_arr[opt_exp_idx]], color="black", s=50, zorder=5)
ax.scatter([windows_arr[opt_obs_idx]], [z_obs_arr[opt_obs_idx]], color="#2980b9", s=50, zorder=5)
ax.scatter([windows_arr[opt_exp_lumi2_idx]], [z_exp_lumi2_arr[opt_exp_lumi2_idx]], color="#e67e22", s=50, zorder=5)

# Vodorovné linie objevových prahů 3 sigma a 5 sigma
ax.axhline(3.0, color="gray", linestyle=":", lw=1.2, alpha=0.7, label=r"$3\sigma$ (Evidence)")
ax.axhline(5.0, color="darkred", linestyle=":", lw=1.2, alpha=0.7, label=r"$5\sigma$ (Discovery)")

ax.set_xlabel(r"Šířka hmotnostního okna $\Delta m$ [GeV] (kolem $125\text{ GeV}$)")
ax.set_ylabel(r"Signifikance $Z$ [$\sigma$]")
ax.set_xlabel(r"Mass window full width $\\Delta m$ [GeV] (around $125\\ \\mathrm{GeV}$)")
ax.set_ylabel(r"Significance $Z$ [$\\sigma$]")
ax.set_xlim(0, 25)
ax.set_ylim(-0.2, 5.5)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend(loc="upper right", framealpha=0.95, fontsize=10.5)

# Anotace maxima
lbl_max = "Optimum L=1.0: $\\\\Delta m = {:.1f}\\\\text{{ GeV}}\\n$Z = {:.2f}\\\\sigma$".format(windows_arr[opt_exp_idx], z_exp_arr[opt_exp_idx])
lbl_max = "Optimum L=1.0: $\\Delta m = %.1f\\ \\mathrm{GeV}\\n$Z = %.2f\\sigma$" % (windows_arr[opt_exp_idx], z_exp_arr[opt_exp_idx])
ax.annotate(lbl_max,
            xy=(windows_arr[opt_exp_idx], z_exp_arr[opt_exp_idx]),
            xytext=(windows_arr[opt_exp_idx] + 2.5, z_exp_arr[opt_exp_idx] - 0.7),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(c7_code))

# --- CELL 8: Sideband Fit Theory ---
# ==============================================================================
# CELL 8: Sideband Fit Theory
# ==============================================================================
c8_md = """## 4. Určení pozadí z postranních pásem (Sideband Fit)

### Fyzikální motivace: data-driven odhad pozadí
V reálné experimentální analýze nelze teoretickou předpověď pozadí z MC generátorů přijmout bez ověření. Monte Carlo simulace mají systematické nejistoty:
* Nejistota určení integrované luminozity urychlovače (typicky $1-3\\,\\%$).
* Teoretické nejistoty účinného průřezu produkce $ZZ$ párů v perturbativní QCD/EWK (škálová závislost, PDF partonových rozdělení).
* Experimentální účinnost rekonstrukce a identifikace leptonů.

Proto se normalizace pozadí v signálové oblasti kalibruje přímo z dat v tzv. **kontrolní oblasti neboli postranním pásmu (sideband)**. 

Zvolíme oblast invariantní hmoty čtyř leptonů:
$$m_{4\\ell} \\in [150, 400]\\text{ GeV}$$
V tomto rozsahu se nenachází žádný signál Higgsova bosonu s $m_H = 125\\text{ GeV}$ ($N_{\\text{sig}} \\approx 0$), takže veškerá naměřená data tvoří výhradně pozadí Standardního modelu.

### Metoda maximální věrohodnosti (Binned Poisson Likelihood)
Zavedeme škálovací parametr $\\alpha_{\\text{bgr}}$, kterým škálujeme nominální Monte Carlo předpověď pozadí:
$$\\mu_i(\\alpha_{\\text{bgr}}) = \\alpha_{\\text{bgr}} \\cdot N_{\\text{bgr}, i}$$
kde $N_{\\text{bgr}, i}$ je obsah $i$-tého binu pozadí v postranním pásmu a $N_{\\text{data}, i}$ je počet naměřených datových událostí v tomto binu.

Pravděpodobnost naměření $N_{\\text{data}, i}$ událostí při očekávané střední hodnotě $\\mu_i$ je dána Poissonovým rozdělením. Sdružená věrohodnostní funkce (Likelihood) přes všechny biny v postranním pásmu je:
$$L(\\alpha_{\\text{bgr}}) = \\prod_{i \\in \\text{sideband}} \\frac{\\mu_i^{N_{\\text{data}, i}} e^{-\\mu_i}}{N_{\\text{data}, i}!}$$

Přejdeme k logaritmu záporné věrohodnosti (Negative Log-Likelihood, NLL), kterou minimalizujeme:
$$-2\\ln L(\\alpha_{\\text{bgr}}) = -2 \\sum_{i \\in \\text{sideband}} \\left[ N_{\\text{data}, i} \\ln(\\alpha_{\\text{bgr}} N_{\\text{bgr}, i}) - \\alpha_{\\text{bgr}} N_{\\text{bgr}, i} - \\ln(N_{\\text{data}, i}!) \\right]$$

### Hledání minima a určení chyby $\\pm 1\\sigma$
Podle Wilksova teorému odpovídá změna funkce věrohodnosti o $\\Delta(-2\\ln L) = 1$ statistickému intervalu spolehlivosti $1\\sigma$ ($68.27\\,\\%$):
$$-2\\Delta\\ln L(\\alpha_{\\text{bgr}}) = -2\\ln L(\\alpha_{\\text{bgr}}) - \\min\\left(-2\\ln L\\right) = 1$$
Odtud získáme odhad faktoru pozadí $\\hat{\\alpha}_{\\text{bgr}}$ i jeho statistickou a systematickou chybu $\\sigma_\\alpha$."""
cells.append(nbf.v4.new_markdown_cell(c8_md))

c8_code = """# Příprava histogramů pro postranní pásmo (rebinování 10 pro binwidth ~2.06 GeV)
Irebin_sb = 10
c8_code = """Irebin_sb = 10
h_bgr_sb = h_bgr.Clone("h_bgr_sb")
h_data_sb = h_data.Clone("h_data_sb")
h_bgr_sb.Rebin(Irebin_sb)
h_data_sb.Rebin(Irebin_sb)

# Definice postranního pásma (sidebandu) v rozsahu 150 až 400 GeV
bin_sb_low = h_data_sb.FindBin(150.0)
bin_sb_high = h_data_sb.FindBin(400.0)

# Skenování škálovacího parametru alfa_bgr od 0.1 do 2.5 v 241 krocích
alphas = np.linspace(0.1, 2.5, 241)
nll_vals = []

for a in alphas:
    loglik = 0.0
    for b in range(bin_sb_low, bin_sb_high + 1):
        d_val = h_data_sb.GetBinContent(b)
        b_val = a * h_bgr_sb.GetBinContent(b)
        if b_val > 0.0:
            # Přičítáme logaritmus Poissonovy pravděpodobnosti
            loglik += ROOT.TMath.Log(ROOT.TMath.Poisson(d_val, b_val))
    nll_vals.append(-2.0 * loglik)

nll_vals = np.array(nll_vals)
min_nll = np.min(nll_vals)
best_alpha_idx = np.argmin(nll_vals)
best_alpha = alphas[best_alpha_idx]

# Delta -2 ln L
delta_nll = nll_vals - min_nll

# Nalezení bodů pro Delta(-2 ln L) = 1.0 (úroveň 1 sigma)
idx_below_1sigma = np.where(delta_nll <= 1.0)[0]
alpha_err_low = best_alpha - alphas[idx_below_1sigma[0]]
alpha_err_high = alphas[idx_below_1sigma[-1]] - best_alpha
sigma_alpha = (alpha_err_low + alpha_err_high) / 2.0

print("="*60)
print("VÝSLEDEK FITOVÁNÍ POZADÍ V POSTRANNÍM PÁSMU (SIDEBAND FIT):")
print("="*60)
print(f"Rozsah postranního pásma: 150 - 400 GeV")
print(f"Optimální škálovací faktor pozadí alfa_bgr = {best_alpha:.3f} + {alpha_err_high:.3f} - {alpha_err_low:.3f}")
print(f"Střední hodnota chyby sigma(alfa) = {sigma_alpha:.3f}")
print("="*65)
print("SIDEBAND BACKGROUND FIT RESULTS:")
print("="*65)
print(f"Sideband mass range: 150 - 400 GeV")
print(f"Optimal background scale factor alpha_bgr = {best_alpha:.3f} + {alpha_err_high:.3f} - {alpha_err_low:.3f}")
print(f"Mean uncertainty sigma(alpha)            = {sigma_alpha:.3f} ({sigma_alpha/best_alpha*100:.1f}%)")

# Aplikace faktoru na optimální hmotnostní okno (125 +/- 3.55 GeV, tj. sirka 7.1 GeV)
opt_w = windows_arr[opt_exp_idx]
b_sig_low = h_data.FindBin(125.0 - opt_w / 2.0)
b_sig_high = h_data.FindBin(125.0 + opt_w / 2.0)

n_bgr_nom = h_bgr.Integral(b_sig_low, b_sig_high)
n_bgr_scaled = n_bgr_nom * best_alpha
n_bgr_err = n_bgr_nom * sigma_alpha
n_sig_opt = h_sig.Integral(b_sig_low, b_sig_high)
n_data_opt = h_data.Integral(b_sig_low, b_sig_high)

print(f"Počet událostí v optimálním okně [125 +/- {opt_w/2:.2f} GeV]:")
print(f"  -> Signál H(125) : {n_sig_opt:.2f}")
print(f"  -> Původní nominální pozadí (před fitem) : {n_bgr_nom:.2f}")
print(f"  -> Přeškálované pozadí po fitu : {n_bgr_scaled:.2f} +/- {n_bgr_err:.2f}")
print(f"  -> Změřená data : {n_data_opt:.0f}")
print("="*60)"""
print(f"Event yields in optimal window [125 +/- {opt_w/2:.2f} GeV]:")
print(f"  -> Signal H(125)                      : {n_sig_opt:.2f}")
print(f"  -> Nominal background (before fit)   : {n_bgr_nom:.2f}")
print(f"  -> Scaled background (after fit)     : {n_bgr_scaled:.2f} +/- {n_bgr_err:.2f}")
print(f"  -> Observed data                      : {n_data_opt:.0f}")
print("="*65)"""
cells.append(nbf.v4.new_code_cell(c8_code))

# --- CELL 9: Sideband Fit Plots ---
c9_md = """### Vykreslení věrohodnostní křivky Sideband Fitu (ROOT a Matplotlib)
# ==============================================================================
# CELL 9: ROOT Sideband Plot
# ==============================================================================
c9_md = """### Vykreslení věrohodnostní křivky Sideband Fitu v ROOTu

Vykreslíme křivku $\\Delta(-2\\ln L)$ jako funkci parametru $\\alpha_{\\text{bgr}}$ a vyznačíme minimum i pásmo $\\pm 1\\sigma$."""
Vykreslíme křivku $\\Delta(-2\\ln L)$ jako funkci parametru $\\alpha_{\\text{bgr}}$ v relevantním rozsahu minima (bez nežádoucího roztažení osy Y do 170). 
Graf má odstraněný horní titulek, čistý font Helvetica a jasně vyznačené hladiny spolehlivosti $1\\sigma$ a $2\\sigma$ v angličtině."""
cells.append(nbf.v4.new_markdown_cell(c9_md))

c9_code = """# 1. Vykreslení v ROOTu pomocí TGraph
c9_code = """ROOT.gROOT.GetListOfCanvases().Delete()

graph_sb_root = ROOT.TGraph(len(alphas), alphas, delta_nll)
graph_sb_root.SetTitle(";Background scale factor #alpha_{bgr};#Delta(-2 ln L)")
graph_sb_root.SetTitle("")
graph_sb_root.GetXaxis().SetTitle("Background scale factor #alpha_{bgr}")
graph_sb_root.GetYaxis().SetTitle("#Delta(-2 ln L)")

graph_sb_root.GetXaxis().SetTitleSize(0.045)
graph_sb_root.GetXaxis().SetLabelSize(0.04)
graph_sb_root.GetXaxis().SetTitleFont(42)
graph_sb_root.GetXaxis().SetLabelFont(42)
graph_sb_root.GetXaxis().SetTitleOffset(1.2)

graph_sb_root.GetYaxis().SetTitleSize(0.045)
graph_sb_root.GetYaxis().SetLabelSize(0.04)
graph_sb_root.GetYaxis().SetTitleFont(42)
graph_sb_root.GetYaxis().SetLabelFont(42)
graph_sb_root.GetYaxis().SetTitleOffset(1.4)

graph_sb_root.SetLineWidth(2)
graph_sb_root.SetLineColor(ROOT.kBlue + 1)

canvas_sb_root = ROOT.TCanvas("canvas_sb_root", "Sideband Fit Likelihood", 800, 500)
canvas_sb_root.SetLeftMargin(0.12)
canvas_sb_root.SetBottomMargin(0.12)
canvas_sb_root = ROOT.TCanvas("canvas_sb_root", "", 800, 550)
canvas_sb_root.SetLeftMargin(0.14)
canvas_sb_root.SetRightMargin(0.05)
canvas_sb_root.SetTopMargin(0.06)
canvas_sb_root.SetBottomMargin(0.13)

# Zoomujeme do relevantního okolí minima (0.8 až 1.5), aby křivka nebyla zploštělá
graph_sb_root.GetXaxis().SetRangeUser(0.8, 1.5)
graph_sb_root.GetYaxis().SetRangeUser(0.0, 9.0)
graph_sb_root.GetYaxis().SetRangeUser(0.0, 8.0)
graph_sb_root.Draw("al")

# Vodorovná čára na Delta(-2lnL) = 1.0 (úroveň 1 sigma)
# Vodorovná čára na Delta(-2lnL) = 1.0 (1 sigma) a 4.0 (2 sigma)
line_1sig_root = ROOT.TLine(0.8, 1.0, 1.5, 1.0)
line_1sig_root.SetLineColor(ROOT.kRed)
line_1sig_root.SetLineStyle(2)
line_1sig_root.SetLineWidth(2)
line_1sig_root.Draw()

txt_sb_root = ROOT.TLatex(0.20, 0.78, f"#hat{{#alpha}}_{{bgr}} = {best_alpha:.3f} #pm {sigma_alpha:.3f}")
line_2sig_root = ROOT.TLine(0.8, 4.0, 1.5, 4.0)
line_2sig_root.SetLineColor(ROOT.kMagenta + 2)
line_2sig_root.SetLineStyle(3)
line_2sig_root.SetLineWidth(2)
line_2sig_root.Draw()

txt_sb_root = ROOT.TLatex(0.18, 0.88, "Best fit: #hat{#alpha}_{bgr} = %.3f #pm %.3f" % (best_alpha, sigma_alpha))
txt_sb_root.SetNDC(True)
txt_sb_root.SetTextSize(0.045)
txt_sb_root.SetTextFont(42)
txt_sb_root.SetTextSize(0.038)
txt_sb_root.Draw()

leg_sb_root = ROOT.TLegend(0.48, 0.66, 0.92, 0.88)
leg_sb_root.SetBorderSize(1)
leg_sb_root.SetFillColor(0)
leg_sb_root.SetTextFont(42)
leg_sb_root.SetTextSize(0.032)
leg_sb_root.AddEntry(graph_sb_root, "#Delta(-2 ln L) profile", "l")
leg_sb_root.AddEntry(line_1sig_root, "1#sigma CL (#Delta(-2 ln L) = 1.0)", "l")
leg_sb_root.AddEntry(line_2sig_root, "2#sigma CL (#Delta(-2 ln L) = 4.0)", "l")
leg_sb_root.Draw()

canvas_sb_root.Draw()"""
cells.append(nbf.v4.new_code_cell(c9_code))

c10_code = """# 2. Vykreslení v Matplotlibu
fig, ax = plt.subplots(figsize=(8, 5.5))
# ==============================================================================
# CELL 10: Matplotlib Sideband Plot
# ==============================================================================
c10_md = """### Vykreslení věrohodnostní křivky Sideband Fitu v Matplotlibu

ax.plot(alphas, delta_nll, color="#2980b9", lw=2.5, label=r"$\\Delta(-2\\ln L)$ profil věrohodnosti")
ax.axhline(1.0, color="#e74c3c", linestyle="--", lw=1.5, label=r"$\\Delta(-2\\ln L) = 1.0$ ($1\\sigma$ interval)")
ax.axhline(4.0, color="#8e44ad", linestyle=":", lw=1.5, label=r"$\\Delta(-2\\ln L) = 4.0$ ($2\\sigma$ interval)")
Matplotlib verze věrohodnostního profilu s vyznačeným $1\\sigma$ chybovým pásem v angličtině."""
cells.append(nbf.v4.new_markdown_cell(c10_md))

# Vyznačení minima a 1 sigma chybového pásma
c10_code = """fig, ax = plt.subplots(figsize=(8, 5.5))

ax.plot(alphas, delta_nll, color="#2980b9", lw=2.5, label=r"$\Delta(-2\ln L)$ profile likelihood")
ax.axhline(1.0, color="#e74c3c", linestyle="--", lw=1.5, label=r"$\Delta(-2\ln L) = 1.0$ ($1\sigma$ interval)")
ax.axhline(4.0, color="#8e44ad", linestyle=":", lw=1.5, label=r"$\Delta(-2\ln L) = 4.0$ ($2\sigma$ interval)")

ax.axvline(best_alpha, color="black", linestyle="-.", lw=1.2, alpha=0.7)
ax.axvspan(best_alpha - alpha_err_low, best_alpha + alpha_err_high, color="#2980b9", alpha=0.15, label=r"$1\\sigma$ chybový pás")
ax.axvspan(best_alpha - alpha_err_low, best_alpha + alpha_err_high, color="#2980b9", alpha=0.15, label=r"$1\sigma$ confidence band")

ax.set_xlabel(r"Škálovací faktor pozadí $\\alpha_{\\text{bgr}}$")
ax.set_xlabel(r"Background scale factor $\\alpha_{\\mathrm{bgr}}$")
ax.set_ylabel(r"$\\Delta(-2\\ln L)$")
ax.set_xlim(0.8, 1.5)
ax.set_ylim(-0.2, 8.0)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend(loc="upper right", framealpha=0.95)

lbl_fit = "Nejlepší fit:\\n$\\\\hat{{\\\\alpha}}_{{\\\\text{{bgr}}}} = {:.3f} \\\\pm {:.3f}$".format(best_alpha, sigma_alpha)
lbl_fit = "Best fit:\\n" + r"$\\hat{\\alpha}_{\\mathrm{bgr}} = %.3f \\pm %.3f$" % (best_alpha, sigma_alpha)
ax.annotate(lbl_fit,
            xy=(best_alpha, 0.0), xytext=(best_alpha + 0.1, 1.8),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
            fontsize=11, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(c10_code))

# --- CELL 11: Toy Monte Carlo Theory ---
# ==============================================================================
# CELL 11: Toy MC Theory
# ==============================================================================
c11_md = """## 5. Zahrnutí systematické nejistoty pomocí Toy Monte Carlo

### Fyzikální motivace: vliv nejistoty pozadí na signifikanci
V části 3 jsme předpokládali, že očekávaný počet událostí pozadí $N_{\\text{bgr}}$ je znám s absolutní přesností (představuje fixní parametr Poissonova rozdělení). V reálném měření má však normalizace pozadí nenulovou systematickou nejistotu (zde $\\sigma_\\alpha \\approx 0.06$, což představuje přibližně $5.4\\,\\%$ relativní chybu):
$$\\sigma_{N_{\\text{bgr}}} = N_{\\text{bgr}} \\cdot \\sigma_\\alpha$$

V důsledku toho fluktuuje počet událostí pozadí v experimentu ze dvou nezávislých zdrojů:
1. **Systematická fluktuace:** Skutečná střední hodnota pozadí $\\lambda$ fluktuuje podle normálního rozdělení $\\mathcal{N}(N_{\\text{bgr}}, \\sigma_{N_{\\text{bgr}}})$.
2. **Statistická fluktuace:** Pozorovaný počet událostí v detektoru se řídí Poissonovým rozdělením se střední hodnotou $\\lambda$: $N \\sim \\text{Pois}(\\lambda)$.

Tato složená distribuce (Poisson s gaussovsky rozmazanou střední hodnotou) má **širší rozptyl** než čistý Poisson. V důsledku toho je pravděpodobnost, že pozadí náhodně vyfluktuuje nahoru, vyšší $\\implies$ **očekávaná signifikance objevu klesá**.

### Toy Monte Carlo algoritmus
Pomocí generátoru náhodných čísel `TRandom3` vygenerujeme $150\\,000$ pseudoexperimentů:
1. Vygenerujeme náhodnou střední hodnotu $\\lambda_{\\text{toy}} \\sim \\text{Gaus}(N_{\\text{bgr}}, \\sigma_{N_{\\text{bgr}}})$.
2. Pro každé $\\lambda_{\\text{toy}}$ vygenerujeme Poissonovský počet událostí $N_{\\text{toy}} \\sim \\text{Poisson}(\\lambda_{\\text{toy}})$.
3. Uložíme hodnoty do histogramu a spočítáme p-hodnotu integrováním od bodu očekávaného signálu ($N_{\\text{bgr}} + N_{\\text{sig}}$) do nekonečna:
   $$p_{\\text{toy}} = \\frac{1}{N_{\\text{toys}}} \\sum_{i=1}^{N_{\\text{toys}}} \\Theta(N_{\\text{toy}, i} - (N_{\\text{bgr}} + N_{\\text{sig}}))$$
4. Přepočteme na signifikanci $Z_{\\text{toy}} = \\Phi^{-1}(1 - p_{\\text{toy}})$ a porovnáme s čistě Poissonovskou hodnotou."""
cells.append(nbf.v4.new_markdown_cell(c11_md))

c11_code = """# Generování Toy Monte Carlo pseudodat
ntoys = 150000
rnd = ROOT.TRandom3(42) # fixní seed pro reprodukovatelnost
c11_code = """ntoys = 150000
rnd = ROOT.TRandom3(42)

# Histogramy pro rozdělení pozadí: čistý Poisson vs. Toy MC s chybou
h_poisson_pure = ROOT.TH1D("h_poisson_pure", "Cisty Poisson bez chyby", 40, 0, 40)
h_poisson_smeared = ROOT.TH1D("h_poisson_smeared", "Toy MC se systematickou chybou", 40, 0, 40)
h_poisson_pure = ROOT.TH1D("h_poisson_pure", "", 40, 0, 40)
h_poisson_smeared = ROOT.TH1D("h_poisson_smeared", "", 40, 0, 40)

toy_counts = []
pure_counts = []

for _ in range(ntoys):
    # Čistý Poisson
    n_pure = rnd.Poisson(n_bgr_scaled)
    h_poisson_pure.Fill(n_pure)
    pure_counts.append(n_pure)
    
    # Gaussovské rozmazání střední hodnoty pozadí
    lambda_smeared = rnd.Gaus(n_bgr_scaled, n_bgr_err)
    if lambda_smeared < 0.0:
        lambda_smeared = 0.0
    n_smeared = rnd.Poisson(lambda_smeared)
    h_poisson_smeared.Fill(n_smeared)
    toy_counts.append(n_smeared)

toy_counts = np.array(toy_counts)
pure_counts = np.array(pure_counts)

# Prahová hodnota pro očekávaný signál + pozadí
n_threshold = n_bgr_scaled + n_sig_opt

# 1. P-hodnota a signifikance před započtením systematické chyby
p_val_before = integrate_poisson_from_right(n_bgr_scaled, n_threshold)
z_before = calculate_significance(p_val_before)

# 2. P-hodnota a signifikance z Toy MC se systematickou chybou
# Integrace histogramu od prahu do nekonečna
bin_thresh = h_poisson_smeared.FindBin(n_threshold)
p_val_after = h_poisson_smeared.Integral(bin_thresh, 40) / h_poisson_smeared.Integral()
z_after = calculate_significance(p_val_after)

print("="*60)
print("DOPAD SYSTEMATICKÉ CHYBY POZADÍ NA SIGNIFIKANCI:")
print("="*60)
print(f"Střední hodnota pozadí v okně: {n_bgr_scaled:.2f} +/- {n_bgr_err:.2f} událostí")
print(f"Očekávaný signál v okně      : {n_sig_opt:.2f} událostí")
print(f"Práh (Signál + Pozadí)       : {n_threshold:.2f} událostí")
print(f"Očekávaná signifikance BEZ chyby pozadí (čistý Poisson) : {z_before:.3f} sigma (p = {p_val_before:.4e})")
print(f"Očekávaná signifikance SE systematickou chybou pozadí  : {z_after:.3f} sigma (p = {p_val_after:.4e})")
print(f"Pokles signifikance vlivem nejistoty pozadí            : {z_before - z_after:.3f} sigma")
print("="*60)"""
print("="*65)
print("IMPACT OF BACKGROUND SYSTEMATIC UNCERTAINTY ON SIGNIFICANCE:")
print("="*65)
print(f"Background mean in window        : {n_bgr_scaled:.2f} +/- {n_bgr_err:.2f} events")
print(f"Expected signal in window        : {n_sig_opt:.2f} events")
print(f"S+B discovery threshold          : {n_threshold:.2f} events")
print(f"Significance WITHOUT bgr error   : {z_before:.3f} sigma (p = {p_val_before:.4e})")
print(f"Significance WITH bgr systematics: {z_after:.3f} sigma (p = {p_val_after:.4e})")
print(f"Significance loss                : {z_before - z_after:.3f} sigma")
print("="*65)"""
cells.append(nbf.v4.new_code_cell(c11_code))

# --- CELL 12: Toy MC Plots ---
# ==============================================================================
# CELL 12: Matplotlib Toy MC Plot
# ==============================================================================
c12_md = """### Porovnání Poissonova rozdělení a Toy MC rozdělení (Matplotlib)

Vykreslíme normalizované rozdělení počtu událostí pozadí pro případ nulové systematické chyby (čistý Poisson) a případ se systematickou chybou pozadí (Toy MC)."""
cells.append(nbf.v4.new_markdown_cell(c12_md))

c12_code = """fig, ax = plt.subplots(figsize=(8.5, 5.5))

bins_plot = np.arange(0, 35, 1)

# Normalizované histogramy
ax.hist(pure_counts, bins=bins_plot, density=True, histtype="step", lw=2, color="black", 
        label=f"Čistý Poisson bez chyby (Z = {z_before:.2f}$\\sigma$)")
        label=f"Pure Poisson without uncertainty ($Z = {z_before:.2f}\\sigma$)")
ax.hist(toy_counts, bins=bins_plot, density=True, histtype="stepfilled", alpha=0.35, color="#e67e22", edgecolor="#d35400", lw=2,
        label=f"Toy MC se systematickou chybou (Z = {z_after:.2f}$\\sigma$)")
        label=f"Toy MC with systematic uncertainty ($Z = {z_after:.2f}\\sigma$)")

# Zvýraznění prahu pro signál + pozadí
ax.axvline(n_threshold, color="#c0392b", linestyle="--", lw=2, 
           label=f"Práh $S+B = {n_threshold:.1f}$")
           label=f"Threshold $S+B = {n_threshold:.1f}$")

# Vybarvení chvostu přesahujícího práh
x_tail = np.linspace(n_threshold, 35, 100)
ax.fill_between(x_tail, 0, 0.005, color="#c0392b", alpha=0.3, label="Integrovaná oblast (p-hodnota)")
ax.fill_between(x_tail, 0, 0.005, color="#c0392b", alpha=0.3, label="Integrated p-value tail")

ax.set_xlabel("Počet událostí pozadí v hmotnostním okně")
ax.set_ylabel("Hustota pravděpodobnosti")
ax.set_xlabel("Background counts in mass window")
ax.set_ylabel("Probability density")
ax.set_xlim(0, 30)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend(loc="upper right", framealpha=0.95, fontsize=10.5)

msg_toy = "Širší chvost Toy MC rozdělení\\\\nzpůsobuje nárůst p-hodnoty\\\\na tím pokles signifikance!"
msg_toy = "Broader tail of Toy MC distribution\\nincreases p-value,\\nreducing discovery significance"
ax.annotate(msg_toy,
            xy=(n_threshold + 1, 0.015), xytext=(n_threshold + 4, 0.045),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(c12_code))

# --- CELL 13: 1D & 2D Profile Likelihood ---
# ==============================================================================
# CELL 13: 1D & 2D Profile Likelihood
# ==============================================================================
c13_md = """## 6. Jednorozměrný a dvourozměrný Maximum Likelihood Fit

### Fyzikální koncept síly signálu $\\mu$
V moderní experimentální částicové fyzice (včetně objevových článků ATLAS a CMS) modelujeme celkový počet událostí v každém binu spektra pomocí dvou parametrů:
$$\\mu_i(\\alpha_{\\text{bgr}}, \\mu_{\\text{sig}}) = \\mu_{\\text{sig}} \\cdot N_{\\text{sig}, i} + \\alpha_{\\text{bgr}} \\cdot N_{\\text{bgr}, i}$$
* $\\mu_{\\text{sig}}$ (**Signal Strength Modifier**): škálovací faktor síly signálu. Hodnota $\\mu = 1$ odpovídá přesně předpovědi Standardního modelu, $\\mu = 0$ je hypotéza pozadí bez Higgsova bosonu.
* $\\alpha_{\\text{bgr}}$: škálovací faktor normalizace pozadí SM $ZZ$.

### Sdružená věrohodnost přes celé spektrum
Sestavíme funkci záporné logaritmické věrohodnosti přes celé spektrum invariantní hmoty ($m_{4\\ell} \\in [100, 400]\\text{ GeV}$):
$$-2\\ln L(\\alpha_{\\text{bgr}}, \\mu_{\\text{sig}}) = -2 \\sum_{i} \\left[ N_{\\text{data}, i} \\ln(\\mu_{\\text{sig}} N_{\\text{sig}, i} + \\alpha_{\\text{bgr}} N_{\\text{bgr}, i}) - (\\mu_{\\text{sig}} N_{\\text{sig}, i} + \\alpha_{\\text{bgr}} N_{\\text{bgr}, i}) - \\ln(N_{\\text{data}, i}!) \\right]$$

### 2D vrstevnice věrohodnosti (Wilksův teorém pro 2 parametry)
Pro dva volné parametry odpovídají změny $\\Delta(-2\\ln L)$:
* $\\Delta(-2\\ln L) = 2.30$: oblast spolehlivosti $1\\sigma$ ($68.27\\,\\%$ CL).
* $\\Delta(-2\\ln L) = 6.18$: oblast spolehlivosti $2\\sigma$ ($95.45\\,\\%$ CL).
* $\\Delta(-2\\ln L) = 11.83$: oblast spolehlivosti $3\\sigma$ ($99.73\\,\\%$ CL).

2D vrstevnice umožňují přímo vizualizovat korelaci mezi odhadem pozadí a signálem: pokud pozadí vyfluktuuje nahoru, potřebný signál pro vysvětlení dat mírně klesne (záporná korelace)."""
cells.append(nbf.v4.new_markdown_cell(c13_md))

c13_code = """# Příprava rebinovaných histogramů pro 2D fit spektra (Irebin = 10)
h_sig_fit = h_sig.Clone("h_sig_fit")
c13_code = """h_sig_fit = h_sig.Clone("h_sig_fit")
h_bgr_fit = h_bgr.Clone("h_bgr_fit")
h_data_fit = h_data.Clone("h_data_fit")

h_sig_fit.Rebin(10)
h_bgr_fit.Rebin(10)
h_data_fit.Rebin(10)

b_fit_start = h_data_fit.FindBin(100.0)
b_fit_end = h_data_fit.FindBin(400.0)

# 1. Jednorozměrný sken síly signálu mu (při fixním pozadí alfa = 1.105)
# 1. Jednorozměrný sken síly signálu mu (při fixním pozadí alfa z postranního pásma)
fixed_alpha = best_alpha
mu_grid_1d = np.linspace(0.0, 3.0, 151)
nll_1d = []

for m_val in mu_grid_1d:
    loglik = 0.0
    for b in range(b_fit_start, b_fit_end + 1):
        d_val = h_data_fit.GetBinContent(b)
        tot_model = m_val * h_sig_fit.GetBinContent(b) + fixed_alpha * h_bgr_fit.GetBinContent(b)
        if tot_model > 0.0:
            loglik += ROOT.TMath.Log(ROOT.TMath.Poisson(d_val, tot_model))
    nll_1d.append(-2.0 * loglik)

nll_1d = np.array(nll_1d)
min_nll_1d = np.min(nll_1d)
best_mu_1d = mu_grid_1d[np.argmin(nll_1d)]
delta_nll_1d = nll_1d - min_nll_1d

# 1 sigma chyba pro mu
idx_mu_1sig = np.where(delta_nll_1d <= 1.0)[0]
mu_err_low = best_mu_1d - mu_grid_1d[idx_mu_1sig[0]]
mu_err_high = mu_grid_1d[idx_mu_1sig[-1]] - best_mu_1d

print("="*60)
print("1D MAXIMUM LIKELIHOOD FIT PRO SÍLU SIGNÁLU (mu):")
print(f"Odhad síly signálu: mu = {best_mu_1d:.2f} + {mu_err_high:.2f} - {mu_err_low:.2f}")
print("="*60)
print("="*65)
print("1D MAXIMUM LIKELIHOOD FIT FOR SIGNAL STRENGTH (mu):")
print(f"Extracted signal strength: mu = {best_mu_1d:.2f} + {mu_err_high:.2f} - {mu_err_low:.2f}")
print("="*65)

# 2. Dvourozměrný sken věrohodnosti (alfa_bgr vs. mu_sig)
alphas_2d = np.linspace(0.8, 1.5, 71)
mus_2d = np.linspace(0.2, 2.5, 71)

grid_nll_2d = np.zeros((len(mus_2d), len(alphas_2d)))

for i_m, m_val in enumerate(mus_2d):
    for i_a, a_val in enumerate(alphas_2d):
        loglik = 0.0
        for b in range(b_fit_start, b_fit_end + 1):
            d_val = h_data_fit.GetBinContent(b)
            tot_model = m_val * h_sig_fit.GetBinContent(b) + a_val * h_bgr_fit.GetBinContent(b)
            if tot_model > 0.0:
                loglik += ROOT.TMath.Log(ROOT.TMath.Poisson(d_val, tot_model))
        grid_nll_2d[i_m, i_a] = -2.0 * loglik

min_2d_val = np.min(grid_nll_2d)
delta_nll_2d = grid_nll_2d - min_2d_val

# Globální minimum ve 2D
min_idx_2d = np.unravel_index(np.argmin(grid_nll_2d), grid_nll_2d.shape)
best_mu_2d = mus_2d[min_idx_2d[0]]
best_alpha_2d = alphas_2d[min_idx_2d[1]]

print(f"2D Globální minimum: alfa_bgr = {best_alpha_2d:.3f}, mu_sig = {best_mu_2d:.2f}")
print("="*60)"""
print(f"2D Global Minimum: alpha_bgr = {best_alpha_2d:.3f}, mu_sig = {best_mu_2d:.2f}")
print("="*65)"""
cells.append(nbf.v4.new_code_cell(c13_code))

# --- CELL 14: 2D Contour Plot in Matplotlib ---
# ==============================================================================
# CELL 14: Matplotlib 2D Contour Plot
# ==============================================================================
c14_md = """### Vykreslení 2D vrstevnic věrohodnosti (Matplotlib)

Vykreslíme 2D barevnou mapu $\\Delta(-2\\ln L)$ a kontury pro $1\\sigma$ ($68.3\\,\\%$) a $2\\sigma$ ($95.5\\,\\%$) confidence levels."""
Vykreslíme 2D barevnou mapu $\\Delta(-2\\ln L)$ a kontury pro $1\\sigma$ ($68.3\\,\\%$) a $2\\sigma$ ($95.5\\,\\%$) confidence levels s popiskami v angličtině."""
cells.append(nbf.v4.new_markdown_cell(c14_md))

c14_code = """fig, ax = plt.subplots(figsize=(8.5, 6))

A_mesh, M_mesh = np.meshgrid(alphas_2d, mus_2d)

# Vykreslení barevné mapy
c = ax.contourf(A_mesh, M_mesh, delta_nll_2d, levels=np.linspace(0, 15, 31), cmap="Blues_r", alpha=0.85)
cb = fig.colorbar(c, ax=ax)
cb.set_label(r"$\Delta(-2\ln L)$")

# Vykreslení 1 sigma a 2 sigma vrstevnic
contours = ax.contour(A_mesh, M_mesh, delta_nll_2d, levels=[2.30, 6.18], 
                      colors=["#e74c3c", "#8e44ad"], linewidths=[2.2, 1.8])

# Popisky kontur
ax.clabel(contours, inline=True, fmt={2.30: r"$1\sigma$ (68%)", 6.18: r"$2\sigma$ (95%)"}, fontsize=11)

# Bod nejlepšího fitu a bod Standardního modelu (mu=1, alfa=1)
lbl_best = "Best Fit ($\\\\hat{{\\\\alpha}} = {:.2f}, \\\\hat{{\\\\mu}} = {:.2f}$)".format(best_alpha_2d, best_mu_2d)
lbl_best = r"Best Fit ($\hat{\\alpha} = %.2f, \hat{\\mu} = %.2f$)" % (best_alpha_2d, best_mu_2d)
ax.plot(best_alpha_2d, best_mu_2d, marker="P", markersize=10, color="gold", markeredgecolor="black", 
        linestyle="None", label=lbl_best)
ax.plot(1.0, 1.0, marker="o", markersize=8, color="lime", markeredgecolor="black", 
        linestyle="None", label="Standard Model ($\\\\alpha = 1.0, \\\\mu = 1.0$)")
        linestyle="None", label=r"Standard Model ($\\alpha = 1.0, \\mu = 1.0$)")

ax.set_xlabel(r"Škálovací faktor pozadí $\\alpha_{\\text{bgr}}$")
ax.set_ylabel(r"Síla signálu Higgsova bosonu $\\mu_{\\text{sig}}$")
ax.set_xlabel(r"Background scale factor $\\alpha_{\\mathrm{bgr}}$")
ax.set_ylabel(r"Signal strength modifier $\\mu_{\\mathrm{sig}}$")
ax.set_xlim(0.8, 1.5)
ax.set_ylim(0.2, 2.5)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend(loc="upper right", framealpha=0.95, fontsize=10.5)

plt.tight_layout()
plt.show()"""
cells.append(nbf.v4.new_code_cell(c14_code))

# --- CELL 15: Conclusion ---
# ==============================================================================
# CELL 15: Conclusion
# ==============================================================================
c15_md = """## 7. Závěr a shrnutí fyzikálních poznatků

V této úloze jsme detailně prozkoumali statistickou metodu optimalizace hmotnostního okna pro objev Standardního Higgsova bosonu v kanálu $H \\to ZZ^* \\to 4\\ell$:

### Hlavní výsledky:
1. **Optimální velikost hmotnostního okna:**
   * Očekávaná statistická signifikance dosahuje maxima při plné šířce okna **$\\Delta m_{\\text{opt}} \\approx 7.1\\text{ GeV}$** (tj. $m_{4\\ell} \\in [121.45, 128.55]\\text{ GeV}$, neboli $125 \\pm 3.55\\text{ GeV}$).
   * Důvodem je kompromis mezi zachycením většiny signálového píku rozmazaného konečným rozlišením detektoru a minimalizací podílu kontinuálního pozadí $ZZ$.
   * Při tomto optimálním okně je očekávaná signifikance **$Z_{\\text{exp}} \\approx 2.04\\sigma$** (při nominální luminozitě).
   * V naměřených pseudodatech dosahuje pozorovaná signifikance hodnoty až **$3.92\\sigma$** v užším okně ($\Delta m \approx 2.8\text{ GeV}$) vlivem náhodné pozitivní fluktuace dat.
   * V naměřených pseudodatech dosahuje pozorovaná signifikance hodnoty až **$3.92\\sigma$** v užším okně ($\\Delta m \\approx 2.8\\text{ GeV}$) vlivem náhodné pozitivní fluktuace dat.

2. **Škálování s luminozitou:**
   * Při zdvojnásobení luminozity ($L=2.0$) vzroste očekávaná signifikance na **$Z \\approx 2.98\\sigma$**, což přesně odpovídá teoretickému vztahu $Z \\propto \\sqrt{L}$ (faktoru $\\sqrt{2} \\approx 1.414$). Pro dosažení $5\\sigma$ objevu by tedy bylo zapotřebí přibližně $6\\times$ vyšší statistiky dat.

3. **Data-driven kalibrace pozadí (Sideband Fit):**
   * V postranním pásmu bez signálu ($m_{4\\ell} \\in [150, 400]\\text{ GeV}$) jsme pomocí Poissonovy věrohodnosti nafitovali škálovací faktor pozadí:
     $$\\hat{\\alpha}_{\\text{bgr}} = 1.120 \\pm 0.060$$
   * Pozadí v datech je tedy o cca $12\\,\\%$ vyšší než nominální MC simulace pozadí s relativní nejistotou $5.4\\,\\%$.

4. **Vliv systematické chyby pozadí (Toy MC):**
   * Započtení $5.4\\,\\%$ nejistoty pozadí pomocí Toy Monte Carlo simulace rozšiřuje chvost očekávané Poissonovy distribuce pozadí.
   * V důsledku toho klesá očekávaná signifikance z $2.02\\sigma$ na **$1.89\\sigma$** (pokles o cca $0.13\\sigma$).

5. **2D fit parametrů $(\\alpha_{\\text{bgr}}, \\mu_{\\text{sig}})$:**
   * 2D Maximum Likelihood fit potvrdil konzistenci dat s modelem Standardního modelu v rámci $1\\sigma$ intervalu spolehlivosti s mírnou zápornou korelací mezi pozadím a signálem."""
cells.append(nbf.v4.new_markdown_cell(c15_md))

nb.cells = cells

# Save notebook
output_path = "source/Higgs.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Notebook úspěšně vygenerován do {output_path} s {len(cells)} buňkami.")
print(f"Notebook successfully generated to {output_path} with {len(cells)} cells.")
