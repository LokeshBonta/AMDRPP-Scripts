import subprocess
import csv
import shlex, subprocess
import os

non_scalar = ["vx_image","vx_array","vx_matrix"]
scalar_type = ["int8_t","uint8_t","int16_t","uint16_t","vx_int32","vx_uint32","vx_int64","vx_uint64","vx_float32","vx_float64"]
ovx_type = ["VX_TYPE_INT8","VX_TYPE_UINT8","VX_TYPE_INT16","VX_TYPE_UINT16","VX_TYPE_INT32","VX_TYPE_UINT32","VX_TYPE_INT64","VX_TYPE_UINT64","VX_TYPE_FLOAT32","VX_TYPE_FLOAT64"]
rpp_type = ["Rpp8s","Rpp8u","Rpp16s","Rpp16u","Rpp32s","Rpp32u","Rpp64s","Rpp64u","Rpp32f","Rpp64f"]

copy_rights = r'''
/*
Copyright (c) 2015 Advanced Micro Devices, Inc. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

'''


def write_internal_publish_header(func_name, file_name):
    f = open(file_name,"w+")
    header_start = r'''
#ifndef _PUBLISH_KERNELS_H_
#define _PUBLISH_KERNELS_H_

#include "internal_rpp.h"

extern "C" SHARED_PUBLIC vx_status VX_API_CALL vxPublishKernels(vx_context context);
vx_status ADD_KERENEL(std::function<vx_status(vx_context)>);
vx_status get_kernels_to_publish();

'''
    line1 = []
    line2 = []
    for function in func_name:
        temp1 = ""
        temp2 = ""
        line1.append("vx_status "+function+"_Register(vx_context);\n")
        line2.append("#define VX_KERNEL_RPP_"+function.upper()+"_NAME      "+"\"org.rpp."+function+"\"\n")
    line1.append("\n \n")
    header_end = "\n #endif //_AMDVX_EXT__PUBLISH_KERNELS_H_"
    f.write(header_start)
    file_contents = line1 + line2
    for line in file_contents:
        f.write(line)
    f.write(header_end)

def write_kernel_rpp_header(func_name, file_name):
    f = open(file_name,"w+")
    header_start = r'''
#ifndef _VX_KERNELS_RPP_H_
#define _VX_KERNELS_RPP_H_

#define OPENVX_KHR_RPP   "vx_khr_rpp"
//////////////////////////////////////////////////////////////////////
// SHARED_PUBLIC - shared sybols for export
// STITCH_API_ENTRY - export API symbols
#if _WIN32
#define SHARED_PUBLIC extern "C" __declspec(dllexport)
#else
#define SHARED_PUBLIC extern "C" __attribute__ ((visibility ("default")))
#endif

//! \brief The macro for error checking from OpenVX status.
#define ERROR_CHECK_STATUS(call) { vx_status status = (call); if(status != VX_SUCCESS){ vxAddLogEntry(NULL, status, "ERROR: failed with status = (%d) at " __FILE__ "#%d\n", status, __LINE__); return status; }}
#define STATUS_ERROR_CHECK(call){vx_status status = call; if(status!= VX_SUCCESS) return status;}
#define PARAM_ERROR_CHECK(call){vx_status status = call; if(status!= VX_SUCCESS) goto exit;}
//! \brief The macro for error checking from OpenVX object.
#define ERROR_CHECK_OBJECT(obj)  { vx_status status = vxGetStatus((vx_reference)(obj)); if(status != VX_SUCCESS){ vxAddLogEntry((vx_reference)(obj), status, "ERROR: failed with status = (%d) at " __FILE__ "#%d\n", status, __LINE__); return status; }}

//////////////////////////////////////////////////////////////////////
// common header files
#include <VX/vx.h>
#include <vx_ext_rpp.h>
#include <vx_ext_amd.h>
#include <iostream>
#include <string.h>

#define ERRMSG(status, format, ...) printf("ERROR: " format, __VA_ARGS__), status


#define VX_LIBRARY_RPP         1

enum vx_kernel_ext_amd_rpp_e
{'''
    header_end = '''
};

//////////////////////////////////////////////////////////////////////
//! \brief Common data shared across all nodes in a graph
struct RPPCommonHandle {
#if ENABLE_OPENCL
    cl_command_queue cmdq;
#endif
    void* cpuHandle = NULL;
    int count;
    bool exhaustiveSearch;
};
//////////////////////////////////////////////////////////////////////
//! \brief The utility functions
vx_node createNode(vx_graph graph, vx_enum kernelEnum, vx_reference params[], vx_uint32 num);
vx_status createGraphHandle(vx_node node, RPPCommonHandle ** pHandle);
vx_status releaseGraphHandle(vx_node node, RPPCommonHandle * handle);
int getEnvironmentVariable(const char* name);

#endif //__KERNELS_H__
'''
    line = []
    for idx,function in enumerate(func_name):
        line.append("VX_KERNEL_RPP_"+function.upper()+" = VX_KERNEL_BASE(VX_ID_AMD, VX_LIBRARY_RPP) +"+hex(idx)+",\n")
    f.write(header_start)
    f.write("\n")
    for i in line:
        f.write(i)
    f.write(header_end)

