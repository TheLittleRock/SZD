#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include <TFile.h>
#include  "RooAddPdf.h"
#include "RooExponential.h"
#include "RooFitResult.h"
#include "RooMinimizer.h"
using namespace RooFit ;


// =============================================
// How to run this:
// root -l 'Mass_fit.cpp(1)'	// with 1 being number for i
// =============================================

void JpsiMass_fit_v1()
{
    TFile *inputFile = TFile::Open("jpsi_single_mass.root");
    TTree *tree = ((TTree *)inputFile->Get("tree"));

    RooRealVar x("JpsiMass","J/#psi mass",2100.,4200.) ; //sem přijdou pak někdy data

    RooDataSet *data = new RooDataSet("data","data",RooArgSet(x),Import(*tree)) ;

    RooRealVar mean1("mean1","mean of gaussian1",3100,3040,3150.) ;
    RooRealVar sigma1("sigma1","width of gaussian1", 100.,10.,300.) ;
    RooGaussian gauss1("gauss1","signal2", x,mean1,sigma1) ;

    RooRealVar mean2("mean2","mean of gaussian2",3600,3540,3950.) ;
    RooRealVar sigma2("sigma2","width of gaussian2", 100.,10.,400.) ;    
    RooGaussian gauss2("gauss2","signal2", x,mean2,sigma2) ;
    
    RooRealVar tau("tau", "tau", -0.001, -0.01, 0.0);
    RooExponential bck("bck", "background", x, tau);

    RooRealVar fraction1("fraction1", "fraction1", 0.1, 0.0, 1.0);
    RooRealVar fraction2("fraction2", "fraction2", 0.1, 0.0, 1.0);

    RooAbsPdf *TotalPDF = new RooAddPdf("TotalPDF", "TotalPDF", RooArgList(gauss1,gauss2, bck), RooArgList(fraction1, fraction2));
        
    RooFitResult *fr = TotalPDF->fitTo(*data,Save(true));
    
    RooPlot* xframe = x.frame(Title("Gaussian p.d.f.")) ;
    data->plotOn(xframe,Binning(50)) ;
    TotalPDF->plotOn(xframe,VisualizeError(*fr),Name("Errors"),FillColor(kOrange)) ;
    TotalPDF->plotOn(xframe,Components(RooArgSet(gauss1,gauss2)),VisualizeError(*fr),Name("Errors"),FillColor(kGreen)) ;
    TotalPDF->plotOn(xframe,LineColor(kRed),Name("Fit result")) ;
    TotalPDF->plotOn(xframe,Components(bck),LineStyle(kDashed),LineColor(kBlue-1)) ;
    TotalPDF->plotOn(xframe,Components(RooArgSet(gauss1,gauss2)),LineStyle(kDashed),LineColor(kGreen+1)) ;
    
    TotalPDF->paramOn(xframe);
    TotalPDF->Print("t");
    xframe->Draw() ;
}

void JpsiMass_fit_v2()
{
    TFile *inputFile = TFile::Open("jpsi_single_mass.root");
    TTree *tree = ((TTree *)inputFile->Get("tree"));

    RooRealVar x("JpsiMass","J/#psi mass",2100.,4200.) ; //sem přijdou pak někdy data

    RooDataSet *data = new RooDataSet("data","data",RooArgSet(x),Import(*tree)) ;

    RooRealVar mean1("mean1","mean of gaussian1",3100,3040,3150.) ;
    RooRealVar sigma1("sigma1","width of gaussian1", 100.,10.,300.) ;
    RooGaussian gauss1("gauss1","signal2", x,mean1,sigma1) ;

    RooRealVar mean2("mean2","mean of gaussian2",3600,3540,3950.) ;
    RooRealVar sigma2("sigma2","width of gaussian2", 100.,10.,400.) ;    
    RooGaussian gauss2("gauss2","signal2", x,mean2,sigma2) ;
    
    RooRealVar tau("tau", "tau", -0.001, -0.01, 0.0);
    RooExponential bck("bck", "background", x, tau);

    RooRealVar N1("N1", "N1", 1000, 0.0, 10000);
    RooRealVar N2("N2", "N2", 1000, 0.0, 10000);
    RooRealVar N3("N3", "N3", 1000, 0.0, 100000);

    RooAbsPdf *TotalPDF = new RooAddPdf("TotalPDF", "TotalPDF", RooArgList(gauss1,gauss2, bck), RooArgList(N1, N2, N3));
        
//    RooFitResult *fr = TotalPDF->fitTo(*data,Extended(),Save(true));
    RooFitResult *fr = TotalPDF->fitTo(*data,Save(true));
    
    RooPlot* xframe = x.frame(Title("Gaussian p.d.f.")) ;
    data->plotOn(xframe,Binning(50)) ;
    TotalPDF->plotOn(xframe,VisualizeError(*fr),Name("Errors"),FillColor(kOrange)) ;
    TotalPDF->plotOn(xframe,Components(RooArgSet(gauss1,gauss2)),VisualizeError(*fr),Name("Errors"),FillColor(kGreen)) ;
    TotalPDF->plotOn(xframe,LineColor(kRed),Name("Fit result")) ;
    TotalPDF->plotOn(xframe,Components(bck),LineStyle(kDashed),LineColor(kBlue-1)) ;
    TotalPDF->plotOn(xframe,Components(RooArgSet(gauss1,gauss2)),LineStyle(kDashed),LineColor(kGreen+1)) ;
    
    TotalPDF->paramOn(xframe);
    TotalPDF->Print("t");
    xframe->Draw() ;
}

