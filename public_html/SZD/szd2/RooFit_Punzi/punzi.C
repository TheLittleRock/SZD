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

using namespace RooFit;
using namespace std;

// Macros to ilustrate arXiv:physics/0401045 [physics.data-an]

RooDataSet* generate1(const int &nEvents = 150) {
    // Generate data: 1/3 * Gauss(0,1) + 2/3 * Gauss(1,1)
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar f("f", "f", 1./3.);
    RooGaussian gaussA("gaussA", "gaussA", x, RooConst(0.), RooConst(1.));
    RooGaussian gaussB("gaussB", "gaussB", x, RooConst(1.), RooConst(1.));
    RooAddPdf model("model", "model", RooArgList(gaussA, gaussB), f);
    RooDataSet* data = model.generate(x, nEvents);
    return data;
}

RooDataSet* generate2(const int &nEvents = 150) {
    // Generate data: 1/3 * Gauss(0,sigma(variable, better)) + 2/3 * Gauss(1,sigma(variable, worse))
    // Could be 1/3 * signal (better resolution) + 2/3 * background (worse resolution)
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar xErr("xErr", "xErr", .1, 10.);
    RooRealVar f("f", "f", 1./3.);

    xErr.setRange(1., 2.);
    RooUniform xErrA("xErrA", "xErrA", xErr); // Uniform distribution (1., 2.)
    RooHistPdf pdfXErrA("pdfXErrA", "pdfXErrA", xErr, *(xErrA.generate(xErr, f.getVal() * nEvents)->binnedClone())); // PDF from generated histogram

    RooGaussModel gaussA("gaussA", "gaussA scaled by per-event error", x, RooConst(0.), xErr, RooConst(1.), RooConst(1.));
    RooProdPdf modelA("modelA", "modelA", pdfXErrA, Conditional(gaussA, x));
    RooDataSet* dataA = modelA.generate(RooArgSet(x, xErr), f.getVal() * nEvents);

    xErr.setRange(1.5, 3.);
    RooUniform xErrB("xErrB", "xErrB", xErr); // Uniform distribution (1.5, 3.)
    RooHistPdf pdfXErrB("pdfXErrB", "pdfXErrB", xErr, *(xErrB.generate(xErr, nEvents - f.getVal() * nEvents)->binnedClone())); // PDF from generated histogram

    // PICK ONE; difference???
//    RooGaussian gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr);
    RooGaussModel gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr, RooConst(1.), RooConst(1.));

    RooProdPdf modelB("modelB", "modelB", pdfXErrB, Conditional(gaussB, x));
    RooDataSet* dataB = modelB.generate(RooArgSet(x, xErr), nEvents - f.getVal() * nEvents);

    RooCategory type("type", "type");
    type.defineType("A");
    type.defineType("B");

    xErr.setRange(.1, 10.);
    RooDataSet* data = new RooDataSet("data", "data", RooArgSet(x, xErr), Index(type), Import("A", *dataA), Import("B", *dataB)); // Data = 1/3 * DataA + 2/3 * DataB

    delete dataA;
    delete dataB;
    return data;
}


RooDataSet* generate3(const int &nEvents = 150) {
    // Generate data: 1/3 * Gauss(0,sigma(variable, better)) + 2/3 * Gauss(1,sigma(variable, worse))
    // Could be 1/3 * signal (better resolution) + 2/3 * background (worse resolution)
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar xErr("xErr", "xErr", .1, 10.);
    RooRealVar f("f", "f", 1./3.);

    xErr.setRange(1., 2.);
    RooUniform xErrA("xErrA", "xErrA", xErr); // Uniform distribution (1., 2.)
    RooHistPdf pdfXErrA("pdfXErrA", "pdfXErrA", xErr, *(xErrA.generate(xErr, f.getVal() * nEvents)->binnedClone())); // PDF from generated histogram

    RooGaussModel gaussA("gaussA", "gaussA scaled by per-event error", x, RooConst(0.), xErr, RooConst(1.), RooConst(1.));
    RooProdPdf modelA("modelA", "modelA", pdfXErrA, Conditional(gaussA, x));
    RooDataSet* dataA = modelA.generate(RooArgSet(x, xErr), f.getVal() * nEvents);

// HERE: this is the only difference wrt generate2: use the same range
    xErr.setRange(1., 2.);
    RooUniform xErrB("xErrB", "xErrB", xErr); // Uniform distribution (1.5, 3.)
    RooHistPdf pdfXErrB("pdfXErrB", "pdfXErrB", xErr, *(xErrB.generate(xErr, nEvents - f.getVal() * nEvents)->binnedClone())); // PDF from generated histogram

    // PICK ONE; difference???
//    RooGaussian gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr);
    RooGaussModel gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr, RooConst(1.), RooConst(1.));

    RooProdPdf modelB("modelB", "modelB", pdfXErrB, Conditional(gaussB, x));
    RooDataSet* dataB = modelB.generate(RooArgSet(x, xErr), nEvents - f.getVal() * nEvents);

    RooCategory type("type", "type");
    type.defineType("A");
    type.defineType("B");

    xErr.setRange(.1, 10.);
    RooDataSet* data = new RooDataSet("data", "data", RooArgSet(x, xErr), Index(type), Import("A", *dataA), Import("B", *dataB)); // Data = 1/3 * DataA + 2/3 * DataB

    delete dataA;
    delete dataB;
    return data;
}



