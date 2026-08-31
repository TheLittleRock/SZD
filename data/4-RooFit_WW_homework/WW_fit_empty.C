#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "TROOT.h"
#include "TCanvas.h"
#include "TH1.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooGaussModel.h"
#include "RooConstVar.h"
#include "RooProdPdf.h"
#include "RooHistPdf.h"
#include "RooUniform.h"
#include "RooCategory.h"
#include "RooAddPdf.h"
#include "RooPlot.h"
#include "TCanvas.h"

//#include <stdio.h>
#include <iostream>

using namespace RooFit;
using namespace std;




void WW_fit(const int &nEvents = 14000){
//	jde o fitovani jedine promenne zvane "etaeta" = soucin dvou pseudorapidit, to neni podstatne
//	we deal with one variable "etaeta" = product of two muon rapidities;

//	nactu data / load data
//	signal - 2 models
	TFile fin1("data_WWsignal_data.root");
	TH1D* h_Sdata = (TH1D*)fin1.Get("LepPair_etaprod");
	TFile fin11("data_WWsignal_model.root");
	TH1D* h_Smodel = (TH1D*)fin11.Get("LepPair_etaprod");
// 	pozadi/background processes - WZ, ttbar
	TFile fin2("data_ttbarbkg.root");
	TH1D* h_top = (TH1D*)fin2.Get("LepPair_etaprod");

	TFile fin3("data_WZbkg.root");
	TH1D* h_wz = (TH1D*)fin3.Get("LepPair_etaprod");
	h_wz->Scale(1.766/1.315);	//a scale factor, ignore that

// 	vystup budu ukladat do histogramu - protoze me zajima statisticka chyba fitu
//	tj. pojedu loop pres fluktuace dat

//	we perform a fit and store the output number to histogram - 
//	then repeat the fit with another random data -> get distribution

        TFile *MyFile = new TFile("WW_fit_output_14k_10Kopak.root","RECREATE");

//	normalizace:
//	jeden z modelu (WWsignal_data) budu brat jako data a druhy (WWsignal_model) jako model, ktery na data fituju
//	u "dat" beru pomer signal ku bkg takovy jaky je na vstupu, u "MC" tento pomer zjistuju

//	we have 2 datasets for signal: h_Sdata is real data, h_Smodel we fit on data
//	data we mix as it is; MC we want to fit fraction of signal vs background

        Double_t n_WW_Sdata = h_Sdata->Integral("width");
        Double_t n_WW_Smodel = h_Smodel->Integral("width");
        Double_t n_WZ = h_wz->Integral("width");
        Double_t n_top = h_top->Integral("width");

//   printf ("HERE Integral %1.5f    %1.5f     %1.5f \n", n_WW_Sdata ,n_WZ, n_top );

        Double_t n_sum_Sdata = n_WW_Sdata + n_WZ + n_top;

    	RooRealVar etaeta("etaeta", "etaeta", -6., 6.);

//	celkova normalizace me neza, chci jen pomer
//	we get ratios from number of events
    	RooRealVar f_WW_Sdata("f_WW_Sdata", "f_WW_Sdata", (n_WW_Sdata/n_sum_Sdata) );
    	RooRealVar f_WZ_Sdata("f_WZ_Sdata", "f_WZ_Sdata", (n_WZ/n_sum_Sdata) );
//we will not need this:    	RooRealVar f_top_min("f_top_min", "f_top_min", (n_top/n_sum_Sdata) );

//   printf ("HERE f %1.5f    %1.5f \n", f_WW_Sdata.getValV(), (n_WW_Sdata/n_sum_Sdata));

// ================ ODTUD SAMI ==============

//	pomocne distribuce ktere pak sectu v pomeru ktery jsem zjistil
// 	first prepare pdf's using the fractions we know

//	i.e. do for each datset:
//	TH1D to RooDataHist 
//	RooDataHist to RooHistPdf
//	declare two fractions: one for WW signal (Smodel), second for WZ background (ttbar bck will be 1-f_WW-f_WZ )
//	combine them to prepare pdf for data and for MC: RooAddPdf

// CODE HERE

//	proc to delam pres pomery a nescitam proste ty puvodni histogramy?
//	protoze RooHistPdf jsou PDFka - tj. fce normovany na 1 !!!
//	why not to use original histograms directly in sum? - pdf's are normalized to 1  

    TH1F histFww("histFww","histFww", 50, 0., 0.3);
    TH1F histFwz("histFwz","histFwz", 50, 0.3, 0.5);

//	tohle je ten loop na zjisteni chyby - s jinymi daty ziskam jiny pomer - a to vse si reguluju promennou nEvents
//	ktera je dana luminositou - to si predpocitam a zde je to konstanta

//	this is the loop to estimate variance of the fit - different data gives different fractions
//	nEvents is a constant here, given by the cross section and expected luminosity

//	10k of repeats is arbitrary, may choose larger ...
    for (int i = 0; i < 10000; i++) {


//	nageneruj nova data
//	generate random data
        RooDataSet* data = 	// generujte nEvents eventu

//	fit your model to data


        histFww.Fill( 
        histFwz.Fill( 




    }




        RooDataHist fHist("fHist", "fHist", RooArgList(f_fit_WW_Smodel), &histFww);

    
    	RooRealVar g_mean("g_mean", "Mean of Gaussian", 0.01, 0.0, 0.4);
    	RooRealVar g_sigma("g_sigma", "Width of Gaussian", 0.05, 0.0, 0.5);
  	RooGaussian g("g", "Gaussian Fit", f_fit_WW_Smodel, g_mean, g_sigma);

	TCanvas c1("c1","c1", 800, 600);

	RooPlot *fframe = f_fit_WW_Smodel.frame();
	fHist.plotOn(fframe, LineColor(kBlue), LineStyle(kSolid) );
	RooFitResult* fitResult = g.fitTo(fHist, RooFit::Save());
	g.plotOn(fframe); 
  	g.paramOn(fframe);
	fframe->Draw();
	
    	TLatex latex;
    	latex.SetTextSize(0.04);
    	latex.SetNDC();  // Use normalized coordinates (0 to 1)
    	latex.DrawLatex(0.5, 0.5, Form("frac of signal = %.3f #pm %.3f", g_mean.getVal(), g_sigma.getVal()));	
	
    	c1.SaveAs("Fww.pdf");




  MyFile->Write();
  MyFile->Close();







}

