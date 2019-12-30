#include <opencv2/opencv.hpp>
#include <opencv/highgui.h>

#include <string>
#include <vector>
#include <stdio.h>
#include <unistd.h>
#include <CL/cl.h>
#include <VX/vx.h>
#include <vx_ext_amd.h>
#include <vx_ext_rpp.h>
#include<chrono>
using namespace std;
using namespace std::chrono; 


static const size_t MAX_COMPRESSED_JPEG_SIZE = 1024*1024*1024; // 1 Meg

struct OCL {
    cl_command_queue cmd_queue;
    cl_context context;
    cl_device_id device_id;
    OCL( cl_context _context, cl_device_id _device_id, cl_command_queue _queue): cmd_queue (_queue), context(_context), device_id(_device_id) {}
    OCL() {cmd_queue = nullptr; context = nullptr; device_id = nullptr; }
};


struct ImageInfo {
    vx_size w;// Width of the image
    vx_size h;// Height of the image (including all the images batched in the current image)
    vx_size p;// Number of color planes
    vx_df_image col_fmt;
    vx_size sz;
    vx_enum mem_type;
    ImageInfo() {
        w = 0;
        h = 0;
        p = 0;
        sz = 0;
        mem_type = 0;
    }
    ImageInfo(int width, int height, int planes, vx_enum _mem_type, vx_df_image _col_fmt) {
        w = width;
        h = height;
        p = planes;
        sz = width*height*planes;
        mem_type = _mem_type;
        col_fmt = _col_fmt;
    }
};


struct Image {
    void *buf[4] = {nullptr};// pointer to planes used to store the pixels
    vx_image img = nullptr;
    ImageInfo info;
    Image(){
        img = 0;
        for(int i = 0; i < 4; i++)
            buf[i] = nullptr;
    }
};

vx_rectangle_t getRectArea(Image image, unsigned out_idx, int regions);
int initOpenCL(vx_context context, OCL &ocl);
int createImage(vx_context context,  Image* output, bool allocate, vx_uint32 alignpixels = 8);
int decode_image(unsigned char* encoded_buffer, unsigned fsize, cv::Mat& mat_output, int w, int h, int p);
int load_image(const std::string& file_path, unsigned char* encoded_buffer);

