//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Jul 20 17:20:29 2018 by ROOT version 6.08/06
// from TTree strom/strom
// found on file: HERWIG_test.root
//////////////////////////////////////////////////////////

#ifndef HBOM_h
#define HBOM_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"

class HBOM {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Double_t        event_weight;
   Double_t        Xsec;
   vector<double>  *Jet_true_px;
   vector<double>  *Jet_true_py;
   vector<double>  *Jet_true_pz;
   vector<double>  *Jet_true_e;
   vector<double>  *Jet_reco0_px;
   vector<double>  *Jet_reco0_py;
   vector<double>  *Jet_reco0_pz;
   vector<double>  *Jet_reco0_e;
   vector<double>  *Jet_reco1_px;
   vector<double>  *Jet_reco1_py;
   vector<double>  *Jet_reco1_pz;
   vector<double>  *Jet_reco1_e;
   vector<double>  *Jet_reco2_px;
   vector<double>  *Jet_reco2_py;
   vector<double>  *Jet_reco2_pz;
   vector<double>  *Jet_reco2_e;
   vector<double>  *Jet_reco3_px;
   vector<double>  *Jet_reco3_py;
   vector<double>  *Jet_reco3_pz;
   vector<double>  *Jet_reco3_e;
   vector<double>  *Jet_reco4_px;
   vector<double>  *Jet_reco4_py;
   vector<double>  *Jet_reco4_pz;
   vector<double>  *Jet_reco4_e;
   vector<double>  *Jet_reco5_px;
   vector<double>  *Jet_reco5_py;
   vector<double>  *Jet_reco5_pz;
   vector<double>  *Jet_reco5_e;

   // List of branches
   TBranch        *b_event_weight;   //!
   TBranch        *b_Xsec;   //!
   TBranch        *b_Jet_true_px;   //!
   TBranch        *b_Jet_true_py;   //!
   TBranch        *b_Jet_true_pz;   //!
   TBranch        *b_Jet_true_e;   //!
   TBranch        *b_Jet_reco0_px;   //!
   TBranch        *b_Jet_reco0_py;   //!
   TBranch        *b_Jet_reco0_pz;   //!
   TBranch        *b_Jet_reco0_e;   //!
   TBranch        *b_Jet_reco1_px;   //!
   TBranch        *b_Jet_reco1_py;   //!
   TBranch        *b_Jet_reco1_pz;   //!
   TBranch        *b_Jet_reco1_e;   //!
   TBranch        *b_Jet_reco2_px;   //!
   TBranch        *b_Jet_reco2_py;   //!
   TBranch        *b_Jet_reco2_pz;   //!
   TBranch        *b_Jet_reco2_e;   //!
   TBranch        *b_Jet_reco3_px;   //!
   TBranch        *b_Jet_reco3_py;   //!
   TBranch        *b_Jet_reco3_pz;   //!
   TBranch        *b_Jet_reco3_e;   //!
   TBranch        *b_Jet_reco4_px;   //!
   TBranch        *b_Jet_reco4_py;   //!
   TBranch        *b_Jet_reco4_pz;   //!
   TBranch        *b_Jet_reco4_e;   //!
   TBranch        *b_Jet_reco5_px;   //!
   TBranch        *b_Jet_reco5_py;   //!
   TBranch        *b_Jet_reco5_pz;   //!
   TBranch        *b_Jet_reco5_e;   //!

   HBOM(TTree *tree=0);
   virtual ~HBOM();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
   virtual Double_t DeltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2);
};

#endif

#ifdef HBOM_cxx
HBOM::HBOM(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("HERWIG_test.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("HERWIG_test.root");
      }
      f->GetObject("strom",tree);

   }
   Init(tree);
}

