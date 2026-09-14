#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooGaussModel.h"
#include "RooPolynomial.h"
#include "RooConstVar.h"
#include "RooLandau.h"
#include "RooProdPdf.h"
#include "RooHistPdf.h"
#include "RooCategory.h"
#include "RooAddPdf.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TH1.h"

using namespace RooFit ;
using namespace std;

// Macros to ilustrate arXiv:physics/0401045 [physics.data-an]

// to run this:
//
//	root 'punzi_landau.C(1)'


void punzi_landau(const int &fittype, const TString &file = "out.png") {
  
    RooRealVar x("x", "x", -10., 15.);
    RooRealVar xErr("xErr", "xErr", .1, 10.);
  
    RooGaussModel genGauss("genGauss", "genGauss", x, RooConst(2.), xErr, RooConst(1.), RooConst(1.));
//    RooGaussian genGauss("genGauss", "genGauss", x, RooConst(2.), xErr);
  
    RooLandau genLandauSig("genLSig", "genLSig", xErr, RooConst(1.), RooConst(.2));  
  
    RooDataHist* histXErrSig = genLandauSig.generate(xErr, 10000)->binnedClone();  
  
    RooHistPdf pdfXErrSig("pdfXErrSig", "pdfXErrSig", xErr, *histXErrSig);  
  
    RooProdPdf genModelSig("genModelSig", "genModelSig", pdfXErrSig, Conditional(genGauss, x));  
  
    RooDataSet* dataSig = genModelSig.generate(RooArgSet(x, xErr), 10000);  
  


//    (dataSig->createHistogram(x,xErr))->Draw("colz")  ;
  
  
    RooLandau genLandauBck("genLandauBck", "genLandauBck", xErr, RooConst(2.), RooConst(.6));
    RooDataHist* histXErrBck = genLandauBck.generate(xErr, 10000)->binnedClone();
    RooHistPdf pdfXErrBck("pdfXErrBck", "pdfXErrBck", xErr, *histXErrBck);
 
    RooPolynomial genPol("genPol", "genPol", x, RooConst(-0.03));
    RooProdPdf genModelBck("genModelBck", "genModelBck", pdfXErrBck, Conditional(genPol, x));
    
    RooDataSet* dataBck = genModelBck.generate(RooArgSet(x, xErr), 30000);

    RooCategory type("type", "type");
    type.defineType("signal");
    type.defineType("background");

    RooDataSet* data = new RooDataSet("data", "data", RooArgSet(x, xErr), Index(type), Import("signal", *dataSig), Import("background", *dataBck));  
  
  

//===================================================================================

  if(fittype == 1){
  
  // SINGLE GAUSS FIT
  
    RooRealVar mean("mean", "mean", 0., -10., 10.);
    RooRealVar sf("sf", "sf", 1., .5, 5.);  
    RooGaussModel sig("gauss", "gauss", x, mean, xErr, RooConst(1.), sf);  
  
  	// bck: linear with unknown slope cF
    RooRealVar c("c", "c", -1., 1.);
    RooPolynomial bck("pol", "pol", x, c);  
  
    RooRealVar frac("frac", "frac", 0., 1.);  
  
    RooAddPdf model("model", "model", RooArgSet(sig, bck), frac);  
  
    RooPlot* fX = x.frame(Title("Fit of x")); 
     
    model.fitTo(*data);
//	will this improve it??
//  model.fitTo(*data, ConditionalObservables(xErr));
    data->plotOn(fX);
    model.paramOn(fX, Layout(.54, .99, .92));
    model.plotOn(fX);
    model.plotOn(fX, ProjWData(*data), LineColor(kRed));   
    fX->Draw();    
   
  }
  
//===================================================================================


  if(fittype == 2){ 
  
    // DOUBLE GAUSS FIT
    //===============================
   
    RooRealVar mean("mean", "mean", 0., -10., 10.);
    RooRealVar sigma1("s1", "s1", 1., 1., 10.);
    RooRealVar sigma2("s2", "s2", 5., 1., 10.);
    
    RooRealVar fracSigF("fracSigF", "fracSigF", .2, 0., 1.);	// ratio 1 to 2 gauss    
    
    RooGaussian sigF1("sigF1", "sigF1", x, mean, sigma1);
    RooGaussian sigF2("sigF2", "sigF2", x, mean, sigma2);

    RooAddPdf sigF("sigF", "sigF", RooArgSet(sigF1, sigF2), fracSigF);	        

  	// bck: linear with unknown slope cF
    RooRealVar c("c", "c", -1., 1.);
    RooPolynomial bck("bck", "bck", x, c);

    RooRealVar frac("frac", "frac", 0., 1.);

    RooAddPdf model("model", "model", RooArgSet(sigF, bck), frac);  
    
    RooPlot* fX = x.frame(Title("Double Gauss")); 
     
    model.fitTo(*data);
    data->plotOn(fX);
    model.paramOn(fX, Layout(.54, .99, .92));
    model.plotOn(fX, Components(bck), LineColor(kBlue));    
    model.plotOn(fX, Components(sigF), LineColor(kGreen));   
    model.plotOn(fX, LineColor(kRed));   
    fX->Draw();      
 

  }
    
//===================================================================================

  if(fittype == 3){

//	PUNZI - finally!


	// parametry Landaua pro signal
    RooRealVar aSig("aSig", "aSig", .1, 5.);
    RooRealVar bSig("bSig", "bSig", .1, 5.);

	// parametry Landaua pro background
    RooRealVar aBck("aBck", "aBck", .1, 5.);
    RooRealVar bBck("bBck", "bBck", .1, 5.);


    RooRealVar frac("frac", "frac", 0., 1.);


    RooLandau lanSig("lanSig", "lanSig", xErr, aSig, bSig);
    RooLandau lanBck("lanBck", "lanBck", xErr, aBck, bBck);
    RooLandau lanSB("lanSB"  , "lanSB",  xErr, aBck, bBck);	// SideBands
    
    RooAddPdf punziLandau("punziLandau", "punziLandau", RooArgSet(lanSig, lanBck), frac);

    RooDataSet* dataSB = (RooDataSet*)data->reduce("x < -2. || x > 10");		

	//now we fit the params of Landau for Background
    lanSB.fitTo(*dataSB);

    aBck.setConstant();
    bBck.setConstant();
    
     	//now we fit the remaining data(errors) - both signal and bkg.; params for bkg is fixed;
    punziLandau.fitTo(*data);

    aSig.setConstant();
    bSig.setConstant();    
    
    
    
    RooRealVar mean("mean", "mean", 0., -10., 10.);
    RooRealVar sf("sf", "sf", 1., .5, 5.);
    RooGaussModel gauss("gauss", "gauss", x, mean, xErr, RooConst(1.), sf);
    
    RooProdPdf sig("sig", "sig", lanSig, Conditional(gauss, x));
//	TRY IT without the "Conditional"
//    RooProdPdf sig("sig", "sig", lanSig, gauss);
    
    RooRealVar c("c", "c", -1., 1.);
    RooPolynomial pol("pol", "pol", x, c);
    
    RooProdPdf bck("bck", "bck", lanBck, Conditional(pol, x));
//	TRY IT without the "Conditional"
//    RooProdPdf bck("bck", "bck", lanBck, pol));
    
    RooAddPdf model("model", "model", RooArgSet(sig, bck), frac);
    
    RooPlot* fX = x.frame(Title("Punzi fit")); 

    model.fitTo(*data);
    data->plotOn(fX);
    model.paramOn(fX, Layout(.54, .99, .92));


    model.plotOn(fX, Components(bck), LineColor(kBlue));    
    model.plotOn(fX, Components(sig), LineColor(kGreen));   
    model.plotOn(fX, LineColor(kRed));  

//TODO: what ProjWData does??
//    model.plotOn(fX);
//    model.plotOn(fX, ProjWData(*data), LineColor(kRed));

    
     
    
    
    fX->Draw();



  }
    
    
    
    

    
    
  
  
  
  
  
//  TCanvas canvas1("canvas1","canvas1", 600, 400);

//  if ( ! file.IsNull() ) canvas1.SaveAs(file);   
  
}  
