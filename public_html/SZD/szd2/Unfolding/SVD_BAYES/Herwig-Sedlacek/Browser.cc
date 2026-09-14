// -*- C++ -*-
//
// This is the implementation of the non-inlined, non-templated member
// functions of the BrowserAnalysis class.
//

#include "Browser.h"
#include "ThePEG/Interface/ClassDocumentation.h"
#include "ThePEG/EventRecord/Particle.h"
#include "ThePEG/Repository/UseRandom.h"
#include "ThePEG/Repository/EventGenerator.h"
#include "ThePEG/Utilities/DescribeClass.h"


//using namespace LHAPDF;
using namespace Mira;
using namespace HepMC;
using namespace Herwig;
using namespace std;
using namespace fastjet;

Browser::Browser() {}

Browser::~Browser() {}



#ifndef LWH_AIAnalysisFactory_H
#ifndef LWH 
#define LWH ThePEGLWH
#endif
#include "ThePEG/Analysis/LWH/AnalysisFactory.h"
#endif

void Browser::analyze(tEventPtr event, long ieve, Int_t loop, Int_t state) {
  AnalysisHandler::analyze(event, ieve, loop, state);
  // Rotate to CMS, extract final state particles and call analyze(particles).



//  Double_t JetLepDRmin = 0.4;
  
  Double_t Rparam4 = 0.6;			//R of the jet 
//  Double_t Rparam6 = 0.6;			//R of the jet 
//  Double_t track_pTmin =atof(gSystem->Getenv("PTLEAD")); //minimal pT of the jet's leading track

  Double_t track_pTmin = 200.;
  TLorentzVector temp_track;

  event_weight = event->weight();
  Nevt++; 

  CrossSection sigma = generator()->eventHandler()->integratedXSec();
  Xsec = sigma/nanobarn;


  Jet_true_px.clear();
  Jet_true_py.clear();
  Jet_true_pz.clear();
  Jet_true_e.clear();

  Jet_reco_px.clear();
  Jet_reco_py.clear();
  Jet_reco_pz.clear();
  Jet_reco_e.clear();

//==========================================================================
//  Final state - missing ET + jets
//==========================================================================

  tPVector all_final_particles;
//  event->selectFinalState(inserter(all_final_particles));
  all_final_particles = event->getFinalState(); 
 
  vector<PseudoJet> jet_true_particles;
  vector<PseudoJet> jet_reco_particles;

  Double_t lead_track_true_pt = 0.0;
  Double_t lead_track_reco_pt = 0.0;

//  vector<PPtr> final_muons;

  Double_t PX, PY, PZ, En;

// loop over final state particles - select whatever you want!
  for (tPVector::const_iterator iter = all_final_particles.begin(); iter != all_final_particles.end(); iter++) 
  {
//  particle variables in ThePEG library is:
//  https://thepeg.hepforge.org/doxygen/classThePEG_1_1Particle.html

//    if( (fabs((*iter)->id()) != 12) && (fabs((*iter)->id()) != 14) && (fabs((*iter)->id()) != 16) && (fabs((*iter)->momentum().eta()) < 2.5) )
//   if ( ( (**iter).dataPtr()->charged() ) && (fabs((*iter)->momentum().eta()) < 2.5) && ((*iter)->momentum().perp() > 200. ) )
if ( (fabs((*iter)->id()) != 12) && (fabs((*iter)->id()) != 14) && (fabs((*iter)->id()) != 16) && (fabs((*iter)->momentum().eta()) < 2.5) && ((*iter)->momentum().perp() > 200. ) )
   {
// standard way how to make jets:
      PX = (**iter).momentum().x()/GeV;
      PY = (**iter).momentum().y()/GeV;
      PZ = (**iter).momentum().z()/GeV;
      En = (**iter).momentum().t()/GeV;
 
      jet_true_particles.push_back(PseudoJet(PX,PY,PZ,En));

      Double_t PT = (**iter).momentum().perp()/GeV;
		//cout<<"track PT: "<<PT<<endl;

      if(lead_track_true_pt < PT) lead_track_true_pt = PT;

      Double_t rnd = gRandom->Uniform(0,1);  
      if(efficiencyPP(PT) < rnd) continue;

      PT = smear_track_pt(PT);
		//cout<<"track PT smeared: "<<PT<<endl;
      temp_track.SetPtEtaPhiE(PT,(*iter)->momentum().eta(),(*iter)->momentum().phi(),En);

      PX = temp_track.Px();
      PY = temp_track.Py();
      PZ = temp_track.Pz();
      En = temp_track.E();

      jet_reco_particles.push_back(PseudoJet(PX,PY,PZ,En));

      if(lead_track_reco_pt < PT) lead_track_reco_pt = PT;


//  ... or we can make jets only from charged particles:
//  https://thepeg.hepforge.org/doxygen/classThePEG_1_1ParticleData.html

//      if ( (**iter).dataPtr()->charged() ) jet_particles.push_back(PseudoJet(PX,PY,PZ,En));
    }
   
//    if( fabs((*iter)->id()) == 13 ) final_muons.push_back( (*iter) );
   
  }
  

//  final_muons = sort_particles_pt(final_muons);
//  if(final_muons.size() < 2){ cout << "EVENT WITHOUT 2 MUONS!!" << endl; return;}
  RecombinationScheme recomb_scheme = E_scheme;
  fastjet::Strategy strategie = Best;

  JetDefinition jet_def_antiktR4(antikt_algorithm,Rparam4,recomb_scheme,strategie);
//  JetDefinition jet_def_antiktR6(antikt_algorithm,Rparam6,recomb_scheme,strategie);
//	AreaDefinition area_def(active_area_explicit_ghosts,GhostedAreaSpec(1.0,1,0.01));

 // ClusterSequenceArea cs_true(jet_true_particles, jet_def_antiktR4,area_def);
 // ClusterSequenceArea cs_reco(jet_reco_particles, jet_def_antiktR4,area_def);
ClusterSequence cs_true(jet_true_particles, jet_def_antiktR4);
ClusterSequence cs_reco(jet_reco_particles, jet_def_antiktR4);

  vector<PseudoJet> inclusive_true_jets = cs_true.inclusive_jets(5.);
  vector<PseudoJet> inclusive_reco_jets = cs_reco.inclusive_jets(5.);
  vector<PseudoJet> sorted_true_jets = sorted_by_pt(inclusive_true_jets);
  vector<PseudoJet> sorted_reco_jets = sorted_by_pt(inclusive_reco_jets);

 /*   vector<PseudoJet> Accepted_true_jets;
    vector<PseudoJet> Accepted_reco_jets;

	


  for(UInt_t i=0;i<sorted_true_jets.size();i++){
	vector<PseudoJet> constituents=sorted_by_pt(sorted_true_jets[i].constituents());
	double lead_track=0;
	if(constituents.size()>0) lead_track = constituents[0].perp();
    for(UInt_t j=0;j<constituents.size();j++){
      Double_t pt = constituents[j].perp(); 
		//if(pt>0.2)cout<<"true jet track pT:"<<pt<<endl;
    }
    if(lead_track > track_pTmin && (sorted_true_jets[i].area()>=0.2) && (fabs(sorted_true_jets[i].eta()) < 0.7 )) Accepted_true_jets.push_back( sorted_true_jets[i] );
  }

  for(UInt_t i = 0; i<Accepted_true_jets.size(); i++){
    h_Jet_true_pt->Fill(Accepted_true_jets[i].perp());
  }
  
  if(!sorted_reco_jets.size()>0)return;
  //cout<<"# of reco jets:"<<sorted_reco_jets.size()<<endl;
  for(UInt_t i=0;i<sorted_reco_jets.size();i++){
  //cout<<"jet #"<<i<<endl;
	vector<PseudoJet> constituents=sorted_by_pt(sorted_reco_jets[i].constituents());
	//cout<<"# of constituents:"<<constituents.size()<<endl;
	double lead_track=0;
	if(!constituents.size()>0) continue;
	lead_track = constituents[0].perp();
	//cout<<"pTlead:"<<lead_track<<endl;
    if(lead_track > track_pTmin && (sorted_reco_jets[i].area()>=0.2) && (fabs(sorted_reco_jets[i].eta()) < 0.7 )) Accepted_reco_jets.push_back( sorted_reco_jets[i] );
  }

  for(UInt_t i = 0; i<Accepted_reco_jets.size(); i++){
    h_Jet_reco_pt->Fill(Accepted_reco_jets[i].perp());
  }

*/

	//JET MATCHING
 /* for(UInt_t i = 0; i<sorted_true_jets.size(); i++){
    for(Int_t j = sorted_reco_jets.size()-1; j>=0; j--){
      if(DeltaR(sorted_true_jets[i].eta(),sorted_true_jets[i].phi(),sorted_reco_jets[j].eta(),sorted_reco_jets[j].phi()) < 0.6) {
	h_Jet_RM_pt->Fill(sorted_true_jets[i].perp(),sorted_reco_jets[j].perp(),1.0);
       sorted_reco_jets.erase(sorted_reco_jets.begin()+j);
      }	
    }
  }*/






// ==================================
// Event History Access
// ==================================

// depending on what to look for: parton-jet matching, interacting partons, origin of lepton (prompt/non-prompt), intermediate particle ...

/*

  vector<PPtr> PrimInter_med_vector = event->primarySubProcess()->intermediates();
  PPtr PrimInter_med_particle = PrimInter_med_vector[0];

  vector<PPtr> HME_out = event->primarySubProcess()->outgoing();

  PPair HME_in = event->primarySubProcess()->incoming();

  // MPI - additional hard processes, by default QCD2to2
  vector<PPtr> MPI_out;
  PPair MPI_in;
  Int_t NumOfInter_subprocesses = event->primaryCollision()->subProcesses().size();
  if( NumOfInter_subprocesses > 1 ){

    MPI_out = event->primaryCollision()->subProcesses()[1]->outgoing();
    MPI_in  = event->primaryCollision()->subProcesses()[1]->incoming();
  }


  Bool_t found;
//  vector<tcPPtr> HME_out_shuffled;

  for(Int_t it = HME_out.size()-1; it>=0; it--) {
    tcPPtr p = HME_out[it];   
    if( fabs(p->id()) == 13 ){
      found = false;
      while(!found){
        for(UInt_t it2 = 0; it2 < p->children().size(); it2++ ){
          tcPPtr pp = p->children()[it2]; 
  	  if(fabs(pp->id())==13){
	    if(pp->children().size() == 0){	// is final state
//	      HME_out_shuffled.push_back( pp );
//	      cout or do whatever you want;		
	      found=true;
	      break;
	    }else{
	      p = pp;
	      break;
	    }
	  }
        }
      }
      break;	// do this only for one particle, otherwise it does not work
    } // else HME_out.erase(HME_out.begin()+it); // erase neutrino; keep only muons in case of W decays!
  }



*/

// ==================================
// Event selection
// ==================================

/*
  Double_t muon1_pt, muon1_eta, muon1_phi, muon2_pt, muon2_eta, muon2_phi, muonpair_m, pair_px, pair_py, pair_pz, pair_e;


	muon1_pt  = final_muons[0]->momentum().perp()/1000.;
        muon1_eta = final_muons[0]->momentum().eta();
	muon1_phi = final_muons[0]->momentum().phi();
        muon2_pt  = final_muons[1]->momentum().perp()/1000.;
        muon2_eta = final_muons[1]->momentum().eta();
	muon2_phi = final_muons[1]->momentum().phi();	
	pair_px = final_muons[0]->momentum().x()/1000. + final_muons[1]->momentum().x()/1000.;
	pair_py = final_muons[0]->momentum().y()/1000. + final_muons[1]->momentum().y()/1000.;
	pair_pz = final_muons[0]->momentum().z()/1000. + final_muons[1]->momentum().z()/1000.;
	pair_e = final_muons[0]->momentum().e()/1000. + final_muons[1]->momentum().e()/1000.;

	muonpair_m = sqrt(pair_e*pair_e - pair_px*pair_px - pair_py*pair_py - pair_pz*pair_pz);


    if(    ( muon1_pt > 20. )
   	&& ( muon2_pt > 10. )
     	&& ( fabs(muon1_eta) < 2.5 )
     	&& ( fabs(muon2_eta) < 2.5 )
      ){

//  we need to remove lepton-induced jets
      for(Int_t i = sorted_R4_jets.size()-1; i>=0; i--)
      {
      
        if(  (DeltaR(sorted_R4_jets[i].eta(),sorted_R4_jets[i].phi(),muon1_eta, muon1_phi) < JetLepDRmin) 
	  || (DeltaR(sorted_R4_jets[i].eta(),sorted_R4_jets[i].phi(),muon2_eta, muon2_phi) < JetLepDRmin) )
        sorted_R4_jets.erase(sorted_R4_jets.begin()+i);
      }


// TTree filling

  Mu1_pt = muon1_pt;
  Mu1_eta = muon1_eta;
  Mu2_pt = muon2_pt;
  Mu2_eta = muon2_eta;
  MuMu_M = muonpair_m;
  if( sorted_R4_jets.size() > 0 ) Jet1_pt = sorted_R4_jets[0].perp(); else Jet1_pt = 0.0;

  strom->Fill();

// Histogram filling:

  h_Lep1_pt->Fill(muon1_pt,event_weight);
  h_Lep1_eta->Fill(muon1_eta,event_weight);

  h_Lep2_pt->Fill(muon2_pt,event_weight);
  h_Lep2_eta->Fill(muon2_eta,event_weight);

  h_lep_m->Fill(muonpair_m, event_weight);

  if( sorted_R4_jets.size() > 0 ) h_Jet1_Pt->Fill(sorted_R4_jets[0].perp(), event_weight); 

  
  } // end if accepted event
*/

//  if( lead_track_true_pt > track_pTmin){
  for(UInt_t i = 0; i < sorted_true_jets.size(); i++)
  {
    Jet_true_px.push_back(sorted_true_jets[i].px());
    Jet_true_py.push_back(sorted_true_jets[i].py());
    Jet_true_pz.push_back(sorted_true_jets[i].pz());
    Jet_true_e.push_back(sorted_true_jets[i].e());
  }
//}
//  if( lead_track_reco_pt > track_pTmin){
  for(UInt_t i = 0; i < sorted_reco_jets.size(); i++)
  {
    Jet_reco_px.push_back(sorted_reco_jets[i].px());
    Jet_reco_py.push_back(sorted_reco_jets[i].py());
    Jet_reco_pz.push_back(sorted_reco_jets[i].pz());
    Jet_reco_e.push_back(sorted_reco_jets[i].e());
  }
//}

  strom->Fill();

}


