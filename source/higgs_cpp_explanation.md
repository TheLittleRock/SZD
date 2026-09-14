# Podrobný rozbor C++ kódu pro Higgs analýzu (`Higgs_full.C`)

Tento dokument slouží jako detailní referenční příručka a komentář k originálnímu C++ kódu `Higgs_full.C` (a cvičení `HIGGS_empty.C`) z předmětu **SZD2**. Je koncipován speciálně pro vývojáře a fyziky zvyklé na programování v **Pythonu**, kteří potřebují do hloubky porozumět mechanismům jazyka C++, objektovému modelu frameworku **CERN ROOT**, správě paměti a statistickým metodám použitým při objevu Higgsova bosonu.

---

## 1. Základní koncepty C++ a CERN ROOT pro Pythonisty

Než se ponoříme do samotného kódu, shrňme zásadní rozdíly mezi Pythonem a C++ v prostředí ROOTu.

### 1.1 Typový systém a deklarace proměnných
* **Python:** Dynamicky typovaný jazyk. Proměnná vzniká přiřazením (`x = 5.0`).
* **C++:** Staticky typovaný jazyk. Každá proměnná i návratová hodnota funkce musí mít předem explicitně deklarovaný typ (`double x = 5.0;`, `int n = 10;`, `TH1D *hist = nullptr;`).

### 1.2 Ukazatele (Pointers), paměť a operátor šipky (`->`)
V C++ se objekty často vytvářejí na haldě (heap) pomocí klíčového slova `new`. Proměnná pak neobsahuje přímo objekt, ale jeho **adresu v paměti** (ukazatel, pointer, označovaný hvězdičkou `*`):

```cpp
TH1D *h_mass = new TH1D("h_mass", "Title", 100, 0, 100);
```

* V Pythonu k atributům a metodám přistupujeme tečkou: `hist.Draw()`.
* V C++, pokud pracujeme s **ukazatelem**, používáme operátor šipky `->`:
  ```cpp
  h_mass->Draw();  // ekvivalent (*h_mass).Draw()
  ```
  Pokud bychom měli objekt přímo na zásobníku (stack, bez `new`), použila by se tečka: `hist.Draw()`. V ROOT kódech se však u grafických objektů a histogramů téměř výhradně používají ukazatele.

### 1.3 Správa paměti a ROOT Object Ownership (Vlastnictví objektů)
CERN ROOT má specifický systém vlastnictví paměti, který je častým zdrojem chyb pro programátory přecházející z Pythonu:
1. **Adresářové vlastnictví (`TDirectory` a `gDirectory`):**
   * Když vytvoříte histogram (`new TH1D(...)`), ROOT jej automaticky zaregistruje do aktuálně otevřeného adresáře (`gDirectory`).
   * Když otevřete soubor `TFile *file = new TFile("data.root", "READ")`, tento soubor se stane aktuálním `gDirectory`.
   * **Pozor na past:** Pokud načtete histogram ze souboru pomocí `file->Get("...")` a soubor zavřete, ROOT histogram automaticky smaže z paměti!
   * **Řešení:** Proto se v C++ kódu používá metoda `Clone()`:
     ```cpp
     h_mass = (TH1D*) file->Get("h_m4l_ZZ_fake")->Clone("h_mass");
     ```
     Ta vytvoří nezávislou kopii v paměti, která přežije i po uzavření souboru.

### 1.4 Přetypování (Type Casting)
V C++ metoda `file->Get("...")` vrací obecný bázový ukazatel `TObject*`. Aby kompilátor věděl, že jde o jednorozměrný histogram s plovoucí řádovou čárkou (`TH1D`), musíme provést explicitní přetypování (C-style cast):
```cpp
(TH1D*) file->Get("h_m4l_ZZ_fake")
```
V Pythonu (`PyROOT`) toto probíhá automaticky na pozadí díky reflexi.

### 1.5 Číslování binů v ROOT histogramech (1-based indexing)
Na rozdíl od Pythonu a NumPy, kde se pole indexují od 0:
* **Bin 0:** Underflow bin (události pod minimem osy $X$).
* **Bin 1:** První platný bin histogramu ($x_{\min} \le x < x_1$).
* **Bin $N$ (`GetNbinsX()`):** Poslední platný bin histogramu.
* **Bin $N+1$:** Overflow bin (události nad maximem osy $X$).
Proto všechny for-cykly přes biny začínají od 1:
```cpp
for (int i_bin = 1; i_bin <= h->GetNbinsX(); i_bin++) { ... }
```

