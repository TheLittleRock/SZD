
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


Double_t DeltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2)
{
    Double_t deta= eta1-eta2;
    Double_t dphi= TVector2::Phi_mpi_pi(phi1-phi2);

    return TMath::Sqrt( deta*deta+dphi*dphi);
}

void Fill_hist_sim()
{
    TFile *fin_sim = new TFile("HERWIG_simulace.root", "OPEN");
    TTree *tree_sim = (TTree*) fin_sim->Get("strom");

    //Histogramy pro unfolding
    TH1D* h_true_pt = new TH1D("h_true_pt","h_true_pt",100,0.,100);
    h_true_pt->SetXTitle("p_{T} (GeV)");
    h_true_pt->SetYTitle("events");
    h_true_pt->Sumw2();

    TH1D* h_reco_pt = new TH1D("h_reco_pt","h_reco_pt",100,0.,100);
    h_reco_pt->SetXTitle("p_{T} (GeV)");
    h_reco_pt->SetYTitle("events");
    h_reco_pt->Sumw2();

    TH2D* h_RM_sim = new TH2D("h_RM_sim", "h_RM_sim", 100,0.,100,100,0.,100);
    h_RM_sim->Sumw2();


    //naplneni histogramu z HERWIG_simulace.root
    Double_t        event_weight=0, Xsec=0;
    vector<double>  *Jet_true_px=0, *Jet_true_py=0, *Jet_true_pz=0, *Jet_true_e=0, *Jet_reco_px=0, *Jet_reco_py=0, *Jet_reco_pz=0, *Jet_reco_e=0;

    TBranch         *b_event_weight, *b_Xsec,*b_Jet_true_px,*b_Jet_true_py,*b_Jet_true_pz,*b_Jet_true_e,*b_Jet_reco_px,*b_Jet_reco_py,*b_Jet_reco_pz,*b_Jet_reco_e;

    tree_sim->SetBranchAddress("event_weight", &event_weight, &b_event_weight);
    tree_sim->SetBranchAddress("Xsec", &Xsec, &b_Xsec);
    tree_sim->SetBranchAddress("Jet_true_px", &Jet_true_px, &b_Jet_true_px);
    tree_sim->SetBranchAddress("Jet_true_py", &Jet_true_py, &b_Jet_true_py);
    tree_sim->SetBranchAddress("Jet_true_pz", &Jet_true_pz, &b_Jet_true_pz);
    tree_sim->SetBranchAddress("Jet_true_e", &Jet_true_e, &b_Jet_true_e);
    tree_sim->SetBranchAddress("Jet_reco_px", &Jet_reco_px, &b_Jet_reco_px);
    tree_sim->SetBranchAddress("Jet_reco_py", &Jet_reco_py, &b_Jet_reco_py);
    tree_sim->SetBranchAddress("Jet_reco_pz", &Jet_reco_pz, &b_Jet_reco_pz);
    tree_sim->SetBranchAddress("Jet_reco_e", &Jet_reco_e, &b_Jet_reco_e);

// naplneni histogramu - je potreba i jet matching


    for (Int_t k = 0; k < tree_sim->GetEntriesFast(); ++k)
    {
        tree_sim ->GetEntry(k);

        if( (Jet_true_px->size()< 1) || (Jet_reco_px->size() < 1) ) continue;

        vector<TLorentzVector> sorted_true_jets;
        vector<TLorentzVector> sorted_reco_jets;

 	// truth jety
        for(UInt_t i = 0; i< Jet_true_px->size(); i++)
        {
            TLorentzVector jet;
            jet.SetPxPyPzE(Jet_true_px->at(i), Jet_true_py->at(i), Jet_true_pz->at(i),Jet_true_e->at(i));
            h_true_pt->Fill(jet.Perp(), 1.0);
            sorted_true_jets.push_back( jet );
        }

 	// reco jety
        for(UInt_t i = 0; i< Jet_reco_px->size(); i++)
        {
            TLorentzVector jet;
            jet.SetPxPyPzE(Jet_reco_px->at(i), Jet_reco_py->at(i), Jet_reco_pz->at(i),Jet_reco_e->at(i));
            h_reco_pt->Fill(jet.Perp(), 1.0);
            sorted_reco_jets.push_back( jet );
        }

 	// truth-reco jet matching
        for(UInt_t i =0; i<sorted_true_jets.size(); i++){
            for(Int_t j = sorted_reco_jets.size()-1; j>=0; j--)
            {
                if(DeltaR(sorted_true_jets[i].Eta(), sorted_true_jets[i].Phi(), sorted_reco_jets[j].Eta(), sorted_reco_jets[j].Phi())<0.6)
                {
                    h_RM_sim->Fill(sorted_true_jets[i].Perp(), sorted_reco_jets[i].Perp(),1.0);
                    sorted_reco_jets.erase(sorted_reco_jets.begin()+j);
                }
            }
        }
    }

    TFile *fout_sim = new TFile("Hist_sim.root", "RECREATE");
    h_true_pt->Write();
    h_reco_pt->Write();
    h_RM_sim->Write();
    fout_sim->Close();

}