LorentzRotation Browser::transform(tcEventPtr event) const {
  return LorentzRotation();
  // Return the Rotation to the frame in which you want to perform the analysis.
}



void Browser::analyze(const tPVector & particles, double weight) {
  AnalysisHandler::analyze(particles);
  // Calls analyze() for each particle.
}


void Browser::analyze(tPPtr, double weight) {}

void Browser::dofinish() {
  AnalysisHandler::dofinish();


  //Scale_histograms();

  file_->Write();
  file_->Close();

}

void Browser::doinitrun() {
  AnalysisHandler::doinitrun();
  // *** ATTENTION *** histogramFactory().registerClient(this); // Initialize histograms.
  // *** ATTENTION *** histogramFactory().mkdirs("/SomeDir"); // Put histograms in specal directory.


  Nevt = 0;
  
  TString hist_name;
//  batch =atoi(gSystem->Getenv("BATCH")); //minimal pT of the jet's leading track
  //file_ = TFile::Open("HERWIG_simulace.root","RECREATE");
  //file_ = TFile::Open("HERWIG_data.root","RECREATE");
  //file_ = TFile::Open("HERWIG_test.root","RECREATE");
  file_ = TFile::Open("HERWIG_test2.root","RECREATE");

//  topDirectory = gDirectory;

  strom = new TTree("strom","strom");
  strom->Branch("event_weight",&event_weight,"event_weight/D");
  strom->Branch("Xsec",&Xsec,"Xsec/D");
  strom->Branch("Jet_true_px",&Jet_true_px);
  strom->Branch("Jet_true_py",&Jet_true_py);
  strom->Branch("Jet_true_pz",&Jet_true_pz);
  strom->Branch("Jet_true_e",&Jet_true_e);
  strom->Branch("Jet_reco_px",&Jet_reco_px);
  strom->Branch("Jet_reco_py",&Jet_reco_py);
  strom->Branch("Jet_reco_pz",&Jet_reco_pz);
  strom->Branch("Jet_reco_e",&Jet_reco_e);



/*
  strom->Branch("Mu1_eta",&Mu1_eta,"Mu1_eta/D");
  strom->Branch("Mu2_pt",&Mu2_pt,"Mu2_pt/D");
  strom->Branch("Mu2_eta",&Mu2_eta,"Mu2_eta/D");
  strom->Branch("MuMu_M",&MuMu_M,"MuMu_M/D");
  strom->Branch("Jet1_pt",&Jet1_pt,"Jet1_pt/D");


  const Int_t h_Pt_bins = 100;
  Double_t    h_Pt_min = 0.;
  Double_t    h_Pt_max = 100.;

  const Int_t h_M_bins = 300;
  Double_t    h_M_min = 0.;
  Double_t    h_M_max = 300.;

  const Int_t h_EtaL_bins = 100;
  Double_t    h_EtaL_min = -10.;
  Double_t    h_EtaL_max = 10.;
  
  
  hist_name = "Lep1_pt";
  h_Lep1_pt = new TH1D(hist_name,hist_name,h_Pt_bins,h_Pt_min,h_Pt_max);
  h_Lep1_pt->SetXTitle("p_{T} [GeV]");
  h_Lep1_pt->SetYTitle("d#sigma/dp_{T} [nb/GeV]");
  h_Lep1_pt->Sumw2();

  hist_name = "Lep2_pt";
  h_Lep2_pt = new TH1D(hist_name,hist_name,h_Pt_bins,h_Pt_min,h_Pt_max);
  h_Lep2_pt->SetXTitle("p_{T} [GeV]");
  h_Lep2_pt->SetYTitle("d#sigma/dp_{T} [nb/GeV]");
  h_Lep2_pt->Sumw2();
  
  hist_name = "Lep1_eta";
  h_Lep1_eta = new TH1D(hist_name,hist_name,h_EtaL_bins,h_EtaL_min,h_EtaL_max);
  h_Lep1_eta->SetXTitle("#eta");
  h_Lep1_eta->SetYTitle("d#sigma/d#eta [nb]");
  h_Lep1_eta->Sumw2(); 
  
  hist_name = "Lep2_eta";
  h_Lep2_eta = new TH1D(hist_name,hist_name,h_EtaL_bins,h_EtaL_min,h_EtaL_max);
  h_Lep2_eta->SetXTitle("#eta");
  h_Lep2_eta->SetYTitle("d#sigma/d#eta [nb]");
  h_Lep2_eta->Sumw2(); 
  
  hist_name = "lep_m";
  h_lep_m = new TH1D(hist_name,hist_name,h_M_bins,h_M_min,h_M_max);
  h_lep_m->SetXTitle("p_{T} [GeV]");
  h_lep_m->SetYTitle("d#sigma/dM [nb/GeV]");
  h_lep_m->Sumw2();

  
  hist_name = "Jet1_Pt";
  h_Jet1_Pt = new TH1D(hist_name,hist_name,h_Pt_bins,h_Pt_min,h_Pt_max);
  h_Jet1_Pt->SetXTitle("Jet1_Pt [GeV]");
  h_Jet1_Pt->SetYTitle("d#sigma/dp_{T} [nb/GeV]");
  h_Jet1_Pt->Sumw2();
*/
  
/*
  hist_name = "Jet_true_pt";
  h_Jet_true_pt = new TH1D(hist_name,hist_name,50,0.,50.);
  h_Jet_true_pt->SetXTitle("p_{T} [GeV]");
  h_Jet_true_pt->SetYTitle("d#sigma/dp_{T} [nb/GeV]");
  h_Jet_true_pt->Sumw2();

  hist_name = "Jet_reco_pt";
  h_Jet_reco_pt = new TH1D(hist_name,hist_name,50,0.,50.);
  h_Jet_reco_pt->SetXTitle("p_{T} [GeV]");
  h_Jet_reco_pt->SetYTitle("d#sigma/dp_{T} [nb/GeV]");
  h_Jet_reco_pt->Sumw2();

  hist_name = "Jet_RM_pt";
  h_Jet_RM_pt = new TH2D(hist_name,hist_name,50,0.,50.,50,0.,50.);
  h_Jet_RM_pt->Sumw2();


*/

}


