#define HBOM_cxx
#include "HBOM.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <TF1.h>
#include <TGraph.h>
#include <TLegend.h>
#include <TLegend.h>

void HBOM::Loop()
{
//   In a ROOT session, you can do:
//      root> .L HBOM.C
//      root> HBOM t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
     if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;

   TH1D* h_Jet_true_pt = new TH1D("Jet_true_pt","Jet_true_pt",20,0.,60);
   h_Jet_true_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_true_pt->SetYTitle("events");
   h_Jet_true_pt->Sumw2();

   TH1D* h_Jet_reco0_pt = new TH1D("Jet_reco0_pt","Jet_reco0_pt",20,0.,60);
   h_Jet_reco0_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_reco0_pt->SetYTitle("events");
   h_Jet_reco0_pt->Sumw2();

   TH1D* h_Jet_reco1_pt = new TH1D("Jet_reco1_pt","Jet_reco1_pt",20,0.,60);
   h_Jet_reco1_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_reco1_pt->SetYTitle("events");
   h_Jet_reco1_pt->Sumw2();

   TH1D* h_Jet_reco2_pt = new TH1D("Jet_reco2_pt","Jet_reco2_pt",20,0.,60);
   h_Jet_reco2_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_reco2_pt->SetYTitle("events");
   h_Jet_reco2_pt->Sumw2();

   TH1D* h_Jet_reco3_pt = new TH1D("Jet_reco3_pt","Jet_reco3_pt",20,0.,60);
   h_Jet_reco3_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_reco3_pt->SetYTitle("events");
   h_Jet_reco3_pt->Sumw2();

   TH1D* h_Jet_reco4_pt = new TH1D("Jet_reco4_pt","Jet_reco4_pt",20,0.,60);
   h_Jet_reco4_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_reco4_pt->SetYTitle("events");
   h_Jet_reco4_pt->Sumw2();

   TH1D* h_Jet_reco5_pt = new TH1D("Jet_reco5_pt","Jet_reco5_pt",20,0.,60);
   h_Jet_reco5_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_reco5_pt->SetYTitle("events");
   h_Jet_reco5_pt->Sumw2();

   TH1D* h_Jet_Unfolded_pol4_pt = new TH1D("Jet_Unfolded_pol4_pt","Jet_Unfolded_pol4_pt",20,0.,60);
   h_Jet_Unfolded_pol4_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_Unfolded_pol4_pt->SetYTitle("events");
   h_Jet_Unfolded_pol4_pt->Sumw2();


   TH1D* h_Jet_Unfolded_pol3_pt = new TH1D("Jet_Unfolded_pol3_pt","Jet_Unfolded_pol3_pt",20,0.,60);
   h_Jet_Unfolded_pol3_pt->SetXTitle("p_{T} (GeV)");
   h_Jet_Unfolded_pol3_pt->SetYTitle("events");
   h_Jet_Unfolded_pol3_pt->Sumw2();

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

	if( (Jet_true_px->size()< 1) || (Jet_reco0_px->size() < 1) || (Jet_reco1_px->size() < 1)|| (Jet_reco2_px->size() < 1)|| (Jet_reco3_px->size() < 1)|| (Jet_reco4_px->size() < 1)|| (Jet_reco5_px->size() < 1) ) continue;

	vector<TLorentzVector> sorted_true_jets;
	vector<TLorentzVector> sorted_reco0_jets;
	vector<TLorentzVector> sorted_reco1_jets;
	vector<TLorentzVector> sorted_reco2_jets;
	vector<TLorentzVector> sorted_reco3_jets;
	vector<TLorentzVector> sorted_reco4_jets;
	vector<TLorentzVector> sorted_reco5_jets;

	for(UInt_t i = 0; i< Jet_true_px->size(); i++)
	{
	TLorentzVector jet;
	jet.SetPxPyPzE(Jet_true_px->at(i), Jet_true_py->at(i), Jet_true_pz->at(i),Jet_true_e->at(i));
	h_Jet_true_pt->Fill(jet.Perp(), 1.0);
	sorted_true_jets.push_back( jet );
	}

	for(UInt_t i = 0; i< Jet_reco0_px->size(); i++)
	{
	TLorentzVector jet;
	jet.SetPxPyPzE(Jet_reco0_px->at(i), Jet_reco0_py->at(i), Jet_reco0_pz->at(i),Jet_reco0_e->at(i));
	h_Jet_reco0_pt->Fill(jet.Perp(), 1.0);
	sorted_reco0_jets.push_back( jet );
	}

	for(UInt_t i = 0; i< Jet_reco1_px->size(); i++)
	{
	TLorentzVector jet;
	jet.SetPxPyPzE(Jet_reco1_px->at(i), Jet_reco1_py->at(i), Jet_reco1_pz->at(i),Jet_reco1_e->at(i));
	h_Jet_reco1_pt->Fill(jet.Perp(), 1.0);
	sorted_reco1_jets.push_back( jet );
	}

	for(UInt_t i = 0; i< Jet_reco2_px->size(); i++)
	{
	TLorentzVector jet;
	jet.SetPxPyPzE(Jet_reco2_px->at(i), Jet_reco2_py->at(i), Jet_reco2_pz->at(i),Jet_reco2_e->at(i));
	h_Jet_reco2_pt->Fill(jet.Perp(), 1.0);
	sorted_reco2_jets.push_back( jet );
	}

	for(UInt_t i = 0; i< Jet_reco3_px->size(); i++)
	{
	TLorentzVector jet;
	jet.SetPxPyPzE(Jet_reco3_px->at(i), Jet_reco3_py->at(i), Jet_reco3_pz->at(i),Jet_reco3_e->at(i));
	h_Jet_reco3_pt->Fill(jet.Perp(), 1.0);
	sorted_reco3_jets.push_back( jet );
	}

	for(UInt_t i = 0; i< Jet_reco4_px->size(); i++)
	{
	TLorentzVector jet;
	jet.SetPxPyPzE(Jet_reco4_px->at(i), Jet_reco4_py->at(i), Jet_reco4_pz->at(i),Jet_reco4_e->at(i));
	h_Jet_reco4_pt->Fill(jet.Perp(), 1.0);
	sorted_reco4_jets.push_back( jet );
	}

	for(UInt_t i = 0; i< Jet_reco5_px->size(); i++)
	{
	TLorentzVector jet;
	jet.SetPxPyPzE(Jet_reco5_px->at(i), Jet_reco5_py->at(i), Jet_reco5_pz->at(i),Jet_reco5_e->at(i));
	h_Jet_reco5_pt->Fill(jet.Perp(), 1.0);
	sorted_reco5_jets.push_back( jet );
	}

   }

  TGraph* compare = new TGraph();
  for(Int_t bin = 1; bin <= 20; bin++)
	{
	compare->SetPoint(0,0,h_Jet_reco0_pt->GetBinContent(bin));
	compare->SetPoint(1,1,h_Jet_reco1_pt->GetBinContent(bin));
	compare->SetPoint(2,2,h_Jet_reco2_pt->GetBinContent(bin));
	compare->SetPoint(3,3,h_Jet_reco3_pt->GetBinContent(bin));
	compare->SetPoint(4,4,h_Jet_reco4_pt->GetBinContent(bin));
	compare->SetPoint(5,5,h_Jet_reco5_pt->GetBinContent(bin));

    compare->Fit("pol4");
    TF1 * fit_pol4 = compare->GetFunction("pol4");
    h_Jet_Unfolded_pol4_pt->SetBinContent(bin, fit_pol4->Eval(-1));

    compare->Fit("pol3");
    TF1 * fit_pol3 = compare->GetFunction("pol3");
	h_Jet_Unfolded_pol3_pt->SetBinContent(bin, fit_pol3->Eval(-1));
	compare->Clear();

	}

