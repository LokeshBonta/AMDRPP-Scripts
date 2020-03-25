#include <stdio.h> 
#include <dirent.h>
#include <string.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include "/opt/rocm/rpp/include/rppi.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>
using namespace cv;
using namespace std;
#include <CL/cl.hpp>
#define images 100
int G_IP_CHANNEL = 3;
int G_MODE = 1;
char src[1000] = {"/home/ulagammai/ulagammai/TESTSUITE_RPP/Input_Images/RGB"};
char src_second[1000] = {"/home/ulagammai/ulagammai/TESTSUITE_RPP/Input_Images/RGB1"};
char dst[1000] = {"/home/ulagammai/ocl-Unit-Testing/output"};
char funcType[1000] = {"BatchPD"};

int main(int argc, char **argv)
{
    int ip_channel = G_IP_CHANNEL;
    int mode = G_MODE;
    char *funcName = argv[1];
    
    if(mode == 0)
    {
        strcat(funcType,"_CPU");
    }
    else if (mode == 1)
    {
        strcat(funcType,"_GPU");
    }
    else
    {
        strcat(funcType,"_HIP");
    }
    if(ip_channel == 1)
    {
        strcat(funcType,"_PLN");
    }
    else
    {
        strcat(funcType,"_PKD");
    }
    
    int i = 0, j = 0;
    int minHeight = 30000, minWidth = 30000, maxHeight = 0, maxWidth = 0;
    int minDstHeight = 30000, minDstWidth = 30000, maxDstHeight = 0, maxDstWidth = 0;
   unsigned long long count = 0;
    unsigned long long ioBufferSize = 0;
        unsigned long long oBufferSize = 0;
    
    static int noOfImages = 0;


    Mat image,image_second;
    
    struct dirent *de;
    char src1[1000];
    strcpy(src1, src);
    strcat(src1, "/");
    char src1_second[1000];
    strcpy(src1_second, src_second);
    strcat(src1_second, "/");
    strcat(funcName,funcType);
    strcat(dst,"/");
    strcat(dst,funcName);
    mkdir(dst, 0700);
    strcat(dst,"/");

    DIR *dr = opendir(src); 
    while ((de = readdir(dr)) != NULL) 
    {
        if(strcmp(de->d_name,".") == 0 || strcmp(de->d_name,"..") == 0)
            continue;
        noOfImages += 1;
    }
    closedir(dr);
    int test_case = atoi(argv[1]); // Give Test Case here
    RppiSize *srcSize = (RppiSize *)calloc(noOfImages, sizeof(RppiSize));
    RppiSize *dstSize = (RppiSize *)calloc(noOfImages, sizeof(RppiSize));
    //const int images = noOfImages;
    char imageNames[images][1000];

    DIR *dr1 = opendir(src);
    while ((de = readdir(dr1)) != NULL) 
    {
        if(strcmp(de->d_name,".") == 0 || strcmp(de->d_name,"..") == 0) 
            continue;
        strcpy(imageNames[count],de->d_name);
        char temp[1000];
        strcpy(temp,src1);
        strcat(temp, imageNames[count]);
        if(ip_channel == 3)
        {
            image = imread(temp, 1);
        }
        else
        {
            image = imread(temp, 0);
        }
        srcSize[count].height = image.rows;
        srcSize[count].width = image.cols;
        if(maxHeight < srcSize[count].height)
            maxHeight = srcSize[count].height;
        if(maxWidth < srcSize[count].width)
            maxWidth = srcSize[count].width;
        if(minHeight > srcSize[count].height)
            minHeight = srcSize[count].height;
        if(minWidth > srcSize[count].width)
            minWidth = srcSize[count].width;
        
	dstSize[count].height = image.rows ;
        dstSize[count].width = image.cols  ;
        if(maxDstHeight < dstSize[count].height)
            maxDstHeight = dstSize[count].height;
        if(maxDstWidth < dstSize[count].width)
            maxDstWidth = dstSize[count].width;
        if(minDstHeight > dstSize[count].height)
            minDstHeight = dstSize[count].height;
        if(minDstWidth > dstSize[count].width)
            minDstWidth = dstSize[count].width;

        count++;
    }
    closedir(dr1); 

    ioBufferSize = (unsigned long long)maxHeight * (unsigned long long)maxWidth * (unsigned long long)ip_channel * (unsigned long long)noOfImages;
    oBufferSize = (unsigned long long)maxDstHeight * (unsigned long long)maxDstWidth * (unsigned long long)ip_channel * (unsigned long long)noOfImages;

    Rpp8u *input = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));
        Rpp8u *input_second = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));
    Rpp8u *output = (Rpp8u *)calloc(oBufferSize, sizeof(Rpp8u));
    
    RppiSize maxSize,maxDstSize;
    maxSize.height = maxHeight;
    maxSize.width = maxWidth;
    maxDstSize.height = maxDstHeight;
    maxDstSize.width = maxDstWidth;

    DIR *dr2 = opendir(src);
    DIR *dr2_second = opendir(src_second);
    count = 0;
    i = 0;
    while ((de = readdir(dr2)) != NULL) 
    {
        if(strcmp(de->d_name,".") == 0 || strcmp(de->d_name,"..") == 0) 
            continue;
        count = (unsigned long long)i * (unsigned long long)maxHeight * (unsigned long long)maxWidth * (unsigned long long)ip_channel;
        char temp[1000];
        strcpy(temp,src1);
        strcat(temp, de->d_name);
	char temp_second[1000];
        strcpy(temp_second,src1_second);
        strcat(temp_second, de->d_name);     
        if(ip_channel == 3)
        {
            image = imread(temp, 1);
	    image_second = imread(temp_second, 1);
        }
        else
        {
            image = imread(temp, 0);
            image_second = imread(temp_second, 0);
        }
        Rpp8u *ip_image = image.data;
        Rpp8u *ip_image_second = image_second.data;
        for(j = 0 ; j < srcSize[i].height; j++)
        {
            for(int x = 0 ; x < srcSize[i].width ; x++)
            {
                for(int y = 0 ; y < ip_channel ; y ++)
                {
                    input[count + ((j * maxWidth * ip_channel) + (x * ip_channel) + y)] = ip_image[(j * srcSize[i].width * ip_channel) + (x * ip_channel) + y];
                    input_second[count + ((j * maxWidth * ip_channel) + (x * ip_channel) + y)] = ip_image_second[(j * srcSize[i].width * ip_channel) + (x * ip_channel) + y];
                }
            }
        }
        i++;
    }
    closedir(dr2); 
	Rpp32u minnewMin = 0, maxnewMin = 128, newMin[images];
	Rpp32u minnewMax = 129, maxnewMax = 255, newMax[images];
	for(i = 0 ; i < images ; i++)
	{
		newMin[i] = ((maxnewMin - minnewMin) / images) * i + minnewMin;
		newMax[i] = ((maxnewMax - minnewMax) / images) * i + minnewMax;
	}

	Rpp32u minkernelSize = 6, maxkernelSize = 7, kernelSize[images];
	for(i = 0 ; i < images ; i++)
	{
        kernelSize[i]  = 3;
	}
   Rpp32f minstdDev = 0.5, maxstdDev = 100, stdDev[images];
	for(i = 0 ; i < images ; i++)
	{
        stdDev[i] = 15.0;
		//stdDev[i] = ((maxstdDev - minstdDev) / images) * i + minstdDev;
		//cout<<"\nstdDev"<<stdDev[i];
	}
	Rpp32f minsnowPercentage = 0, maxsnowPercentage = 1, snowPercentage[images];
	for(i = 0 ; i < images ; i++)
	{
		snowPercentage[i] = ((maxsnowPercentage - minsnowPercentage) / images) * i + minsnowPercentage;
		//cout<<"\nsnowPercentage"<<snowPercentage[i];
	}