IBPtr Browser::clone() const {
  return new_ptr(*this);
}

IBPtr Browser::fullclone() const {
  return new_ptr(*this);
}


// If needed, insert default implementations of virtual function defined
// in the InterfacedBase class here (using ThePEG-interfaced-impl in Emacs).



// *** Attention *** The following static variable is needed for the type
// description system in ThePEG. Please check that the template arguments
// are correct (the class and its base class), and that the constructor
// arguments are correct (the class name and the name of the dynamically
// loadable library where the class implementation can be found).
DescribeNoPIOClass<Browser,AnalysisHandler>
  describeMiraBrowser("Mira::Browser", "Browser.so");

void Browser::Init() {

  static ClassDocumentation<Browser> documentation
    ("There is no documentation for the Browser class");

}




//void Browser::Scale_histograms()
//{
/*
  CrossSection sigma = generator()->eventHandler()->integratedXSec();
  double Xsec = sigma/nanobarn;
  Xsec = Xsec/Nevt;
//  double sc;

 
  h_Lep1_pt->Scale(Xsec,"width");
  h_Lep2_pt->Scale(Xsec,"width");
  h_Lep1_eta->Scale(Xsec,"width");
  h_Lep2_eta->Scale(Xsec,"width");  
  h_lep_m->Scale(Xsec,"width");
  h_Jet1_Pt->Scale(Xsec,"width");
*/
// be careful with scaling!  "width" means scale it wrt bin width! -> Integral gives Xsection when hist->Integral("width") 
  
