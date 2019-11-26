import subprocess
import csv
import shlex, subprocess
import os
from write_header import write_internal_publish_header,write_kernel_rpp_header
from write_header import write_vx_ext_rpp_header,write_internal_publishkernel_cpp,write_kernel_rpp_cpp

csv_name = "/home/mcw/AMD_RPP_shobi/ktnotes/scripts/RPP_Automation/MivisionX_automation/mivisionx.csv"
src_dir = "/home/mcw/AMD_RPP_shobi/ktnotes/MIVISION/amd_openvx_extensions/amd_rpp/"
non_scalar = ["vx_image","vx_array","vx_matrix"]
non_scalar_type = ["VX_TYPE_IMAGE","VX_TYPE_ARRAY","VX_TYPE_MATRIX"]
scalar_type = ["int8_t","uint8_t","int16_t","uint16_t","vx_int32","vx_uint32","vx_int64","vx_uint64","vx_float32","vx_float64"]
ovx_type = ["VX_TYPE_INT8","VX_TYPE_UINT8","VX_TYPE_INT16","VX_TYPE_UINT16","VX_TYPE_INT32","VX_TYPE_UINT32","VX_TYPE_INT64","VX_TYPE_UINT64","VX_TYPE_FLOAT32","VX_TYPE_FLOAT64"]
rpp_type = ["Rpp8s","Rpp8u","Rpp16s","Rpp16u","Rpp32s","Rpp32u","Rpp64s","Rpp64u","Rpp32f","Rpp64f"]
param_status_type = ["VX_INPUT","VX_OUTPUT","VX_BIDIRECTIONAL"]
param_status = ["I","O","B"]
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

def write_structure(func, param_list, structure):
    structure.append("struct "+func+"LocalData { \n\tRPPCommonHandle handle; \n\tRppiSize dimensions; \n\tRpp32u device_type;\n")
    temp_cl = ["#if ENABLE_OPENCL\n"]
    idx = 0
    while idx < len(param_list):
        if param_list[idx] in non_scalar:
            temp_cl.append("\tcl_mem cl_"+param_list[idx+1]+";\n")
            structure.append("\tRppPtr_t "+param_list[idx+1]+";\n")
        else:
            structure.append("\t"+rpp_type[scalar_type.index(param_list[idx])]+ " "+param_list[idx+1]+";\n")
        idx += 3
    structure += temp_cl
    structure.append("#endif \n};\n\n")
    return structure

def write_refresh(func,params,refresh):
    refresh.append("static vx_status VX_CALLBACK refresh"+func+"(vx_node node, const vx_reference *parameters, vx_uint32 num, "+func+"LocalData *data)\n{\n\tvx_status status = VX_SUCCESS;\n ")
    refresh.append("\tSTATUS_ERROR_CHECK(vxQueryImage((vx_image)parameters[0], VX_IMAGE_HEIGHT, &data->dimensions.height, sizeof(data->dimensions.height)));\n\tSTATUS_ERROR_CHECK(vxQueryImage((vx_image)parameters[0], VX_IMAGE_WIDTH, &data->dimensions.width, sizeof(data->dimensions.width)));\n")
    scalar_copy = "\tSTATUS_ERROR_CHECK(vxReadScalarValue((vx_scalar)parameters[param_idx], &data->param_name));\n"
    copy_opencl = "\t\tSTATUS_ERROR_CHECK(vxQueryparam_type((vx_image)parameters[param_idx], copy_type, &data->param_name, sizeof(data->param_name)));\n"
    copy_host = "\t\tSTATUS_ERROR_CHECK(vxQueryparam_type((vx_image)parameters[param_idx], copy_type, &data->param_name, sizeof(vx_uint8)));\n"
    non_scalar_opencl = []
    non_scalar_host = []
    idx = 0
    while (idx < len(params)):
        if params[idx] not in non_scalar:
            refresh.append((scalar_copy.replace("param_idx",str(idx/3))).replace("param_name",params[idx+1]))
        elif(params[idx] == "vx_image"):
            non_scalar_opencl.append(copy_opencl.replace("param_idx",str(idx/3)).replace("param_name","cl_"+params[idx+1]).replace("copy_type","VX_IMAGE_ATTRIBUTE_AMD_OPENCL_BUFFER").replace("param_type","Image"))
            non_scalar_host.append(copy_host.replace("param_idx",str(idx/3)).replace("param_name",params[idx+1]).replace("copy_type","VX_IMAGE_ATTRIBUTE_BUFFER").replace("param_type","Image"))
        elif(params[idx] == "vx_array"):
            non_scalar_opencl.append(copy_opencl.replace("param_idx",str(idx/3)).replace("param_name","cl_"+params[idx+1]).replace("copy_type","VX_ARRAY_ATTRIBUTE_BUFFER_OPENCL").replace("param_type","Array"))
            non_scalar_host.append(copy_host.replace("param_idx",str(idx/3)).replace("param_name",params[idx+1]).replace("copy_type","VX_ARRAY_ATTRIBUTE_BUFFER").replace("param_type","Array"))
        idx += 3
    refresh.append("\tif(data->device_type == AGO_TARGET_AFFINITY_GPU) {\n")
    refresh.append("#if ENABLE_OPENCL\n")
    refresh += non_scalar_opencl
    refresh.append("#endif\n")
    refresh.append("\t}\n")
    refresh.append("\tif(data->device_type == AGO_TARGET_AFFINITY_CPU) {\n")
    refresh += non_scalar_host
    refresh.append("\t}\n\treturn status; \n}\n\n")
    return refresh