int main(int argc, const char** argv) {
        if(argc != 9) {
        printf("Usage: rppTest <input file name1> <input file name1>  <width>  <height> <planes> <ovx node id>  <host/ocl id> <num_of_iters>... \n");
        return -1;
    }
    int counter = 3;
    int width = atoi(argv[counter++]);
    int height = atoi(argv[counter++]);
    int planes = atoi(argv[counter++]);
    int ovx_func_id = atoi(argv[counter++]);
    int host = atoi(argv[counter++]);
    int num_of_iters = atoi(argv[counter++]);

    int d_w = width;
    int d_h = height;

    unsigned char* encoded_buffer = new unsigned char[MAX_COMPRESSED_JPEG_SIZE];
    unsigned char* encoded_buffer1 = new unsigned char[MAX_COMPRESSED_JPEG_SIZE];
    std::string file_path(argv[1]);
    std::string file_path1(argv[2]);

    int fsize = load_image(file_path, encoded_buffer);
    int fsize1 = load_image(file_path1, encoded_buffer1);

    if( fsize < 0 || fsize1 < 0){
        printf("Couldn't read the file %s\n", file_path.c_str());
        return -1;
    }

    int w= width, h = height, p = planes;
    cv::Mat decoded_image;
    cv::Mat decoded_image1;
    if(decode_image(encoded_buffer, fsize, decoded_image, w, h, p) != 0) {
        printf("Couldn't decode the image \n");
        return -2;
    } else {
        printf("Image of size %dx%dx%d decoded\n", w,h,p);
    }
    if(decode_image(encoded_buffer1, fsize1, decoded_image1, w, h, p) != 0) {
        printf("Couldn't decode the image \n");
        return -2;
    } else {
        printf("Image of size %dx%dx%d decoded\n", w,h,p);
    }
    vx_status status;
    AgoTargetAffinityInfo affinity = {0};

    affinity.device_type = (host ? AGO_TARGET_AFFINITY_CPU: AGO_TARGET_AFFINITY_GPU);
    printf(">>>> Setting the processing affinity to %s <<<<\n", (host ? "AGO_TARGET_AFFINITY_CPU": "AGO_TARGET_AFFINITY_GPU"));
    affinity.device_info = 0;
    vx_context context = vxCreateContext();
    if((status = vxGetStatus((vx_reference)context)) != VX_SUCCESS) {
        printf("ERROR: vxCreateContext: failed (%d)\n", status);
        return -3;
    }

    if((status = vxSetContextAttribute(context, VX_CONTEXT_ATTRIBUTE_AMD_AFFINITY, &affinity, sizeof(affinity)))!= VX_SUCCESS) {
        printf("ERROR: setting context affinity failed (%d)\n", status);
        return -3;
    }

    // std::cerr<<"\n ****************Gonna Load kernels**************";
    vxLoadKernels(context, "vx_rpp");
    // std::cerr<<"\n ****************Loaded kernels**************";
    vx_graph graph = vxCreateGraph(context);
    if((status = vxGetStatus((vx_reference)graph)) != VX_SUCCESS) {
        printf("ERROR: vxCreateGraph: failed (%d)\n", status);
        return -4;
    }

    if((status = vxSetGraphAttribute(graph, VX_GRAPH_ATTRIBUTE_AMD_AFFINITY, &affinity, sizeof(affinity))) != VX_SUCCESS) {
        printf("ERROR: vxSetGraphAttribute: failed (%d)\n", status);
        return -4;
    }

    Image input, input1, master_output;
    int regions = 1;
    // std::vector<Image> outputs;
    // outputs.resize(4);
    input.info = ImageInfo(w,h,p, (host ? VX_MEMORY_TYPE_HOST:VX_MEMORY_TYPE_OPENCL), ((p==1)?VX_DF_IMAGE_U8:VX_DF_IMAGE_RGB));
    input1.info = ImageInfo(w,h,p, (host ? VX_MEMORY_TYPE_HOST:VX_MEMORY_TYPE_OPENCL), ((p==1)?VX_DF_IMAGE_U8:VX_DF_IMAGE_RGB));
    master_output.info = ImageInfo(d_w,regions*d_h,p, (host ? VX_MEMORY_TYPE_HOST:VX_MEMORY_TYPE_OPENCL), ((p==1)?VX_DF_IMAGE_U8:VX_DF_IMAGE_RGB));
    // master_output.info = ImageInfo(d_w,regions*d_h,p, (host ? VX_MEMORY_TYPE_HOST:VX_MEMORY_TYPE_OPENCL), ((p==1)?VX_DF_IMAGE_U32:VX_DF_IMAGE_U32));



    printf("Done creating input/master_output images, input image buffer size %d , master_output buffer size %d\n",(int)input.info.sz, (int)master_output.info.sz );
    printf("Going to create input/master_output images\n");
    createImage(context, &input, true);
    createImage(context, &input1, true);
    createImage(context, &master_output, true);

#if 0
    for(int i = 0; i < regions; i++) {
		auto area = getRectArea(master_output, i, regions);
		printf("area[%d] %d %d %d %d\n", i, area.start_x, area.start_y, area.end_x, area.end_y);
		outputs[i].img = vxCreateImageFromROI(master_output.img, &area);
		outputs[i].info.sz = master_output.info.sz/regions;
		if(outputs[i].img == nullptr){
			printf("Error creating the output image out of the master image\n");
		}
	}
#endif
    OCL ocl;
    if(!host)
        initOpenCL(context, ocl);

    vx_status arr_status1, arr_status2;
    vx_node ret, ret1, ret2;
    vx_uint32 jitter = 3;
    vx_scalar JITTER = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &jitter);
    vx_uint32 kernelSize = 3;
    vx_scalar KERNELSIZE = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &kernelSize);
    vx_uint32 sobelType = 1;
    vx_scalar SOBELTYPE = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &sobelType);
    vx_float32 alphaAccumulate = 0.5;
    vx_scalar ALPHA_ACCUMULATE = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &kernelSize);
    vx_uint8 min;
    vx_uint8 max;
    vx_uint32 minLoc;
    vx_uint32 maxLoc;
    vx_uint32 cmin = 10;
    vx_uint32 cmax = 250;
    vx_scalar CMIN = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &cmin);
    vx_scalar CMAX = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &cmax);
    vx_uint8 c1 = 25;
    vx_uint8 c2 = 180;
    vx_scalar C1 = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT8, &c1);
    vx_scalar C2 = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT8, &c2);
    vx_scalar MIN = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT8, &min);
    vx_scalar MAX = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT8, &max);
    vx_scalar MINLOC = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &minLoc);
    vx_scalar MAXLOC = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &maxLoc);

    vx_array affineArray = vxCreateArray(context, VX_TYPE_FLOAT32, 10);
	vx_float32 arrVal[6] = {1.0,0.0,5,0,1.0,5};
    size_t bytes = 6 * sizeof(vx_float32);
	vx_size stride = sizeof(vx_float32);
    arr_status1 =  vxAddArrayItems(affineArray,6,arrVal,stride);