Rpp32f minrainPercentage = 0.5, maxrainPercentage = 1, rainPercentage[images];
	Rpp32u minrainWidth = 3, maxrainWidth = 6, rainWidth[images];
	Rpp32u minrainHeight = 6, maxrainHeight = 10, rainHeight[images];
	Rpp32f mintransparency = 0.5, maxtransparency = 1, transparency[images];
	for(i = 0 ; i < images ; i++)
	{
		rainPercentage[i] = minrainPercentage;
		rainWidth[i] = ((maxrainWidth - minrainWidth) / images) * i + minrainWidth;
		//cout<<"\nrainWidth"<<rainWidth[i];
		rainHeight[i] = ((maxrainHeight - minrainHeight) / images) * i + minrainHeight;
		//cout<<"\nrainHeight"<<rainHeight[i];
		transparency[i] = mintransparency;
	}
	Rpp32f minnoiseProbability = 0.2, maxnoiseProbability = 1, noiseProbability[images];
	for(i = 0 ; i < images ; i++)
	{
		noiseProbability[i] = minnoiseProbability;
	}
	
Rpp32f minstrength = 1.5, maxstrength = 3, strength[images];
	Rpp32f minzoom = 0, maxzoom = 1, zoom[images];
	for(i = 0 ; i < images ; i++)
	{
		strength[i] = ((maxstrength - minstrength) / images) * i + minstrength;
		//cout<<"\nstrength"<<strength[i];
		zoom[i] = ((maxzoom - minzoom) / images) * i + minzoom;
		//cout<<"\nzoom"<<zoom[i];
	}
	Rpp32f mingamma = 0.5, maxgamma = 1, gamma[images];
	for(i = 0 ; i < images ; i++)
	{
		gamma[i] = mingamma;
	}
	Rpp32f minfogValue = 0, maxfogValue = 1, fogValue[images];
	for(i = 0 ; i < images ; i++)
	{
		fogValue[i] = ((maxfogValue - minfogValue) / images) * i + minfogValue;
		//cout<<"\nfogValue"<<fogValue[i];
	}
	Rpp32u minflipAxis = 0, maxflipAxis = 2, flipAxis[images];
	for(i = 0 ; i < images ; i++)
	{
		flipAxis[i] = ((maxflipAxis - minflipAxis) / images) * i + minflipAxis;
		//cout<<"\nflipAxis"<<flipAxis[i];
	}
	Rpp32f minexposureFactor = 0.5, maxexposureFactor = 4, exposureFactor[images];
	for(i = 0 ; i < images ; i++)
	{
		exposureFactor[i] = ((maxexposureFactor - minexposureFactor) / images) * i + minexposureFactor;
		//cout<<"\nexposureFactor"<<exposureFactor[i];
	}
	Rpp32s minadjustmentValue = 0, maxadjustmentValue = 100, adjustmentValue[images];
	for(i = 0 ; i < images ; i++)
	{
		
		adjustmentValue[i] = 70;
		//adjustmentValue[i] = ((maxadjustmentValue - minadjustmentValue) / images) * i + minadjustmentValue;
		//cout<<"\nadjustmentValue"<<adjustmentValue[i];
	}
        Rpp32f minalpha = 0.5, maxalpha = 1, alpha[images];
	Rpp32f minbeta = 0.5, maxbeta = 255, beta[images];
	for(i = 0 ; i < images ; i++)
	{
		alpha[i] = minalpha;
		beta[i] = ((maxbeta - minbeta) / images) * i + minbeta;
		//cout<<"\nbeta"<<beta[i];
	}

    Rpp32f minangle = 10, maxangle = 200, angle[images];
	for(i = 0 ; i < images ; i++)
	{
		angle[i] = 50;;
	}

    Rpp32f affine_array[6*images];
    for(i = 0; i < images; i=i+6)
    {
        affine_array[i] = 1.0;
        affine_array[i+1] = 1.5;
        affine_array[i+2] = 2.0;
        affine_array[i+3] = 2.0;
        affine_array[i+4] = 2.5;
        affine_array[i+5] = 3.0;
    }
    
    Rpp32u x1[images];
    Rpp32u x2[images];
    Rpp32u y1[images];
    Rpp32u y2[images];

    for(i = 0; i < images; i++)
    {
       x1[i] = 100;
       x2[i] = 300;
       y1[i] = 200;
       y2[i] = 350;
    }

	cl_mem d_input, d_input_second, d_output;
	cl_platform_id platform_id;
	cl_device_id device_id;
	cl_context theContext;
	cl_command_queue theQueue;
	cl_int err;
    err = clGetPlatformIDs(1, &platform_id, NULL);
    err = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_GPU, 1, &device_id, NULL);
    theContext = clCreateContext(0, 1, &device_id, NULL, NULL, &err);
    theQueue = clCreateCommandQueue(theContext, device_id, 0, &err);
    d_input = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
    d_input_second = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
    d_output = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
    err = clEnqueueWriteBuffer(theQueue, d_input, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), input, 0, NULL, NULL);
    err = clEnqueueWriteBuffer(theQueue, d_input_second, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), input_second, 0, NULL, NULL);
	rppHandle_t handle;
   
	rppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages);

	clock_t start, end;   
	double cpu_time_used;
	start = clock();
    string test_case_name;
	switch (test_case)
    {
    case 0:
        test_case_name = "contrast";
        rppi_contrast_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, newMin, newMax, noOfImages, handle);
        break;
    case 1:
        test_case_name = "jitter";
        rppi_jitter_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, kernelSize, noOfImages, handle);
        break;
    case 2:
        test_case_name = "blur";
	    rppi_blur_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, kernelSize, noOfImages, handle);
	    break;
    case 3:
        test_case_name = "brightness";
	    rppi_brightness_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, alpha, beta, noOfImages, handle);
        break;
    case 4:
        test_case_name = "blend";
        rppi_blend_u8_pkd3_batchPD_gpu(d_input, d_input_second, srcSize, maxSize, d_output, alpha, noOfImages, handle);
        break;
    case 5:
        test_case_name = "color_temperature";
	rppi_color_temperature_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, adjustmentValue, noOfImages, handle);
        break;
    case 6:
        test_case_name = "gamma_correction";
	rppi_gamma_correction_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, gamma, noOfImages, handle);
        break;
    case 7:
        test_case_name = "fog";
	rppi_fog_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, fogValue, noOfImages, handle);
        break;
    case 8:
        test_case_name = "snow";
	rppi_snow_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, snowPercentage, noOfImages, handle);
        break;
    case 9:
        test_case_name = "lens_correction";
        rppi_lens_correction_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, strength, zoom, noOfImages, handle);
        break;
    case 10:
        test_case_name = "noise";
        
	rppi_noise_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, noiseProbability, noOfImages, handle);

        break;
    case 11:
        test_case_name = "pixelate";
	rppi_pixelate_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, noOfImages, handle);
        break;
    case 12:
        test_case_name = "exposure";
        rppi_exposure_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, exposureFactor, noOfImages, handle);
        break;
    case 13:
        test_case_name = "fisheye";
        rppi_fisheye_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, noOfImages, handle);
        break;
    case 14:
        test_case_name = "vignette";
        rppi_vignette_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, stdDev, noOfImages, handle);
        break;
    case 15:
        test_case_name = "flip";
	rppi_flip_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, flipAxis, noOfImages, handle);
	break;
    case 16:
        test_case_name = "rain";
	rppi_rain_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, rainPercentage, rainWidth, rainHeight, transparency, noOfImages, handle);
        break;
    case 17:
        test_case_name = "rotate";
	rppi_rotate_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, dstSize, maxSize, angle, noOfImages, handle);
        break;
    case 18:
        test_case_name = "warp-affine";
	rppi_warp_affine_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, dstSize, maxSize, affine_array, noOfImages, handle);
        break;
    
    case 19:
        test_case_name = "resize";
	rppi_resize_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, dstSize, maxDstSize, noOfImages, handle);
        break;
    
    case 20:
        test_case_name = "resize-crop";
	rppi_resize_crop_u8_pkd3_batchPD_gpu(d_input, srcSize, maxSize, d_output, dstSize, maxDstSize, x1, x2, y1, y2, noOfImages, handle);
        break;
    
    default:
        break;
    }
	

    end = clock();
	cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	cout<<" BatchPD : "<<cpu_time_used<<endl;  

	clEnqueueReadBuffer(theQueue, d_output, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), output, 0, NULL, NULL);

	rppDestroyGPU(handle);


    count = 0;
    for(j = 0 ; j < noOfImages ; j++)
    {
        int op_size = maxHeight * maxWidth * ip_channel;
        Rpp8u *temp_output = (Rpp8u *)calloc(op_size, sizeof(Rpp8u));
        for(i = 0 ; i < op_size ; i++)
        {
            temp_output[i] = output[count];
            count++;
        }
        char temp[1000];
        strcpy(temp,dst);
        strcat(temp, imageNames[j]);
        Mat mat_op_image;
        if(ip_channel == 3)
        {
            mat_op_image = Mat(maxHeight, maxWidth, CV_8UC3, temp_output);
            imwrite(temp, mat_op_image);
        }
        if(ip_channel == 1)
        {
            mat_op_image = Mat(maxHeight, maxWidth, CV_8UC1, temp_output);
            imwrite(temp, mat_op_image);
        }
        free(temp_output);
    }

    free(srcSize);
    free(input);
    free(output);
    free(input_second);
	 return 0; 
}
