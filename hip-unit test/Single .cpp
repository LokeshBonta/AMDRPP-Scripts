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
#include "hip/hip_runtime_api.h"
using namespace cv;
using namespace std;
#define images 100

void check_hip_error(void)
{
	hipError_t err = hipGetLastError();
	if (err != hipSuccess)
	{
 		cerr<< "Error: "<< hipGetErrorString(err)<<endl;
		exit(err);
	}
}
int G_IP_CHANNEL = 3;
int G_MODE = 2;
char funcType[1000] = {"Single"};
char src[1000] = {"/home/ulagammai/ulagammai/TESTSUITE_RPP/Input_Images/RGB"};
char dst[1000] = {"/home/ulagammai/Hip-Unit-Testing/output"};

int main(int argc, char **argv)
{
    int ip_channel = G_IP_CHANNEL;
    int mode = G_MODE;
    char *funcName = argv[1]; 
    //char *src = argv[2];
    //char *dst = argv[3];
    //char *src2 = argv[4];
    
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
    unsigned long long count = 0;
    unsigned long long ioBufferSize = 0, oBufferSize = 0;
    
    static int noOfImages = 0;


    Mat image;
    
    struct dirent *de;
    char src1[1000];
    strcpy(src1, src);
    strcat(src1, "/");
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
        break;
    }
    closedir(dr);

    RppiSize *srcSize = (RppiSize *)calloc(noOfImages, sizeof(RppiSize));
    RppiSize *dstSize = (RppiSize *)calloc(noOfImages, sizeof(RppiSize));
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
        ioBufferSize += (unsigned long long)srcSize[count].height * (unsigned long long)srcSize[count].width * (unsigned long long)ip_channel;
        dstSize[count].height = image.rows ;
        dstSize[count].width = image.cols  ;
        oBufferSize += (unsigned long long)dstSize[count].height * (unsigned long long)dstSize[count].width * (unsigned long long)ip_channel;

        count++;
        break;
    }
    closedir(dr1); 

    Rpp8u *input = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));
    Rpp8u *output = (Rpp8u *)calloc(oBufferSize, sizeof(Rpp8u));

    DIR *dr2 = opendir(src);
    count = 0;
    i = 0;
    while ((de = readdir(dr2)) != NULL) 
    {
        if(strcmp(de->d_name,".") == 0 || strcmp(de->d_name,"..") == 0) 
            continue;
        char temp[1000];
        strcpy(temp,src1);
        strcat(temp, de->d_name);
        if(ip_channel == 3)
        {
            image = imread(temp, 1);
        }
        else
        {
            image = imread(temp, 0);
        }
        Rpp8u *ip_image = image.data;
        for(j = 0 ; j < srcSize[i].height * srcSize[i].width * ip_channel ; j++)
        {
            input[count] = ip_image[j];
            
            count++;
        }
        i++;
        break;
    }
    closedir(dr2); 
	Rpp32u minnewMin = 0, maxnewMin = 128, newMin;
	Rpp32u minnewMax = 129, maxnewMax = 255, newMax;
	newMin = (Rpp32u) ((rand() % (int) (maxnewMin - minnewMin)) + minnewMin);
		//cout<<"\nnewMin"<<newMin;
	newMax = (Rpp32u) ((rand() % (int) (maxnewMax - minnewMax)) + minnewMax);
		//cout<<"\nnewMax"<<newMax;

	int *d_input, *d_input_second, *d_output;
	hipMalloc(&d_input, ioBufferSize * sizeof(Rpp8u));
	hipMalloc(&d_input_second, ioBufferSize * sizeof(Rpp8u));
	hipMalloc(&d_output, ioBufferSize * sizeof(Rpp8u));
	check_hip_error();
	hipMemcpy(d_input, input, ioBufferSize * sizeof(Rpp8u), hipMemcpyHostToDevice);
        hipMemcpy(d_input_second, input, ioBufferSize * sizeof(Rpp8u), hipMemcpyHostToDevice);
	check_hip_error();

    rppHandle_t handle;
    hipStream_t stream;
    hipStreamCreate(&stream);
    rppCreateWithStreamAndBatchSize(&handle, stream, noOfImages);

	clock_t start, end;   
	double cpu_time_used;
	start = clock();
    string test_case_name;
    int test_case = atoi(argv[1]);
    uint kernelSize = 3;
    Rpp32f alpha = 0.5;
    Rpp32f beta = 100;
    Rpp32s adjustmentValue = 100;
    Rpp32f exposureFactor = 0.5;
    Rpp32u flipAxis = 0;
    Rpp32f fogValue = 1;
    Rpp32f gamma = 0.5;
    Rpp32f strength = 1.5;
    Rpp32f zoom = 0;
    Rpp32f noiseProbability = 0.5;
    Rpp32f rainPercentage = 0.5; 
    Rpp32u rainWidth = 3; 
    Rpp32u rainHeight = 6;
    Rpp32f transparency = 0.5;
    Rpp32f stdDev = 20;
    Rpp32f snowPercentage = 0.4;
    Rpp32f angle = 135.0;
    Rpp32f affine[6] = {1.0, 2.0, 1.0, 1.0, 1.0, 2.0};
    Rpp32f coordinates[4] = {100, 200, 200, 400}
    switch (test_case)
    {
    case 0:
        test_case_name = "contrast";
        rppi_contrast_u8_pkd3_gpu(d_input, srcSize[0], d_output, newMin, newMax, handle);
        break;
    case 1:
        test_case_name = "jitter";
        rppi_jitter_u8_pkd3_gpu(d_input, srcSize[0], d_output, kernelSize, handle);
        break;
    case 2:
        test_case_name = "blur";
        rppi_blur_u8_pkd3_gpu(d_input, srcSize[0], d_output, kernelSize, handle);
	break;
    case 3:
        test_case_name = "brightness";
        rppi_brightness_u8_pkd3_gpu(d_input, srcSize[0], d_output, alpha, beta, handle);
        break;
    case 4:
        test_case_name = "blend";
	rppi_blend_u8_pkd3_gpu(d_input, d_input_second, srcSize[0], d_output, alpha, handle);
        break;
    case 5:
        test_case_name = "color_temperature";
	rppi_color_temperature_u8_pkd3_gpu(d_input, srcSize[0], d_output, adjustmentValue, handle);
        break;
    case 6:
        test_case_name = "gamma_correction";
        rppi_gamma_correction_u8_pkd3_gpu(d_input, srcSize[0], d_output, gamma, handle);
        break;
    case 7:
        test_case_name = "fog";
        rppi_fog_u8_pkd3_gpu(d_input, srcSize[0], d_output, fogValue, handle);
        break;
    case 8:
        test_case_name = "snow";
        rppi_snow_u8_pkd3_gpu(d_input, srcSize[0], d_output, snowPercentage, handle);
        break;
    case 9:
        test_case_name = "lens_correction";
        rppi_lens_correction_u8_pkd3_gpu(d_input, srcSize[0], d_output, strength, zoom, handle);
        break;
    case 10:
        test_case_name = "noise";
        rppi_noise_u8_pkd3_gpu(d_input, srcSize[0], d_output, noiseProbability, handle);
        break;
    case 11:
        test_case_name = "pixelate";
        rppi_pixelate_u8_pkd3_gpu(d_input, srcSize[0], d_output, handle);
        break;
    case 12:
        test_case_name = "exposure";
        rppi_exposure_u8_pkd3_gpu(d_input, srcSize[0], d_output, exposureFactor, handle);
        break;
    case 13:
        test_case_name = "fisheye";
	rppi_fisheye_u8_pkd3_gpu(d_input, srcSize[0], d_output, handle);
        break;
    case 14:
        test_case_name = "vignette";
        rppi_vignette_u8_pkd3_gpu(d_input, srcSize[0], d_output, stdDev, handle);
        break;
    case 15:
        test_case_name = "flip";
        rppi_flip_u8_pkd3_gpu(d_input, srcSize[0], d_output, flipAxis, handle);
        break;
    case 16:
        test_case_name = "rain";
        rppi_rain_u8_pkd3_gpu(d_input, srcSize[0], d_output, rainPercentage, rainWidth, rainHeight, transparency, handle);
        break;
    case 17:
        test_case_name = "rotate";
        rppi_rotate_u8_pkd3_gpu(d_input, srcSize[0], d_output, dstSize[0], angle, handle);
        break;
    case 18:
        test_case_name = "warp-affine";
        rppi_warp_affine_u8_pkd3_gpu(d_input, srcSize[0], d_output, dstSize[0], affine, handle);
        break;
    case 19:
        test_case_name = "resize";
        rppi_resize_u8_pkd3_gpu(d_input, srcSize[0], d_output, dstSize[0], handle);
    case 20:
        test_case_name = "resize_crop";
        rppi_resize_u8_pkd3_gpu(d_input, srcSize[0], d_output, dstSize[0], coordinates[0], coordinates[1],
        coordinates[2], coordinates[4],  handle);
    
    default:
        break;
    }
    end = clock();
	cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	cout<<"\n Single : "<<cpu_time_used<<endl;  

	hipMemcpy(output,d_output,oBufferSize * sizeof(Rpp8u),hipMemcpyDeviceToHost);

	rppDestroyGPU(handle);

    count = 0;
    for(j = 0 ; j < noOfImages ; j++)
    {
        int op_size = srcSize[j].height * srcSize[j].width * ip_channel;
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
            mat_op_image = Mat(srcSize[j].height, srcSize[j].width, CV_8UC3, temp_output);
            imwrite(temp, mat_op_image);
        }
        if(ip_channel == 1)
        {
            mat_op_image = Mat(srcSize[j].height, srcSize[j].width, CV_8UC1, temp_output);
            imwrite(temp, mat_op_image);
        }
        free(temp_output);
    }

    free(srcSize);
    free(input);
    free(output);
	 return 0; 
}
