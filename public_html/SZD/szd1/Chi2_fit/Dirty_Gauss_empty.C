TH1D* peak_generator(float mu=100, float sigma=10, int N_signal=500, int N_bg=2500, bool remove_negative=1)
{

	Double_t nbins=100;
	
	//signal
	TF1* fce1=new TF1("fce1","[0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2]))",0,200);
	fce1->SetParameter(0,1); //A
	fce1->SetParameter(1,mu); //mu
	fce1->SetParameter(2,sigma); //sigma

	//background
	TF1* fce2=new TF1("fce2","[0]*x+[1]",0,200);
//	fce2->SetParameter(0,-0.05); //a
	fce2->SetParameter(0,0.0); //a		//konstantni background
	fce2->SetParameter(1,100); //b
   
	TCanvas *c1 = new TCanvas("c1","signal+background",10,10,900,600);
	TH1D *hsb=new TH1D("hsb","hsb",nbins,0,200);
 
	//generate signal + background sample (e.g. invariant mass of unlike-sign pairs of kaons and pions)
	for(int n=0; n<N_signal;n++)
	{
		//first generate the signal...
		double rnd=fce1->GetRandom();
		hsb->Fill(rnd);
	} 
	for(int n=0; n<N_bg;n++)
	{
		//...and then generate the background
		double rnd=fce2->GetRandom();
		hsb->Fill(rnd);
	}
	hsb->SetTitle("signal+background (ULS)");
	hsb->Draw();

	TCanvas *c2 = new TCanvas("c2","background (LS)",10,10,900,600);
	TH1D *hbg=new TH1D("hbg","hbg",nbins,0,200);
	
	//generate pure background sample (eg. using like-sign sample)
	for(int n=0; n<N_bg;n++)
	{
		double rnd=fce2->GetRandom();
		hbg->Fill(rnd);
	}
	hbg->SetTitle("background (LS)");
	hbg->Draw();
		
	//subtract background form signal+background
	TCanvas *c3 = new TCanvas("c3","signal after BG subtraction",10,10,900,600);
	TH1D *hsg=(TH1D*)hsb->Clone("hsg");
	hsg->Add(hbg,-1);

	//remove negative values
	if(remove_negative)
	{
		for(int bn=1; bn<=hsg->GetNbinsX();bn++)
		{
			float val=hsg->GetBinContent(bn);
			if(val<0)hsg->SetBinContent(bn,0);
		}
	}
	hsg->SetTitle("signal after BG subtraction");
	hsg->Draw("e");

	//open file and save
//	TFile* fout=new TFile("output_gauss.root","RECREATE");
//	fout->cd();
//	hsb->Write();
//	hbg->Write();
//	hsg->Write();
//	fout->Close();

 	return hsg;
}
 

float lhood(TH1D* hdata, float a, float b, TF1* f1)
{
	f1->SetParameter(0,a);
	f1->SetParameter(1,b);
	float logLhood=0;
	int npoints=hdata->GetNbinsX();
	for(int i=1; i<=npoints; i++) //loop over histogram bins
	{
		//read x data and their counts from histogram
		float x=hdata->GetBinCenter(i);
		int n=hdata->GetBinContent(i);
		float width=hdata->GetBinWidth(i);
		float prob=(f1->Eval(x)); 

		logLhood+=n*TMath::Log(prob);
	}
	return logLhood;
}


float lhood_binned(TH1D* hdata, float a, float b, TF1* f1)
{
	f1->SetParameter(0,a);
	f1->SetParameter(1,b);
	float logLhood=0;
	int npoints=hdata->GetNbinsX();
	for(int i=1; i<=npoints; i++) //loop over histogram bins
	{
		//read x data and their counts from histogram
		float x=hdata->GetBinCenter(i);
		int n=hdata->GetBinContent(i);
		float width=hdata->GetBinWidth(i);
		float prob=(f1->Eval(x)); 

		logLhood+=n*TMath::Log(prob)-prob;
	}
	return logLhood;
}


float chi2(TH1D* hdata, float a, float b, TF1* f1)
{

//   YOUR CODE HERE

	return chi2;
}