def write_validate(func,params,validate):
    validate.append("static vx_status VX_CALLBACK validate"+func+"(vx_node node, const vx_reference parameters[], vx_uint32 num, vx_meta_format metas[])\n")
    validate.append("{\n\tvx_status status = VX_SUCCESS;\n\tvx_enum scalar_type;\n")
    scalar_check = []
    input_img_check = []
    output_img_check = []
    affinity_check = '\tSTATUS_ERROR_CHECK(vxQueryScalar((vx_scalar)parameters[param_idx], VX_SCALAR_TYPE, &scalar_type, sizeof(scalar_type)));\n \tif(scalar_type != param_type) return ERRMSG(VX_ERROR_INVALID_TYPE, "validate: Paramter: #param_idx type=%d (must be size)\\n", scalar_type);\n'
    idx = 0
    while (idx < len(params)):
        if params[idx] not in non_scalar:
            scalar_check.append((affinity_check.replace("param_idx",str(idx/3))).replace("param_type",ovx_type[scalar_type.index(params[idx])]))
        elif(params[idx] == "vx_image"):
            if(params[idx+2] == "I"):
                if(len(input_img_check) == 0):
                    input_img_check.append("\t// Check for input parameters \n")
                    input_img_check.append("\tvx_parameter input_param; \n\tvx_image input; \n\tvx_df_image df_image;\n")
                input_img_check.append("\tinput_param = vxGetParameterByIndex(node,"+str(idx/3)+");\n")
                input_img_check.append("\tSTATUS_ERROR_CHECK(vxQueryParameter(input_param, VX_PARAMETER_ATTRIBUTE_REF, &input, sizeof(vx_image)));\n")
                input_img_check.append("\tSTATUS_ERROR_CHECK(vxQueryImage(input, VX_IMAGE_ATTRIBUTE_FORMAT, &df_image, sizeof(df_image))); \n")
                input_img_check.append("\tif(df_image != VX_DF_IMAGE_U8 && df_image != VX_DF_IMAGE_RGB) \n\t{\n")
                temp = '\t\treturn ERRMSG(VX_ERROR_INVALID_FORMAT, "validate: func_change: image: #param_idx format=%4.4s (must be RGB2 or U008)\\n", (char *)&df_image);\n\t}\n\n'
                input_img_check.append((temp.replace("param_idx",str(idx/3))).replace("func_change",func))
            elif(params[idx+2] == "O") or (params[idx+2] == "B"):
                if(len(output_img_check) == 0):
                    output_img_check.append("\t// Check for output parameters \n")
                    output_img_check.append("\tvx_image output; \n\tvx_df_image format; \n\tvx_parameter output_param; \n\tvx_uint32  height, width; \n")
                output_img_check.append("\toutput_param = vxGetParameterByIndex(node,"+str(idx/3)+");\n")
                output_img_check.append("\tSTATUS_ERROR_CHECK(vxQueryParameter(output_param, VX_PARAMETER_ATTRIBUTE_REF, &output, sizeof(vx_image))); \n")
                output_img_check.append("\tSTATUS_ERROR_CHECK(vxQueryImage(output, VX_IMAGE_ATTRIBUTE_WIDTH, &width, sizeof(width))); \n")
                output_img_check.append("\tSTATUS_ERROR_CHECK(vxQueryImage(output, VX_IMAGE_ATTRIBUTE_HEIGHT, &height, sizeof(height))); \n")
                output_img_check.append("\tSTATUS_ERROR_CHECK(vxSetMetaFormatAttribute(metas[param_idx], VX_IMAGE_ATTRIBUTE_WIDTH, &width, sizeof(width)));\n".replace("param_idx",str(idx/3)))
                output_img_check.append("\tSTATUS_ERROR_CHECK(vxSetMetaFormatAttribute(metas[param_idx], VX_IMAGE_ATTRIBUTE_HEIGHT, &height, sizeof(height)));\n".replace("param_idx",str(idx/3)))
                output_img_check.append("\tSTATUS_ERROR_CHECK(vxSetMetaFormatAttribute(metas[param_idx], VX_IMAGE_ATTRIBUTE_FORMAT, &df_image, sizeof(df_image)));\n".replace("param_idx",str(idx/3)))
        idx += 3
    scalar_check.append((affinity_check.replace("param_idx",str(len(params)/3))).replace("param_type","VX_TYPE_UINT32"))
    output_img_check.append("\tvxReleaseImage(&input);\n\tvxReleaseImage(&output);\n\tvxReleaseParameter(&output_param);\n\tvxReleaseParameter(&input_param);\n\treturn status;\n}\n\n")
    validate = validate + scalar_check + input_img_check + output_img_check
    return validate