def write_vx_ext_rpp_header(func_name, params_list, func_declaration, file_name):
    f = open(file_name,"w+")
    header_start = r'''
#ifndef _VX_EXT_RPP_H_
#define _VX_EXT_RPP_H_

#include <VX/vx.h>
#include "kernels_rpp.h"

#if ENABLE_OPENCL
#include <CL/cl.h>
#endif


/*!***********************************************************************************************************
                    RPP VX_API_ENTRY C Function NODE
*************************************************************************************************************/
'''
    header_end = "#endif //_VX_EXT_RPP_H_"
    temp = 'extern "C" SHARED_PUBLIC vx_node VX_API_CALL vxExtrppNode_'
    input_variant = ["I","O","B"]
    for idx,func in enumerate(func_name):
        temp1 = temp+func+"(vx_graph graph,"
        idy = 0
        temp_list = params_list[idx]
        while(idy < len(temp_list)):
            if temp_list[idy] in non_scalar:
                temp1 += temp_list[idy]+" " +temp_list[idy+1]+","
            else:
                temp1 += "vx_scalar " +temp_list[idy+1]+","
            idy += 3
        temp1 = temp1[:-1]
        temp1 += ");\n"
        func_declaration.append(temp1)
    f.write(header_start)
    for line in func_declaration:
        f.write(line)
    f.write(header_end)



def write_internal_publishkernel_cpp(func_name, file_name):
    f = open(file_name,"w+")
    cpp_start = r'''
#include "internal_publishKernels.h"
#include "vx_ext_rpp.h"

/**********************************************************************
  PUBLIC FUNCTION for OpenVX user defined functions
  **********************************************************************/
extern "C"  SHARED_PUBLIC vx_status VX_API_CALL vxPublishKernels(vx_context context)
{
	vx_status status = VX_SUCCESS;

	STATUS_ERROR_CHECK(get_kernels_to_publish());
	STATUS_ERROR_CHECK(Kernel_List->PUBLISH(context));

	return status;
}

/************************************************************************************************************
Add All Kernels to the Kernel List
*************************************************************************************************************/
vx_status get_kernels_to_publish()
{
	vx_status status = VX_SUCCESS;

	Kernel_List = new Kernellist(MAX_KERNELS);'''
    cpp_end = '''
    	return status;
}

/************************************************************************************************************
Add Kernels to the Kernel List
*************************************************************************************************************/
vx_status ADD_KERENEL(std::function<vx_status(vx_context)> func)
{
	vx_status status = VX_SUCCESS;
	STATUS_ERROR_CHECK(Kernel_List->ADD(func));
	return status;
}'''
    f.write(cpp_start)
    for func in func_name:
        f.write("\n\tSTATUS_ERROR_CHECK(ADD_KERENEL("+func+"_Register));")
    f.write(cpp_end)

