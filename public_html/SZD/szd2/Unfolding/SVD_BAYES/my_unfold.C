#include <iostream>
#include <vector>

#include <TH1.h>
#include <TH2.h>
#include <TFile.h>
#include <TTree.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TVectorF.h>
#include <TLorentzVector.h>
#include <TLegend.h>
#include <TSystem.h>

/*
#include "RooUnfoldResponse.h"
#include "RooUnfoldBayes.h"
#include "RooUnfoldSvd.h"
#include "RooUnfoldTUnfold.h"
#include "RooUnfoldIds.h"
*/

using namespace std;


void my_unfold()
{

//    gSystem->Load("$ROOUNFOLD/libRooUnfold"); // nacteni knihoven ROOUNFOLD
    gSystem->Load("/data2/vyuka/szd/Programs/RooUnfold_2026/libRooUnfold");

    const int num_iter = 4; //počet itarací

    //tahani pripravenych histogramu - simulace
    TFile *finput_sim = new TFile("Hist_sim.root", "OPEN");


    TH1D *h_true = (TH1D*)finput_sim->Get("h_true_pt");
    TH1D *h_reco = (TH1D*)finput_sim->Get("h_reco_pt");
//    TH2D *h_RM = (TH2D*)finput_sim->Get("h_RM_sim2");
    TH2D *h_RM = (TH2D*)finput_sim->Get("h_RM_sim");

/*
    TH1D *h_true = (TH1D*) h_true_pt->Clone("h_true");
    TH1D *h_reco = (TH1D*) h_reco_pt->Clone("h_reco");
    TH2D *h_RM = (TH2D*) h_RM_sim->Clone("h_RM");
*/

    //tahani pripravenych histogramu - data
    TFile *finput_data = new TFile("Hist_data.root", "OPEN");

    TH1D *h_data= (TH1D*)finput_data->Get("h_data_pt");
//    TH1D *h_data= (TH1D*) h_data_pt->Clone("h_data");


    //HERE: RESPONSE FOR UNFOLDING:
    RooUnfoldResponse response (h_reco,h_true,h_RM); //response matice

    //priprava histogramu pro unfolded data
    TH2D* hCov_SVD=new TH2D("hCov_SVD","hCov_SVD", 50,10.,30.,50,10.,30.);
    TH1D* h_unfolded_SVD[num_iter];
    TH2D* hCov_BAYES=new TH2D("hCov_BAYES","hCov_BAYES", 50,10.,30.,50,10.,30.);
    TH1D* h_unfolded_BAYES[num_iter];

    for(int iter=0; iter<num_iter; iter++){

        cout<<"UNFOLDING"<<endl;
        cout<<"iterace: "<<iter<<endl;
        cout << "" << endl;

        //SvD a Bayes unfold
        RooUnfoldSvd    unfoldSvD(&response, h_data, iter+1);
//CODE HERE:  1 line analogous to the above
//Bayes unfolding:
        RooUnfoldBayes unfoldBayes(&response, h_data, iter+1);







//	TUnfold zase nekdy jindy
//      RooUnfoldTUnfold unfoldT(&response, h_data);


// http://hepunx.rl.ac.uk/~adye/software/unfold/htmldoc/RooUnfold.html
// Creates reconstructed distribution. Error calculation varies by withError:
//    0: No errors
//    1: Errors from the square root of the diagonals of the covariance matrix given by the unfolding
//    2: Errors from the square root of of the covariance matrix given by the unfolding
//    3: Errors from the square root of the covariance matrix from the variation of the results in toy MC tests



        h_unfolded_SVD[iter]= (TH1D*) unfoldSvD.Hreco();
//CODE HERE:  1 line analogous to the above
//Bayes unfolding:

        h_unfolded_BAYES[iter] = (TH1D*) unfoldBayes.Hreco();






//        TH1D* hDvec=(TH1D*) unfoldSvD.GetDvec();	//?? neni v manualu  TVectorD ErecoV() dava diagonalni prvky cov matice


        TMatrixD covM_SVD=(TMatrixD) unfoldSvD.Eunfold();
//CODE HERE:  1 line analogous to the above
//Bayes unfolding:

        TMatrixD covM_BAYES = (TMatrixD) unfoldBayes.Eunfold();



	// prevod matice na TH2

        for(Int_t i=0; i<50; i++){
            for(Int_t j=0; j<50; j++){
                hCov_SVD->SetBinContent(i+1, j+1, covM_SVD(i,j));
            }
        }
//CODE HERE:  4 lines analogous to the above
//Bayes unfolding:
        for(Int_t i=0; i<50; i++){    
            for(Int_t j=0; j<50; j++){
                hCov_BAYES->SetBinContent(i+1, j+1, covM_BAYES(i,j));
            }
        }






    }   //end of loop for iterations

        cout << "TADY 0" << endl;
    //Draw
//    gStyle->SetOptStat(0);
    TCanvas *c_compare = new TCanvas();
    c_compare->Divide(2,1);


    h_reco->SetLineColor(3);
    h_true->SetLineColor(1);
    h_reco->SetMarkerColor(3);
    h_true->SetMarkerColor(1);
    h_reco->SetMarkerStyle(1);
    h_true->SetMarkerStyle(1);
    h_data->SetLineColor(2);
    h_data->SetMarkerColor(2);
    h_data->SetMarkerStyle(1);



    c_compare->cd(1);	//SVD plot
        h_data->Draw("hist");
        h_reco->Draw("hist,same");
        h_true->Draw("hist,same");
    for (int i = 3; i < num_iter; ++i){
    
        h_unfolded_SVD[i]->SetLineColor(i+5);
        h_unfolded_BAYES[i]->SetLineColor(i);
    
        h_unfolded_SVD[i]->SetMarkerColor(i+5);
        h_unfolded_BAYES[i]->SetMarkerColor(i);

        h_unfolded_SVD[i]->SetMarkerStyle(5);
        h_unfolded_BAYES[i]->SetMarkerStyle(2);
       

        h_unfolded_SVD[i]->SetMaximum(3000);
        //h_unfolded_SVD[i]->GetXaxis()->SetRange(10, 30);
        h_unfolded_SVD[i]->SetTitle("SvD unfold, RECO and true data");
        h_unfolded_SVD[i]->GetXaxis()->SetTitle("p_{t} GeV");
        h_unfolded_SVD[i]->GetYaxis()->SetTitle("Counts");

        h_unfolded_SVD[i]->Draw("same");
        //h_unfolded_BAYES[i]->Draw("P,same");


    }

        
    
    TLegend *leg_compare = new TLegend(0.7,0.7,0.9,0.9);
    leg_compare->AddEntry(h_true,"True data","l");
    leg_compare->AddEntry(h_reco,"Reco data","l");
    leg_compare->AddEntry(h_unfolded_SVD[3],"Unfolded","p");
        
    leg_compare->Draw();     
        
        
        //Bayes histograms
        c_compare->cd(2);	//Bayes plot
        h_data->Draw("hist");
        h_reco->Draw("hist,same");
        h_true->Draw("hist,same");

        for (int i = 3; i < num_iter; ++i){
            h_unfolded_BAYES[i]->Draw("same");
        }
        
        
        cout << "3" << endl;

    TCanvas *c_matrices = new TCanvas();
    c_matrices->Divide(2,1);
        cout << "4" << endl;
    c_matrices->cd(1);
    hCov_SVD->SetTitle("Covariant matrix SVD");
    hCov_SVD->Draw("SURF2");
        cout << "5" << endl;
    c_matrices->cd(2);
//    hCov_BAYES->SetTitle("Covariant matrix SVD");
    hCov_BAYES->Draw("SURF2");


    TCanvas *c_RM = new TCanvas();
    h_RM->Draw("colz");

        cout << "6" << endl;

}