//=====================================================================================================================

double fit0(RooDataSet* data) {
    // Simple fit with double Gauss
    // "f" is a parameter of interest
    // Model = f * Gauss(0,sigma) + (1-f) * Gauss(1,sigma) - sigma is fixed
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar f("f", "f", .5, 0., 1.);

    RooGaussian gaussA("gaussA", "gaussA", x, RooConst(0.), RooConst(1.));
    RooGaussian gaussB("gaussB", "gaussB", x, RooConst(1.), RooConst(1.));
    RooAddPdf model("model", "model", RooArgList(gaussA, gaussB), f);

    model.fitTo(*data);
    delete data;
    return f.getVal();
}

double fit1a(RooDataSet* data) {
    // Simple fit with double Gauss
    // "f" is a parameter of interest
    // Model = f * Gauss(0,sigma) + (1-f) * Gauss(1,sigma) - sigma is fitted
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar f("f", "f", .5, 0., 1.);

    RooRealVar xErrFitted("xErrFitted", "xErrFitted", .1, 10.);

    RooGaussian gaussA("gaussA", "gaussA", x, RooConst(0.), xErrFitted);
    RooGaussian gaussB("gaussB", "gaussB", x, RooConst(1.), xErrFitted);

    RooAddPdf model("model", "model", RooArgList(gaussA, gaussB), f);
    model.fitTo(*data);
    delete data;
    return f.getVal();
}

double fit1b(RooDataSet* data) {
    // Simple fit with double Gauss
    // "f" is a parameter of interest
    // Model = f * Gauss(0,sigma) + (1-f) * Gauss(1,sigma) - sigma is fitted
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar f("f", "f", .5, 0., 1.);

    RooRealVar xErr("xErr", "xErr", .1, 10.);
    RooGaussian gaussA("gaussA", "gaussA", x, RooConst(0.), xErr);
    RooGaussian gaussB("gaussB", "gaussB", x, RooConst(1.), xErr);

    RooAddPdf model("model", "model", RooArgList(gaussA, gaussB), f);
    model.fitTo(*data);
    delete data;
    return f.getVal();
}


double fit2(RooDataSet* data) {
    // Simple fit with double Gauss
    // "f" is a parameter of interest
    // Model = f * Gauss(0,sigma) + (1-f) * Gauss(1,sigma) - sigma is fitted
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar xErr("xErr", "xErr", .1, 10.);
    RooRealVar f("f", "f", .5, 0., 1.);

    // modification: RooGaussModel can also have scale factors for both parameters; let's set them to 1
    RooGaussModel gaussA("gaussA", "gaussA scaled by per-event error", x, RooConst(0.), xErr, RooConst(1.), RooConst(1.));
    RooGaussModel gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr, RooConst(1.), RooConst(1.));
    RooAddPdf model("model", "model", RooArgList(gaussA, gaussB), f);

    model.fitTo(*data);
    delete data;
    return f.getVal();
}

double fit3(RooDataSet* data) {
    // Same as fit2(), but using RooFit option "ConditionalObservables(xErr)", can be used if "error" type A = "error" type B (not our case)
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar xErr("xErr", "xErr", .1, 10.);
    RooRealVar f("f", "f", .5, 0., 1.);

    RooGaussModel gaussA("gaussA", "gaussA scaled by per-event error", x, RooConst(0.), xErr, RooConst(1.), RooConst(1.));
    RooGaussModel gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr, RooConst(1.), RooConst(1.));
    RooAddPdf model("model", "model", RooArgList(gaussA, gaussB), f);

    model.fitTo(*data, ConditionalObservables(xErr));
    delete data;
    return f.getVal();
}

double fit4(RooDataSet* data) {
    // Fit with double Gauss, each scaled by per-event "error" AND multiplied by PDF of this "error"
    // "f" is a parameter of interest
    // Model = f * Gauss(0,sigma(variable)) * Uniform(sigma(variable)) + (1-f) * Gauss(1,sigma(variable)) * Uniform(sigma(variable))
    // Uniform distribution is not an ideal example here... It's not clear if the term can be factorised out...
    // Same as fit2(), but using general distribution of "error", same for type A and type B (not our case)
    // Should give the same result as fit3(), ie. not biased, but not precise
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar xErr("xErr", "xErr", .1, 10.);
    RooRealVar f("f", "f", .5, 0., 1.);

    RooUniform xErrPdf("xErrPdf", "xErrPdf", xErr);
    RooGaussModel gaussA("gaussA", "gaussA scaled by per-event error", x, RooConst(0.), xErr, RooConst(1.), RooConst(1.));
    RooGaussModel gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr, RooConst(1.), RooConst(1.));
    RooProdPdf modelA("modelA", "modelA", xErrPdf, Conditional(gaussA, x));
    RooProdPdf modelB("modelB", "modelB", xErrPdf, Conditional(gaussB, x));
    RooAddPdf model("model", "model", RooArgList(modelA, modelB), f);

    model.fitTo(*data);
    delete data;
    return f.getVal();
}