---

## 2. Přehled souborů: `HIGGS_empty.C` vs. `Higgs_full.C`

Cvičící na přednášce poskytl studentům skeletonový soubor `HIGGS_empty.C` a plnou referenční verzi `Higgs_full.C`.

* **`HIGGS_empty.C`:** Obsahuje hlavičky, načítání dat `GetMassDistribution`, kostru pro `MassPlot` a prázdné funkce se zakomentovanými částmi pro `Significance_Optimization`, `SideBandFit` a `GenerateToyDataSet`.
* **`Higgs_full.C`:** Kompletně implementovaný skript s plnými těly 6 procedur:
  1. `GetMassDistribution`: načítání a škálování spektra invariantní hmotnosti 4 leptonů.
  2. `MassPlot`: vykreslení složeného spektra (Signál + Pozadí + Data) se správným škálováním.
  3. `Significance_Optimization`: sken velikosti hmotnostního okna $\Delta m$ a hledání maxima signifikance pro nominální luminozitu i pro dvojnásobnou luminozitu ($L=2.0$).
  4. `SideBandFit`: určení normalizace pozadí z postranních pásem ($150 - 400\text{ GeV}$) pomocí binned Poisson likelihood a odhad systematické chyby z $\Delta(-2\ln L) = 1$.
  5. `GenerateToyDataSet`: Toy Monte Carlo pro modelování dopadu systematické chyby normalizace pozadí na očekávanou signifikanci.
  6. `Fit1DLikelihood` & `Fit2DLikelihood`: Jednorozměrný a dvourozměrný profilový fit věrohodnosti pro sílu signálu $\mu_{\text{sig}}$ a faktor pozadí $\alpha_{\text{bgr}}$.

---

## 3. Detailní rozbor kódu řádek po řádku

Pojďme nyní rozebrat jednotlivé bloky originálního C++ kódu `Higgs_full.C`.

### 3.1 Hlavičkové soubory a dopředné deklarace

```cpp
#include "TBox.h"
#include "TArrow.h"
#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TLine.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TROOT.h"
#include "TLatex.h"
#include "TFile.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "Math/QuantFuncMathCore.h"
#include "Math/ProbFuncMathCore.h" // for ROOT::Math::gaussian_cdf

#include <iostream>
using namespace std;
```

#### Co to znamená v Pythonu?
* `#include "TH1D.h"` je v C++ ekvivalent importu konkrétní třídy. V Pythonu by to odpovídalo `from ROOT import TH1D`. C++ preprocesor doslova vloží obsah hlavičkového souboru na toto místo.
* `<iostream>` je standardní C++ knihovna pro vstup a výstup (odpovídá `sys.stdout` nebo funkci `print`).
* `using namespace std;` říká kompilátoru, že funkce jako `cout`, `endl` nebo kontejnery `vector` pocházejí ze standardního jmenného prostoru `std`. Nemusíme pak psát `std::cout`.

#### Dopředné deklarace (Forward Declarations)
```cpp
void Fit1DLikelihood(int Irebin = 10);
void Fit2DLikelihood(int Irebin = 10);
TH1D * GetMassDistribution(int Itype = 1, double scalefactor = 1.00);
void MassPlot(int Irebin = 20);
void SideBandFit(int Irebin = 10);
double Get_TestStatistic(TH1D *h_mass_dataset, TH1D *h_template_bgr, TH1D *h_template_sig);
TH1D * GenerateToyDataSet(TH1D *h_mass_template, double alpha, double lower, double upper, double N_bgr);
double IntegratePoissonFromRight(double mu, int N_obs);
double IntegrateFromRight(TH1D * h_X_bgr, double X_value);
vector<double> Get_Quantiles( TH1D* hist );
void AddText( Double_t txt_x = 0.50, Double_t txt_y = 0.50, const char * txt = "dummy", ... );
```
* **Proč jsou v C++ nutné?** C++ kompilátor čte soubor shora dolů od prvního řádku. Pokud by funkce `MassPlot()` volala `GetMassDistribution()`, která by byla definována až níže, kompilátor by zahlásil chybu `identifier not found`. Dopředná deklarace kompilátoru oznámí: *"Tato funkce existuje, má takové parametry a vrací tento typ, její tělo najdeš později."*
* V Pythonu toto není potřeba, protože funkce se vyhodnocují až v době běhu (runtime).

