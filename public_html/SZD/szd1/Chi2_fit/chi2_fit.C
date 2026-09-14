// comparison of Chi2 root and by hand
// fitting of four numbers (bins) by one value; error matters!



  UInt_t N_hits;
  vector<Double_t> x_position, x_error;
  const Double_t pi = TMath::Pi();

  const Double_t Xmin = 1.0;
  const Double_t Xmax = 5.0;


void chi2_fit(){

  x_position.clear(); 
  x_position.push_back(0.42);
  x_position.push_back(0.38);
  x_position.push_back(0.32);
  x_position.push_back(0.33);
  x_error.clear(); 
  x_error.push_back(0.06);
  x_error.push_back(0.08);
  x_error.push_back(0.07);
  x_error.push_back(0.05);

//  or fixed-size array
//  float y[4]={0.42,0.38,0.32,0.33};
//  float sigma[4]={0.06,0.08,0.07,0.05};

  Int_t  grid_x_size = 100;

  const Int_t nbins = 4;
  Double_t bins[nbins+1]={1.0,1.5,2.0,3.0,5.0};

  TH1D* h_1=new TH1D("h_1","h_1",nbins,bins);
  for(int binx=1; binx<=nbins; binx++){
    h_1->SetBinContent(binx,x_position[binx-1]);
    h_1->SetBinError(binx,x_error[binx-1]);
  }

// 1) by hand:
  Double_t CHI2;
  Double_t c;
  Double_t MINCHI2 = 10000;
  Double_t BESTC = 0.;
  for(int ci=0; ci<=grid_x_size; ci++){
  CHI2=0;
  c= 0.32 + (0.42-0.32)/grid_x_size*ci;
    for(int binx=1; binx<=nbins; binx++){
      CHI2 = CHI2 + ( ( (x_position[binx-1] - c)*(x_position[binx-1]-c) )/ (x_error[binx-1]*x_error[binx-1]) );
    }
  if(MINCHI2>CHI2){ MINCHI2 = CHI2; BESTC = c; }
 
  }
  

cout << "by hand: " << BESTC << "  with Chi2 " << MINCHI2 << endl;

// 2) root default fit

  TF1* f1=new TF1("f1","[0]",0,4);
  f1->SetParameter(0,0.5);

  h_1->Draw("");
  h_1->Fit(f1);

cout <<  "default: " << f1->GetParameter(0) << "   by hand: " << BESTC << endl;

cout << " Chi2 default:  " <<  f1->GetChisquare()  << "  by hand: "  << MINCHI2 <<endl;
cout << "NDF is number of bins - 1 = 3; check root: " << f1->GetNDF() << endl;


}