switch(ovx_func_id) {
        case 0:
        {
            printf(">>>> Running RPP Extension Function <<<<\n");
            //ret = vxExtrppNode_AbsoluteDifference(graph, input.img, input1.img, master_output.img);
            //ret = vxExtrppNode_Accumulate(graph, input.img, input1.img);
            //ret = vxExtrppNode_Erode(graph, input.img, master_output.img,KERNELSIZE);
            //ret = vxExtrppNode_Dilate(graph, input.img, master_output.img,KERNELSIZE);
            //ret = vxExtrppNode_AccumulateSquared(graph, input.img);
            // ret = vxExtrppNode_AccumulateWeighted(graph, input.img, input1.img, ALPHA_ACCUMULATE);
            // ret = vxExtrppNode_ChannelCombine(graph, input.img, input1.img, input1.img,master_output.img);
            // ret = vxExtrppNode_MinMaxLoc(graph,input.img, min, max, minLoc, maxLoc);
            // ret = vxExtrppNode_HistogramEqualize(graph, input.img, master_output.img);
            // ret = vxExtrppNode_Thresholding(graph, input.img, master_output.img,C1,C2);
            // ret = vxExtrppNode_DataObjectCopy(graph, input.img, master_output.img);
            // ret = vxExtrppNode_BilateralFilter(graph, input.img, master_output.img,KERNELSIZE, S1, S2);
            // ret = vxExtrppNode_BoxFilter(graph, input.img, master_output.img,KERNELSIZE);
            //  ret = vxExtrppNode_Sobel(graph, input.img, master_output.img,KERNELSIZE);
            // ret = vxExtrppNode_DataObjectCopy(graph, input.img, master_output.img);
            // ret = vxExtrppNode_LocalBinaryPattern(graph, input.img, master_output.img);
            // ret = vxExtrppNode_BoxFilter(graph, input.img, master_output.img,KERNELSIZE);
             //ret = vxExtrppNode_Sobel(graph, input.img, master_output.img,SOBELTYPE);
            // ret = vxExtrppNode_MedianFilter(graph, input.img, master_output.img,KERNELSIZE);
            // ret = vxExtrppNode_GaussianFilter(graph, input.img, master_output.img,SDEV,KERNELSIZE);
            // ret = vxExtrppNode_WarpAffine(graph, input.img, master_output.img,affineArray);
            // ret = vxExtrppNode_Min(graph, input.img, input1.img, master_output.img);
            // ret = vxExtrppNode_InclusiveOR(graph, input.img, input1.img, master_output.img);
            // ret = vxExtrppNode_BitwiseAND(graph, input.img, input1.img, master_output.img);
            // ret = vxExtrppNode_BitwiseNOT(graph, input.img, master_output.img);
            // ret = vxExtrppNode_Max(graph, input.img, input1.img, master_output.img);
            // ret = vxExtrppNode_Phase(graph, input.img, input1.img, master_output.img);
            // ret = vxExtrppNode_Magnitude(graph, input.img, input1.img, master_output.img);
            // ret = vxExtrppNode_ExclusiveOR(graph, input.img, input1.img, master_output.img);
            // ret = vxExtrppNode_Multiply(graph, input.img, input1.img, master_output.img);
            //  ret = vxExtrppNode_Subtract(graph, input.img, input1.img, master_output.img);
             ret = vxExtrppNode_Add(graph, input.img, input1.img, master_output.img);


        }
            break;
        case 1:
        {
           // vx_image intermediate1 = vxCreateVirtualImage(graph, input.info.w, input.info.h, VX_DF_IMAGE_VIRT);
            //vx_image intermediate2 = vxCreateVirtualImage(graph, input.info.w, input.info.h, VX_DF_IMAGE_VIRT);
            //  vx_image intermediate3 = vxCreateVirtualImage(graph, input.info.w, input.info.h, VX_DF_IMAGE_VIRT);
            //vx_image intermediate4 = vxCreateVirtualImage(graph, 0, 0, VX_DF_IMAGE_VIRT);
            printf(">>>> Running Main OVX Function      <<<<\n");
            ret = vxGaussian3x3Node(graph, input.img, master_output.img);
            //ret = vxDilate3x3Node(graph, intermediate1, intermediate2);
            //ret = vxErode3x3Node(graph, intermediate2, intermediate3);
            //ret = vxGaussian3x3Node(graph, intermediate3, master_output.img);
        }
            break;
    }

    std::cerr<<"\n Gonna add the OVX node to graph \n";

    if((status = vxGetStatus((vx_reference)ret)) != VX_SUCCESS) {
        printf("ERROR adding the OVX node to graph failed, error_id %d\n", status);
        return -5;
    }
    std::cerr<<"\n adding the OVX node to graph";