---

### 3.2 Funkce `GetMassDistribution`: Načítání a škálování dat

```cpp
TH1D * GetMassDistribution(int Itype, double scalefactor){
  //-- [1] Get histogram from the file
  TH1D *h_mass = 0;
  TDirectory* dir = gDirectory;   
  TFile *file = new TFile("Histograms_fake.root", "READ");
  dir->cd();

  //-- Higgs 125
  if(Itype == 125){
    h_mass  = (TH1D*) file->Get("h_m4l_Higgs125_fake")->Clone("h_mass");     
  }
  //-- Higgs 200
  if(Itype == 200){
    h_mass  = (TH1D*) file->Get("h_m4l_Higgs200_fake")->Clone("h_mass");     
  }
  //-- ZZ SM background
  if(Itype == 1){
    h_mass  = (TH1D*) file->Get("h_m4l_ZZ_fake")->Clone("h_mass");     
  }
  //-- data
  if(Itype == 2){
    h_mass  = (TH1D*) file->Get("h_m4l_data_fake")->Clone("h_mass");     
  }
  
  //-- [2] scale histograms
  int Nbins = h_mass->GetNbinsX();
  for (int i_bin = 1; i_bin < Nbins; i_bin++){
    double mu_bin = h_mass->GetBinContent(i_bin);
    h_mass -> SetBinContent( i_bin, scalefactor * mu_bin);
  }

  //-- [3] return histogram   
  return h_mass;
}
```

#### Klíčové mechanismy:
1. `TDirectory* dir = gDirectory; ... dir->cd();`:
   Tento trik uloží ukazatel na aktuální pracovní adresář před otevřením souboru. Otevření `TFile` totiž změní globální `gDirectory` na onen soubor. Zavoláním `dir->cd()` se vrátíme do původního kontextu.
2. `Clone("h_mass")`:
   Klíčový krok pro zachování histogramu v operační paměti RAM. Bez `Clone()` by ukazatel směřoval na objekt vlastněný souborem `file`.
3. `for (int i_bin = 1; i_bin < Nbins; i_bin++)`:
   * Manuální for-cyklus pro škálování obsahu jednotlivých binů.
   * Všimněte si, že autor napsal `i_bin < Nbins` místo `i_bin <= Nbins` (vynechal poslední bin). V Python/ROOT můžeme jednoduše použít `h_mass.Scale(scalefactor)`.

---

### 3.3 Funkce `MassPlot`: Vykreslení spektra

```cpp
void MassPlot(int Irebin){
  gROOT->Clear();
  gROOT->Delete();

  TCanvas * canvas1 = new TCanvas("canvas1","Standard Canvas",600,400);  
  canvas1->SetLeftMargin(0.125);
  canvas1->SetBottomMargin(0.125); 
  canvas1->cd(); 

  TH1D *h_sig  = GetMassDistribution(125);
  TH1D *h_bgr  = GetMassDistribution(1);
  TH1D *h_data = GetMassDistribution(2);

  // Převzorkování binů (Rebinning)
  h_sig->Rebin(Irebin);
  h_bgr->Rebin(Irebin);
  h_data->Rebin(Irebin);

  // Vytvoření kumulativního histogramu Signál + Pozadí
  TH1D *h_sig_plus_bgr = (TH1D*) h_bgr->Clone("h_sig_plus_bgr");
  h_sig_plus_bgr->Reset();
  for (int i_bin = 1; i_bin < h_bgr->GetNbinsX(); i_bin++){
       h_sig_plus_bgr->SetBinContent(i_bin, h_sig->GetBinContent(i_bin) + h_bgr->GetBinContent(i_bin));
  }

  // Nastavení vizuálních stylů a kreslení
  double Data_max = h_data->GetBinContent(h_data->GetMaximumBin());
  double Ymax_plot = 1.10 * (Data_max + TMath::Sqrt(Data_max));
  h_sig_plus_bgr->SetFillColor(7); // tyrkysová (cyan)
  h_sig_plus_bgr->SetAxisRange(0., Ymax_plot, "Y");
  h_sig_plus_bgr->SetAxisRange(0., 400., "X");
  h_bgr->SetFillColor(2);          // červená

  h_sig_plus_bgr->Draw("hist");  
  h_bgr->Draw("same");  
  h_bgr->Draw("axis same");  
  h_data->Draw("e same");

  // Legenda a uložení
  TLegend *leg1 = new TLegend(0.65, 0.65, 0.90, 0.85);
  leg1->SetBorderSize(0); leg1->SetFillColor(0);
  leg1->AddEntry(h_bgr, " SM(ZZ)", "f");
  leg1->AddEntry(h_sig_plus_bgr, " Higgs", "f");
  leg1->Draw();

  canvas1->Print(Form("./MassPlot_rebin%d.gif", Irebin));
}
```

