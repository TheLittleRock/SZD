//void RAA()
{

  Double_t xAxis1[31] = {0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 60, 70, 80, 100};
  TH1D *hpp = new TH1D("hpp","measured data pp",30, xAxis1);
  hpp->SetBinContent(1,1.118516);
  hpp->SetBinContent(2,0.1920894);
  hpp->SetBinContent(3,0.007120608);
  hpp->SetBinContent(4,0.001577695);
  hpp->SetBinContent(5,0.0004146155);
  hpp->SetBinContent(6,0.0001296542);
  hpp->SetBinContent(7,4.644327e-05);
  hpp->SetBinContent(8,2.057404e-05);
  hpp->SetBinContent(9,9.958874e-06);
  hpp->SetBinContent(10,4.334099e-06);
  hpp->SetBinContent(11,1.442999e-06);
  hpp->SetBinContent(12,5.654266e-07);
  hpp->SetBinContent(13,2.407638e-07);
  hpp->SetBinContent(14,1.094223e-07);
  hpp->SetBinContent(15,3.354351e-08);
  hpp->SetBinContent(16,6.04691e-09);
  hpp->SetBinContent(17,7.423793e-10);
  hpp->SetBinContent(18,3.350337e-11);
  hpp->SetBinError(1,0.0006107765);
  hpp->SetBinError(2,0.0003700558);
  hpp->SetBinError(3,4.49924e-05);
  hpp->SetBinError(4,1.821935e-05);
  hpp->SetBinError(5,7.447584e-06);
  hpp->SetBinError(6,2.939223e-06);
  hpp->SetBinError(7,1.155389e-06);
  hpp->SetBinError(8,5.875219e-07);
  hpp->SetBinError(9,1.855936e-07);
  hpp->SetBinError(10,1.141886e-07);
  hpp->SetBinError(11,3.0114e-08);
  hpp->SetBinError(12,5.526975e-09);
  hpp->SetBinError(13,2.701332e-09);
  hpp->SetBinError(14,1.525211e-09);
  hpp->SetBinError(15,6.343152e-10);
  hpp->SetBinError(16,9.460454e-11);
  hpp->SetBinError(17,2.709424e-11);
  hpp->SetBinError(18,4.271672e-13);
  hpp->SetEntries(1000);


  TH1D *hAA = new TH1D("hAA","measured data AA",30, xAxis1);
  hAA->SetBinContent(4,0.0004135252);
  hAA->SetBinContent(5,0.0001128615);
  hAA->SetBinContent(6,5.329878e-05);
  hAA->SetBinContent(7,2.740152e-05);
  hAA->SetBinContent(8,1.417387e-05);
  hAA->SetBinContent(9,8.002939e-06);
  hAA->SetBinContent(10,3.765388e-06);
  hAA->SetBinContent(11,1.418623e-06);
  hAA->SetBinContent(12,5.724047e-07);
  hAA->SetBinContent(13,2.704585e-07);
  hAA->SetBinContent(14,1.308473e-07);
  hAA->SetBinContent(15,3.482406e-08);
  hAA->SetBinContent(16,5.969517e-09);
  hAA->SetBinContent(17,8.159869e-10);
  hAA->SetBinContent(18,1.976192e-11);
  hAA->SetBinError(4,1.06535e-06);
  hAA->SetBinError(5,4.957864e-07);
  hAA->SetBinError(6,3.151375e-07);
  hAA->SetBinError(7,2.136749e-07);
  hAA->SetBinError(8,1.451485e-07);
  hAA->SetBinError(9,1.005136e-07);
  hAA->SetBinError(10,5.988379e-08);
  hAA->SetBinError(11,3.659272e-08);
  hAA->SetBinError(12,2.201622e-08);
  hAA->SetBinError(13,1.464843e-08);
  hAA->SetBinError(14,9.694462e-09);
  hAA->SetBinError(15,3.96629e-09);
  hAA->SetBinError(16,1.470905e-09);
  hAA->SetBinError(17,4.142606e-10);
  hAA->SetBinError(18,1.499208e-11);
  hAA->SetEntries(60);




  // Extracting spectra
  // vybereme si 3 biny v rozmezi 20 az 40 abychom kodily v loopech a bylo to jasne
  // jde o to ze budeme vykreslovat 3 obrazky pro kazdy bin a pro 30 puvodnich binu by to byl mazec ...

  // we choose 3 bins for pt from 20 to 40 so we have to code it in loop (like a real case)
  // but since we want to visualize all plots, 3 are enough (out of 30 above)

  const Int_t iNumBins = 3;

  Double_t dAxis[iNumBins+1] = {20,25,30,40};

  TH1D* h_data_pp = new TH1D("h_data_pp","pp",iNumBins,dAxis);
  TH1D* h_data_AA = new TH1D("h_data_AA","AA",iNumBins,dAxis);
  TH1D* h_data_RAA = new TH1D("h_data_RAA","RAA",iNumBins,dAxis);

  // pro kazdy bin nactu hodnoty a chyby v danem binu a ulozim to do histogramu, 
  // spoctu pomer hodnot a ulozim do histogramu - ale co s chybama v binech?

  // load the values to new histograms for the 3 bins
  // we have ratio = the means, but how to calculate the sigma?

  for(Int_t i = 1; i <= iNumBins; i++)
  {
    Double_t dValuePP = hpp->GetBinContent(14+i);
    Double_t dSigmaPP = hpp->GetBinError(14+i);
    h_data_pp->SetBinContent(i,dValuePP);
    h_data_pp->SetBinError(i,dSigmaPP);

    Double_t dValueAA = hAA->GetBinContent(14+i);
    Double_t dSigmaAA = hAA->GetBinError(14+i);
    h_data_AA->SetBinContent(i,dValueAA);
    h_data_AA->SetBinError(i,dSigmaAA);

    Double_t dValueRAA = dValueAA/dValuePP;

    h_data_RAA->SetBinContent(i,dValueRAA);
  }


  //Systematics
   if(gRandom) delete gRandom;
  gRandom = new TRandom3(0);

  TCanvas* cAsym = new TCanvas("cAsym","Systematics",1300,600);
  cAsym->Divide(3,3);		// 3 obrazky pro 3 biny

  // a trick - for meaningful values - scaling of the values to be roughly 1.
  // can do this as this will cancel in the ratio
  Double_t Factor[iNumBins] = {1e8,1e9,1e10}; 
  // then we work with multiplied values: h_data_pp->GetBinContent(k+1)*Factor[k] , h_data_pp->GetBinError(k+1)*Factor[k] ,  kde k = 0,1,2

  
  // 3 histograms for 3 bins - for random values and their ratio = Err; THIS IS WHAT I WANT TO PLOT and RAA histogram fitted
  TH1D* h_toy_pp[iNumBins]; //pp
  TH1D* h_toy_AA[iNumBins]; //AA
  TH1D* h_toy_RAA[iNumBins]; //ratio for fit

  // histogram binning and ranges
  Double_t MinBinVal = -5;
  Double_t MaxBinVal = 20;
  Double_t MinBinErr = -1;
  Double_t MaxBinErr = 3.5;
  Int_t    nBinsVal = 1001;
  Int_t    nBinsErr = 1001;



  	//  define funcion of Gauss at the given range MinBinVal-MaxBinVal - for value generation
	// we need these functions to generate toy data - mean is the ration, sigma of gauss = bin error of data
// ** CODE HERE
  
    TF1* GaussFuncPP [iNumBins];
    TF1* GaussFuncAA [iNumBins];

    for (int i = 0; i < iNumBins; i++){
      GaussFuncPP[i] = new TF1(("PPgaus"+to_string(i)).c_str(), "gaus", MinBinVal, MaxBinVal);
      GaussFuncPP[i]->SetParameters(1, h_data_pp->GetBinContent(i+1)*Factor[i], h_data_pp->GetBinError(i+1)*Factor[i]);
      GaussFuncAA[i] = new TF1(("AAgaus"+to_string(i)).c_str(), "gaus", MinBinVal, MaxBinVal);
      GaussFuncAA[i]->SetParameters(1, h_data_AA->GetBinContent(i+1)*Factor[i], h_data_AA->GetBinError(i+1)*Factor[i]);
    }

    	//  define 3 functions leftGauss & rightGauss for fitting both sides of ratio histogram
	//  3x because you have 3 bins to fit
// ** CODE HERE

    TF1* leftGauss [iNumBins];
    TF1* rightGauss [iNumBins];

    for (int i = 0; i < iNumBins; i++){
      leftGauss[i] = new TF1(("leftGauss"+to_string(i)).c_str(), "gaus", MinBinVal, h_data_RAA->GetBinContent(i+1));
      rightGauss[i] = new TF1(("rightGauss"+to_string(i)).c_str(), "gaus", h_data_RAA->GetBinContent(i+1), MaxBinVal);
    }

  	// here store the results
  	Double_t RAAval[iNumBins];	// RAA from data - the mean
        RAAval[0] = h_data_RAA->GetBinContent(1);
        RAAval[1] = h_data_RAA->GetBinContent(2);
        RAAval[2] = h_data_RAA->GetBinContent(3);

	//MAIN TASK - FILL THESE VARIABLES
  	Double_t sigma_left[iNumBins];
  	Double_t sigma_right[iNumBins];

    Double_t ERRsigma_left[iNumBins];
  	Double_t ERRsigma_right[iNumBins];


  // loop over bins:
  for(Int_t k = 0; k < iNumBins; k++)
  {

      h_toy_pp[k] = new TH1D("h_toy_pp","h_toy_pp",nBinsVal,MinBinVal,MaxBinVal);
      h_toy_AA[k] = new TH1D("h_toy_AA","h_toy_AA",nBinsVal,MinBinVal,MaxBinVal);
      h_toy_RAA[k] = new TH1D("h_toy_RAA","h_toy_RAA",nBinsErr,MinBinErr,MaxBinErr);

      // since we loop from 0, the first bin has index 1 => k+1 bin
      // here is the trick to set every value around 1 using the binContent*Factor[k] and binErr*Factor[k]Factor
      // this is the crucial step - to set parameters of the gauss according to the data


// ** CODE HERE
// nevim, co sem chces dat, ale funguje to, kdyz sem nic nenapisu :)

      for(Int_t p = 0; p < 100000+1; p++)
      {
	// fill toy histograms with randomly sampled numbers

// ** CODE HERE   
        Double_t pp_toy_val = GaussFuncPP[k]->GetRandom();
        Double_t AA_toy_val = GaussFuncAA[k]->GetRandom();
        Double_t RAA_toy_val = AA_toy_val/pp_toy_val;

        h_toy_pp[k]->Fill(pp_toy_val);
        h_toy_AA[k]->Fill(AA_toy_val);
        h_toy_RAA[k]->Fill(RAA_toy_val);
      }


  // so we have pseudodata for the ratio - let's fit
      // plotting toy data:
      Int_t N = k*3;
      cAsym->cd(N+1);
      h_toy_pp[k]->Draw();
      cAsym->cd(N+2);
      h_toy_AA[k]->Draw();
      cAsym->cd(N+3);
      h_toy_RAA[k]->Draw();


	// set parameters for 3x gauss left, 3x gause right (i.e. for 3 bins)
	// FixParameter()   for mean
	// dont forget to set the normalization!!! -- it depends on the amount of toy data
	// fit the toy RAA
	// fill the pre-prepared variables for sigmas

// ** CODE HERE

    leftGauss[k]->SetParameter(1, RAAval[k]);
    leftGauss[k]->FixParameter(1, RAAval[k]);
    leftGauss[k]->SetParameter(2, 1);

    rightGauss[k]->SetParameter(1, RAAval[k]);
    rightGauss[k]->FixParameter(1, RAAval[k]);
    rightGauss[k]->SetParameter(2, 1);

    h_toy_RAA[k]->Fit(("leftGauss"+to_string(k)).c_str(), "RBq");
    h_toy_RAA[k]->Fit(("rightGauss"+to_string(k)).c_str(), "RBq");

    sigma_left[k] = abs(leftGauss[k]->GetParameter(2)); 
    sigma_right[k] = abs(rightGauss[k]->GetParameter(2)); 

    ERRsigma_left[k] = abs(leftGauss[k]->GetParError(2)); 
    ERRsigma_right[k] = abs(rightGauss[k]->GetParError(2));    

    leftGauss[k]->SetLineColor(kGreen);
    leftGauss[k]->Draw("Same");

    rightGauss[k]->SetLineColor(kRed);
    rightGauss[k]->Draw("Same");

  }   // end of loop over bins


  std::cout << "### Results Review ###" << std::endl;
  for(Int_t m = 0; m < iNumBins; m++)
  {
      std::cout << "RAA:" << RAAval[m] <<" AsymLeft:" << sigma_left[m] << " (pm " << ERRsigma_left[m]  << ") " << "  AsymRight:" << sigma_right[m]  << " (pm " << ERRsigma_right[m]  << ") " << endl;
  }
  std::cout << "=======================" << std::endl;

  //Konverzion of histogram to points in graph:
  Double_t dX[3] = {22.5,27.5,35.};
  Double_t dXEL[3] = {2.5,2.5,5.};
  Double_t dXEH[3] = {2.5,2.5,5.};
  Double_t dYEH[3];
  Double_t dYEL[3];

  for(Int_t i = 0; i < 4; i++)
  {
    dYEL[i] = TMath::Abs(sigma_left[i]);
    dYEH[i] = TMath::Abs(sigma_right[i]);
  }


  TGraphAsymmErrors* geRAA = new TGraphAsymmErrors(3,dX,RAAval,dXEH,dXEL,dYEH,dYEL);
  geRAA->SetTitle("RAA");


  //Plotting
  TCanvas* cBin = new TCanvas("cBin","Bins",1300,600);

  cBin->Divide(2,1);

  cBin->cd(1);
  cBin->GetPad(1)->SetLogy();

  h_data_pp->SetMarkerColor(3);
  h_data_pp->SetLineColor(3);
  h_data_pp->Draw("e");

  h_data_AA->SetMarkerColor(2);
  h_data_pp->SetLineColor(2);
  h_data_AA->Draw("same");


  cBin->cd(2);
  //h_data_RAA->Draw("E");
  geRAA->Draw("ap");














}