def write_kernel_rpp_cpp(func_name,params_list, func_declaration, file_name):
    f = open(file_name,"w+")
    cpp_start = r'''
#include "kernels_rpp.h"

vx_uint32 getGraphAffinity(vx_graph graph)
{
    AgoTargetAffinityInfo affinity;
    vxQueryGraph(graph, VX_GRAPH_ATTRIBUTE_AMD_AFFINITY,&affinity, sizeof(affinity));;
    if(affinity.device_type != AGO_TARGET_AFFINITY_GPU && affinity.device_type != AGO_TARGET_AFFINITY_CPU)
        affinity.device_type = AGO_TARGET_AFFINITY_CPU;
   // std::cerr<<"\n affinity "<<affinity.device_type;
    return affinity.device_type;
}
'''
    cpp_end = r'''
// utility functions
vx_node createNode(vx_graph graph, vx_enum kernelEnum, vx_reference params[], vx_uint32 num)
{
    vx_status status = VX_SUCCESS;
    vx_node node = 0;
    vx_context context = vxGetContext((vx_reference)graph);
    if(vxGetStatus((vx_reference)context) != VX_SUCCESS) {
        return NULL;
    }
    vx_kernel kernel = vxGetKernelByEnum(context, kernelEnum);
    if(vxGetStatus((vx_reference)kernel) == VX_SUCCESS) {
        node = vxCreateGenericNode(graph, kernel);
        if (node) {
            vx_uint32 p = 0;
            for (p = 0; p < num; p++) {
                if (params[p]) {
                    status = vxSetParameterByIndex(node, p, params[p]);
                    if (status != VX_SUCCESS) {
                        char kernelName[VX_MAX_KERNEL_NAME];
                        vxQueryKernel(kernel, VX_KERNEL_NAME, kernelName, VX_MAX_KERNEL_NAME);
                        vxAddLogEntry((vx_reference)graph, status, "createNode: vxSetParameterByIndex(%s, %d, 0x%p) => %d\n", kernelName, p, params[p], status);
                        vxReleaseNode(&node);
                        node = 0;
                        break;
                    }
                }
            }
        }
        else {
            vxAddLogEntry((vx_reference)graph, VX_ERROR_INVALID_PARAMETERS, "createNode: failed to create node with kernel enum %d\n", kernelEnum);
            status = VX_ERROR_NO_MEMORY;
        }
        vxReleaseKernel(&kernel);
    }
    else {
        vxAddLogEntry((vx_reference)graph, VX_ERROR_INVALID_PARAMETERS, "createNode: failed to retrieve kernel enum %d\n", kernelEnum);
        status = VX_ERROR_NOT_SUPPORTED;
    }
    return node;
}

#if ENABLE_OPENCL
int getEnvironmentVariable(const char * name)
{
    const char * text = getenv(name);
    if (text) {
        return atoi(text);
    }
    return -1;
}

vx_status createGraphHandle(vx_node node, RPPCommonHandle ** pHandle)
{
    RPPCommonHandle * handle = NULL;
    STATUS_ERROR_CHECK(vxGetModuleHandle(node, OPENVX_KHR_RPP, (void **)&handle));
    if(handle) {
        handle->count++;
    }
    else {
        handle = new RPPCommonHandle;
        memset(handle, 0, sizeof(*handle));
        const char * searchEnvName = "NN_MIOPEN_SEARCH";
        int isEnvSet = getEnvironmentVariable(searchEnvName);
        if (isEnvSet > 0)
            handle->exhaustiveSearch = true;

        handle->count = 1;
        STATUS_ERROR_CHECK(vxQueryNode(node, VX_NODE_ATTRIBUTE_AMD_OPENCL_COMMAND_QUEUE, &handle->cmdq, sizeof(handle->cmdq)));

    }
    *pHandle = handle;
    return VX_SUCCESS;
}

vx_status releaseGraphHandle(vx_node node, RPPCommonHandle * handle)
{
    handle->count--;
    if(handle->count == 0) {
        //TBD: release miopen_handle
        delete handle;
        STATUS_ERROR_CHECK(vxSetModuleHandle(node, OPENVX_KHR_RPP, NULL));
    }
    return VX_SUCCESS;
}
#endif
'''
    f.write(cpp_start)
    for idx,func in enumerate(func_name):
        declr = func_declaration[idx]
        declr = declr.replace('extern "C" SHARED_PUBLIC','VX_API_ENTRY')
        declr = declr[:-2] + "\n{"
        start = ["\tvx_node node = NULL;","\tvx_context context = vxGetContext((vx_reference)graph);","\tif(vxGetStatus((vx_reference)context) == VX_SUCCESS) {"]
        affinity = ["\t\tvx_uint32 dev_type = getGraphAffinity(graph);","\t\tvx_scalar DEV_TYPE = vxCreateScalar(vxGetContext((vx_reference)graph), VX_TYPE_UINT32, &dev_type);"]
        ref_dec = ["\t\tvx_reference params[] = {"]
        node_create = "\t\t}; \n\t\t node = createNode(graph, VX_KERNEL_RPP_, params, nop);"
        ref_affinity = ["\t\t\t(vx_reference) DEV_TYPE"]
        ref_arr = []
        idy = 0
        temp_param = params_list[idx]
        while(idy < len(temp_param)):
            # type = temp_param[idy]
            param = temp_param[idy+1]
            # if type not in non_scalar:
            #     temp_scalar = ""
            #     temp_scalar = "vx_scalar "+param.upper()+ "= vxCreateScalar(vxGetContext((vx_reference)graph), "
            #     temp_scalar += ovx_type[scalar_type.index(type)]+", &"+param
            #     scalar.append(temp_scalar)
            #     ref_arr.append("(vx_reference) "+param.upper()+",")
            # else:
            ref_arr.append("\t\t\t(vx_reference) "+param+",")
            idy += 3
        param_cnt = len(temp_param)/3+1
        node_create = node_create.replace("VX_KERNEL_RPP_","VX_KERNEL_RPP_"+func.upper())
        node_create = node_create.replace("nop",str(param_cnt))
        end = ["\t}","\treturn node;","}"]
        contents = []
        contents = [declr] + start + affinity + ref_dec + ref_arr + ref_affinity + [node_create] + end
        for line in contents:
            f.write(line+"\n")
    f.write(cpp_end)