void Fill_hist_data()
{
    TFile *fin_data = new TFile("HERWIG_data.root", "OPEN");

    TTree *tree_data = (TTree*) fin_data->Get("strom");

    //Histogramy pro unfold
    TH1D* h_data_pt = new TH1D("h_data_pt","h_data_pt",100,0.,100);
    h_data_pt->SetXTitle("p_{T} (GeV)");
    h_data_pt->SetYTitle("events");
    h_data_pt->Sumw2();


    //naplneni histogramu z HERWIG_data.root

    Double_t        event_weight=0, Xsec=0;
    vector<double>  *Jet_true_px=0, *Jet_true_py=0, *Jet_true_pz=0, *Jet_true_e=0, *Jet_reco_px=0, *Jet_reco_py=0, *Jet_reco_pz=0, *Jet_reco_e=0;

    TBranch         *b_event_weight, *b_Xsec,*b_Jet_true_px,*b_Jet_true_py,*b_Jet_true_pz,*b_Jet_true_e,*b_Jet_reco_px,*b_Jet_reco_py,*b_Jet_reco_pz,*b_Jet_reco_e;

    tree_data->SetBranchAddress("event_weight", &event_weight, &b_event_weight);
    tree_data->SetBranchAddress("Xsec", &Xsec, &b_Xsec);
    tree_data->SetBranchAddress("Jet_true_px", &Jet_true_px, &b_Jet_true_px);
    tree_data->SetBranchAddress("Jet_true_py", &Jet_true_py, &b_Jet_true_py);
    tree_data->SetBranchAddress("Jet_true_pz", &Jet_true_pz, &b_Jet_true_pz);
    tree_data->SetBranchAddress("Jet_true_e", &Jet_true_e, &b_Jet_true_e);
    tree_data->SetBranchAddress("Jet_reco1_px", &Jet_reco_px, &b_Jet_reco_px);
    tree_data->SetBranchAddress("Jet_reco1_py", &Jet_reco_py, &b_Jet_reco_py);
    tree_data->SetBranchAddress("Jet_reco1_pz", &Jet_reco_pz, &b_Jet_reco_pz);
    tree_data->SetBranchAddress("Jet_reco1_e", &Jet_reco_e, &b_Jet_reco_e);

    for (Int_t k = 0; k < tree_data->GetEntriesFast(); ++k)
    {
        tree_data ->GetEntry(k);

        if( (Jet_true_px->size()< 1) || (Jet_reco_px->size() < 1) ) continue;

//        vector<TLorentzVector> sorted_reco_jets;

        for(UInt_t i = 0; i< Jet_reco_px->size(); i++)
        {
            TLorentzVector jet;
            jet.SetPxPyPzE(Jet_reco_px->at(i), Jet_reco_py->at(i), Jet_reco_pz->at(i),Jet_reco_e->at(i));
            h_data_pt->Fill(jet.Perp(), 1.0);
//            sorted_reco_jets.push_back( jet );
        }
    }

    TFile *fout_sim = new TFile("Hist_data.root", "RECREATE");
    h_data_pt->Write();
    fout_sim->Close();


}