//gaussian distribution
double Fgaussian(double* x, double* par)
{
	double pi=TMath::Pi();
	double denom=TMath::Sqrt(2*pi*par[1]*par[1]);
	
	double y;
	if(par[1]>0)
	{
		float frac=((x[0]-par[0])/par[1]);
		y=(par[2]/denom)*TMath::Exp(-0.5*frac*frac);
	}
	else y=0;
	return y;
}


void Dirty_Gauss(){


        TH1D *hsignal = peak_generator(100., 10., 500, 2500, 1);

	float integral=hsignal->Integral(30,170,"width"); //for normalization

	
	//declare theoretical function
	//(in this case a Gaussian)
	float xmin=0;
	float xmax=200;
	TF1* ftheory=new TF1("ftheory", Fgaussian, xmin, xmax,3);
	ftheory->SetParameter(2, integral); //set normalization

	TF1* ftheory_2=new TF1("ftheory_2", Fgaussian, xmin, xmax,3);
	ftheory_2->SetParameter(2, integral); //set normalization	
	
	//parameter grid histogram
	int abins=200;
	float amin=80; //interval in which we look for mu
	float amax=120; //interval in which we look for mu
	int bbins=200;
	float bmin=0.5; //interval in which we look for sigma
	float bmax=50.5; //interval in which we look for sigma
	TH2D* hProbAB=new TH2D("hprob", "probability of parameters; #mu; #sigma",abins,amin,amax,bbins,bmin,bmax);
	
	//find maximum for likelihood, minimum for chi2
	float mlm_tmax=0.;
	float mlm_tmin=1E9;
	float mlm_aextreme=0.; //best value of mu
	float mlm_bextreme=0.; //best value of sigma
	
	float chi2_tmax=0.;
	float chi2_tmin=1E9;
	float chi2_aextreme=0.; //best value of mu
	float chi2_bextreme=0.; //best value of sigma	
	
	
	for(int abn=1; abn<=hProbAB->GetNbinsX(); abn++){
	for(int bbn=1; bbn<=hProbAB->GetNbinsY(); bbn++){
		float mu=hProbAB->GetXaxis()->GetBinCenter(abn);
		float sigma=hProbAB->GetYaxis()->GetBinCenter(bbn);
		float chi=0;
		float mlm=0;

//			mlm=lhood(hsignal, mu, sigma, ftheory);
			mlm=lhood_binned(hsignal, mu, sigma, ftheory);
//			if (mu == 93) cout << sigma << "   " << test << endl;
			if(mlm>mlm_tmax)
			{
				mlm_tmax=mlm;
				mlm_aextreme=mu;
				mlm_bextreme=sigma;
			}
			chi=chi2(hsignal, mu, sigma, ftheory);
			if(chi<chi2_tmin)
			{
				chi2_tmin=chi;
				chi2_aextreme=mu;
				chi2_bextreme=sigma;
			}
			hProbAB->SetBinContent(abn,bbn,chi);

	}} //loops over bins
	
	//here we can put one more searching loop with much finer binning, looking only into a close vicinity of the previously found optimal mu and sigma
	
	cout<<"MLM: optimal mu: " << mlm_aextreme <<" , sigma: "<<mlm_bextreme<<endl;
	cout<<"chi2: optimal mu: " << chi2_aextreme <<" , sigma: "<<chi2_bextreme<<endl;
	
	ftheory->SetParameter(0,mlm_aextreme);
	ftheory->SetParameter(1,mlm_bextreme);
	ftheory->SetLineColor(3);	

	ftheory_2->SetParameter(0,chi2_aextreme);
	ftheory_2->SetParameter(1,chi2_bextreme);
	ftheory_2->SetLineColor(4);	
	
	//draw histograms
	TCanvas* c1=new TCanvas("c1","parameter map",10,10,800,600);
	c1->cd();
	c1->SetLogz();
	hProbAB->Draw("COLZ");
	
	TCanvas* c2=new TCanvas("c2","signal",10,10,800,600);
	c2->cd();
	hsignal->Draw("E");
	ftheory->Draw("same");
	ftheory_2->Draw("same");
	
}



