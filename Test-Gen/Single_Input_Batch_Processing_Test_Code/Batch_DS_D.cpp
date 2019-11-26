#include <stdio.h> 
#include <dirent.h>
#include<string.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <CL/cl.hpp>
#include "/opt/rocm/rpp/include/rppi.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include<time.h> 

using namespace cv;
using namespace std;

int G_IP_CHANNEL = INPUT%1;
int G_MODE = INPUT%2;
char src[1000] = {"INPUT%3"}; 
char dst[1000] = {"INPUT%4"};
char funcName[1000] = {"INPUT%5"};
char funcType[1000] = {"_Batch_DS_ROID"};
float G_MAX_ALPHA = 4;
float G_MAX_BETA = 255;

int main(int argc, char **argv)
{
    srand(time(0));
    
    int ip_channel = G_IP_CHANNEL;
    int mode = G_MODE;
    
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
        strcat(funcType,"_HIP")
    }
    if(ip_channel == 1)
    {
        strcat(funcType,"_PLN");
    }
    else
    {
        strcat(funcType,"_PKD")
    }
    
    int i = 0, j = 0;
    unsigned long long count = 0;
    unsigned long long ioBufferSize = 0;
    
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
    }
    closedir(dr);

    RppiSize *srcSize = (RppiSize *)calloc(noOfImages, sizeof(RppiSize));
    RppiROI *roiPoints = (RppiROI *)calloc(noOfImages, sizeof(RppiROI));
    const int images = noOfImages;
    char imageNames[images][1000];
    
    /* Get all image dimensions */
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
        while(1)
        {
            roiPoints[count].x = rand() % srcSize[count].width; 
            roiPoints[count].y = rand() % srcSize[count].height; 
            roiPoints[count].roiHeight = (rand() % srcSize[count].height) * 3; 
            roiPoints[count].roiWidth = (rand() % srcSize[count].width) * 3;
            roiPoints[count].roiHeight -= roiPoints[count].y; 
            roiPoints[count].roiWidth -= roiPoints[count].x;
            if((roiPoints[count].y + roiPoints[count].roiHeight > roiPoints[count].y && roiPoints[count].x + roiPoints[count].roiWidth > roiPoints[count].x) && (roiPoints[count].y + roiPoints[count].roiHeight < srcSize[count].height && roiPoints[count].x + roiPoints[count].roiWidth < srcSize[count].width))
                break;
        }
        count++;
    }
    closedir(dr1); 
    
    /* Allocate input and out put buffer */
    Rpp8u *input = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));
    Rpp8u *output = (Rpp8u *)calloc(ioBufferSize, sizeof(Rpp8u));

    /* Read the input image */
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
    }
    closedir(dr2); 

/* CODE BEGINS HERE */ 
    
/* CODE ENDS HERE */

    /* Write image */
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
    free(roiPoints);
    return 0;
}