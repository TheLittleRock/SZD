#include <vector>
#include <iostream>
#include <TMath.h>
#include <TVector2.h>
#include <algorithm>



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

using namespace std;


Double_t DeltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2)
{
    Double_t deta= eta1-eta2;
    Double_t dphi= TVector2::Phi_mpi_pi(phi1-phi2);

    return TMath::Sqrt( deta*deta+dphi*dphi);
}

void my_treeReader()
{
    TFile *fin_sim = new TFile("../Pythia/output_pythia.root", "OPEN");
    TTree *tree_sim = (TTree*) fin_sim->Get("strom");

    //Histogramy pro unfolding
    TH1D* h_true_pt = new TH1D("h_true_pt","h_true_pt",50,10.,30.);
    h_true_pt->SetXTitle("p_{T} (GeV)");
    h_true_pt->SetYTitle("events");
    h_true_pt->Sumw2();

    TH1D* h_reco_pt = new TH1D("h_reco_pt","h_reco_pt",50,10.,30.);
    h_reco_pt->SetXTitle("p_{T} (GeV)");
    h_reco_pt->SetYTitle("events");
    h_reco_pt->Sumw2();

    TH2D* h_RM_sim = new TH2D("h_RM_sim", "h_RM_sim", 50,10.,30.,50,10.,30.);
    h_RM_sim->Sumw2();

    TH2D* h_RM_sim2 = new TH2D("h_RM_sim2", "h_RM_sim2", 50,10.,30.,50,10.,30.);
    h_RM_sim2->Sumw2();


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
    tree_sim->SetBranchAddress("Jet_reco1_px", &Jet_reco_px, &b_Jet_reco_px);
    tree_sim->SetBranchAddress("Jet_reco1_py", &Jet_reco_py, &b_Jet_reco_py);
    tree_sim->SetBranchAddress("Jet_reco1_pz", &Jet_reco_pz, &b_Jet_reco_pz);
    tree_sim->SetBranchAddress("Jet_reco1_e", &Jet_reco_e, &b_Jet_reco_e);

// naplneni histogramu - je potreba i jet matching


    for (Int_t k = 0; k < tree_sim->GetEntriesFast(); ++k)
    {
        tree_sim ->GetEntry(k);

        cout << k << '\r';

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
 	
 	    // sort jets by decreasing pT
        sort(sorted_true_jets.begin(), sorted_true_jets.end(),
             [](const TLorentzVector& a, const TLorentzVector& b) {
                 return a.Perp() > b.Perp();
             });

        sort(sorted_reco_jets.begin(), sorted_reco_jets.end(),
             [](const TLorentzVector& a, const TLorentzVector& b) {
                 return a.Perp() > b.Perp();
             });

        for(UInt_t i = 0; i < sorted_true_jets.size(); i++) {

            double minDeltaR = 999.0; //set minDelta
            int bestRecoIndex = -1; //set best index

            //go through all reco jets and look for the closest
            for(UInt_t j = 0; j < sorted_reco_jets.size(); j++) {

                double dR = DeltaR(sorted_true_jets[i].Eta(),
                                   sorted_true_jets[i].Phi(),
                                   sorted_reco_jets[j].Eta(),
                                   sorted_reco_jets[j].Phi());
    
                // save the smallest DeltaR and its index
                if(dR < minDeltaR) {
                    minDeltaR = dR;
                    bestRecoIndex = j;
                }
            }

            //match the closest jets if closer than jet radius R = 0.6
            if(bestRecoIndex != -1 && minDeltaR < 0.6) {

                h_RM_sim->Fill(sorted_reco_jets[bestRecoIndex].Perp(),
                               sorted_true_jets[i].Perp(),
                               1.0);

                h_RM_sim2->Fill(sorted_true_jets[i].Perp(),
                                sorted_reco_jets[bestRecoIndex].Perp(),
                                1.0);

                // erase the reco jet to not use it again
                sorted_reco_jets.erase(sorted_reco_jets.begin() + bestRecoIndex);
            }
        }
    }
 	
 	

    TFile *fout_sim = new TFile("Hist_sim.root", "RECREATE");
    h_true_pt->Write();
    h_reco_pt->Write();
    h_RM_sim->Write();
    h_RM_sim2->Write();
    fout_sim->Close();

}

void Fill_hist_data()
{
    TFile *fin_data = new TFile("../Pythia/output_pythia.root", "OPEN");

    TTree *tree_data = (TTree*) fin_data->Get("strom");

    //Histogramy pro unfold
    TH1D* h_data_pt = new TH1D("h_data_pt","h_data_pt",50,10.,30.);
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

        cout << k << '\r';

        if( (Jet_true_px->size()< 1) || (Jet_reco_px->size() < 1) ) continue;

        vector<TLorentzVector> sorted_reco_jets;

        for(UInt_t i = 0; i< Jet_reco_px->size(); i++)
        {
            TLorentzVector jet;
            jet.SetPxPyPzE(Jet_reco_px->at(i), Jet_reco_py->at(i), Jet_reco_pz->at(i),Jet_reco_e->at(i));
            h_data_pt->Fill(jet.Perp(), 1.0);
            sorted_reco_jets.push_back( jet );
        }
    }

    TFile *fout_sim = new TFile("Hist_data.root", "RECREATE");
    h_data_pt->Write();
    fout_sim->Close();


}

