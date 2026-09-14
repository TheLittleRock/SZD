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
    // We choose 3 bins in the range of 20 to 40 to simplify looping
    // The goal is to visualize 3 plots per bin, as plotting all 30 original bins would be too much.

    const Int_t iNumBins = 3;  // Number of bins
    Double_t dAxis[iNumBins+1] = {20, 25, 30, 40};  // Bin edges

    // Define histograms for pp, AA, and RAA
    TH1D* h_data_pp = new TH1D("h_data_pp", "pp", iNumBins, dAxis);
    TH1D* h_data_AA = new TH1D("h_data_AA", "AA", iNumBins, dAxis);
    TH1D* h_data_RAA = new TH1D("h_data_RAA", "RAA", iNumBins, dAxis);

    // Load values and errors for each bin, calculate the RAA ratio, and store it
    for (Int_t i = 1; i <= iNumBins; i++) {
        Double_t dValuePP = hpp->GetBinContent(14 + i);  // Get pp value from original bin
        Double_t dSigmaPP = hpp->GetBinError(14 + i);    // Get pp error from original bin
        h_data_pp->SetBinContent(i, dValuePP);           // Set pp bin value
        h_data_pp->SetBinError(i, dSigmaPP);             // Set pp bin error

        Double_t dValueAA = hAA->GetBinContent(14 + i);  // Get AA value from original bin
        Double_t dSigmaAA = hAA->GetBinError(14 + i);    // Get AA error from original bin
        h_data_AA->SetBinContent(i, dValueAA);           // Set AA bin value
        h_data_AA->SetBinError(i, dSigmaAA);             // Set AA bin error

        Double_t dValueRAA = dValueAA / dValuePP;        // Calculate RAA as ratio of AA/pp
        h_data_RAA->SetBinContent(i, dValueRAA);         // Store RAA value
    }

    // Systematic uncertainty generation
    if (gRandom) delete gRandom;
    gRandom = new TRandom3(0);  // Initialize random generator

    TCanvas* cAsym = new TCanvas("cAsym", "Systematics", 1300, 600);
    cAsym->Divide(3, 3);  // Create a 3x3 canvas for the 3 bins

    // Scaling factors to normalize values for easier plotting (these will cancel in the ratio)
    Double_t Factor[iNumBins] = {1e8, 1e9, 1e10};  // Scaling factors per bin

    // Create histograms for toy data for pp, AA, and their ratio RAA
    TH1D* h_toy_pp[iNumBins];   // pp toy histograms
    TH1D* h_toy_AA[iNumBins];   // AA toy histograms
    TH1D* h_toy_RAA[iNumBins];  // RAA ratio toy histograms

    // Histogram binning and ranges
    Double_t MinBinVal = -5, MaxBinVal = 20;
    Double_t MinBinErr = -1, MaxBinErr = 3.5;
    Int_t nBinsVal = 1001, nBinsErr = 1001;

    // Define Gaussian functions over the range MinBinVal-MaxBinVal for toy data generation
    // ** CODE HERE

    // Define functions for left and right Gaussian fits on both sides of the ratio histogram
    // ** CODE HERE

    // Store results of RAA and the fit asymmetry parameters
    Double_t RAAval[iNumBins];  // RAA values (means)
    RAAval[0] = h_data_RAA->GetBinContent(1);
    RAAval[1] = h_data_RAA->GetBinContent(2);
    RAAval[2] = h_data_RAA->GetBinContent(3);

    Double_t sigma_left[iNumBins];   // Left-side sigma from fit
    Double_t sigma_right[iNumBins];  // Right-side sigma from fit

    // Loop over bins
    for (Int_t k = 0; k < iNumBins; k++) {
        h_toy_pp[k] = new TH1D("h_toy_pp", "h_toy_pp", nBinsVal, MinBinVal, MaxBinVal);
        h_toy_AA[k] = new TH1D("h_toy_AA", "h_toy_AA", nBinsVal, MinBinVal, MaxBinVal);
        h_toy_RAA[k] = new TH1D("h_toy_RAA", "h_toy_RAA", nBinsErr, MinBinErr, MaxBinErr);

        // Scale data to values around 1 using binContent * Factor[k] and binError * Factor[k]
        // This is crucial for setting the Gaussian parameters according to the data

        // ** CODE HERE

        // Generate toy data
        for (Int_t p = 0; p < 100001; p++) {
            // Fill toy histograms with randomly sampled numbers

            // ** CODE HERE
        }

        // Plot the toy data
        Int_t N = k * 3;  // Index offset for 3 histograms per bin
        cAsym->cd(N + 1); h_toy_pp[k]->Draw();
        cAsym->cd(N + 2); h_toy_AA[k]->Draw();
        cAsym->cd(N + 3); h_toy_RAA[k]->Draw();

        // Set Gaussian fit parameters (mean is fixed, normalization depends on toy data size)
        // Perform the fit and store sigmas in sigma_left and sigma_right

        // ** CODE HERE
    }

    // Print results
    std::cout << "### Results Review ###" << std::endl;
    for (Int_t m = 0; m < iNumBins; m++) {
        std::cout << "RAA: " << RAAval[m] << " AsymLeft: " << sigma_left[m] << "  AsymRight: " << sigma_right[m] << std::endl;
    }
    std::cout << "=======================" << std::endl;

    // Convert histogram to points in graph
    Double_t dX[3] = {22.5, 27.5, 35.0};  // X values for bins
    Double_t dXEL[3] = {2.5, 2.5, 5.0};   // X low errors
    Double_t dXEH[3] = {2.5, 2.5, 5.0};   // X high errors
    Double_t dYEH[3], dYEL[3];            // Y high and low errors

    for (Int_t i = 0; i < 3; i++) {
        dYEL[i] = TMath::Abs(sigma_left[i]);  // Fill Y low errors from fit
        dYEH[i] = TMath::Abs(sigma_right[i]); // Fill Y high errors from fit
    }

    TGraphAsymmErrors* geRAA = new TGraphAsymmErrors(3, dX, RAAval, dXEH, dXEL, dYEH, dYEL);
    geRAA->SetTitle("RAA");

    // Plotting
    TCanvas* cBin = new TCanvas("cBin", "Bins", 1300, 600);
    cBin->Divide(2, 1);

    // Plot pp and AA histograms
    cBin->cd(1);
    cBin->GetPad(1)->SetLogy();

    h_data_pp->SetMarkerColor(3);
    h_data_pp->SetLineColor(3);
    h_data_pp->Draw("e");

    h_data_AA->SetMarkerColor(2);
    h_data_AA->SetLineColor(2);
    h_data_AA->Draw("same");

    // Plot RAA with asymmetric errors
    cBin->cd(2);
    geRAA->Draw("ap");
}
