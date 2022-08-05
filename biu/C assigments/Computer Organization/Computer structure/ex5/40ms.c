	/* aviv shisman 206558157*/


	/* my Full solution is in myFunction function */

typedef struct {
   unsigned char red;
   unsigned char green;
   unsigned char blue;
} pixel;

typedef struct {
    int red;
    int green;
    int blue;
    int num;
} pixel_sum;


/* Compute min and max of two integers, respectively */
int min(int a, int b) { return (a < b ? a : b); }
int max(int a, int b) { return (a > b ? a : b); }

/*
 * initialize_pixel_sum - Initializes all fields of sum to 0
 */
void initialize_pixel_sum(pixel_sum *sum) {
	sum->red = sum->green = sum->blue = 0;
	sum->num = 0;
	return;
}

/*
 * assign_sum_to_pixel - Truncates pixel's new value to match the range [0,255]
 */
static void assign_sum_to_pixel(pixel *current_pixel, pixel_sum sum, int kernelScale) {

	// divide by kernel's weight
	sum.red = sum.red / kernelScale;
	sum.green = sum.green / kernelScale;
	sum.blue = sum.blue / kernelScale;

	// truncate each pixel's color values to match the range [0,255]
	current_pixel->red = (unsigned char) (min(max(sum.red, 0), 255));
	current_pixel->green = (unsigned char) (min(max(sum.green, 0), 255));
	current_pixel->blue = (unsigned char) (min(max(sum.blue, 0), 255));
	return;
}

/*
* sum_pixels_by_weight - Sums pixel values, scaled by given number
*/
static void sum_pixels_by_weight(pixel_sum *sum, pixel p, int weight) {
	sum->red += ((int) p.red) * weight;
	sum->green += ((int) p.green) * weight;
	sum->blue += ((int) p.blue) * weight;
	sum->num++;
	return;
}

/*
 *  Applies kernel for pixel at (i,j)
 */
static pixel applyKernel(int dim, int i, int j, pixel *src, int kernelSize, int kernel[kernelSize][kernelSize], int kernelScale) {

	int ii, jj;
	int currRow, currCol;
	pixel_sum sum;
	pixel current_pixel;

	initialize_pixel_sum(&sum);

	for(ii = max(i-1, 0); ii <= min(i+1, dim-1); ii++) {
		for(jj = max(j-1, 0); jj <= min(j+1, dim-1); jj++) {

			int kRow, kCol;

			// compute row index in kernel
			if (ii < i) {
				kRow = 0;
			} else if (ii > i) {
				kRow = 2;
			} else {
				kRow = 1;
			}

			// compute column index in kernel
			if (jj < j) {
				kCol = 0;
			} else if (jj > j) {
				kCol = 2;
			} else {
				kCol = 1;
			}

			// apply kernel on pixel at [ii,jj]
			//sum_pixels_by_weight(&sum, src[calcIndex(ii, jj, dim)], kernel[kRow][kCol]);
		}
	}

	// assign kernel's result to pixel at [i,j]
	assign_sum_to_pixel(&current_pixel, sum, kernelScale);
	return current_pixel;
}

/*
* Apply the kernel over each pixel.
* Ignore pixels where the kernel exceeds bounds. These are pixels with row index smaller than kernelSize/2 and/or
* column index smaller than kernelSize/2
*/
void smooth(int dim, pixel *src, pixel *dst, int kernelSize, int kernel[kernelSize][kernelSize], int kernelScale) {

	int i, j;
	int start=kernelSize / 2;
	int end=dim - kernelSize / 2;
	//int calcIndex=((i)*(dim)+(j));
	int calc=start*dim; 
	for (i =start ; i <end; ++i) {
		for (j = start ; j < end; ++j) {
			dst[calc+j] = applyKernel(dim, i, j, src, kernelSize, kernel, kernelScale);
		}
		calc+=dim;
		
	}
}

void charsToPixels(Image *charsImg, pixel* pixels) {

	int row, col;
	int help1=0;
	int help2=0;
	int mult1=0;
	int mult2=0;
	for (row = 0 ; row < m ; ++row) {
		for (col = 0 ; col < n ; ++col) {
			help1=mult2 + col;
			help2=mult1 + 3*col;
			pixels[help1].red = image->data[help2];
			pixels[help1].green = image->data[help2 + 1];
			pixels[help1].blue = image->data[help2 + 2];
		}
		mult1+=n; //3*row*n
		mult1+=n;
		mult1+=n;
		mult2+=n; //row*n
	}
}

