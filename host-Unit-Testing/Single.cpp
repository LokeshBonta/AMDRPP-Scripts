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
char src[1000] = {"/inputpath/"};
char src_second[1000] = {"/input2path/"};
char dst[1000] = {"/output/path/"};
char funcType[1000] = {"Single"};


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
    unsigned long long count = 0;
    unsigned long long ioBufferSize = 0;
    
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
        break;
    }
    closedir(dr);

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
        ioBufferSize += (unsigned long long)srcSize[count].height * (unsigned long long)srcSize[count].width * (unsigned long long)ip_channel;

        count++;
        break;
    }
    closedir(dr1); 

    Rpp8u *input = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));
    Rpp8u *input_second = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));
    Rpp8u *output = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));

    /* Read the input image */
    DIR *dr2 = opendir(src);
    DIR *dr2_second = opendir(src_second);
    count = 0;
    i = 0;
    while ((de = readdir(dr2)) != NULL) 
    {
        if(strcmp(de->d_name,".") == 0 || strcmp(de->d_name,"..") == 0) 
            continue;
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
        for(j = 0 ; j < srcSize[i].height * srcSize[i].width * ip_channel ; j++)
        {
            input[count] = ip_image[j];
            input_second[count] = ip_image_second[j];
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
    
    rppHandle_t handle;
	rppCreateWithBatchSize(&handle, noOfImages);
 
	
	clock_t start, end;   
	double cpu_time_used;
	start = clock();


string test_case_name;
    int test_case = atoi(argv[1]);
    uint kernelSize = 5;
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
    Rpp32f affine[6] = {1.0, 1.0, 0.01, 0.05, 0.15, 1.0};
    Rpp32f coordinates[4] = {100, 200, 250, 300};
    switch (test_case)
    {
    case 0:
        test_case_name = "contrast";
        rppi_contrast_u8_pkd3_host(input, srcSize[0], output, newMin, newMax, handle);
        break;
    case 1:
        test_case_name = "jitter";
        rppi_jitter_u8_pkd3_host(input, srcSize[0], output, kernelSize, handle);
        break;
    case 2:
        test_case_name = "blur";
        rppi_blur_u8_pkd3_host(input, srcSize[0], output, kernelSize, handle);
	break;
    case 3:
        test_case_name = "brightness";
        rppi_brightness_u8_pkd3_host(input, srcSize[0], output, alpha, beta, handle);
        break;
    case 4:
        test_case_name = "blend";
	rppi_blend_u8_pkd3_host(input, input_second, srcSize[0], output, alpha, handle);
        break;
    case 5:
        test_case_name = "color_temperature";
	rppi_color_temperature_u8_pkd3_host(input, srcSize[0], output, adjustmentValue, handle);
        break;
    case 6:
        test_case_name = "gamma_correction";
        rppi_gamma_correction_u8_pkd3_host(input, srcSize[0], output, gamma, handle);
        break;
    case 7:
        test_case_name = "fog";
        rppi_fog_u8_pkd3_host(input, srcSize[0], output, fogValue, handle);
        break;
    case 8:
        test_case_name = "snow";
        rppi_snow_u8_pkd3_host(input, srcSize[0], output, snowPercentage, handle);
        break;
    case 9:
        test_case_name = "lens_correction";
        rppi_lens_correction_u8_pkd3_host(input, srcSize[0], output, strength, zoom, handle);
        break;
    case 10:
        test_case_name = "noise";
        rppi_noise_u8_pkd3_host(input, srcSize[0], output, noiseProbability, handle);
        break;
    case 11:
        test_case_name = "pixelate";
        rppi_pixelate_u8_pkd3_host(input, srcSize[0], output, handle);
        break;
    case 12:
        test_case_name = "exposure";
        rppi_exposure_u8_pkd3_host(input, srcSize[0], output, exposureFactor, handle);
        break;
    case 13:
        test_case_name = "fisheye";
	rppi_fisheye_u8_pkd3_host(input, srcSize[0], output, handle);
        break;
    case 14:
        test_case_name = "vignette";
        rppi_vignette_u8_pkd3_host(input, srcSize[0], output, stdDev, handle);
        break;
    case 15:
        test_case_name = "flip";
        rppi_flip_u8_pkd3_host(input, srcSize[0], output, flipAxis, handle);
        break;
    case 16:
        test_case_name = "rain";
        rppi_rain_u8_pkd3_host(input, srcSize[0], output, rainPercentage, rainWidth, rainHeight, transparency, handle);
        break;
    case 17:
        test_case_name = "rotate";
        rppi_rotate_u8_pkd3_host(input, srcSize[0], output, dstSize[0], angle, handle);
        break;
    case 18:
        test_case_name = "warp-affine";
        rppi_warp_affine_u8_pkd3_host(input, srcSize[0], output, dstSize[0], affine, handle);
        break;
    case 19:
        test_case_name = "resize";
        rppi_resize_u8_pkd3_host(input, srcSize[0], output, dstSize[0], handle);
    case 20:
        test_case_name = "resize_crop";
        rppi_resize_crop_u8_pkd3_host(input, srcSize[0], output, dstSize[0], coordinates[0], coordinates[1],
        coordinates[2], coordinates[3],  handle);
   
    
    default:
        break;
    }
    

    end = clock();
	cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	cout<<" Single : "<<cpu_time_used<<endl;  

    	rppDestroyHost(handle);


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
    free(input_second);
	 return 0; 
}
