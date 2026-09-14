

//jak daleko musi Newton sedet, aby na nej nespadlo jablko?

void newton(int counts=50000, float sigma=1.5, int bins=100)
{
	TDatime dt;
	UInt_t curtime = dt.Get();
	UInt_t seed = curtime;
	TRandom3 *rnd= new TRandom3(seed);
	float maxR=0;
	TH2D* h2=new TH2D("h2","h2",bins,-6.0,6.0,bins,-6.0,6.0);
	for(int i = 0; i<counts; i++)
	{
		float x=rnd->Gaus(0,sigma);
		float y=rnd->Gaus(0,sigma);
		float r=TMath::Sqrt(x*x+y*y);
		if(r>maxR)maxR=r;
		h2->Fill(x,y);
	}

	h2->Draw("COLZ");


  // dont forget underflow / overflow
  double i_full = h2->Integral(0,bins+1,0,bins+1);		
  double part = i_full*0.998;
  double i_part = 0.0;
  double range = 5.1;
  double step = 12./bins;
  
  while(i_part < part){	    //here uncomment


	// make a "circle"
	const Int_t n = 30;
	Double_t x[n+1],y[n+1];
	Double_t rcut = range;
	Double_t dphi = TMath::TwoPi()/n;
	for (Int_t i=0;i<n;i++) {
	  x[i] = rcut*TMath::Cos(i*dphi);
	  y[i] = rcut*TMath::Sin(i*dphi);
	}
	x[n] = x[0]; y[n] = y[0];
	TCutG *mycut = new TCutG("mycut",n+1,x,y);
	mycut->SetLineWidth(2);
	mycut->Draw("same");			//here comment-out

	//h2->Draw("surf1 [mycut]");
	//h2->Draw("COLZ [mycut]");

	i_part = mycut->IntegralHist(h2);
	cout << "Integral %\t" << i_part/i_full << "\t Range \t" << range << endl;
  
	range += step;  

  } 	 //here uncomment

	cout << "Int " << i_full << "  i_part" << i_part << endl;
	cout<<"max R:"<<maxR<<endl;


	
}  //here uncomment

//  TRY v GUI canvasu: SetShowProjectionX/Y