void pixelsToChars(pixel* pixels, Image *charsImg) {

	int row, col;
	int help1=0;
	int help2=0;
	int mult1=0;
	int mult2=0;
	for (row = 0 ; row < m ; ++row) {
		for (col = 0 ; col < n ; ++col) {
			help1=mult1 + 3*col;
			help2=mult2 + col;
			image->data[help1] = pixels[help2].red;
			image->data[help1+ 1] = pixels[help2].green;
			image->data[help1 + 2] = pixels[help2].blue;
		}
		mult1+=n; //3*row*n
		mult1+=n;
		mult1+=n;
		mult2+=n; //row*n
	}
}

void copyPixels(pixel* src, pixel* dst) {

	int row, col;
	int help=0;
	int mult=0;
	for (row = 0 ; row < m ; ++row) {
		for (col = 0 ; col < n ; ++col) {
			help=mult+ col;
			dst[help].red = src[help].red;
			dst[help].green = src[help].green;
			dst[help].blue = src[help].blue;
		}
		mult+=n;//row*n
	}
}

int calcIndex(int i, int j, int n) {
	return ((i)*(n)+(j));
}

void doConvolution(Image *image, int kernelSize, int kernel[kernelSize][kernelSize], int kernelScale) {

	pixel* pixelsImg = malloc(m*n*sizeof(pixel));
	pixel* backupOrg = malloc(m*n*sizeof(pixel));

	charsToPixels(image, pixelsImg);
	copyPixels(pixelsImg, backupOrg);

	smooth(m, backupOrg, pixelsImg, kernelSize, kernel, kernelScale);

	pixelsToChars(pixelsImg, image);

	free(pixelsImg);
	free(backupOrg);
}


