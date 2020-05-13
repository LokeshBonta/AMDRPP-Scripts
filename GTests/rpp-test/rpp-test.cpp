#include <gtest/gtest.h>
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
char src[1000] = {"/home/lokesh/AMD/sample"};
char src_second[1000] = {"/home/lokesh/AMD/sample"};
char dst[1000] = {"/home/neel/Ulagammai/Output"};
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
    Rpp8u *cpu_output = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));
    
   
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
    int test_case = atoi(argv[1]);
    Rpp32u newMin = 30;
Rpp32u newMax = 100;
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
    Rpp32f coordinates[4] = {100, 200, 200, 400};
    Rpp32f hueShift = 10;
    Rpp32f saturationFactor = 10;
    Rpp8u minThreshold = 10;
    Rpp8u maxThreshold = 30;
    Rpp32u numOfPixels = 4;
		Rpp32u gaussianKernelSize = 7;
		Rpp32f kValue = 1;
		Rpp32f threshold = 15;
		Rpp32u nonmaxKernelSize = 5;
     	Rpp32u sobelType = 1;
		Rpp8u min = 10;
		Rpp8u max = 30;
        Rpp32u crop_pos_x = 100;
	    Rpp32u crop_pos_y = 100;
        Rpp32u xRoiBegin = 50;
		Rpp32u yRoiBegin = 50;
        	Rpp32u xRoiEnd  = 200;
        	Rpp32u yRoiEnd  = 200;
        	Rpp32u mirrorFlag = 0;

	
        Rpp32f perspective[9];

        perspective[0] = 1;
        perspective[1] = 0;
        perspective[2] = 0.5;
        perspective[3] = 0;
        perspective[4] = 1;
        perspective[5] = 0.5;  
        perspective[6] = 1;
        perspective[7] = 0;
        perspective[8] = 0.5;
        Rpp32f percentage = 100;
        Rpp32u numbeoOfShadows =12;
        Rpp32u maxSizeX = 12;
	    Rpp32u maxSizey = 15;
        Rpp32u extractChannelNumber = 1;


    switch (test_case)
    {
    case 1:
        test_case_name = "brightness";
        rppi_brightness_u8_pkd3_gpu(d_input, srcSize[0], d_output, alpha, beta, handle);
        rppi_brightness_u8_pkd3_host(input, srcSize[0], cpu_output, alpha, beta, handle);
        break;
    default:
        break;
    }
    
    end = clock();
	cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	cout<<" Single : "<<cpu_time_used<<endl;  

	clEnqueueReadBuffer(theQueue, d_output, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), output, 0, NULL, NULL);
            int res = 1;
             count = 0;

    for(int i = 0; i < srcSize[0].height * srcSize[0].width * 3; i++)
    {

        if(std::abs(output[i] - cpu_output[i]) > 5)
            count++;
        if(count > 30)
            {res = 0; break;}
    }
    cout << res << count << endl;
	rppDestroyGPU(handle);
    free(srcSize);
    free(input);
    free(output);
    free(cpu_output);
    free(input_second);
	return 0; 
}

// TEST(CPU_OUTPUT, GPU_OUTPUT) 
//     {
//         ASSERT_TRUE(CPU_OUTPT.isApprox(GPU_OUTPUT));
//     }

// //MAIN FUNCTION TO CALL TESTS
// int main(int argc, char **argv) 
// {
//     testing::InitGoogleTest(&argc, argv);
//     return RUN_ALL_TESTS();
// }