def write_process(func,params,process):
    process.append("static vx_status VX_CALLBACK process"+func+"(vx_node node, const vx_reference * parameters, vx_uint32 num) \n{ \n\tRppStatus status = RPP_SUCCESS;\n\t"+func+"LocalData * data = NULL;\n\tSTATUS_ERROR_CHECK(vxQueryNode(node, VX_NODE_LOCAL_DATA_PTR, &data, sizeof(data)));\n")
    process.append("\tvx_df_image df_image = VX_DF_IMAGE_VIRT;\n\tSTATUS_ERROR_CHECK(vxQueryImage((vx_image)parameters[0], VX_IMAGE_ATTRIBUTE_FORMAT, &df_image, sizeof(df_image)));\n")
    opencl_call = []
    host_call = []
    opencl_call.append("\tif(data->device_type == AGO_TARGET_AFFINITY_GPU) {\n#if ENABLE_OPENCL\n\t\tcl_command_queue handle = data->handle.cmdq;\n")
    opencl_call.append("\t\trefresh"+func+"(node, parameters, num, data);\n\t\tif (df_image == VX_DF_IMAGE_U8 ){ \n ")
    host_call.append("\tif(data->device_type == AGO_TARGET_AFFINITY_CPU) {\n\t\trefresh"+func+"(node, parameters, num, data);\n \t\tif (df_image == VX_DF_IMAGE_U8 ){\n")
    opencl_params = "("
    host_params = "("
    idx = 0
    while (idx < len(params)):
        if params[idx] in non_scalar:
            if(params[idx+2] == "O"):
                opencl_params += "data->dimensions,"
                opencl_params += "(void *)data->cl_"+params[idx+1]+","
                host_params += "data->dimensions,"
                host_params += "data->"+params[idx+1]+","
            else:
                opencl_params += "(void *)data->cl_"+params[idx+1]+","
                host_params += "data->"+params[idx+1] + ","
        else:
            opencl_params += "data->"+params[idx+1]+","
            host_params += "data->"+params[idx+1]+","
        idx += 3
    opencl_params += "(void *)handle);"
    host_params = host_params[:-1] +");"
    #host_params = host_params[:-1] +",NULL);" TO be included in the future
    rpp_func = "rppi_fname_u8_format_mode" #to pass the function name from rpp
    opencl_call.append("\t\t\tstatus = "+rpp_func.replace("fname",func.lower()).replace("format","pln1").replace("mode","gpu")+opencl_params+"\n\t\t}\n\t\telse if(df_image == VX_DF_IMAGE_RGB) {\n\t\t\tstatus = "+rpp_func.replace("fname",func.lower()).replace("format","pkd3").replace("mode","gpu")+opencl_params+"\n\t\t}\n\t\treturn status;\n#endif\n\t}\n")
    host_call.append("\t\t\tstatus = "+rpp_func.replace("fname",func.lower()).replace("format","pln1").replace("mode","host")+host_params+"\n\t\t}\n\t\telse if(df_image == VX_DF_IMAGE_RGB) {\n\t\t\tstatus = "+rpp_func.replace("fname",func.lower()).replace("format","pkd3").replace("mode","host")+host_params+"\n\t\t}\n\t\treturn status;\n\t}\n}\n\n")
    process += opencl_call + host_call
    return process


