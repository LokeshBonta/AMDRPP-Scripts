import subprocess
import csv
import shlex, subprocess
import os

rpp_src_dir = "/home/lokeswara/Desktop/AMD-RPP/scripting/"
csv_name = '/home/lokeswara/Desktop/AMD-RPP/AMDRPP-Scripts/API-Gen/imgaug.csv'
local_path = rpp_src_dir

rpp_types = ["Rpp8u", "Rpp8s", "Rpp16u", "Rpp16s", "Rpp32u", "Rpp32s", "Rpp64u", "Rpp64s", "Rpp32f", "Rpp64f", "RppiSize"]
function_name_list = []
image_format = ["pln1", "pln3", "pkd3"]
device = ["gpu","host"]
data_types = ["u8"]
batch_list = [ "nonbatch","batch"]
roi_list = ["nonroi","ROIS","ROID"]
parameter_list = ["S","D"]
resolution_list = ["S", "D"]
modules = []
module_list = []
header_file_names = []
func_category_list = []
geometric_function = ["function2"]

# NEW GPU CODE

set_non_roi_gpu = "\tRppiROI roiPoints;\n\troiPoints.x = 0;\n\troiPoints.y = 0;\n\troiPoints.roiHeight = 0;\n\troiPoints.roiWidth = 0;\n"
set_param_index_gpu = "\tRpp32u paramIndex = 0;\n"
copy_src_size_gpu = "\tcopy_srcSize(srcSize, rpp::deref(rppHandle));\n"
copy_src_size_max_non_padding_gpu = "\tcopy_srcMaxSize (rpp::deref(rppHandle));\n"
copy_src_size_max_padding_gpu = "\tcopy_srcMaxSize (maxSrcSize, rpp::deref(rppHandle));\n"
copy_dst_size_gpu = "\tcopy_dstSize(dstSize, rpp::deref(rppHandle));\n"
copy_dst_size_max_non_padding_gpu = "\tcopy_dstMaxSize (rpp::deref(rppHandle));\n"
copy_dst_size_max_padding_gpu = "\tcopy_dstMaxSize (maxDstSize, rpp::deref(rppHandle));\n"
copy_roi_points_gpu = "\tcopy_roi(roiPoints, rpp::deref(rppHandle));\n"
copy_src_batch_index_pln1_gpu = "\tget_srcBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PLANAR);\n"
copy_src_batch_index_pln3_gpu = "\tget_srcBatchIndex (rpp::deref(rppHandle), 3, RPPI_CHN_PLANAR);\n"
copy_src_batch_index_pkd3_gpu = "\tget_srcBatchIndex (rpp::deref(rppHandle), 3, RPPI_CHN_PACKED);\n"
copy_dst_batch_index_pln1_gpu = "\tget_dstBatchIndex (rpp::deref(rppHandle), 1, RPPI_CHN_PLANAR);\n"
copy_dst_batch_index_pln3_gpu = "\tget_dstBatchIndex (rpp::deref(rppHandle), 3, RPPI_CHN_PLANAR);\n"
copy_dst_batch_index_pkd3_gpu = "\tget_dstBatchIndex (rpp::deref(rppHandle), 3, RPPI_CHN_PACKED);\n"
copy_float_gpu = "\tcopy_param_float ("
copy_uint_gpu = "\tcopy_param_uint ("
copy_int_gpu = "\tcopy_param_int ("
copy_uchar_gpu = "\tcopy_param_uchar ("
copy_char_gpu = "\tcopy_param_char ("
copy_param_end_gpu = ", rpp::deref(rppHandle), paramIndex++);\n"
compile_flag_1_gpu = "\n#ifdef OCL_COMPILE\n\t{\n\t\t" 
ocl_function_formate_pln1_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
ocl_function_formate_pln3_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
ocl_function_formate_pkd3_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
ocl_function_formate_pln1_2_input_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
ocl_function_formate_pln3_2_input_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
ocl_function_formate_pkd3_2_input_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
ocl_function_formate_pln1_3_input_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\tstatic_cast<cl_mem>(srcPtr3),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
ocl_function_formate_pln3_3_input_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\tstatic_cast<cl_mem>(srcPtr3),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
ocl_function_formate_pkd3_3_input_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\tstatic_cast<cl_mem>(srcPtr3),\n\t\t\tstatic_cast<cl_mem>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
ocl_function_formate_pln1_nodst_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
ocl_function_formate_pln3_nodst_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
ocl_function_formate_pkd3_nodst_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
ocl_function_formate_pln1_2_input_nodst_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
ocl_function_formate_pln3_2_input_nodst_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
ocl_function_formate_pkd3_2_input_nodst_gpu = "_cl_batch(\n\t\t\tstatic_cast<cl_mem>(srcPtr1),\n\t\t\tstatic_cast<cl_mem>(srcPtr2),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
compile_flag_2_gpu = "\t}\n#elif defined (HIP_COMPILE)\n\t{\n\t\t"
hip_function_formate_pln1_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
hip_function_formate_pln3_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
hip_function_formate_pkd3_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
hip_function_formate_pln1_2_input_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
hip_function_formate_pln3_2_input_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
hip_function_formate_pkd3_2_input_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
hip_function_formate_pln1_3_input_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr3),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
hip_function_formate_pln3_3_input_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr3),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
hip_function_formate_pkd3_3_input_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr3),\n\t\t\tstatic_cast<Rpp8u*>(dstPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
hip_function_formate_pln1_nodst_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
hip_function_formate_pln3_nodst_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
hip_function_formate_pkd3_nodst_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
hip_function_formate_pln1_2_input_nodst_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 1\n\t\t);\n"
hip_function_formate_pln3_2_input_nodst_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PLANAR, 3\n\t\t);\n"
hip_function_formate_pkd3_2_input_nodst_gpu = "_hip_batch(\n\t\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\t\trpp::deref(rppHandle),\n\t\t\tRPPI_CHN_PACKED, 3\n\t\t);\n"
compile_flag_3_gpu = "\t}\n#endif //BACKEND\n\n\treturn RPP_SUCCESS;\n}"