//}




/*
bool Browser::isParton(int id)
{
  bool dec = false;
  int partonIDs[9] = {1, 2, 3, 4, 5, 6, 7, 8, 21};
  for (int i=0; i<9; i++) {
    if (fabs(id) == partonIDs[i]) dec=true;
  }
  return dec;
}


bool Browser::isRemnant(int id)
{
  bool dec = false;
  if( (fabs(id) > 1000) && (fabs(id) < 6000) ) dec=true;
 
// remnant is actually PDGID 81 in Herwig

  return dec;
}
*/

vector<PPtr> Browser::sort_particles_pt(vector<PPtr> particles)
{
  Double_t temp_pt1, temp_pt2;
  bool swapped = true;
  Int_t treshold = Int_t(particles.size()-2);
  do{
    swapped = false;
    for (Int_t i = 0; i <= treshold; i++)
    {
      temp_pt1 = particles[i]->momentum().perp();
      temp_pt2 = particles[i+1]->momentum().perp();
      if( temp_pt1 < temp_pt2 ) 
      { 
        swap(particles[i], particles[i+1] );
        swapped = true;
      }
    }
  } while (swapped == true);
  return particles;
}


vector<tcPPtr> Browser::sort_particles_pt(vector<tcPPtr> particles)
{
  Double_t temp_pt1, temp_pt2;
  bool swapped = true;
  Int_t treshold = Int_t(particles.size()-2);
  do{
    swapped = false;
    for (Int_t i = 0; i <= treshold; i++)
    {
      temp_pt1 = particles[i]->momentum().perp();
      temp_pt2 = particles[i+1]->momentum().perp();
      if( temp_pt1 < temp_pt2 ) 
      { 
        swap(particles[i], particles[i+1] );
        swapped = true;
      }
    }
  } while (swapped == true);
  return particles;
}