#### Klíčové mechanismy:
1. `Rebin(Irebin)`: Sdružuje sousední biny. Originální histogram má šířku binu $\sim 0.205\text{ GeV}$ ($3600$ binů od $60$ do $800\text{ GeV}$). Při `Irebin = 20` se biny rozšíří na $\sim 4.11\text{ GeV}$, což je vhodné pro vizualizaci s nízkou statistikou.
2. `Draw("same")` a `Draw("e same")`:
   * V ROOTu první volání `Draw()` vytvoří souřadný systém a osy.
   * Parametr `"same"` zabrání smazání plátna a nakreslí objekt přes předchozí.
   * Parametr `"e"` znamená vykreslení chybových úseček (Poisson error bars $\sqrt{N}$).
   * Parametr `"hist"` vykreslí histogram jako plnou křivku/plochu bez bodů.
3. Pořadí kreslení: Nejdříve se vykreslí celkový součet $S+B$ (tyrkysově), přes něj menší pozadí $B$ (červeně), a nakonec naměřená data s chybovými úsečkami (`"e same"`). Tím vzniká vrstvený sloupcový graf (stacked histogram).

---

### 3.4 Funkce `Significance_Optimization`: Hledání optimálního hmotnostního okna

Toto je jádro celé úlohy. Zkoumáme, jak závisí statistická signifikance objevu na šířce okna $\Delta m$ centrovaného kolem $125\text{ GeV}$.

```cpp
void Significance_Optimization(double Lumi_scalefactor = 1.00){
  TH1D *h_sig  = GetMassDistribution(125, Lumi_scalefactor);
  TH1D *h_bgr  = GetMassDistribution(1, Lumi_scalefactor);
  TH1D *h_data = GetMassDistribution(2, Lumi_scalefactor);

  // Definice histogramů jako kontejnerů pro závislost Z na Delta m
  TH1D *h_masswindow          = new TH1D("h_masswindow","",250,0.,25.);          
  TH1D *h_masswindow_expected = new TH1D("h_masswindow_expected","",250,0.,25.); 
  TH1D *h_masswindow_observed = new TH1D("h_masswindow_observed","",250,0.,25.); 

  for (int i_bin = 1; i_bin < h_masswindow->GetNbinsX(); i_bin++ ){
    double masswindow_fullwidth = h_masswindow->GetBinCenter(i_bin); 

    // [a] Spočítání počtu událostí v okně [125 - Delta m / 2, 125 + Delta m / 2]
    double Ndata_win = h_data->Integral(h_data->FindBin(125 - masswindow_fullwidth/2.),
                                        h_data->FindBin(125 + masswindow_fullwidth/2.));
    double Nbgr_win  = h_bgr->Integral(h_bgr->FindBin(125 - masswindow_fullwidth/2.),
                                       h_bgr->FindBin(125 + masswindow_fullwidth/2.));
    double Nsig_win  = h_sig->Integral(h_sig->FindBin(125 - masswindow_fullwidth/2.),
                                       h_sig->FindBin(125 + masswindow_fullwidth/2.));

    // [b] Očekávaná signifikance: pozorování S + B při hypotéze pozadí B
    double pvalue_expected = IntegratePoissonFromRight(Nbgr_win, Nbgr_win + Nsig_win);
    if (pvalue_expected == 0 || pvalue_expected == 1) 
        h_masswindow_expected->SetBinContent(i_bin, 0);
    else {
        double significance_expected = ROOT::Math::gaussian_quantile_c(pvalue_expected, 1);
        h_masswindow_expected->SetBinContent(i_bin, significance_expected);
    }

    // [c] Pozorovaná signifikance v reálných datech: pozorování N_data při hypotéze pozadí B
    double pvalue_observed = IntegratePoissonFromRight(Nbgr_win, Ndata_win);
    if (pvalue_observed == 0 || pvalue_observed == 1) 
        h_masswindow_observed->SetBinContent(i_bin, 0);
    else {
        double significance_observed = ROOT::Math::gaussian_quantile_c(pvalue_observed, 1);
        h_masswindow_observed->SetBinContent(i_bin, significance_observed);
    }
  }
}
```