/*
	if((status = vxGetStatus((vx_reference)ret2)) != VX_SUCCESS) {
		printf("ERROR adding the OVX node to graph failed, error_id %d\n", status);
		return -6;
	}
*/
// Problem is here----------------------------
    if((status = vxVerifyGraph(graph)) != VX_SUCCESS) {
        printf("ERROR: vxVerifyGraph: failed (%d)\n", status);
        return -7;
    }


    printf("Going to copy input image size %d to the image's buffer size %d\n",w*h*p, input.info.sz );
    if(host) {
        memcpy((unsigned char*)input.buf[0],  decoded_image.data, w*h*p);
    } else {
        clEnqueueWriteBuffer(ocl.cmd_queue, (cl_mem)input.buf[0], CL_TRUE, 0, w*h*p, decoded_image.data, 0, NULL, NULL);
    }
    //printf("Going to run process graph \n");
    auto start = high_resolution_clock::now(); 
	for(int i =0; i< num_of_iters; i++){
			if((status = vxProcessGraph(graph)) != VX_SUCCESS) {
			printf("ERROR: Couldn't run graph %d\n", status);
			return -6;
		}
	}
    
	auto end = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(end - start); 
	std::cout << duration.count() << endl;
	std::cout << "time_taken " << duration.count() / num_of_iters << std::endl;

    sleep(1);
    cv::Mat out_image(regions*h, w, ((p==1)?CV_8UC1:CV_8UC3));

    printf("Going to copy output image from it's buffer \n");
    if(host) {
        memcpy( out_image.data, (unsigned char*)master_output.buf[0],w*h*p*regions );
    } else {
        clEnqueueReadBuffer(ocl.cmd_queue, (cl_mem)master_output.buf[0], CL_TRUE, 0, w*h*p*regions,  out_image.data, 0 , NULL, NULL);
    }


    printf("Going to display the input/output image\n");
    cv::imshow("input", decoded_image);
    cv::imshow("processed1", out_image);

    cv::waitKey(0);
    //std::vector<int> compression_params;
    //compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
    //compression_params.push_back(9);


    //cv::imwrite("output.png", out_image, compression_params);

    printf("Done!\n");

    return 0;
}

vx_rectangle_t getRectArea(Image image, unsigned out_idx, int regions) {
    int augmentation_stride = (image.info.h) / regions ;

    vx_rectangle_t area = { (vx_uint32)0,  (vx_uint32)out_idx*augmentation_stride, (vx_uint32)image.info.w ,(vx_uint32)(out_idx+1)*augmentation_stride};
    return area;
}

int load_image(const std::string& file_path, unsigned char* encoded_buffer) {
    FILE* fPtr = fopen(file_path.c_str(), "rb");// Open the file,

    if(!fPtr) // Check if it is ready for reading
        return -2;

    fseek(fPtr, 0 , SEEK_END);// Take the file read pointer to the end

    unsigned fsize = ftell(fPtr);// Check how many bytes are there between and the current read pointer position (end of the file)

    if(fsize == 0) {
        fclose(fPtr);
        return -3;
    }

    fseek(fPtr, 0 , SEEK_SET);// Take the file pointer back to the start

    if(fsize > MAX_COMPRESSED_JPEG_SIZE) {
        fclose(fPtr);
        printf("Larger than %d bytes input file %s detected\n", (int)MAX_COMPRESSED_JPEG_SIZE,  file_path.c_str());
        return -4;
    }

    fread(encoded_buffer, sizeof(unsigned char), fsize, fPtr);// Read the file and load the contents into the vector

    fclose(fPtr);

    return fsize;
}