def write_initialize(func,params,initialize):
    initialize.append("static vx_status VX_CALLBACK initialize"+func+"(vx_node node, const vx_reference *parameters, vx_uint32 num) \n{\n\t"+func+"LocalData * data = new "+func+"LocalData;\n")
    initialize.append("\tmemset(data, 0, sizeof(*data));\n#if ENABLE_OPENCL\n\tSTATUS_ERROR_CHECK(vxQueryNode(node, VX_NODE_ATTRIBUTE_AMD_OPENCL_COMMAND_QUEUE, &data->handle.cmdq, sizeof(data->handle.cmdq)));\n#endif\n")
    initialize.append("\tSTATUS_ERROR_CHECK(vxCopyScalar((vx_scalar)parameters["+str(len(params)/3)+"], &data->device_type, VX_READ_ONLY, VX_MEMORY_TYPE_HOST));")
    initialize.append("\trefresh"+func+"(node, parameters, num, data);\n")
    initialize.append("\n\tSTATUS_ERROR_CHECK(vxSetNodeAttribute(node, VX_NODE_LOCAL_DATA_PTR, &data, sizeof(data)));\n\treturn VX_SUCCESS;\n}\n\n")
    return initialize

def write_uninitialize(func,params,uninitialize):
    uninitialize.append("static vx_status VX_CALLBACK uninitialize"+func+"(vx_node node, const vx_reference *parameters, vx_uint32 num)\n{\n\t")
    uninitialize.append(func+"LocalData * data; \n\tSTATUS_ERROR_CHECK(vxQueryNode(node, VX_NODE_LOCAL_DATA_PTR, &data, sizeof(data)));\n")
    uninitialize.append("\tdelete(data);\n\treturn VX_SUCCESS; \n}\n\n")
    return  uninitialize

