



  UInt_t N_hits;
  vector<Double_t> x_position;
  const Double_t pi = TMath::Pi();
  const Double_t e_const = TMath::E();


  const Double_t Xmin = 0;
  const Double_t Xmax = 10.0;
  const Double_t Ymin = 0;
  const Double_t Ymax = 10.0;

Double_t llhood( Double_t x, Double_t y)
{

  Double_t llh=0;
  for(int k=0; k<N_hits; k++)
  {
// vzdy je dulezite si uvedomit, jak mame sestaven ten likelihood - ted to je 1/XX -> hledame maximum (z negativnich hodnot)
//    ale jde to samo prevezt jen na XX a tedy hledani minima...
    Double_t breit=(y)/(y*y+(x_position[k]-x)*(x_position[k]-x));		// zde nemusi byt konstanta pi ani nic jineho - jde nam o extrem funkce...
    llh+=TMath::Log(breit);
  }
  return llh;
}


void majak_mira(){


  x_position.clear(); 

// nacist data z root souboru

  TFile fin1("hits.root");
  TVectorD* temp_vec = (TVectorD*)fin1.Get("x_position");
  N_hits = temp_vec->GetNoElements();

  for(UInt_t i =0; i< N_hits;i++)  x_position.push_back( (*temp_vec)[i] );
  fin1.Close();  

// nacist data z text souboru

/*
  TTree *MyTree = new TTree("MyTree", "MyTree");

  MyTree->ReadFile("hits.dat", "x_pos");
  
  Float_t temp_x;
  MyTree->SetBranchAddress("x_pos",&temp_x);
  
  N_hits = MyTree->GetEntries();

  for(UInt_t i=0; i<N_hits;i++){
    MyTree->GetEntry(i);
    x_position.push_back( (Double_t)temp_x );
  }
*/


  Double_t max=-1000000;
  Double_t maxx;
  Double_t maxy;

  Int_t  grid_x_size = 1000;
  Int_t  grid_y_size = 1000;

  double Xbin_edge_shift = Xmax/grid_x_size*0.5;
  double Ybin_edge_shift = Ymax/grid_y_size*0.5;

  TH2D* mapa=new TH2D("mapa","mapa;x;y",grid_x_size,(Xmin+Xbin_edge_shift),(Xmax+Xbin_edge_shift),grid_y_size,(Ymin+Ybin_edge_shift),(Ymax+Ybin_edge_shift));


  TH1D* xslice_yconst=new TH1D("xslice_yconst","xslice_yconst;x;likelihood",grid_x_size,(Xmin+Xbin_edge_shift),(Xmax+Xbin_edge_shift));
  
  TH1D* yslice_xconst=new TH1D("yslice_xconst","yslice_xconst;y;likelihood",grid_y_size,(Ymin+Ybin_edge_shift),(Ymax+Ybin_edge_shift));

  TH1D* xslice=new TH1D("xslice","xslice;x;likelihood",grid_x_size,(Xmin+Xbin_edge_shift),(Xmax+Xbin_edge_shift));


  TH1D* xdistr=new TH1D("xdistr","xdistr;x;hits",grid_x_size,(Xmin+Xbin_edge_shift),(Xmax+Xbin_edge_shift));
  for(int k=0; k<N_hits; k++)
  {
    xdistr->Fill(x_position[k],1.0);
  }

  for(int binx=1; binx<=grid_x_size; binx++){
      cout << " binx " << binx << '\r';

    for(int biny=1; biny<=grid_y_size; biny++){

//      int biny = 100;

      double xp=(binx)*Xmax/grid_x_size;
      double yp=(biny)*Ymax/grid_y_size;

      double llhd=llhood(xp,yp);
//      cout<<"filling  x:"<<xp<<" y: "<<yp<<" likelyhood: "<<llhd<<endl;
      if(llhd>max){
        max=llhd;
        maxx=xp;
        maxy=yp;
      } 
     xslice->Fill(xp,llhd);	// do not care what yp	

     mapa->Fill(xp,yp, llhd);
      
      if (yp == 0.7) {  xslice_yconst->Fill(xp,llhd); }
      if (xp == 3.5) {  yslice_xconst->Fill(yp,llhd); }

    }
  }

  Double_t total =0.; 
  for(int k=0; k<N_hits; k++)
  {
    total += x_position[k];
  }
  total=total/N_hits; 

  cout<<endl;
  cout<<" max-likely x: "<<maxx<<"  y: "<<maxy<<"  likelyhood: "<<max<<endl;
  cout<<" average x: "<<total<< endl;


// alternativa k ziskani x projekce:
//  TH1D *xslice = mapa->ProjectionX("xslice");


  TCanvas *c1 = new TCanvas("c1","c1",10,10,1000,600);
//  mapa->Draw("COLZ");
  
  
// CONTOUR  
// find minimum LL value
double maxLL = mapa->GetMaximum();

// 1-sigma contour for 2 parameters (Δ(-logL) = 1.15)
double level = maxLL - 9;

mapa->SetContour(1);
mapa->SetContourLevel(0, level);

mapa->Draw("COLZ");     // draw heat map
mapa->Draw("CONT3 SAME");  // draw contour line

// optional: make contour thicker & colored
gStyle->SetLineWidth(3);
gStyle->SetLineColor(kBlack);

  
  
  
  TCanvas *c2 = new TCanvas("c2","c2",10,10,1000,600);
  xslice->Draw("hist");

  TCanvas *c3 = new TCanvas("c3","c3",10,10,1000,600);
  xslice_yconst->Draw("hist");

  TCanvas *c4 = new TCanvas("c4","c4",10,10,1000,600);
  yslice_xconst->Draw("hist");

  TCanvas *c5 = new TCanvas("c5","c5",10,10,1000,600);
  xdistr->Draw("hist");

/*
  xslice_yconst->Scale(-1*xdistr->Integral()/xslice_yconst->Integral());
  for(int binx=1; binx<=grid_x_size; binx++){
    xslice_yconst->SetBinContent(binx,xslice_yconst->GetBinContent(binx)+50);
  }
  xslice_yconst->Scale(xdistr->Integral()/xslice_yconst->Integral());
  xslice_yconst->Draw("hist,same");
*/


// NEW - wrt winter-HW 

// the number 1 in the option stands for X axis, 2 for Y axis

    double x_lower_error = mapa->GetXaxis()->GetBinCenter(mapa->FindFirstBinAbove(mapa->GetMaximum() -0.5,1));   
    double y_lower_error = mapa->GetYaxis()->GetBinCenter(mapa->FindFirstBinAbove(mapa->GetMaximum() -0.5,2));

    double x_upper_error = mapa->GetXaxis()->GetBinCenter(mapa->FindLastBinAbove(mapa->GetMaximum() -0.5,1)); 
    double y_upper_error = mapa->GetYaxis()->GetBinCenter(mapa->FindLastBinAbove(mapa->GetMaximum() -0.5,2)); 

// NOTE: these values ARE NOT sigmas; these are mean - sigma, mean + sigma;

cout << "2D: x_lower_error " << x_lower_error << "  x_upper_error " << x_upper_error << endl;

cout << "2D: y_lower_error " << y_lower_error << "  y_upper_error " << y_upper_error << endl;



    double x_lower_error_1D = xslice_yconst->GetXaxis()->GetBinCenter(xslice_yconst->FindFirstBinAbove(xslice_yconst->GetMaximum() -0.5));   
    double x_upper_error_1D = xslice_yconst->GetXaxis()->GetBinCenter(xslice_yconst->FindLastBinAbove(xslice_yconst->GetMaximum() -0.5));


cout << "1D: x_lower_error (yconst) " << x_lower_error_1D << "  x_upper_error " << x_upper_error_1D << endl;


    double x_lower_error_1D_2 = xslice->GetXaxis()->GetBinCenter(xslice->FindFirstBinAbove(xslice->GetMaximum() -0.5));   
    double x_upper_error_1D_2 = xslice->GetXaxis()->GetBinCenter(xslice->FindLastBinAbove(xslice->GetMaximum() -0.5));


cout << "1D: x_lower_error " << x_lower_error_1D_2 << "  x_upper_error " << x_upper_error_1D_2 << endl;



    double y_lower_error_1D = yslice_xconst->GetXaxis()->GetBinCenter(yslice_xconst->FindFirstBinAbove(yslice_xconst->GetMaximum() -0.5));   
    double y_upper_error_1D = yslice_xconst->GetXaxis()->GetBinCenter(yslice_xconst->FindLastBinAbove(yslice_xconst->GetMaximum() -0.5));


cout << "1D: y_lower_error (yconst) " << y_lower_error_1D << "  y_upper_error " << y_upper_error_1D << endl;




}