#### Fyzikální a matematický význam:
1. **`FindBin(125 \pm \Delta m / 2)`:** Převádí fyzikální hodnotu hmotnosti v GeV na odpovídající celočíselný index binu.
2. **`Integral(bin_low, bin_high)`:** Sečte obsahy binů v daném intervalu. Protože pracujeme s jemně binnovaným histogramem ($205\text{ MeV}$ na bin), součet binů věrně odpovídá integrálu diferenciálního účinného průřezu.
3. **`IntegratePoissonFromRight(mu, N_obs)`:**
   Počítá pravděpodobnost (p-value), že při očekávaném pozadí $\mu = N_{\text{bgr}}$ nastane náhodnou statistickou fluktuací pozorování alespoň $N_{\text{obs}}$ událostí:
   $$p = P(n \ge N_{\text{obs}} \mid \mu) = \sum_{n = N_{\text{obs}}}^{\infty} \frac{\mu^n e^{-\mu}}{n!} = 1 - \sum_{n = 0}^{N_{\text{obs}} - 1} \frac{\mu^n e^{-\mu}}{n!}$$
4. **`ROOT::Math::gaussian_quantile_c(p, 1)`:**
   Převádí jednostrannou p-hodnotu na počet směrodatných odchylek normálního rozdělení (signifikanci $Z$):
   $$Z = \Phi^{-1}(1 - p)$$
   Kde $\Phi$ je distribuční funkce standardního normálního rozdělení $\mathcal{N}(0, 1)$. Například pro $p = 0.0227$ je $Z \approx 2.0\sigma$, pro $p = 1.35 \times 10^{-3}$ je $Z = 3.0\sigma$ (Evidence), pro $p = 2.87 \times 10^{-7}$ je $Z = 5.0\sigma$ (Discovery).
5. **Použití `TH1D` jako datového kontejneru:**
   V C++ ROOTu je velmi běžné použít histogram jako pole pro ukládání závislostí `y(x)`, protože se snadno vykreslí pomocí `Draw("l")` a má vestavěné metody jako `GetMaximumBin()` a `GetBinCenter()`. V Pythonu bychom pro tento účel použili NumPy pole (`np.array`) a Matplotlib.

---

### 3.5 Funkce `SideBandFit`: Kalibrace pozadí z postranních pásem

V experimentální praxi nemůžeme slepě věřit teoretické simulaci Monte Carlo pozadí. V signálové oblasti ($m_{4\ell} \approx 125\text{ GeV}$) může být přítomen nový signál, ale v oblasti vyšších hmotností ($150 - 400\text{ GeV}$) očekáváme čisté pozadí $ZZ$ Standardního modelu bez signálu (tzv. **Sideband**). Zde můžeme normalizaci pozadí přesně zkalibrovat.

```cpp
void SideBandFit(int Irebin){
  TH1D *h_bgr  = GetMassDistribution(1);
  TH1D *h_data = GetMassDistribution(2);
  h_bgr->Rebin(Irebin);
  h_data->Rebin(Irebin);

  TH1D *h_scalefactor_bgr = new TH1D("h_scalefactor_bgr","",100,0.1,10.); 

  // [2a] Skenování parametru škálování pozadí alpha
  for (int i_bin_sf = 1; i_bin_sf <= h_scalefactor_bgr->GetNbinsX(); i_bin_sf++){
    double scalefactor_bgr = h_scalefactor_bgr->GetBinCenter(i_bin_sf);
  
    // [2b] Výpočet binned Poisson log-věrohodnosti přes biny v rozsahu 150 až 400 GeV
    double loglik = 1e-10;
    for (int i_bin = h_data->FindBin(150); i_bin <= h_data->FindBin(400); i_bin++){
      loglik += TMath::Log(TMath::Poisson(h_data->GetBinContent(i_bin),
                                          scalefactor_bgr * h_bgr->GetBinContent(i_bin)));   	
    }

    h_scalefactor_bgr->SetBinContent(i_bin_sf, -2. * loglik);   
  }

  // [3] Hledání minima a 1-sigma intervalu podle Wilkova teorému
  TH1D *h_rescaled = (TH1D*) h_scalefactor_bgr->Clone("h_rescaled");  
  h_rescaled->Scale(-1); // obrácení pro použití FindFirstBinAbove

  double min_loglik = h_scalefactor_bgr->GetBinCenter(h_scalefactor_bgr->GetMinimumBin());
  double upper_error = h_rescaled->GetBinCenter(h_rescaled->FindFirstBinAbove(h_rescaled->GetMaximum() - 1));   
  double lower_error = h_rescaled->GetBinCenter(h_rescaled->FindLastBinAbove(h_rescaled->GetMaximum() - 1)); 

  printf("scalefactor = %f + %f - %f \n", min_loglik, upper_error - min_loglik, -lower_error + min_loglik);
}
```