void my_unfold()
{
    gSystem->Load("$ROOUNFOLD/libRooUnfold.so"); // nacteni knihoven ROOUNFOLD
    const int num_iter = 3; //počet itarací

    //tahani pripravenych histogramu - simulace
    TFile *finput_sim = new TFile("Hist_sim.root", "OPEN");

    TH1D *h_true = (TH1D*)finput_sim->Get("h_true_pt");
    TH1D *h_reco = (TH1D*)finput_sim->Get("h_reco_pt");
    TH2D *h_RM = (TH2D*)finput_sim->Get("h_RM_sim");

    //tahani pripravenych histogramu - data
    TFile *finput_data = new TFile("Hist_data.root", "OPEN");

    TH1D *h_data= (TH1D*)finput_data->Get("h_data_pt");

    //unfolding
    RooUnfoldResponse response (h_reco,h_true,h_RM); //response matice

    //priprava histogramu pro unfolded data
    TH2D* hCov_SVD=new TH2D("hCov_SVD","hCov_SVD", 100,0.,100,100,0.,100);
    TH1D* h_unfolded_SVD[num_iter];
    TH2D* hCov_BAYES=new TH2D("hCov_BAYES","hCov_BAYES", 100,0.,100,100,0.,100);
    TH1D* h_unfolded_BAYES[num_iter];

    for(int iter=0; iter<num_iter; iter++)
    {
        cout<<"UNFOLDING"<<endl;
        cout<<"iterace: "<<iter<<endl;
        cout << "" << endl;

        //SvD a Bayes unfold
        RooUnfoldSvd    unfoldSvD(&response, h_data, iter+1);
        RooUnfoldBayes  unfoldb  (&response, h_data, iter+1, 0);

//	TUnfold zase nekdy jindy
//      RooUnfoldTUnfold unfoldT(&response, h_data);


// http://hepunx.rl.ac.uk/~adye/software/unfold/htmldoc/RooUnfold.html
// Creates reconstructed distribution. Error calculation varies by withError:
//    0: No errors
//    1: Errors from the square root of the diagonals of the covariance matrix given by the unfolding
//    2: Errors from the square root of of the covariance matrix given by the unfolding
//    3: Errors from the square root of the covariance matrix from the variation of the results in toy MC tests

        h_unfolded_SVD[iter]= (TH1D*) unfoldSvD.Hreco(3);
        h_unfolded_BAYES[iter]= (TH1D*) unfoldb.Hreco(3);

        TH1D* hDvec=(TH1D*) unfoldSvD.GetDvec();	//?? neni v manualu  TVectorD ErecoV() dava diagonalni prvky cov matice

	TMatrixD covM_BAYES=(TMatrixD) unfoldb.Ereco();
        TMatrixD covM_SVD=(TMatrixD) unfoldSvD.Ereco();

	// prevod matice na TH2
        for(Int_t i=0; i<100; i++){
            for(Int_t j=0; j<100; j++){
                hCov_BAYES->SetBinContent(i+1, j+1, covM_BAYES(i,j));
            }
        }
        for(Int_t i=0; i<100; i++){
            for(Int_t j=0; j<100; j++){
                hCov_SVD->SetBinContent(i+1, j+1, covM_SVD(i,j));
            }
        }

    }

    //Draw
    gStyle->SetOptStat(0);
    TCanvas *c_compare = new TCanvas();
    c_compare->Divide(num_iter,1);

    TLegend *leg_compare = new TLegend(0.7,0.7,0.9,0.9);
    leg_compare->AddEntry(h_true,"True data","l");
    leg_compare->AddEntry(h_reco,"Reco data","l");
    leg_compare->AddEntry(h_unfolded_SVD[0],"Unfolded by SvD","p");
    leg_compare->AddEntry(h_unfolded_BAYES[0],"Unfolded by Bayes","p");

    for (int i = 0; i < num_iter; ++i)
    {
        c_compare->cd(i+1);

        h_unfolded_SVD[i]->SetLineColor(4);
        h_unfolded_BAYES[i]->SetLineColor(2);
        h_reco->SetLineColor(3);
        h_true->SetLineColor(1);

        h_unfolded_SVD[i]->SetMarkerColor(4);
        h_unfolded_BAYES[i]->SetMarkerColor(2);
        h_reco->SetMarkerColor(3);
        h_true->SetMarkerColor(1);

        h_unfolded_SVD[i]->SetMarkerStyle(5);
        h_unfolded_BAYES[i]->SetMarkerStyle(2);
        h_reco->SetMarkerStyle(1);
        h_true->SetMarkerStyle(1);

        // h_unfolded_SVD[i]->Draw("same");
        // h_unfolded_BAYES[i]->Draw("same");
        // h_reco[i]->Draw("same");
        // h_true[i]->Draw("same");

        // h_unfolded_SVD[i]->Draw("same");
        // h_unfolded_BAYES[i]->Draw("same");
        // h_reco[i]->Draw("same");
        // h_true[i]->Draw("same");

        h_unfolded_SVD[i]->SetMaximum(27000);
        h_unfolded_SVD[i]->GetXaxis()->SetRange(1,25);
        h_unfolded_SVD[i]->SetTitle("Comparison of SvD and Bayes unfold, RECO and true data");
        h_unfolded_SVD[i]->GetXaxis()->SetTitle("p_{t} GeV");
        h_unfolded_SVD[i]->GetYaxis()->SetTitle("Counts");

        h_unfolded_SVD[i]->Draw("P");
        h_unfolded_BAYES[i]->Draw("P,same");
        h_reco->Draw("l,same");
        h_true->Draw("same");
        leg_compare->Draw();
    }

    TCanvas *c_matrices = new TCanvas();
    c_matrices->Divide(2,1);

    c_matrices->cd(1);
    hCov_SVD->SetTitle("Covariant matrix SVD");
    hCov_SVD->Draw("SURF2");

    c_matrices->cd(2);
    hCov_BAYES->SetTitle("Covariant matrix SVD");
    hCov_BAYES->Draw("SURF2");


    TFile *fout_unfold = new TFile("hist_unfold.root", "RECREATE"); // kam se pak ulozi vysledek
    hCov_BAYES->Write();
    hCov_SVD->Write();
    h_reco->Write();
    h_true->Write();
    for (int i = 0; i < num_iter; ++i)
    {
        h_unfolded_SVD[i]->Write();
        h_unfolded_BAYES[i]->Write();
    }
    fout_unfold->Close();
}