/* my answer is here,
   i called all of the functions inline and upgraded the code
   to reduce running time.
*/
void myfunction(Image *image, char* srcImgpName, char* blurRsltImgName, char* sharpRsltImgName) {
/*
	* [1, 1, 1]
	* [1, 1, 1]
	* [1, 1, 1]
	*/
	int blurKernel[3][3] = {{1, 1, 1}, {1, 1, 1}, {1, 1, 1}};

	/*
	* [-1, -1, -1]
	* [-1, 9, -1]
	* [-1, -1, -1]
	*/
	int sharpKernel[3][3] = {{-1,-1,-1},{-1,9,-1},{-1,-1,-1}};

	/* blur image 
	Start of DoConvolution*/
	
        int kernelSize=3;
        int kernelScale=9;
        int kernel[3][3]={{1, 1, 1}, {1, 1, 1}, {1, 1, 1}};
       
	pixel* pixelsImg = malloc(m*n*sizeof(pixel));
	pixel* backupOrg = malloc(m*n*sizeof(pixel));

	//charsToPixels(image, pixelsImg);
	pixel* pixels=pixelsImg;
	int row, col;
	int help1=0;
	int help2=0;
	int mult1=0;
	int mult2=0;
	for (row =m-1 ; row >=0 ; --row) {
		for (col = n-1; col >= 0; --col) {
			help1=mult2 + col;
			help2=mult1 + 3*col;
			pixels[help1].red = image->data[help2];
			pixels[help1].green = image->data[help2 + 1];
			pixels[help1].blue = image->data[help2 + 2];
		}
		mult1+=n; //3*row*n
		mult1+=n;
		mult1+=n;
		mult2+=n; //row*n
	}
	
	//copyPixels(pixelsImg, backupOrg);
	pixel *dst=backupOrg;
	pixel *src=pixelsImg;
	pixel *p1 =dst;
	pixel *p2=src;
	p1+=n-1;
	p2+=n-1;
	for (row = m-1; row >=0 ; --row) {
		
		for (col = n-1 ; col >= 0 ; --col) {
			p1->red = p2->red;
			p1->green = p2->green;
			p1->blue = p2->blue;
			--p1;
			--p2;
		}
		p1+=n; // this is for the reset after loop
		p2+=n;
		p1+=n; //this is for row*n
		p2+=n;
	}
	
	//Start of Smooth
	
	int dim=m;
	src=backupOrg;
	dst=pixelsImg;
	int i, j;
	int start=kernelSize / 2;
	int end=dim - kernelSize / 2;

	int calc=start*dim; 
	for (i =start ; i <end; ++i) {
		for (j = start ; j < end; ++j) {
		
		//Start of apply Kernel
			int index1, index2;
			pixel current_pixel;


			
			
			/*these are all constants in these loops
			  so i can calculate them one time and it will be enough
			  no need for calculations every loop.
			*/
			int Max1=i-1;		  //max(i-1, 0) kernel size =3 -> intiallize i=1.5(int) >0 no need for function
			int Min1=i+1; 		  //min(i+1, dim-1); i+1 always <=end and end<dim-1 	
			int Max2=j-1; 		  // max(j-1, 0); same as first one
			int Min2=j+1;             //min(j+1, dim-1); same as second



			int calc2=Max1*dim;	  //int calcIndex=((index1)*(dim)+(index2));
			pixel *p1=src;	          //using pointer to lower memory access cost
			p1=p1+calc2+Max2;
			int red=0,green=0,blue=0;
			for(index1 = 2; index1 >= 0; --index1) { //difference between max to min is 2
				//kernel here is always one's so no need for if's
				for(index2 = 2; index2 >= 0; --index2) { //same
					//same here

					// apply kernel on pixel at [index1,index2]
					/* start of sum_pixels_by_weight(&sum, src[calc+index2], kernel[kRow][kCol]);
				         i moved the function here and because i know kernel is all one's
					 i gave weight the value 1 and removed him becuase mult in 1 is a waste.
					*/
					red+= ((int) (*p1).red);
					green += ((int) (*p1).green) ;
					blue += ((int) (*p1).blue);
					++p1;					
					//didnt use sum.num++;
					//end of function
				}
				//index* dim
				p1+=dim;
				p1-=3;

				
			}

			
			/* assign kernel's result to pixel at [i,j]
			  start of assign_sum_to_pixel(&current_pixel, sum, kernelScale);*/
			  
			// divide by kernel's weight
			
			red = red / kernelScale;
			green = green / kernelScale;
			blue = blue / kernelScale;

			
			// truncate each pixel's color values to match the range [0,255]
			
			current_pixel.red = (unsigned char) (red); 		//sum.x will always be >0 and <=255
			current_pixel.green = (unsigned char) (green);
			current_pixel.blue = (unsigned char) (blue);
			//end of function 
			
			//Apply kernet return value
			dst[calc+j] = current_pixel;
					
		}
		calc+=dim;
	
	}//end of smooth
	
	//pixelsToChars(pixelsImg, image);
	pixels=pixelsImg;
	help1=0;
	help2=0;
	mult1=0;
	mult2=0;
	for (row = m-1 ; row >=0  ; --row) {
		for (col = n-1 ; col >= 0 ; --col) {
			help1=mult1 + 3*col;
			help2=mult2 + col;
			image->data[help1] = pixels[help2].red;
			image->data[help1+ 1] = pixels[help2].green;
			image->data[help1 + 2] = pixels[help2].blue;
		}
		mult1+=n; //3*row*n
		mult1+=n;
		mult1+=n;
		mult2+=n; //row*n
	}
	free(pixelsImg);
	free(backupOrg);
	
	
	//end of DoConvolution
	
	
	

	// write result image to file
	writeBMP(image, srcImgpName, blurRsltImgName);





	//what is this...smooth(m, backupOrg, pixelsImg, kernelSize, sharpKernel, 1);




	/* sharpen the resulting image
	   with DoConvolution */
	   
	kernelScale=1;
	pixel* pixelsImg2 = malloc(m*n*sizeof(pixel));
	pixel* backupOrg2 = malloc(m*n*sizeof(pixel));

	//charsToPixels(image, pixelsImg2);
	pixels=pixelsImg2;
	help1=0;
	help2=0;
	mult1=0;
	mult2=0;
	for (row =m-1 ; row >=0 ; --row) {
		for (col = n-1; col >= 0; --col) {
			help1=mult2 + col;
			help2=mult1 + 3*col;
			pixels[help1].red = image->data[help2];
			pixels[help1].green = image->data[help2 + 1];
			pixels[help1].blue = image->data[help2 + 2];
		}
		mult1+=n; //3*row*n
		mult1+=n;
		mult1+=n;
		mult2+=n; //row*n
	}
	
	//start of copyPixels
	dst=backupOrg2;
	src=pixelsImg2;
	p1 =dst;
	p2=src;
	
	p1+=n-1;
	p2+=n-1;
	for (row = m-1; row >=0 ; --row) {
		
		for (col = n-1 ; col >= 0 ; --col) {

			p1->red = p2->red;
			p1->green = p2->green;
			p1->blue = p2->blue;
			--p1;
			--p2;
		}
		p1+=n; // this is for the reset after loop
		p2+=n;
		p1+=n; //this is for row*n
		p2+=n;
	}
	//end of CopyPixels
	
	//Start of Smooth
	dim=m;
	pixel *src2=backupOrg2;
	pixel *dst2=pixelsImg2;
	
	i=0;
	j=0;
	start=kernelSize / 2;
	end=dim - kernelSize / 2;
	calc=start*dim; 
	for (i =start ; i <end; ++i) {
		for (j = start ; j < end; ++j) {
		
		//Start of apply Kernel
			int index1, index2;
			pixel current_pixel;
			int red=0,blue=0,green=0;//insted of sum_pixel
			
			
			
			/*these are all constants in these loops
			  so i can calculate them one time and it will be enough
			  no need for calculations every loop.
			*/
			
			int Max1=i-1;		//max(i-1, 0) kernel size =3 -> intiallize i=1.5(int) >0
						// no need for function
			int Min1=i+1;		//min(i+1, dim-1); i+1 always <=end and end<dim-1 	
			int Max2=j-1;		// max(j-1, 0); same as first one
			int Min2=j+1;		//min(j+1, dim-1); same as second


	
			
			
			int calc2=Max1*dim;	  //int calcIndex=((index1)*(dim)+(index2));
			pixel *p1=src2;	          //using pointer to lower memory access cost
			p1=p1+calc2+Max2;
			for(index1 = 2; index1 >= 0; --index1) { //difference between max to min is 2
				//kernel here is always one's so no need for if's
				for(index2 = 2; index2 >= 0; --index2) { //same
					//same here

					// apply kernel on pixel at [index1,index2]
					/* start of sum_pixels_by_weight(&sum, src[calc+index2], kernel[kRow][kCol]);
				         i moved the function here and because i know kernel is all one's
					 i gave weight the value 1 and removed him becuase mult in 1 is a waste.
					*/

					if(index1==1 && index2==1){
					 	red += ((int) (*p1).red)*9;
						green += ((int) (*p1).green)*9 ;
						blue += ((int) (*p1).blue)*9;
						++p1;	

					 } //in case we in middle
					 else{
						red -= ((int) (*p1).red);     //weight is -1
						green -= ((int) (*p1).green);
						blue -= ((int) (*p1).blue);
						++p1;					
						//didnt use sum.num++;
						//end of function
					}
				}
				//index* dim
				p1+=dim;
				p1-=3;	
			}
			/* assign kernel's result to pixel at [i,j]
			  start of assign_sum_to_pixel(&current_pixel, sum, kernelScale);*/
			  
			// divide by kernel's weight
			red = red / kernelScale;
			green = green / kernelScale;
			blue = blue / kernelScale;

			// truncate each pixel's color values to match the range [0,255]
			current_pixel.red = (unsigned char) (min(max(red, 0), 255));
			current_pixel.green = (unsigned char) (min(max(green, 0), 255));
			current_pixel.blue = (unsigned char) (min(max(blue, 0), 255));
			
			//end of function
			
			//Apply kernet return value
			dst2[calc+j] = current_pixel;
				
			
			
		//end of apply kernel
		}
		calc+=dim;
		
	}
	//end of smooth
	
	//pixelsToChars(pixelsImg2, image);
	pixels=pixelsImg2;
	help1=0;
	help2=0;
	mult1=0;
	mult2=0;
	for (row = m-1 ; row >=0  ; --row) {
		for (col = n-1; col >=0  ; --col) {
			help1=mult1 + 3*col;
			help2=mult2 + col;
			image->data[help1] = pixels[help2].red;
			image->data[help1+ 1] = pixels[help2].green;
			image->data[help1 + 2] = pixels[help2].blue;
		}
		mult1+=n; //3*row*n
		mult1+=n;
		mult1+=n;
		mult2+=n; //row*n
	}
	
	free(pixelsImg2);
	free(backupOrg2);
	
	//end of DoConvolution
	
	
	// write result image to file
	writeBMP(image, srcImgpName, sharpRsltImgName);
}