void JpsiMass_fit_v3()
{
    TFile *inputFile = TFile::Open("jpsi_single_mass.root");
    TTree *tree = ((TTree *)inputFile->Get("tree"));

    RooRealVar x("JpsiMass","J/#psi mass",2100.,4200.) ; //sem přijdou pak někdy data

    RooDataSet *data = new RooDataSet("data","data",RooArgSet(x),Import(*tree)) ;

    RooRealVar mean1("mean1","mean of gaussian1",3100,3040,3150.) ;
    RooRealVar sigma1("sigma1","width of gaussian1", 100.,10.,300.) ;
    RooGaussian gauss1("gauss1","signal2", x,mean1,sigma1) ;

    RooRealVar mean2("mean2","mean of gaussian2",3600,3540,3950.) ;
    RooRealVar sigma2("sigma2","width of gaussian2", 100.,10.,400.) ;    
    RooGaussian gauss2("gauss2","signal2", x,mean2,sigma2) ;
    
    RooRealVar tau("tau", "tau", -0.001, -0.01, 0.0);
    RooExponential bck("bck", "background", x, tau);

    RooRealVar N1("N1", "N1", 1000, 0.0, 10000);
    RooRealVar N2("N2", "N2", 1000, 0.0, 10000);
    RooRealVar N3("N3", "N3", 1000, 0.0, 100000);

    RooAbsPdf *TotalPDF = new RooAddPdf("TotalPDF", "TotalPDF", RooArgList(gauss1,gauss2, bck), RooArgList(N1, N2,N3));
        

    // Construct function object representing –log(L)
    RooAbsReal* nll = TotalPDF->createNLL(*data) ;
    // Minimize nll w.r.t its parameters
    RooMinimizer m(*nll) ;
    m.minimize("Minuit2", "Migrad");
    m.hesse() ;
    m.minos(sigma2) ;

    //RooFitResult *fr = TotalPDF->fitTo(*data,Extended(),Save(true));
    
    RooPlot* xframe = x.frame(Title("Gaussian p.d.f.")) ;
    data->plotOn(xframe,Binning(50)) ;
    TotalPDF->plotOn(xframe,LineColor(kRed),Name("Fit result")) ;
    TotalPDF->plotOn(xframe,Components(bck),LineStyle(kDashed),LineColor(kBlue-1)) ;
    TotalPDF->plotOn(xframe,Components(RooArgSet(gauss1,gauss2)),LineStyle(kDashed),LineColor(kGreen+1)) ;
    
    TotalPDF->paramOn(xframe);
    TotalPDF->Print("t");

    TCanvas *mass_plot =  new TCanvas("mass_plot","J/#psi and #psi(2S) mass",1200,800) ;
    TCanvas *contour =  new TCanvas("contour","#sigma_2 and #tau contour",800,800) ;
//    TCanvas *profile =  new TCanvas("profile","#sigma_2 L scan and profile",1200,800) ;

    mass_plot->cd();
    xframe->Draw() ;

    contour->cd();
    RooPlot* frameContour = m.contour(sigma2,tau,1,2,3) ;
    frameContour->SetTitle("RooMinuit contour plot") ;
    frameContour->SetMinimum(-0.0011);
    frameContour->SetMaximum(-0.0009);
    frameContour->Draw();

//    profile->cd();
//    RooPlot* profilePlot = sigma2.frame(Title("#sigma_2 likelihood scan and profile likelihood")) ;    
//    nll->plotOn(profilePlot,ShiftToZero()) ;
    
//    RooAbsReal* pll = nll->createProfile(sigma2) ;
//    pll->plotOn(profilePlot,LineColor(kRed)) ;
//    profilePlot->SetMinimum(0) ;
//    profilePlot->SetMaximum(3) ;
//    profilePlot->Draw();


}


void Mass_fit(int i = 1)
{
  if( i==1 ) JpsiMass_fit_v1();
  if( i==2 ) JpsiMass_fit_v2();
  if( i==3 ) JpsiMass_fit_v3();
}



