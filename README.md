# Commnad
imfit source/NGC0237_i.fits -c configs/config_exponential_ic3478_256.dat --sky=130.44

## Excecution
	Image file = source/NGC0237_i.fits
	configuration file = configs/config_exponential_ic3478_256.dat
	original sky level = 130.44 ADU
Reading data image ("source/NGC0237_i.fits") ...
naxis1 [# pixels/row] = 401, naxis2 [# pixels/col] = 321; nPixels_tot = 128721
* No PSF image supplied -- no image convolution will be done!
* No noise image supplied ... will generate noise image from input data image.
Function: Exponential
6 total parameters
Model Object: 128721 data values (pixels)
ModelObject: mask vector applied to weight vector. (128721 valid pixels remain)
6 free parameters (128715 degrees of freedom)
Estimated memory use: 13386984 bytes (12.8 MB)

Performing fit by minimizing chi^2 (data-based errors):
Calling Levenberg-Marquardt solver ...
	mpfit iteration 1: fit statistic = 899991.754897
	mpfit iteration 2: fit statistic = 877639.205624
	mpfit iteration 3: fit statistic = 874686.264109
	mpfit iteration 4: fit statistic = 869847.232298
	mpfit iteration 5: fit statistic = 868733.074002
	mpfit iteration 6: fit statistic = 867039.609545
	mpfit iteration 7: fit statistic = 863805.417986
	mpfit iteration 8: fit statistic = 863511.766156
	mpfit iteration 9: fit statistic = 862900.245271
	mpfit iteration 10: fit statistic = 862535.435476
	mpfit iteration 11: fit statistic = 861814.713521
	mpfit iteration 12: fit statistic = 861714.775490
	mpfit iteration 13: fit statistic = 861515.190940
	mpfit iteration 14: fit statistic = 861452.571619
	mpfit iteration 15: fit statistic = 861327.643956
	mpfit iteration 16: fit statistic = 861309.077121
	mpfit iteration 17: fit statistic = 861271.973586
	mpfit iteration 18: fit statistic = 861261.523816
	mpfit iteration 19: fit statistic = 861240.621877
	mpfit iteration 20: fit statistic = 861237.012257
	mpfit iteration 21: fit statistic = 861229.789242
	mpfit iteration 22: fit statistic = 861229.534328
	mpfit iteration 23: fit statistic = 861228.995511
	mpfit iteration 24: fit statistic = 861228.659202
	mpfit iteration 25: fit statistic = 861228.433716
	mpfit iteration 26: fit statistic = 861227.991593
	mpfit iteration 27: fit statistic = 861227.083256
	mpfit iteration 28: fit statistic = 861226.929824
	mpfit iteration 29: fit statistic = 861226.670661
	mpfit iteration 30: fit statistic = 861226.130372
	mpfit iteration 31: fit statistic = 861226.037731
	mpfit iteration 32: fit statistic = 861225.943654
	mpfit iteration 33: fit statistic = 861225.760077
	mpfit iteration 34: fit statistic = 861225.367918
	mpfit iteration 35: fit statistic = 861225.303149
	mpfit iteration 36: fit statistic = 861225.212794
	mpfit iteration 37: fit statistic = 861225.008474
	mpfit iteration 38: fit statistic = 861224.974013
	mpfit iteration 39: fit statistic = 861224.951560
	mpfit iteration 40: fit statistic = 861224.868986
	mpfit iteration 41: fit statistic = 861224.817682
	mpfit iteration 42: fit statistic = 861224.799035
	mpfit iteration 43: fit statistic = 861224.737272
	mpfit iteration 44: fit statistic = 861224.729336
	mpfit iteration 45: fit statistic = 861224.724563

*** mpfit status = 1 -- SUCCESS: Convergence in fit-statistic value.
  CHI-SQUARE = 861224.724563    (128715 DOF)
  INITIAL CHI^2 = 928228.332389
        NPAR = 6
       NFREE = 6
     NPEGGED = 3
     NITER = 46
      NFEV = 316

Reduced Chi^2 = 6.690943
AIC = 861236.725216, BIC = 861295.316979

X0		135.0000 # +/- 0.0000
Y0		135.0000 # +/- 0.0204
FUNCTION Exponential
PA		6.10791 # +/- 0.0014352	deg (CCW from +y axis)
ell		      0 # +/- 0
I_0		85.4681 # +/- 0.52672	counts/pixel
h		33.3753 # +/- 0.16468	pixels

Saving best-fit parameters in file "bestfit_parameters_imfit.dat"

(Elapsed time: 0.895206 sec for fit, 0.905589 sec total)
Done!

# Second Command
imfit source/NGC0237_i.fits -c configs/config_exponential_ic3478_256.dat --sky=130.44 --save-model=model.fits --save-residual=resid_fits
