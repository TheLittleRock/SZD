// -*- C++ -*-
#ifndef Mira_Browser_H
#define Mira_Browser_H
//
// This is the declaration of the Browse class.
//

#include "ThePEG/Handlers/AnalysisHandler.h"
#include "HepMC/GenParticle.h"
#include "HepMC/GenVertex.h"
#include "HepMC/GenRanges.h"
#include "HepMC/IO_GenEvent.h"
#include "HepMC/IO_AsciiParticles.h"
#include "HepMC/IO_BaseClass.h"
#include "ThePEG/Interface/ClassDocumentation.h"
#include "ThePEG/Interface/Parameter.h"
#include "ThePEG/Interface/Switch.h"
#include "ThePEG/EventRecord/Event.h"
#include "ThePEG/Repository/EventGenerator.h"
#include "ThePEG/Persistency/PersistentOStream.h"
#include "ThePEG/Persistency/PersistentIStream.h"
#include "ThePEG/Config/HepMCHelper.h"

#include "ThePEG/Vectors/Lorentz5Vector.h"
#include "ThePEG/Repository/CurrentGenerator.h"
#include "ThePEG/Repository/EventGenerator.h"
#include "Herwig/Shower/ShowerHandler.h" 
#include "Herwig/UnderlyingEvent/MPIHandler.h" 

#include "Herwig/Hadronization/Cluster.h"
#include "ThePEG/EventRecord/Particle.h"

#include <stdlib.h>     /* srand, rand */

#include "TH2D.h"
#include "TProfile.h"
#include "TFile.h"
#include <stdio.h>
#include <cmath>
#include <TH1.h>
#include "TTree.h"
#include "TRandom.h"
//#include "TF.h"
#include "TF1.h"

#include <TSystem.h>
#include <iostream>
#include <fstream>
#include "TDirectory.h"
#include "TLorentzVector.h"
#include "TApplication.h"


#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"


//#include "LHAPDF/LHAPDF.h"


namespace Mira {

using namespace ThePEG;

/**
 * Here is the documentation of the Browser class.
 *
 * @see \ref BrowserInterfaces "The interfaces"
 * defined for Browser.
 */
class Browser: public AnalysisHandler {

public:

  /** @name Standard constructors and destructors. */
  //@{
  /**
   * The default constructor.
   */
  Browser();

  /**
   * The destructor.
   */
  virtual ~Browser();
  //@}

public:

  /** @name Virtual functions required by the AnalysisHandler class. */
  //@{
  /**
   * Analyze a given Event. Note that a fully generated event
   * may be presented several times, if it has been manipulated in
   * between. The default version of this function will call transform
   * to make a lorentz transformation of the whole event, then extract
   * all final state particles and call analyze(tPVector) of this
   * analysis object and those of all associated analysis objects. The
   * default version will not, however, do anything on events which
   * have not been fully generated, or have been manipulated in any
   * way.
   * @param event pointer to the Event to be analyzed.
   * @param ieve the event number.
   * @param loop the number of times this event has been presented.
   * If negative the event is now fully generated.
   * @param state a number different from zero if the event has been
   * manipulated in some way since it was last presented.
   */
  virtual void analyze(tEventPtr event, long ieve, int loop, int state);

  /**
   * Return a LorentzTransform which would put the event in the
   * desired Lorentz frame.
   * @param event a pointer to the Event to be considered.
   * @return the LorentzRotation used in the transformation.
   */
  virtual LorentzRotation transform(tcEventPtr event) const;

  /**
   * Analyze the given vector of particles. The default version calls
   * analyze(tPPtr) for each of the particles.
   * @param particles the vector of pointers to particles to be analyzed
   * @param weight the weight of the current event.
   */
  virtual void analyze(const tPVector & particles, double weight);

  /**
   * Analyze the given particle.
   * @param particle pointer to the particle to be analyzed.
   * @param weight the weight of the current event.
   */
  virtual void analyze(tPPtr particle, double weight);
  //@}

protected:

  /**
   * Initialize this object. Called in the run phase just before
   * a run begins.
   */
  virtual void doinitrun();

  /**
   * Finalize this object. Called in the run phase just after a
   * run has ended. Used eg. to write out statistics.
   */
  virtual void dofinish();


public:

  /**
   * The standard Init function used to initialize the interfaces.
   * Called exactly once for each class by the class description system
   * before the main function starts or
   * when this class is dynamically loaded.
   */
  static void Init();

protected:

  /** @name Clone Methods. */
  //@{
  /**
   * Make a simple clone of this object.
   * @return a pointer to the new object.
   */
  virtual IBPtr clone() const;

  /** Make a clone of this object, possibly modifying the cloned object
   * to make it sane.
   * @return a pointer to the new object.
   */
  virtual IBPtr fullclone() const;
  //@}


// If needed, insert declarations of virtual function defined in the
// InterfacedBase class here (using ThePEG-interfaced-decl in Emacs).


private:

  /**
   * The assignment operator is private and must never be called.
   * In fact, it should not even be implemented.
   */
  Browser & operator=(const Browser &);

//  std::ofstream* ofs;
  TFile * file_;  
//  TDirectory * topDirectory;
  TTree * strom;


  Int_t Nevt;
  Int_t batch;

  Double_t event_weight;
  Double_t Xsec;

  vector<Double_t> Jet_true_px;
  vector<Double_t> Jet_true_py;
  vector<Double_t> Jet_true_pz;
  vector<Double_t> Jet_true_e;


  vector<Double_t> Jet_reco_px;
  vector<Double_t> Jet_reco_py;
  vector<Double_t> Jet_reco_pz;
  vector<Double_t> Jet_reco_e;


/*
  Double_t  Mu1_pt;
  Double_t  Mu1_eta;
  Double_t  Mu2_pt;
  Double_t  Mu2_eta;
  Double_t  MuMu_M;
  Double_t  Jet1_pt;
*/
/*  
  TH1D *h_Lep1_pt;
  TH1D *h_Lep2_pt;
  TH1D *h_Lep1_eta;
  TH1D *h_Lep2_eta;
  TH1D *h_lep_m;
  TH1D *h_Jet1_Pt;
  */

  //TH1D* h_Jet_true_pt;
  //TH1D* h_Jet_reco_pt;
  //TH2D* h_Jet_RM_pt;

  //void Scale_histograms();
  vector<PPtr> sort_particles_pt(vector<PPtr> particles);
  vector<tcPPtr> sort_particles_pt(vector<tcPPtr> particles);
  vector<Lorentz5Momentum> sort_particles_pt(vector<Lorentz5Momentum> particles);
  Double_t DeltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2);

  Double_t smear_track_pt(Double_t pt);
  Double_t efficiencyPP(Double_t pt);
//  Double_t Eff_track_rec_function(Double_t* x,Double_t* par);

};

}

#endif /* Mira_Browser_H */
