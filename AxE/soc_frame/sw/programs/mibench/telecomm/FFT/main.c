#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "fourier.h"

int my_main(int argc, char *argv[]) {
	unsigned MAXSIZE;
	unsigned MAXWAVES;
	unsigned i,j;
	float *RealIn;
	float *ImagIn;
	float *RealOut;
	float *ImagOut;
	float *coeff;
	float *amp;
	int invfft=0;
	FILE *fp;

	printf("=== AxE FFT MiBench Test ===\n");
	printf("Running FFT with hardcoded parameters...\n");
	
	// Hardcode parameters from runme_small.sh: fft 4 4096
	MAXWAVES = 4;    // 4 waves  
	MAXSIZE = 4096;  // 4096 samples
	invfft = 0;      // Forward FFT (not inverse)
	
	printf("Parameters: MAXWAVES=%d, MAXSIZE=%d, invfft=%d\n", MAXWAVES, MAXSIZE, invfft);
		
 srand(1);

 RealIn=(float*)malloc(sizeof(float)*MAXSIZE);
 ImagIn=(float*)malloc(sizeof(float)*MAXSIZE);
 RealOut=(float*)malloc(sizeof(float)*MAXSIZE);
 ImagOut=(float*)malloc(sizeof(float)*MAXSIZE);
 coeff=(float*)malloc(sizeof(float)*MAXWAVES);
 amp=(float*)malloc(sizeof(float)*MAXWAVES);

 printf("Generating input data...\n");
 
 /* Makes MAXWAVES waves of random amplitude and period */
	for(i=0;i<MAXWAVES;i++) 
	{
		coeff[i] = rand()%1000;
		amp[i] = rand()%1000;
	}
 for(i=0;i<MAXSIZE;i++) 
 {
   /*   RealIn[i]=rand();*/
	 RealIn[i]=0;
	 for(j=0;j<MAXWAVES;j++) 
	 {
		 /* randomly select sin or cos */
		 if (rand()%2)
		 {
		 		RealIn[i]+=coeff[j]*cos(amp[j]*i);
			}
		 else
		 {
		 	RealIn[i]+=coeff[j]*sin(amp[j]*i);
		 }
  	 ImagIn[i]=0;
	 }
 }
 
 printf("Writing input data to files...\n");
 
 // Write RealIn to file
 fp = fopen("fft_input_real.txt", "w");
 if (fp) {
     for (i = 0; i < MAXSIZE; i++) {
         fprintf(fp, "%.6f\n", RealIn[i]);
     }
     fclose(fp);
     printf("RealIn data written to fft_input_real.txt\n");
 } else {
     printf("ERROR: Could not open fft_input_real.txt for writing\n");
 }
 
 // Write ImagIn to file  
 fp = fopen("fft_input_imag.txt", "w");
 if (fp) {
     for (i = 0; i < MAXSIZE; i++) {
         fprintf(fp, "%.6f\n", ImagIn[i]);
     }
     fclose(fp);
     printf("ImagIn data written to fft_input_imag.txt\n");
 } else {
     printf("ERROR: Could not open fft_input_imag.txt for writing\n");
 }

 printf("Performing FFT computation...\n");
 
 /* regular*/
 fft_float (MAXSIZE,invfft,RealIn,ImagIn,RealOut,ImagOut);
 
 printf("FFT computation completed.\n");
 printf("Writing output data to files...\n");
 
 // Write RealOut to file
 fp = fopen("fft_output_real.txt", "w");
 if (fp) {
     for (i = 0; i < MAXSIZE; i++) {
         fprintf(fp, "%.6f\n", RealOut[i]);
     }
     fclose(fp);
     printf("RealOut data written to fft_output_real.txt\n");
 } else {
     printf("ERROR: Could not open fft_output_real.txt for writing\n");
 }
 
 // Write ImagOut to file
 fp = fopen("fft_output_imag.txt", "w");
 if (fp) {
     for (i = 0; i < MAXSIZE; i++) {
         fprintf(fp, "%.6f\n", ImagOut[i]);
     }
     fclose(fp);
     printf("ImagOut data written to fft_output_imag.txt\n");
 } else {
     printf("ERROR: Could not open fft_output_imag.txt for writing\n");
 }
 
 // Print summary to console
 printf("\n=== FFT Results Summary ===\n");
 printf("First 10 RealOut values:\n");
 for (i = 0; i < 10 && i < MAXSIZE; i++) {
     printf("  [%d]: %.6f\n", i, RealOut[i]);
 }
 printf("First 10 ImagOut values:\n");
 for (i = 0; i < 10 && i < MAXSIZE; i++) {
     printf("  [%d]: %.6f\n", i, ImagOut[i]);
 }

 printf("=== FFT MiBench Test Completed Successfully ===\n");
 
 free(RealIn);
 free(ImagIn);
 free(RealOut);
 free(ImagOut);
 free(coeff);
 free(amp);
 exit(0);


}