#### Klíčové mechanismy a Wilksův teorém:
1. **Binned Poisson Likelihood:**
   V každém binu $i$ v postranním pásmu má model předpověď $\mu_i(\alpha) = \alpha \cdot N_{\text{bgr}, i}$. Pravděpodobnost pozorování $N_{\text{data}, i}$ událostí je:
   $$L(\alpha) = \prod_{i \in \text{sideband}} \frac{\mu_i^{N_i} e^{-\mu_i}}{N_i!}$$
   Logaritmováním a vynásobením $-2$:
   $$-2\ln L(\alpha) = -2 \sum_{i} \left[ N_i \ln(\alpha N_{\text{bgr}, i}) - \alpha N_{\text{bgr}, i} - \ln(N_i!) \right]$$
2. **Wilksův teorém a určení $1\sigma$ chyby:**
   Pro velké vzorky má testová statistika $\Delta(-2\ln L) = -2\ln L(\alpha) - \min(-2\ln L)$ asymptoticky rozdělení $\chi^2$ s jedním stupněm volnosti ($1\text{ d.o.f.}$).
   * Podmínka $\Delta(-2\ln L) \le 1.0$ vymezuje **$68.3\%$ interval spolehlivosti ($1\sigma$)**.
   * Podmínka $\Delta(-2\ln L) \le 4.0$ vymezuje **$95.4\%$ interval spolehlivosti ($2\sigma$)**.
3. **Trik s `Scale(-1)` a `FindFirstBinAbove`:**
   Místo numerického hledání kořenů autor otočil funkci vzhůru nohama (`Scale(-1)`), takže minimum se stalo maximem. Pak hledá biny, kde hodnota klesne o $1.0$ pod maximum (`GetMaximum() - 1`).

---

### 3.6 Funkce `GenerateToyDataSet`: Vliv systematické nejistoty na signifikanci

Pokud známe pozadí pouze s nejistotou $\sigma_\alpha \approx 0.06$ ($5.4\%$), nemůžeme již předpokládat, že parametr Poissonova rozdělení je fixní číslo. Počet událostí pozadí v signálovém okně má složené rozdělení (Poisson rozdělení, jehož střední hodnota $\mu$ sama náhodně fluktuuje podle Gaussova rozdělení).

```cpp
TH1D * GenerateToyDataSet(TH1D *h_mass_template, double alpha, double lower, double upper, double N_bgr){
  TRandom3 *R = new TRandom3(0); // 0 = náhodný seed z hodin počítače
  TH1D *h_poisson = new TH1D("h_poisson","",100,0,100);
 	
  for (int i = 0; i < 150000; i++){
    // Generování fluktuující střední hodnoty pozadí z Gaussova rozdělení
    double mu_fluctuated = R->Gaus(N_bgr, 0.06 * N_bgr);
    // Generování Poissonova počtu událostí pro danou fluktuovanou střední hodnotu
    double N_generated = R->PoissonD(mu_fluctuated);
    h_poisson->Fill(N_generated);  		
  }

  return h_poisson;
}
```

#### Fyzikální důsledek:
* Fluktuace střední hodnoty pozadí rozšíří chvost rozdělení (zvětší rozptyl: $\mathrm{Var}(N) = \mu + \sigma_\mu^2$).
* Zvýšená pravděpodobnost v chvostu distribuce zvyšuje p-hodnotu ($p$-value).
* Vyšší p-hodnota znamená **snížení signifikance objevu**. V našem případě klesá signifikance přibližně o $0.02\sigma$, což ukazuje, že kanál $4\ell$ je limitován spíše statistickou chybou než systematickou nejistotou pozadí.

---

### 3.7 Funkce `Fit1DLikelihood` a `Fit2DLikelihood`: Globální fit síly signálu $\mu$ a pozadí $\alpha$