// Graph

    gStyle->SetOptStat(0);
    TCanvas *c_compare = new TCanvas();

    h_Jet_true_pt->SetTitle("Comparision of true, and unfolded data");
    h_Jet_true_pt->GetXaxis()->SetRange(1,9);
    h_Jet_Unfolded_pol4_pt->SetMarkerStyle(2);
    h_Jet_Unfolded_pol3_pt->SetMarkerStyle(5);
    h_Jet_reco5_pt->SetMarkerStyle(1);
    h_Jet_true_pt->SetMarkerColor(1);
    h_Jet_Unfolded_pol4_pt->SetMarkerColor(2);
    h_Jet_Unfolded_pol3_pt->SetMarkerColor(4);
    h_Jet_true_pt->SetLineColor(1);
    h_Jet_reco5_pt->SetLineColor(3);
    h_Jet_Unfolded_pol4_pt->SetLineColor(0);
    h_Jet_Unfolded_pol3_pt->SetLineColor(0);


    TLegend *leg_compare = new TLegend(0.7,0.7,0.9,0.9);
    leg_compare->AddEntry(h_Jet_true_pt,"True data","l");
    leg_compare->AddEntry(h_Jet_reco5_pt,"Reco5 data","l");
    leg_compare->AddEntry(h_Jet_Unfolded_pol4_pt,"Unfolded by pol4","p");
    leg_compare->AddEntry(h_Jet_Unfolded_pol3_pt,"Unfolded by pol3","p");

    h_Jet_true_pt->Draw("");
    h_Jet_Unfolded_pol4_pt->Draw("P,same");
    h_Jet_Unfolded_pol3_pt->Draw("P,same");
    h_Jet_reco5_pt->Draw("l,same");
    leg_compare->Draw();
}


Double_t HBOM::DeltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2)
{
	Double_t deta= eta1-eta2;
	Double_t dphi= TVector2::Phi_mpi_pi(phi1-phi2);

	return TMath::Sqrt( deta*deta+dphi*dphi);
}