int decode_image(unsigned char* encoded_buffer, unsigned fsize, cv::Mat& mat_output, int w, int h, int p) {
    auto mat_compressed = cv::Mat(1, fsize, CV_8UC1, encoded_buffer);
    auto mat_orig = cv::imdecode(mat_compressed,  cv::IMREAD_COLOR);// TODO: set the flag according to input image

    if(mat_orig.rows == 0 || mat_orig.cols == 0) {
        printf("Could not decode the image\n");
        return -5;
    } else {
        printf("Input image of size %d x %d\n", mat_orig.rows, mat_orig.cols);
    }

    cv::Mat mat_scaled;
    cv::resize(mat_orig, mat_scaled, cv::Size(w, h), cv::INTER_NEAREST);
    if(mat_scaled.rows == 0 || mat_scaled.cols == 0)
        return -6;



    unsigned char* decoded_data = mat_scaled.data ;
    int num_channels_out = p;
    int num_channels_in = 3;// TODO: get it from the input image,


    if(num_channels_out == 1 && num_channels_in == 3 ) {
        cv::cvtColor(mat_scaled, mat_output, CV_BGR2GRAY);
    } else {
        mat_output = mat_scaled;
    }

#ifdef DISPLAY_INPUT
    cv::imshow("scaled",mat_scaled);
	cv::imshow("input",mat_orig);
    cv::imshow("output", mat_output);
	cv::waitKey(0);
#endif
    mat_compressed.release();
    mat_orig.release();
    mat_scaled.release();
    return 0;
}

int createImage(vx_context context,  Image* output, bool allocate, vx_uint32 alignpixels)
{

    // TODO: the pointer passed here changes if the number of planes are more than one
    vx_imagepatch_addressing_t addr_in = { 0 };
    void *ptr[1] = { nullptr };
    addr_in.step_x = 1;
    addr_in.step_y = 1;
    addr_in.scale_x = VX_SCALE_UNITY;
    addr_in.scale_y = VX_SCALE_UNITY;
    addr_in.dim_x = output->info.w;
    addr_in.dim_y = output->info.h;
    // TODO: ADD support for other formats

    addr_in.stride_x = output->info.p;

    if (alignpixels == 0)
        addr_in.stride_y = addr_in.dim_x *addr_in.stride_x;
    else
        addr_in.stride_y = ((addr_in.dim_x + alignpixels - 1) & ~(alignpixels - 1))*addr_in.stride_x;

    vx_size size = (addr_in.dim_y+0) * (addr_in.stride_y+0);
    if(allocate)
    {
        if(output->info.mem_type == VX_MEMORY_TYPE_OPENCL) {
            cl_context opencl_context = nullptr;
            // allocate opencl buffer with required dim
            vx_status status = vxQueryContext(context, VX_CONTEXT_ATTRIBUTE_AMD_OPENCL_CONTEXT, &opencl_context, sizeof(opencl_context));
            if (status != VX_SUCCESS){
                printf("vxQueryContext of failed(%d)\n", status);
                return -1;
            }

            cl_int ret = CL_SUCCESS;
            cl_mem clImg = clCreateBuffer(opencl_context, CL_MEM_READ_WRITE, size, NULL, &ret);
            if (!clImg || ret){
                printf("clCreateBuffer of size %d failed(%d)\n", (int)size, ret);
                return -2;
            }
            ptr[0] = clImg;
        } else {
            unsigned char* hostImage = new unsigned char[size];
            memset(hostImage, 127 ,size );
            ptr[0] = hostImage;
        }
        // TODO : handle multiple planes
        output->buf[0] = ptr[0];

    }

    output->img = vxCreateImageFromHandle(context, output->info.col_fmt, &addr_in, ptr, output->info.mem_type);
    if(!output->img){
        printf("Couldn't create the image from handle\n");
        return -4;
    }
    output->info.sz = size;
    return 0;
}


int initOpenCL(vx_context context, OCL &ocl)
{
    cl_int clerr;
    cl_context clcontext;
    cl_device_id dev_id;
    cl_command_queue cmd_queue;
    vx_status vxstatus = vxQueryContext(context, VX_CONTEXT_ATTRIBUTE_AMD_OPENCL_CONTEXT, &clcontext, sizeof(clcontext));
    if (vxstatus != VX_SUCCESS) {
        printf("vxQueryContext of failed(%d)\n", vxstatus);
        return -1;
    }
    cl_int clstatus = clGetContextInfo(clcontext, CL_CONTEXT_DEVICES, sizeof(dev_id), &dev_id, nullptr);
    if (clstatus != VX_SUCCESS) {
        printf("clGetContextInfo of failed(%d)\n", clstatus);
        return -2;
    }
#if defined(CL_VERSION_2_0)
    cmd_queue = clCreateCommandQueueWithProperties(clcontext, dev_id, NULL, &clerr);
#else
    cmd_queue = clCreateCommandQueue(opencl_context, dev_id, 0, &clerr);
#endif
    if(clerr != CL_SUCCESS) {
        printf("Create Command Queue failed %d\n", clerr);
        return -3;
    }

    ocl = OCL( clcontext, dev_id, cmd_queue);

    return 0;
}