Tyto funkce odpovídají modernímu přístupu standardně používanému v experimentech ATLAS a CMS: modelujeme spektrum pomocí dvou parametrů:
$$\mu_i(\alpha_{\text{bgr}}, \mu_{\text{sig}}) = \mu_{\text{sig}} \cdot N_{\text{sig}, i} + \alpha_{\text{bgr}} \cdot N_{\text{bgr}, i}$$
Kde $\mu_{\text{sig}}$ je **Signal Strength Modifier** ($\mu = 1$ je Standardní model, $\mu = 0$ je hypotéza pouze pozadí).

```cpp
void Fit2DLikelihood(int Irebin){
  TH1D *h_bgr  = GetMassDistribution(1);
  TH1D *h_data = GetMassDistribution(2);
  TH1D *h_sig  = GetMassDistribution(125, 1);
  h_bgr->Rebin(Irebin); h_data->Rebin(Irebin); h_sig->Rebin(Irebin);

  TH2D *h_scalefactor = new TH2D("h_scalefactor","",200,0.1,3.01,200,0.1,3.01);

  // 2D grid sken přes mřížku parametrů
  for(int i_bin_sm = 1; i_bin_sm <= h_scalefactor->GetNbinsX(); i_bin_sm++){ 
    for (int i_bin_higgs = 1; i_bin_higgs <= h_scalefactor->GetNbinsY(); i_bin_higgs++){ 
      double scalefactor_bgr = h_scalefactor->GetXaxis()->GetBinCenter(i_bin_sm);
      double scalefactor_sig = h_scalefactor->GetYaxis()->GetBinCenter(i_bin_higgs);

      double loglik = 1e-10;
      for (int i_bin = 1; i_bin <= h_data->GetNbinsX(); i_bin++){
        loglik += TMath::Log(TMath::PoissonI(h_data->GetBinContent(i_bin),
                  scalefactor_sig * h_sig->GetBinContent(i_bin) + 
                  scalefactor_bgr * h_bgr->GetBinContent(i_bin)));   	
      }

      h_scalefactor->SetBinContent(i_bin_sm, i_bin_higgs, -2. * loglik);   
    }
  }

  // Nalezení globálního minima v 2D mřížce
  int minimumSFbin, minimumAlphabin, dummy_z;
  h_scalefactor->GetBinXYZ(h_scalefactor->GetMinimumBin(), minimumSFbin, minimumAlphabin, dummy_z);

  // 1D řezy (projekce) pro extrakci individuálních chyb
  TH1D *h_projX = h_scalefactor->ProjectionX("", minimumAlphabin, minimumAlphabin);
  TH1D *h_projY = h_scalefactor->ProjectionY("", minimumSFbin, minimumSFbin);
}
```

#### Klíčové mechanismy:
1. `TH2D`: Dvourozměrný histogram pro uložení hodnoty věrohodnosti $-2\ln L$ na rovině $(\alpha_{\text{bgr}}, \mu_{\text{sig}})$.
2. `GetBinXYZ(global_bin, binX, binY, binZ)`: Převádí globální 1D index binu v ROOTu zpět na diskrétní souřadnice $(x, y)$.
3. `ProjectionX` a `ProjectionY`: Vytváří jednorozměrné řezy podél souřadnic minima. V naší Python implementaci jsme toto povýšili na vykreslení skutečných **2D vrstevnic (contour plot)** pro hladiny $\Delta(-2\ln L) \in \{2.30, 6.18\}$ ($68\%$ a $95\%$ CL pro 2 parametry).

---

### 3.8 Pomocné statistické funkce

```cpp
// 1. Integrál Poissonova rozdělení zprava (p-hodnota)
double IntegratePoissonFromRight(double mu, int N_obs){
  double integral = 1.; 
  for(int i_obs = 0; i_obs < N_obs; i_obs++){
    integral -= TMath::Poisson(i_obs, mu);
  }
  return integral;
}

// 2. Integrál empirického histogramu zprava
double IntegrateFromRight(TH1D * h_X_bgr, double X_value){
  int Nbins = h_X_bgr->GetNbinsX();
  int X_bin = h_X_bgr->FindBin(X_value); 
  return h_X_bgr->Integral(X_bin, Nbins) / h_X_bgr->Integral();
}

// 3. Výpočet mediánu a 1-sigma / 2-sigma kvantilů z rozdělení
vector<double> Get_Quantiles(TH1D* hist){
  double fraction_1sigma = ROOT::Math::gaussian_cdf(-1., 1., 0.); // ~ 15.87%
  double fraction_2sigma = ROOT::Math::gaussian_cdf(-2., 1., 0.); // ~ 2.28%
  double probs[5] = {fraction_2sigma, fraction_1sigma, 0.50, 1.00 - fraction_1sigma, 1.00 - fraction_2sigma};

  double Xvalues[5];
  hist->GetQuantiles(5, Xvalues, probs);
  
  vector<double> Xvalues_output(5);
  for (int i = 0; i < 5; i++) Xvalues_output[i] = Xvalues[i];
  return Xvalues_output;
}
```