HBOM::~HBOM()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t HBOM::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t HBOM::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void HBOM::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   Jet_true_px = 0;
   Jet_true_py = 0;
   Jet_true_pz = 0;
   Jet_true_e = 0;
   Jet_reco0_px = 0;
   Jet_reco0_py = 0;
   Jet_reco0_pz = 0;
   Jet_reco0_e = 0;
   Jet_reco1_px = 0;
   Jet_reco1_py = 0;
   Jet_reco1_pz = 0;
   Jet_reco1_e = 0;
   Jet_reco2_px = 0;
   Jet_reco2_py = 0;
   Jet_reco2_pz = 0;
   Jet_reco2_e = 0;
   Jet_reco3_px = 0;
   Jet_reco3_py = 0;
   Jet_reco3_pz = 0;
   Jet_reco3_e = 0;
   Jet_reco4_px = 0;
   Jet_reco4_py = 0;
   Jet_reco4_pz = 0;
   Jet_reco4_e = 0;
   Jet_reco5_px = 0;
   Jet_reco5_py = 0;
   Jet_reco5_pz = 0;
   Jet_reco5_e = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("event_weight", &event_weight, &b_event_weight);
   fChain->SetBranchAddress("Xsec", &Xsec, &b_Xsec);
   fChain->SetBranchAddress("Jet_true_px", &Jet_true_px, &b_Jet_true_px);
   fChain->SetBranchAddress("Jet_true_py", &Jet_true_py, &b_Jet_true_py);
   fChain->SetBranchAddress("Jet_true_pz", &Jet_true_pz, &b_Jet_true_pz);
   fChain->SetBranchAddress("Jet_true_e", &Jet_true_e, &b_Jet_true_e);
   fChain->SetBranchAddress("Jet_reco0_px", &Jet_reco0_px, &b_Jet_reco0_px);
   fChain->SetBranchAddress("Jet_reco0_py", &Jet_reco0_py, &b_Jet_reco0_py);
   fChain->SetBranchAddress("Jet_reco0_pz", &Jet_reco0_pz, &b_Jet_reco0_pz);
   fChain->SetBranchAddress("Jet_reco0_e", &Jet_reco0_e, &b_Jet_reco0_e);
   fChain->SetBranchAddress("Jet_reco1_px", &Jet_reco1_px, &b_Jet_reco1_px);
   fChain->SetBranchAddress("Jet_reco1_py", &Jet_reco1_py, &b_Jet_reco1_py);
   fChain->SetBranchAddress("Jet_reco1_pz", &Jet_reco1_pz, &b_Jet_reco1_pz);
   fChain->SetBranchAddress("Jet_reco1_e", &Jet_reco1_e, &b_Jet_reco1_e);
   fChain->SetBranchAddress("Jet_reco2_px", &Jet_reco2_px, &b_Jet_reco2_px);
   fChain->SetBranchAddress("Jet_reco2_py", &Jet_reco2_py, &b_Jet_reco2_py);
   fChain->SetBranchAddress("Jet_reco2_pz", &Jet_reco2_pz, &b_Jet_reco2_pz);
   fChain->SetBranchAddress("Jet_reco2_e", &Jet_reco2_e, &b_Jet_reco2_e);
   fChain->SetBranchAddress("Jet_reco3_px", &Jet_reco3_px, &b_Jet_reco3_px);
   fChain->SetBranchAddress("Jet_reco3_py", &Jet_reco3_py, &b_Jet_reco3_py);
   fChain->SetBranchAddress("Jet_reco3_pz", &Jet_reco3_pz, &b_Jet_reco3_pz);
   fChain->SetBranchAddress("Jet_reco3_e", &Jet_reco3_e, &b_Jet_reco3_e);
   fChain->SetBranchAddress("Jet_reco4_px", &Jet_reco4_px, &b_Jet_reco4_px);
   fChain->SetBranchAddress("Jet_reco4_py", &Jet_reco4_py, &b_Jet_reco4_py);
   fChain->SetBranchAddress("Jet_reco4_pz", &Jet_reco4_pz, &b_Jet_reco4_pz);
   fChain->SetBranchAddress("Jet_reco4_e", &Jet_reco4_e, &b_Jet_reco4_e);
   fChain->SetBranchAddress("Jet_reco5_px", &Jet_reco5_px, &b_Jet_reco5_px);
   fChain->SetBranchAddress("Jet_reco5_py", &Jet_reco5_py, &b_Jet_reco5_py);
   fChain->SetBranchAddress("Jet_reco5_pz", &Jet_reco5_pz, &b_Jet_reco5_pz);
   fChain->SetBranchAddress("Jet_reco5_e", &Jet_reco5_e, &b_Jet_reco5_e);
   Notify();
}

Bool_t HBOM::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void HBOM::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t HBOM::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef HBOM_cxx