double fit5(RooDataSet* data) {
    // Fit with double Gauss, each scaled by per-event "error" AND multiplied by the *REAL* PDF of this "error"
    //"f" is a parameter of interest
    // Model = f * Gauss(0,sigma(variable)) * Uniform(sigma(variable, type A)) + (1-f) * Gauss(1,sigma(variable)) * Uniform(sigma(variable, type B))
    RooRealVar x("x", "x", -10., 10.);
    RooRealVar xErr("xErr", "xErr", .1, 10.);
    RooRealVar f("f", "f", .5, 0., 1.);

    RooCategory type("type", "type");
    type.defineType("A");
    type.defineType("B");

    // Select type A data and create "Punzi" term (PDF) for xErr, in the real data it could be sideband region method
    RooDataSet* dataXErrA = (RooDataSet*)data->reduce(RooArgSet(xErr), "type==type::A");
    RooHistPdf xErrPdfA("xErrPdfA", "xErrPdfA", xErr, *dataXErrA->binnedClone());
    RooGaussModel gaussA("gaussA", "gaussA scaled by per-event error", x, RooConst(0.), xErr, RooConst(1.), RooConst(1.));
    RooProdPdf modelA("modelA", "modelA", xErrPdfA, Conditional(gaussA, x));

    // Select type B data and create "Punzi" term (PDF) for xErr, in the real data it could be sideband region method
    RooDataSet* dataXErrB = (RooDataSet*)data->reduce(RooArgSet(xErr), "type==type::B");
    RooHistPdf xErrPdfB("xErrPdfB", "xErrPdfB", xErr, *dataXErrB->binnedClone());
    RooGaussModel gaussB("gaussB", "gaussB scaled by per-event error", x, RooConst(1.), xErr, RooConst(1.), RooConst(1.));
    RooProdPdf modelB("modelB", "modelB", xErrPdfB, Conditional(gaussB, x));

    RooAddPdf model("model", "model", RooArgList(modelA, modelB), f);

    model.fitTo(*data);
    delete data;
    delete dataXErrA;
    delete dataXErrB;
    return f.getVal();
}




void punzi(const int &type, const int &nToys = 1000, const int &nEvents = 150) {
    TH1F histF("histF", Form("Distribution of \"f\" for example %.0d, #Toys %.0d, #Events %.0d", type, nToys, nEvents), 50, 0., 1.);

    for (int i = 0; i < nToys; i++) {
        double f;
        switch (type) {
            case 0:		                // Paper: Figure 2
                f = fit0(generate1(nEvents));
                break;
            case 1:				
                f = fit1a(generate1(nEvents));
                break;
            case 2:				
                f = fit1b(generate1(nEvents));
                break;
            case 3:
                f = fit1a(generate2(nEvents));
                break;
            case 4:		                // Paper: Figure 3
                f = fit1b(generate2(nEvents));
                break;
            case 5:		// option 11 first!
                f = fit2(generate2(nEvents));
                break;
            case 6:
                f = fit3(generate2(nEvents));
                break;
            case 7:		// compare to option 12 - I see no difference;
                f = fit3(generate3(nEvents));
                break;
            case 8:
                f = fit4(generate2(nEvents));
                break;
            case 9:
                f = fit4(generate3(nEvents));
                break;
                
                // CORRECT: NOT biased, PRECISE, almost true/generated value (1/3)
                // Paper: Figure 4
            case 10:		                // Paper: Figure 4
                f = fit5(generate2(nEvents));
                break;
            case 11:
                f = fit1b(generate3(nEvents));
                break;
            case 12:		
                f = fit2(generate3(nEvents));
                break;
            default:
                f = 0;
        }
        histF.Fill( f );
    }

    TCanvas c1("c1","c1", 800, 600);
    histF.Draw();
    c1.SaveAs(Form("punzi_example%.0d.png", type));

    cout << endl << "====================================" << endl;
    cout << "Type      = " << type << endl;
    cout << "Events    = " << nEvents << endl;
    cout << "Toys      = " << nToys << endl;
    cout << "Mean(f)   = " << histF.GetMean() << " +/- " << histF.GetMeanError() << endl;
    cout << "RMS(f) = " << histF.GetRMS() << endl;
    cout << "StdDev(f) = " << histF.GetStdDev() << " +/- " << histF.GetStdDevError() << endl;

    cout << "Result = " << histF.GetMean(1) << " +/- " << histF.GetStdDev() << endl;
    cout << "====================================" << endl << endl;

//  https://root.cern.ch/doc/v610/classRooMinimizer.html

//  https://root.cern.ch/doc/master/RooGaussModel_8cxx_source.html   -- mean and sigma scale factors multiply it

//  https://root.cern.ch/root/html534/RooProdPdf.html  --  example for conditional prob. F(x,y) G(y) 
}