---

## 4. Rosetta Stone: Srovnání C++ ROOT vs. Python / PyROOT / SciPy

Následující tabulka nabízí přímý překlad nejčastějších C++ ROOT konstrukcí do moderního Pythonu:

| Úkon | Původní C++ ROOT | PyROOT v Pythonu | Čistý Python / NumPy / SciPy |
| :--- | :--- | :--- | :--- |
| **Otevření souboru** | `TFile *f = new TFile("f.root", "READ");` | `f = ROOT.TFile.Open("f.root")` | `uproot.open("f.root")` |
| **Načtení histogramu**| `(TH1D*) f->Get("h")->Clone("h_copy");` | `h = f.Get("h").Clone()` | `counts, edges = hist[...]` |
| **Škálování histogramu** | `h->SetBinContent(i, scale * val);` | `h.Scale(scale)` | `y_scaled = y * scale` |
| **Počet binů** | `h->GetNbinsX()` | `h.GetNbinsX()` | `len(counts)` |
| **Index binu pro $x$**| `h->FindBin(125.0)` | `h.FindBin(125.0)` | `np.digitize(125.0, edges)` |
| **Integrál v intervalu** | `h->Integral(bin_a, bin_b)` | `h.Integral(bin_a, bin_b)` | `np.sum(counts[idx_a:idx_b])` |
| **Poissonova pravděpodobnost** | `TMath::Poisson(k, mu)` | `ROOT.TMath.Poisson(k, mu)` | `scipy.stats.poisson.pmf(k, mu)` |
| **Gaussovský kvantil (Z)** | `ROOT::Math::gaussian_quantile_c(p, 1)` | `ROOT.Math.gaussian_quantile_c(p, 1)` | `scipy.stats.norm.isf(p)` |
| **Gaussovská CDF** | `ROOT::Math::gaussian_cdf(x, sigma, mean)` | `ROOT.Math.gaussian_cdf(x, sigma, mean)` | `scipy.stats.norm.cdf(x, mean, sigma)` |
| **Generování náhodných čísel** | `TRandom3 R(0); R.Gaus(m, s);` | `R = ROOT.TRandom3(0); R.Gaus(m, s)` | `np.random.normal(m, s, size)` |
| **Vykreslení grafu** | `TCanvas c; h->Draw("hist");` | `c = ROOT.TCanvas(); h.Draw("hist")` | `fig, ax = plt.subplots(); ax.hist(...)` |

---

## 5. Shrnutí vztahu C++ makra a Jupyter Notebooku

1. **Shoda metodiky (1:1):**
   Všechny výpočty obsažené v `source/Higgs.ipynb` přesně kopírují a rozšiřují logiku z `Higgs_full.C`. Zahrnují:
   * Sken hmotnostního okna a nalezení optimální šířky $\Delta m \approx 7.15\text{ GeV}$ s očekávanou signifikancí $Z_{\text{exp}} = 2.04\sigma$.
   * Škálování luminozity $L=2.0$ a ověření teoretického nárůstu signifikance o faktor $\sqrt{2}$.
   * Sideband fit faktoru pozadí v rozmezí $150 - 400\text{ GeV}$ s výsledkem $\hat{\alpha}_{\text{bgr}} = 1.120 \pm 0.060$.
   * Modelování systematické chyby normalizace pomocí Toy Monte Carlo.
   * Extrakci síly signálu $\mu$ a 2D kontury věrohodnosti.

2. **Vylepšení v Pythonu:**
   * Kód byl rozčleněn do přehledných kroků doplněných podrobným fyzikálním a teoretickým výkladem v češtině.
   * Grafy jsou generovány dvojmo: jednak přímo v interaktivním **CERN ROOTu** s upraveným publikačním stylem (font 42 Helvetica, bez rušivých horních titulků a stat boxů), a jednak v **Matplotlibu** ve vysokém rozlišení s anglickými popisky.