def write_register(func,params,registration):
    registration.append("vx_status "+func+"_Register(vx_context context)\n{\n\tvx_status status = VX_SUCCESS;\n\t// Add kernel to the context with callbacks\n")
    registration.append(('\tvx_kernel kernel = vxAddUserKernel(context, "org.rpp.func_name",\n\t\tVX_KERNEL_RPP_'+func.upper()+',\n\t\tprocessfunc_name,\n\t\t'+str(len(params)/3 + 1)+',\n').replace("func_name",func))
    registration.append(("\t\tvalidatefunc_name,\n\t\tinitializefunc_name,\n\t\tuninitializefunc_name);\n").replace("func_name", func))
    registration.append("\tERROR_CHECK_OBJECT(kernel);\n\tAgoTargetAffinityInfo affinity;\n\tvxQueryContext(context, VX_CONTEXT_ATTRIBUTE_AMD_AFFINITY,&affinity, sizeof(affinity));\n")
    registration.append("#if ENABLE_OPENCL\n\t// enable OpenCL buffer access since the kernel_f callback uses OpenCL buffers instead of host accessible buffers\n\tvx_bool enableBufferAccess = vx_true_e;\n")
    registration.append("\tif(affinity.device_type == AGO_TARGET_AFFINITY_GPU)\n\t\tSTATUS_ERROR_CHECK(vxSetKernelAttribute(kernel, VX_KERNEL_ATTRIBUTE_AMD_OPENCL_BUFFER_ACCESS_ENABLE, &enableBufferAccess, sizeof(enableBufferAccess)));\n")
    registration.append("#else\n\tvx_bool enableBufferAccess = vx_false_e;\n#endif\n\tif (kernel)\n\t{\n")
    idx = 0
    temp = "\t\tPARAM_ERROR_CHECK(vxAddParameterToKernel(kernel, index, param_status, param_type, VX_PARAMETER_STATE_REQUIRED));\n"
    while (idx < len(params)):
        if(params[idx] in non_scalar):
            registration.append(temp.replace("index",str(idx/3)).replace("param_type",non_scalar_type[non_scalar.index(params[idx])]).replace("param_status",param_status_type[param_status.index(params[idx+2])]))
        else:
            registration.append(temp.replace("index",str(idx/3)).replace("param_type","VX_TYPE_SCALAR").replace("param_status",param_status_type[param_status.index(params[idx+2])]))
        idx += 3
    registration.append(temp.replace("index",str(len(params)/3)).replace("param_type","VX_TYPE_SCALAR").replace("param_status","VX_INPUT"))
    registration.append("\t\tPARAM_ERROR_CHECK(vxFinalizeKernel(kernel));\n\t}\n\tif (status != VX_SUCCESS)\n\t{\n")
    registration.append("\texit:	vxRemoveKernel(kernel);\treturn VX_FAILURE; \n \t}\n\treturn status;\n}\n")
    return registration

def  write_rpp_support_cpp(func_name, params_list):
    include1 = ["#include <kernels_rpp.h>\n","#include <vx_ext_rpp.h>\n","#include <stdio.h>\n","#include <iostream>\n"]
    include2 = ['#include "internal_rpp.h"\n','#include "internal_publishKernels.h"\n','#include </opt/rocm/rpp/include/rpp.h>\n','#include </opt/rocm/rpp/include/rppdefs.h>\n','#include </opt/rocm/rpp/include/rppi.h>\n\n\n']
    for idx,func in enumerate(func_name):
        file_name = src_dir + "source/"+func+".cpp"
        f = open(file_name,"w+")
        params = params_list[idx]
        structure = []
        registration = []
        process = []
        validate = []
        initialize = []
        uninitialize = []
        refresh = []
        structure = write_structure(func, params, structure)
        validate = write_validate(func,params,validate)
        uninitialize = write_uninitialize(func,params,uninitialize)
        registration = write_register(func,params,registration)
        refresh = write_refresh(func,params,refresh)
        process = write_process(func,params,process)
        initialize = write_initialize(func,params,initialize)
        cpp_file = []
        cpp_file = include1 + include2 + structure + refresh + validate + process + initialize +uninitialize + registration
        for line in cpp_file:
            f.write(line)

def process_csv(csv_reader,func_name,params_list):
    for i,row in enumerate(csv_reader):
        func_name.append(row[0])
        idx = 1
        while(idx < len(row)):
            params_list[i].append(row[idx])
            idx += 1

with open(csv_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    f = open(csv_name)
    numline = len(f.readlines())
    # print (numline) ########
    func_name = []
    params_list = [[]for i in range(numline)]
    process_csv(csv_reader,func_name,params_list)
    # print (func_name) ##########
    # print (params_list) #######
    file_name = src_dir+"include/internal_publishKernels.h"
    write_internal_publish_header(func_name,file_name)
    file_name = src_dir+"include/kernels_rpp.h"
    write_kernel_rpp_header(func_name, file_name)
    func_declaration = []
    file_name = src_dir + "include/vx_ext_rpp.h"
    write_vx_ext_rpp_header(func_name, params_list, func_declaration, file_name)
    # print (func_declaration)
    file_name = src_dir +"source/internal_publishKernels.cpp"
    write_internal_publishkernel_cpp(func_name, file_name)
    file_name = src_dir + "source/kernel_rpp.cpp"
    write_kernel_rpp_cpp(func_name,params_list, func_declaration, file_name)
    write_rpp_support_cpp(func_name, params_list)