# NEW CPU CODE

set_non_roi_host = "\tRppiROI roiPoints;\n\troiPoints.x = 0;\n\troiPoints.y = 0;\n\troiPoints.roiHeight = 0;\n\troiPoints.roiWidth = 0;\n"
set_param_index_host = "\tRpp32u paramIndex = 0;\n"
copy_src_size_host = "\tcopy_host_srcSize(srcSize, rpp::deref(rppHandle));\n"
copy_src_size_max_padding_host = "\tcopy_host_maxSrcSize(maxSrcSize, rpp::deref(rppHandle));\n"
copy_dst_size_host = "\tcopy_host_dstSize(dstSize, rpp::deref(rppHandle));\n"
copy_dst_size_max_padding_host = "\tcopy_host_maxDstSize(maxDstSize, rpp::deref(rppHandle));\n"
copy_roi_points_host = "\tcopy_host_roi(roiPoints, rpp::deref(rppHandle));\n"
copy_float_host = "\tcopy_param_float ("
copy_uint_host = "\tcopy_param_uint ("
copy_int_host = "\tcopy_param_int ("
copy_uchar_host = "\tcopy_param_uchar ("
copy_char_host = "\tcopy_param_char ("
copy_param_end_host = ", rpp::deref(rppHandle), paramIndex++);\n"
function_formate_host = "_host_batch<Rpp8u>(\n\t\tstatic_cast<Rpp8u*>(srcPtr),\n"
function_formate_2_input_host = "_host_batch<Rpp8u>(\n\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\tstatic_cast<Rpp8u*>(srcPtr2),\n"
function_formate_3_input_host = "_host_batch<Rpp8u>(\n\t\tstatic_cast<Rpp8u*>(srcPtr1),\n\t\tstatic_cast<Rpp8u*>(srcPtr2),\n\t\tstatic_cast<Rpp8u*>(srcPtr3),\n"
src_size_same_size_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize,\n"
src_size_different_size_host = "\t\tsrcSize,\n"
max_src_size_non_padding_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.srcSize,\n"
max_src_size_padding_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.maxSrcSize,\n"
dst_ptr_host = "\t\tstatic_cast<Rpp8u*>(dstPtr),\n"
dst_size_same_size_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,\n"
dst_size_different_size_host = "\t\tdstSize,\n"
max_dst_size_non_padding_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.dstSize,\n"
max_dst_size_padding_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.maxDstSize,\n"
pass_float_1_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.floatArr["
pass_float_2_host = "].floatmem,\n"
pass_uint_1_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.uintArr["
pass_uint_2_host = "].uintmem,\n"
pass_int_1_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.intArr["
pass_int_2_host = "].intmem,\n"
pass_uchar_1_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.ucharArr["
pass_uchar_2_host = "].ucharmem,\n"
pass_char_1_host = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.charArr["
pass_char_2_host = "].charmem,\n"
pass_roi_host_same = "\t\trpp::deref(rppHandle).GetInitHandle()->mem.mcpu.roiPoints,\n"
pass_roi_host_different = "\t\troiPoints,\n"
pass_batch_size_host = "\t\trpp::deref(rppHandle).GetBatchSize(),\n"
close_pln1_host = "\t\tRPPI_CHN_PLANAR, 1\n\t);\n\n\treturn RPP_SUCCESS;\n}"
close_pln3_host = "\t\tRPPI_CHN_PLANAR, 3\n\t);\n\n\treturn RPP_SUCCESS;\n}"
close_pkd3_host = "\t\tRPPI_CHN_PACKED, 3\n\t);\n\n\treturn RPP_SUCCESS;\n}"

header_code = r'''
#include <rppdefs.h>
#include "rppi_validate.hpp"

#ifdef HIP_COMPILE
#include <hip/rpp_hip_common.hpp>
#incluce "hip/hip_declarations.hpp"

#elif defined(OCL_COMPILE)
#include <cl/rpp_cl_common.hpp>
#include "cl/cl_declarations.hpp"
#endif //backend
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <chrono>
using namespace std::chrono; 

'''

cl_headers = r'''
#include <cl/rpp_cl_common.hpp>
#include "cl_declarations.hpp"
'''

host_headers = '''
#include <cpu/rpp_cpu_common.hpp>
'''

header_guards_start = '''
#include "rppdefs.h"
#include "rpp/rpp.h"
#ifdef __cplusplus
extern "C" {
#endif
'''

header_guards_end = '''
#ifdef __cplusplus
}
#endif
#endif
'''

def cast(object, castedTo):
    temp = "static_cast<" + castedTo + ">(" + object + ")"
    return temp

def validate(batch, roi, parameter, resolution):
    if(batch == "batch") and (roi == "nonroi"):
        return "batch"
    elif(batch == "nonbatch") and (roi == "nonroi"):
        return "basic"
    elif(batch == "nonbatch") and (roi == "ROIS"):
        return "basic_roi"
    elif(batch == "nonbatch") and (roi == "ROID"):
        return False
    return True

def name_generator(function, format, dev, type, api_list):
    if(function not in geometric_function):
        for batch in batch_list:
            for roi in roi_list:
                for parameter in parameter_list:
                    for resolution in resolution_list:
                        if(validate(batch, roi, parameter, resolution) == True):
                            func_name = function+"_"+type+"_"+format+"_"+batch+resolution+parameter+"_"+roi+"_"+dev
                        if(validate(batch, roi, parameter, resolution) == "batch"):
                            func_name = function+"_"+type+"_"+format+"_"+batch+resolution+parameter+"_"+dev
                        if(validate(batch, roi, parameter, resolution) == "basic"):
                            func_name = function+"_"+type+"_"+format+"_"+dev
                        if(validate(batch, roi, parameter, resolution) == "basic_roi"):
                            func_name = function+"_"+type+"_"+format+"_ROI_"+dev
                        if(func_name not in api_list):
                            api_list.append(func_name)
                            if(resolution == "D"):
                                if("DS" in func_name):
                                    api_list.append(func_name.replace("DS","PS"))
                                if("DD" in func_name):
                                    api_list.append(func_name.replace("DD","PD"))
    else:
        func_name = function+"_"+type+"_"+format+"_"+dev
        api_list.append(func_name)
        func_name = function+"_"+type+"_"+format+"_batchSS_"+dev
        api_list.append(func_name)
        func_name = function+"_"+type+"_"+format+"_batchSD_"+dev
        api_list.append(func_name)
        func_name = function+"_"+type+"_"+format+"_batchDS_"+dev
        api_list.append(func_name)
        func_name = function+"_"+type+"_"+format+"_batchDD_"+dev
        api_list.append(func_name)
        func_name = function+"_"+type+"_"+format+"_batchPS_"+dev
        api_list.append(func_name)
        func_name = function+"_"+type+"_"+format+"_batchPD_"+dev
        api_list.append(func_name)

def header_file_generate(api_list, func_category, func_name , func_comments_list, func_args_list):
    include_dir = rpp_src_dir.replace(rpp_src_dir.split('/')[-2],"include")
    file_name = "rppi_"+func_category+".h"
    file_name_header = "rppi_"+func_category+"_h"
    if not os.path.isfile(include_dir+file_name):
        header_file_names.append(include_dir+file_name)
        f = open(include_dir+file_name,"a+")
        header_guards = file_name.upper()
        f.write("#ifndef "+header_guards+"\n#define "+header_guards)
        f.write("\n "+header_guards_start)
    else:
        f = open(include_dir+file_name,"a+")
    contents = f.read()
    function = api_list[0]
    if function in contents :
        print(" function_name :: ", function)
        print("******Skipping function already exists!**********")
    else:
        for api_call in api_list:
            if "batch" not in api_call:
                if "ROI" not in api_call:
                    if "pln1" in api_call:
                        if "gpu" in api_call:
                            f.write("\n\n// ----------------------------------------\n// GPU "+func_name+ " functions")
                        elif "host" in api_call:
                            f.write("\n\n// ----------------------------------------\n// CPU "+func_name+ " functions")
                        f.write(" declaration \n// ----------------------------------------\n")
                        f.write(func_comments_list[0])
                        f.write("\n")
                        i = 1
                        j = 1
                        space = " "
                        while(i < len(func_comments_list) -1):
                            temp_s = func_comments_list[i].split(" ")
                            temp_s.insert(1,func_args_list[j])
                            temp_s = space.join(temp_s)
                            f.write(temp_s)
                            f.write("\n")
                            i += 1
                            j += 2
                        f.write("*returns a  RppStatus enumeration. \n")
                        f.write("*retval RPP_SUCCESS : No error succesful completion\n")
                        f.write("*retval RPP_ERROR : Error \n")
                        f.write("*/")
                        f.write("\n")
            f.write("RppStatus\n ")
            f.write(api_call+";")
            f.write("\n")
    f.close()

def api_calls_generate(api_list, final_api_list, func_args_list, func_param_list):
    for func_name in api_list:
        func_args_list_temp = []
        func_args_list_temp = func_args_list[:]
        if ("PD" in func_name) or ("PS" in func_name):
            idx = func_args_list_temp.index("srcSize") + 1
            func_args_list_temp.insert(idx,"RppiSize")
            func_args_list_temp.insert(idx + 1,"maxSrcSize")
            if("dstSize" in func_args_list_temp):
                idx = func_args_list_temp.index("dstSize") + 1
                func_args_list_temp.insert(idx,"RppiSize")
                func_args_list_temp.insert(idx + 1,"maxDstSize")
        if ("SD" in func_name):
            i = 1
            while(i < len(func_param_list)):
                idx = func_args_list_temp.index(func_param_list[i])
                if("dstSize" != func_args_list_temp[idx]):
                    func_args_list_temp[idx] = "*"+func_args_list_temp[idx]
                i += 1
        if ("DS" in func_name) or ("PS" in func_name):
            idx = func_args_list_temp.index(func_param_list[0])
            func_args_list_temp[idx] = "*"+func_args_list_temp[idx]
            if("dstSize" in func_args_list_temp):
                idx = func_args_list_temp.index("dstSize")
                func_args_list_temp[idx] = "*"+func_args_list_temp[idx]
        if ("DD" in func_name) or ("PD" in func_name):
            i = 0
            while(i < len(func_param_list)):
                idx = func_args_list_temp.index(func_param_list[i])
                func_args_list_temp[idx] = "*"+func_args_list_temp[idx]
                i += 1
        if "ROID" in func_name:
            idx = func_args_list_temp.index("rppHandle_t")
            func_args_list_temp.insert(idx,"RppiROI")
            func_args_list_temp.insert(idx+1,"*roiPoints")
        elif "ROI" in func_name:
            idx = func_args_list_temp.index("rppHandle_t")
            func_args_list_temp.insert(idx,"RppiROI")
            func_args_list_temp.insert(idx+1,"roiPoints")
        elif "ROIS" in func_name:
            idx = func_args_list_temp.index("rppHandle_t")
            func_args_list_temp.insert(idx,"RppiROI")
            func_args_list_temp.insert(idx+1,"roiPoints")
        if "batch" in func_name:
            idx = func_args_list_temp.index("rppHandle_t")
            func_args_list_temp.insert(idx,"Rpp32u")
            func_args_list_temp.insert(idx+1,"nbatchSize")
        func_call = "rppi_"+func_name+"("
        temp = ""
        j = 0
        while(j < len(func_args_list_temp)):
            temp = temp+func_args_list_temp[j]+" "+func_args_list_temp[j+1]+" ,"
            j += 2
        temp = temp[:-1]
        func_call = func_call + temp + ")"
        final_api_list.append(func_call)

def cpp_file_generate_gpu(api_list,func_category,function,module,func_validate_list,func_param_list,func_args_list):
    type = "Rpp8u"
    file = "rppi_"+func_category+".cpp"
    module_path = rpp_src_dir + module + '/'
    if not os.path.isfile(module_path + file):
        f= open(module_path + file,"a+")
        f.write("#include <rppi_" + func_category + ".h>" + header_code)
    else:
        f= open(module_path + file,"a+")
    contents = f.read() ####
    header = " \"cpu/" + 'host_' + func_category + '.hpp" '
    if header not in contents:
        f.seek(0,0)
        f.write("#include"  + header)
    # if 'rppi_' + function in contents :
    #     print(" function_name :: ", function)
    #     print("******Skipping function already exists!**********")

    # else:
    for api_call in api_list:
        if "gpu" in api_call:
            f.write("\n\nRppStatus  \n")
            f.write(api_call + "\n{ \n")
            if ("ROI" not in api_call) and (function not in geometric_function) :
                f.write(set_non_roi_gpu)
            f.write(set_param_index_gpu)
            f.write(copy_src_size_gpu)
            if ("PD_" in api_call) or ("PS_" in api_call):
                f.write(copy_src_size_max_padding_gpu)
            else:
                f.write(copy_src_size_max_non_padding_gpu)
            if "dstSize" in api_call:
                f.write(copy_dst_size_gpu)
                if ("PD_" in api_call) or ("PS_" in api_call):
                    f.write(copy_dst_size_max_padding_gpu)
                else:
                    f.write(copy_dst_size_max_non_padding_gpu)
            if function not in geometric_function:
                f.write(copy_roi_points_gpu)
            if "pln1" in api_call:
                f.write(copy_src_batch_index_pln1_gpu)
            elif "pln3" in api_call:
                f.write(copy_src_batch_index_pln3_gpu)
            else:
                f.write(copy_src_batch_index_pkd3_gpu)
            if "dstSize" in api_call:
                if "pln1" in api_call:
                    f.write(copy_dst_batch_index_pln1_gpu)
                elif "pln3" in api_call:
                    f.write(copy_dst_batch_index_pln3_gpu)
                else:
                    f.write(copy_dst_batch_index_pkd3_gpu)
            idx = 1
            while idx < len(func_param_list):
                if(func_param_list[idx] != "dstSize") and (func_param_list[idx] != "srcSize"):
                    loc = func_args_list.index(func_param_list[idx])
                    param_type = func_args_list[loc -1]
                    if (param_type == "Rpp32f") or (param_type == "float"):
                        f.write(copy_float_gpu)
                        f.write(func_param_list[idx])
                        f.write(copy_param_end_gpu)
                    elif (param_type == "Rpp32u") or (param_type == "unsigned int"):
                        f.write(copy_uint_gpu)
                        f.write(func_param_list[idx])
                        f.write(copy_param_end_gpu)
                    elif (param_type == "Rpp32s") or (param_type == "int"):
                        f.write(copy_int_gpu)
                        f.write(func_param_list[idx])
                        f.write(copy_param_end_gpu)
                    elif (param_type == "Rpp8u") or (param_type == "unsigned char"):
                        f.write(copy_uchar_gpu)
                        f.write(func_param_list[idx])
                        f.write(copy_param_end_gpu)
                    elif (param_type == "Rpp8s") or (param_type == "char"):
                        f.write(copy_char_gpu)
                        f.write(func_param_list[idx])
                        f.write(copy_param_end_gpu)
                idx += 1
            f.write(compile_flag_1_gpu)
            f.write(function)
            if("dstPtr" in api_call):
                if(api_call.count("srcPtr") == 1):
                    if("pln1" in api_call):
                        f.write(ocl_function_formate_pln1_gpu)    
                    elif ("pln3" in api_call):
                        f.write(ocl_function_formate_pln3_gpu)
                    else:
                        f.write(ocl_function_formate_pkd3_gpu)
                elif(api_call.count("srcPtr") == 2):
                    if("pln1" in api_call):
                        f.write(ocl_function_formate_pln1_2_input_gpu)    
                    elif ("pln3" in api_call):
                        f.write(ocl_function_formate_pln3_2_input_gpu)
                    else:
                        f.write(ocl_function_formate_pkd3_2_input_gpu)
                elif(api_call.count("srcPtr") == 3):
                    if("pln1" in api_call):
                        f.write(ocl_function_formate_pln1_3_input_gpu)    
                    elif ("pln3" in api_call):
                        f.write(ocl_function_formate_pln3_3_input_gpu)
                    else:
                        f.write(ocl_function_formate_pkd3_3_input_gpu)
            else:
                if(api_call.count("srcPtr") == 1):
                    if("pln1" in api_call):
                        f.write(ocl_function_formate_pln1_nodst_gpu)    
                    elif ("pln3" in api_call):
                        f.write(ocl_function_formate_pln3_nodst_gpu)
                    else:
                        f.write(ocl_function_formate_pkd3_nodst_gpu)
                elif(api_call.count("srcPtr") == 2):
                    if("pln1" in api_call):
                        f.write(ocl_function_formate_pln1_2_input_nodst_gpu)    
                    elif ("pln3" in api_call):
                        f.write(ocl_function_formate_pln3_2_input_nodst_gpu)
                    else:
                        f.write(ocl_function_formate_pkd3_2_input_nodst_gpu)  
            f.write(compile_flag_2_gpu)
            f.write(function)
            if("dstPtr" in api_call):
                if(api_call.count("srcPtr") == 1):
                    if("pln1" in api_call):
                        f.write(hip_function_formate_pln1_gpu)    
                    elif ("pln3" in api_call):
                        f.write(hip_function_formate_pln3_gpu)
                    else:
                        f.write(hip_function_formate_pkd3_gpu)
                elif(api_call.count("srcPtr") == 2):
                    if("pln1" in api_call):
                        f.write(hip_function_formate_pln1_2_input_gpu)    
                    elif ("pln3" in api_call):
                        f.write(hip_function_formate_pln3_2_input_gpu)
                    else:
                        f.write(hip_function_formate_pkd3_2_input_gpu)
                elif(api_call.count("srcPtr") == 3):
                    if("pln1" in api_call):
                        f.write(hip_function_formate_pln1_3_input_gpu)    
                    elif ("pln3" in api_call):
                        f.write(hip_function_formate_pln3_3_input_gpu)
                    else:
                        f.write(hip_function_formate_pkd3_3_input_gpu)
            else:
                if(api_call.count("srcPtr") == 1):
                    if("pln1" in api_call):
                        f.write(hip_function_formate_pln1_nodst_gpu)    
                    elif ("pln3" in api_call):
                        f.write(hip_function_formate_pln3_nodst_gpu)
                    else:
                        f.write(hip_function_formate_pkd3_nodst_gpu)
                elif(api_call.count("srcPtr") == 2):
                    if("pln1" in api_call):
                        f.write(hip_function_formate_pln1_2_input_nodst_gpu)    
                    elif ("pln3" in api_call):
                        f.write(hip_function_formate_pln3_2_input_nodst_gpu)
                    else:
                        f.write(hip_function_formate_pkd3_2_input_nodst_gpu)
            f.write(compile_flag_3_gpu)
        else:
            f.write("\n\nRppStatus  \n")
            f.write(api_call + "\n{ \n")
            f.write(set_param_index_host)
            if ("ROID" not in api_call) and (function not in geometric_function) :
                if("ROI" not in api_call):
                    f.write(set_non_roi_host)
                f.write(copy_roi_points_host)
            if("batchD" not in api_call) and ("batchP" not in api_call):
                f.write(copy_src_size_host)
                if("dstSize" in api_call):
                    f.write(copy_dst_size_host)
            if("batchP" in api_call):
                f.write(copy_src_size_max_padding_host)
                if("dstSize" in api_call):
                    f.write(copy_dst_size_max_padding_host)
            if("D_ROI" not in api_call) and ("SD_host" not in api_call) and ("DD_host" not in api_call) and ("PD_host" not in api_call):
                idx = 1
                while idx < len(func_param_list):
                    if(func_param_list[idx] != "dstSize") and (func_param_list[idx] != "srcSize"):
                        loc = func_args_list.index(func_param_list[idx])
                        param_type = func_args_list[loc -1]
                        if (param_type == "Rpp32f") or (param_type == "float"):
                            f.write(copy_float_host)
                            f.write(func_param_list[idx])
                            f.write(copy_param_end_host)
                        elif (param_type == "Rpp32u") or (param_type == "unsigned int"):
                            f.write(copy_uint_host)
                            f.write(func_param_list[idx])
                            f.write(copy_param_end_host)
                        elif (param_type == "Rpp32s") or (param_type == "int"):
                            f.write(copy_int_host)
                            f.write(func_param_list[idx])
                            f.write(copy_param_end_host)
                        elif (param_type == "Rpp8u") or (param_type == "unsigned char"):
                            f.write(copy_uchar_host)
                            f.write(func_param_list[idx])
                            f.write(copy_param_end_host)
                        elif (param_type == "Rpp8s") or (param_type == "char"):
                            f.write(copy_char_host)
                            f.write(func_param_list[idx])
                            f.write(copy_param_end_host)
                    idx += 1          
            f.write("\t")
            f.write(function)
            if(api_call.count("srcPtr") == 1):
                f.write(function_formate_host)
            elif(api_call.count("srcPtr") == 2):
                f.write(function_formate_2_input_host)
            elif(api_call.count("srcPtr") == 3):
                f.write(function_formate_3_input_host)
            if("batchD" in api_call):
                f.write(src_size_different_size_host)
                f.write(src_size_different_size_host)
            elif("batchP" in api_call):
                f.write(src_size_different_size_host)
                f.write(max_src_size_padding_host)
            else:
                f.write(src_size_same_size_host)
                f.write(max_src_size_non_padding_host)
            if("dstPtr" in api_call):
                f.write(dst_ptr_host)
                if("dstSize" in api_call):
                    if("batchD" in api_call):
                        f.write(dst_size_different_size_host)
                        f.write(dst_size_different_size_host)
                    elif("batchP" in api_call):
                        f.write(dst_size_different_size_host)
                        f.write(max_dst_size_padding_host)
                    else:
                        f.write(dst_size_same_size_host)
                        f.write(max_dst_size_non_padding_host)
            if("D_ROI" not in api_call) and ("SD_host" not in api_call) and ("DD_host" not in api_call) and ("PD_host" not in api_call):
                idx = 1
                inc = 0
                while idx < len(func_param_list):
                    if(func_param_list[idx] != "dstSize") and (func_param_list[idx] != "srcSize"):
                        loc = func_args_list.index(func_param_list[idx])
                        param_type = func_args_list[loc -1]
                        if (param_type == "Rpp32f") or (param_type == "float"):
                            f.write(pass_float_1_host)
                            f.write(str(inc))
                            f.write(pass_float_2_host)
                        elif (param_type == "Rpp32u") or (param_type == "unsigned int"):
                            f.write(pass_uint_1_host)
                            f.write(str(inc))
                            f.write(pass_uint_2_host)
                        elif (param_type == "Rpp32s") or (param_type == "int"):
                            f.write(pass_int_1_host)
                            f.write(str(inc))
                            f.write(pass_int_2_host)
                        elif (param_type == "Rpp8u") or (param_type == "unsigned char"):
                            f.write(pass_uchar_1_host)
                            f.write(str(inc))
                            f.write(pass_uchar_2_host)
                        elif (param_type == "Rpp8s") or (param_type == "char"):
                            f.write(pass_char_1_host)
                            f.write(str(inc))
                            f.write(pass_char_2_host)
                        inc += 1
                    idx += 1
            else:
                idx = 1
                while idx < len(func_param_list):
                    if(func_param_list[idx] != "dstSize") and (func_param_list[idx] != "srcSize"):
                        f.write("\t\t" + func_param_list[idx] + ",\n")
                    idx += 1
            if (function not in geometric_function) :
                if ("ROID" not in api_call):
                    f.write(pass_roi_host_same)
                else:
                    f.write(pass_roi_host_different)
            f.write(pass_batch_size_host)
            if("pln1" in api_call):
                f.write(close_pln1_host)
            elif("pln3" in api_call):
                f.write(close_pln3_host)
            else:
                f.write(close_pkd3_host)    
            
def basic_function(func_param_list,func_validate_list,func_args_list,func_comments_list):
    for idx,function in enumerate(function_name_list):
        api_list = []
        module = module_list[idx]
        func_category = func_category_list[idx]
        if module not in modules:
            print("Creating new module ... ", module)
            os.mkdir(rpp_src_dir + module)
            modules.append(module)
            os.mkdir(rpp_src_dir + module + '/cl')
            os.mkdir(rpp_src_dir + module + '/cpu')
            os.mkdir(rpp_src_dir + module + '/hipoc')
        for type in data_types:
            for dev in device:
                for format in image_format:
                    name_generator(function, format, dev, type, api_list)
        final_api_list = []
        api_calls_generate(api_list, final_api_list, func_args_list[idx], func_param_list[idx])
        header_file_generate(final_api_list,func_category,function, func_comments_list[idx], func_args_list[idx])
        cpp_file_generate_gpu(final_api_list,func_category,function,module,func_validate_list[idx], func_param_list[idx], func_args_list[idx])
        print(len(api_list))

def process_csv(csv_reader,numline):
    func_param_list = [[]for i in range(numline)]
    func_validate_list = [[[]for i in range(10)]for i in range(numline)]
    func_args_list = [[]for i in range(numline)]
    func_comments_list = [[]for i in range(numline)]
    for count,row in enumerate(csv_reader):
        module_list.append(row[0])
        func_category_list.append(row[1])
        function_name_list.append(row[2])
        i = 4
        idx = 0
        while(row[i] != "rppHandle"):
            # print(row[i])
            if row[i] in("validate_int_range","validate_float_range","validate_double_range","validate_unsigned_int_range"):
                func_param_list[count].append(row[i-1])
                func_validate_list[count][idx].append(row[i])
                func_validate_list[count][idx].append(row[i+1])
                func_validate_list[count][idx].append(row[i+2])
                i += 3
                idx += 1
            elif row[i] in ("validate_int_max","validate_unsigned_int_max","validate_int_min","validate_unsigned_int_min","validate_float_max","validate_float_min"):
                func_param_list[count].append(row[i-1])
                func_validate_list[count][idx].append(row[i])
                func_validate_list[count][idx].append(row[i+1])
                idx += 1
                i += 2
            elif row[i] in ("validate_image_size"):
                func_param_list[count].append(row[i-1])
                func_validate_list[count][idx].append(row[i])
                idx += 1
                i += 1
            elif row[i] in ("validate"):
                func_param_list[count].append(row[i-1])
                i += 1
            else:
                func_args_list[count].append(row[i])
                i += 1
        func_args_list[count].append(row[i])
        i += 1
        while(i < len(row)):
            func_comments_list[count].append(row[i])
            i += 1
    basic_function(func_param_list,func_validate_list,func_args_list,func_comments_list)

modules = []
for dirs in os.listdir(rpp_src_dir):
    modules.append(dirs)

with open(csv_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    f = open(csv_name)
    numline = len(f.readlines())
    print (numline)
    process_csv(csv_reader,numline)

for each_file in header_file_names:
    f = open(each_file,"a+")
    f.write("\n "+header_guards_end)