vector<Lorentz5Momentum> Browser::sort_particles_pt(vector<Lorentz5Momentum> particles)
{
  Double_t temp_pt1, temp_pt2;
  bool swapped = true;
  Int_t treshold = Int_t(particles.size()-2);
  do{
    swapped = false;
    for (Int_t i = 0; i <= treshold; i++)
    {
      temp_pt1 = particles[i].perp();
      temp_pt2 = particles[i+1].perp();
      if( temp_pt1 < temp_pt2 ) 
      { 
        swap(particles[i], particles[i+1] );
        swapped = true;
      }
    }
  } while (swapped == true);
  return particles;
}



Double_t Browser::DeltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2){
  Double_t deta = eta1-eta2;
  Double_t dphi = TVector2::Phi_mpi_pi(phi1-phi2);
  
  
  return TMath::Sqrt( deta*deta+dphi*dphi );
}

Double_t Browser::efficiencyPP(Double_t pt)
{
   if(pt>9.9)pt=9.9;
//   TF1* f_Efficiency = new TF1("f_EfficiencyCent",Eff_track_rec_function,0,10.0,3);
//   f_Efficiency->SetParameters(9.06946e-01,1.45242e-01,2.87409e+00);
//   Double_t eff=f_Efficiency->Eval(pt);
    Double_t y;
    Double_t A =9.3e-01;
    Double_t B =1.5e-01;
    Double_t C =2.9e+00;
    y=A*(exp(-pow(B/pt,C)));
   return y;
}
/*
Double_t Browser::Eff_track_rec_function(Double_t* x,Double_t* par)
{
    // Track reconstruction efficiency parametrization
    Double_t pt,y;
    Double_t A =9.06946e-01;
    Double_t B =1.45242e-01;
    Double_t C =2.87409e+00;
    pt=x[0];
    y=A*(exp(-pow(B/pt,C)));
    return y;
}
*/
Double_t Browser::smear_track_pt(Double_t pt)
{
//  TF1* fsmear=new TF1("fsmear", gaus,  0., 100.,3);
  Double_t sigma = 0.01*pt*pt;
//  fsmear->SetParameters(1.,pt,sigma); //set normalization
  return gRandom->Gaus(pt,sigma);

}


