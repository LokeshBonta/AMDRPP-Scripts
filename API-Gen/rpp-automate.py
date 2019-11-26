import subprocess
import csv
import shlex, subprocess
import os

def cast(object, castedTo):
    temp = "static_cast<" + castedTo + ">(" + object + ")"
    return temp

# for header file inclusions
def for_each_include(function_name,row, device):
        include_dir = rpp_src_dir.replace(rpp_src_dir.split('/')[-2],"include")
        file_name = "rppi_"+row[1]+".h"
        args = []
        i = 4
        while(row[i] != "RppHandle_t"):
            if row[i] in("validate_int_range","validate_float_range","validate_double_range","validate_unsigned_int_range"):
                i += 3
            elif row[i] in ("validate_int_max","validate_unsigned_int_max","validate_int_min","validate_unsigned_int_min","validate_float_max","validate_float_min"):
                i += 2
            elif row[i] in ("validate_image_size"):
                i+= 1
            else:
                args.append(row[i + 1])
                i += 2
        if device:
            args.append("rppHandle")
        if not os.path.isfile(include_dir+file_name):
            header_file_names.append(include_dir+file_name)
            f = open(include_dir+file_name,"a+")
            header_guards = file_name.upper()
            f.write("#ifndef "+header_guards+"\n#define "+header_guards)
            f.write("\n "+header_guards_start)
        else:
            f = open(include_dir+file_name,"a+")
        if "pln1" in function_name:
            if device:
                f.write("\n\n// ----------------------------------------\n// GPU "+row[2]+ " functions")
                f.write(" declaration \n// ----------------------------------------\n")
                idx = row.index("rppHandle") + 1
                f.write(row[idx])
                f.write("\n")
                idx += 1
                idy = 0
                while(idx < len(row)):
                    if(idy < len(args)):
                        temp_s = row[idx]
                        temp_s = temp_s.split(" ")
                        temp_s.insert(1,args[idy])
                        space = " "
                        temp_s = space.join(temp_s)
                        f.write(temp_s)
                        f.write("\n")
                        idx += 1
                        idy += 1
                    else:
                        f.write(row[idx])
                        f.write("\n")
                        idx += 1
                f.write("*returns a  RppStatus enumeration. \n")
                f.write("*retval RPP_SUCCESS : No error succesful completion\n")
                f.write("*retval RPP_ERROR : Error \n")
                f.write("*/")
            else:
                f.write("\n\n// ----------------------------------------\n// Host "+row[2]+ " functions")
                f.write(" declaration \n// ----------------------------------------\n")
                idx = row.index("rppHandle") + 1
                f.write(row[idx])
                f.write("\n")
                idx += 1
                idy = 0
                while(idx < len(row) - 1):
                    if(idy < len(args)):
                        temp_s = row[idx]
                        temp_s = temp_s.split(" ")
                        temp_s.insert(1,args[idy])
                        space = " "
                        temp_s = space.join(temp_s)
                        f.write(temp_s)
                        f.write("\n")
                        idx += 1
                        idy += 1
                    else:
                        f.write(row[idx])
                        f.write("\n")
                        idx += 1
                f.write("*returns a  RppStatus enumeration. \n")
                f.write("*retval RPP_SUCCESS : No error succesful completion\n")
                f.write("*retval RPP_ERROR : Error \n")
                f.write("*/")
        f.write(function_name+';')
        f.close()

#function definition for each functions in .cpp file
def for_each_functions(function_name, row , module, cl_name, file, header, device , sub_function): 
        module_path = rpp_src_dir + module + '/'
        if not os.path.isfile(module_path + file):
            #print(" module_path + file not present:: ", module_path + file)
            #print("Creating new file ... ", file)
            f= open(module_path + file,"a+")
            f.write("#include <rppi_" + row[1] + ".h>" + header_code)
        else:
            f= open(module_path + file,"a+")
        
        contents =f.read() ####
        if header not in contents:
            f.seek(0,0)
            f.write("#include"  + header)
        if function_name in contents :
            print(" function_name :: ", function_name)
            print("******Skipping function already exists!**********")
        else :
            if "pln1" in function_name:
                if device:
                    f.write("\n \n// ----------------------------------------\n// GPU "+row[2]+" functions ")
                    f.write(" calls \n// ----------------------------------------\n")
                else:
                    f.write("\n \n// ----------------------------------------\n// Host "+row[2]+" functions ")
                    f.write("calls \n// ----------------------------------------\n")
            function_declartion = '\n\nRppStatus' + '\n' + function_name + "("
            arguments = (len(row))
            i = 4
            while(row[i] != "RppHandle_t"):
                if row[i] in ("validate_int_range","validate_float_range","validate_double_range","validate_unsigned_int_range"):
                    i += 3
                elif row[i] in ("validate_int_max","validate_unsigned_int_max","validate_int_min","validate_unsigned_int_min","validate_float_max","validate_float_min"):
                    i += 2
                elif row[i] in ("validate_image_size"):
                    i += 1
                else:
                    function_declartion = function_declartion  + row [i] + " " + row[i + 1]
                    i =  i + 2
                    if(i < arguments - 4):
                        function_declartion = function_declartion + ","
            if device :
                function_declartion = function_declartion[:-1]
                function_declartion = function_declartion + ", RppHandle_t rppHandle) "
                f.write(function_declartion + "\n{\n")
            else :
                function_declartion = function_declartion[:-1]
                function_declartion = function_declartion + ")"
                f.write(function_declartion + "\n{\n")
            for_each_include( function_declartion , row, device)
            params_value = ""

            j = 8
            while(row[j] != "RppHandle_t"):
                if row[j] in("validate_int_range","validate_float_range","validate_double_range","validate_unsigned_int_range"):
                    f.write("\n \t "+row[j]+"( "+row[j+1]+", "+row[j+2]+", &"+row[j-1]+");")
                    j += 3
                elif row[j] in ("validate_int_max","validate_unsigned_int_max","validate_int_min","validate_unsigned_int_min","validate_float_max","validate_float_min"):
                    f.write("\n \t "+row[j]+"("+row[j+1]+", &"+row[j-1]+");")
                    j += 2
                elif row[j] in ("validate_image_size"):
                    f.write("\n \t "+row[j]+"("+row[j-1]+");")
                    j+= 1
                else:
                    j+= 1
            
            if params_value != "":
                params_value = "\n\t\t\t" + params_value
            if device :
                code = "\n \t " + sub_function + "(" 
                i = 4
                while(row[i] != "RppHandle_t"):
                    if(row[i]) == "RppPtr_t":
                        code = code + cast(row[i + 1], "cl_mem") + ", "
                        code = code + "\n\t\t\t"
                        i += 2
                    elif row[i] in("validate_int_range","validate_float_range","validate_double_range","validate_unsigned_int_range"):
                        i += 3
                    elif row[i] in ("validate_int_max","validate_unsigned_int_max","validate_int_min","validate_unsigned_int_min","validate_float_max","validate_float_min"):
                        i += 2
                    elif row[i] in ("validate_image_size"):
                        i+= 1
                    else:
                        code = code + row[i + 1] + ","
                        code = code + "\n\t\t\t"
                        i += 2
                if "pkd" in function_name:
                    code = code + params_value + "RPPI_CHN_PACKED, 3," + "\n\t\t\t" + cast("rppHandle", "cl_command_queue") + ")"
                elif "pln3" in function_name:
                    code = code +  params_value + "RPPI_CHN_PLANAR, 3," + "\n\t\t\t" + cast("rppHandle", "cl_command_queue") + ")"
                else:
                    code = code +  params_value + "RPPI_CHN_PLANAR, 1," + "\n\t\t\t" + cast("rppHandle", "cl_command_queue") + ")"
                f.write("\n\n#ifdef OCL_COMPILE")
                f.write("\n \t {")
                if(time_info):
                    f.write("\n#ifdef TIME_INFO")
                    f.write("\n \t auto start = high_resolution_clock::now();")
                    f.write("\n#endif //TIME_INFO  \n \t \t \t")
                f.write(code + ";")
                if(time_info):
                    f.write("\n \n#ifdef TIME_INFO  \n \t  auto stop = high_resolution_clock::now(); ")
                    f.write(" \n \t auto duration = duration_cast<microseconds>(stop - start); \n \t std::cout << duration.count() << std::endl; \n")
                    f.write("\t std::fstream time_file;\n \t time_file.open (\"rpp_time.csv\",std::fstream::in | std::fstream::out |std::fstream::app);")
                    f.write("\n \t time_file<<\""+function_name+",\";")
                    f.write("\n \t time_file<<duration.count() << endl;")
                    f.write("\n \t time_file.close();\n ")
                    f.write("\n#endif //TIME_INFO")
                f.write("\n \t }")
                f.write(" \n#elif defined (HIP_COMPILE) \n \t { \n \t } \n#endif //BACKEND" + " \n\t\treturn RPP_SUCCESS;" + "\n}")
                f.close()
            else:
                type = "Rpp8u"
                code = "\n\t " + sub_function + "<" + type + ">" + "(" 
                i = 4
                while(row[i] != "RppHandle_t"):
                    if(row[i]) == "RppPtr_t":
                        code = code + cast(row[i + 1], type + "*") + ", "
                        code = code + "\n\t\t\t"
                        i += 2
                    elif row[i] in ("validate_int_range","validate_float_range","validate_double_range","validate_unsigned_int_range"):
                        i += 3
                    elif row[i] in ("validate_int_max","validate_unsigned_int_max","validate_int_min","validate_unsigned_int_min","validate_float_max","validate_float_min"):
                        i += 2
                    elif row[i] in ("validate_image_size"):
                        i+= 1
                    else:
                        code = code + row[i + 1] + ","
                        code = code + "\n\t\t\t"
                        i += 2
                if "pkd3" in function_name:
                    code = code + params_value + "RPPI_CHN_PACKED, 3)"
                elif "pln3" in function_name:
                    code = code + params_value + "RPPI_CHN_PLANAR, 3)"
                else:
                    code = code + params_value + "RPPI_CHN_PLANAR, 1)"
                if(time_info):
                    f.write("\n#ifdef TIME_INFO\n \t")
                    f.write("auto start = high_resolution_clock::now(); \n")
                    f.write("#endif //TIME_INFO \n")
                f.write(code + ";")
                if(time_info):
                    f.write(" \n \n#ifdef TIME_INFO  \n")
                    f.write("\t auto stop = high_resolution_clock::now();")
                    f.write("\n \t auto duration = duration_cast<microseconds>(stop - start);")
                    f.write("\n \t std::cout << duration.count() << std::endl;\n")
                    f.write("\t std::fstream time_file;\n")
                    f.write("\t time_file.open (\"rpp_time.csv\",std::fstream::in | std::fstream::out |std::fstream::app);\n")
                    f.write(" \t time_file<<\""+function_name+",\";")
                    f.write("\n \t time_file<<duration.count() << endl;")
                    f.write(" \n \t time_file.close();")
                    f.write("\n\n#endif //TIME_INFO  \n")
                f.write("\n\treturn RPP_SUCCESS;" + "\n}" )
                f.close()


def basic_function(csv_reader, device):
    print("device", device)
    for row in csv_reader:
        module = row[0]
        file = "rppi_" + row[1] + ".cpp"
        function_name = row[2]
        # create folders needed for modules
        if module not in modules:
            print("Creating new module ... ", module)
            os.mkdir(rpp_src_dir + module)
            modules.append(module)
            os.mkdir(rpp_src_dir + module + '/cl')
            os.mkdir(rpp_src_dir + module + '/cpu')
            os.mkdir(rpp_src_dir + module + '/hipoc')
        # else:
        #     print("*************module already present*************************")
        # just to create file name such as cl_image_augmentation.cpp / host_image_augmentation.cpp
        #row1 image_augmentation / geometric_transform
        if device :
            local_path = rpp_src_dir + module + '/cl/'
            cl_name = local_path + 'cl_' + row[1] + '.cpp'
            sub_function = row[2] + '_cl' 
            # subfunction to call inside outer most functions like brightness_cl
            print(" subfunction cl :: ", sub_function)
            header = ''
            # function_name1 = rppi_flip_u8_pln1_gpu
            function_name1 = "rppi_"+function_name+"_u8_pln1_gpu"
            for_each_functions(function_name1, row , module, cl_name, file, header, device , sub_function)
            # function_name2 = rppi_flip_u8_pln3_gpu
            function_name2 = "rppi_"+function_name+"_u8_pln3_gpu"
            for_each_functions(function_name2, row , module, cl_name, file, header, device , sub_function)
            # function_name3 = rppi_flip_u8_pkd3_gpu
            function_name3 = "rppi_"+function_name+"_u8_pkd3_gpu"
            for_each_functions(function_name3, row , module, cl_name, file, header, device , sub_function)
        else :
            local_path = rpp_src_dir  + module + '/cpu/'
            host_name = local_path + 'host_' + row[1] + '.hpp'
            header = " \"cpu/" + 'host_' + row[1] + '.hpp" '
            #header = " \"cpu/" + 'host_' + row[1] + '_functions.hpp" '
            # subfunction to call inside outer most functions like brightness_host
            sub_function = row[2] + "_host"
            print(" subfunction host pln :: ", sub_function)
            # function_name1 = rppi_flip_u8_pln1_host
            function_name1 = "rppi_"+function_name+"_u8_pln1_host"
            for_each_functions(function_name1, row , module, host_name, file, header, device , sub_function)
            # function_name2 = rppi_flip_u8_pln3_host
            function_name2 = "rppi_"+function_name+"_u8_pln3_host"
            for_each_functions(function_name2, row , module, host_name, file, header, device , sub_function)
            # function_name3 = rppi_flip_u8_pkd3_host
            function_name3 = "rppi_"+function_name+"_u8_pkd3_host"
            for_each_functions(function_name3, row , module, host_name, file, header, device , sub_function)


cl_end = r'''   RppiChnFormat chnFormat, unsigned int channel,
                cl_command_queue theQueue) 
{
    return RPP_SUCCESS;
}
'''

host_end = r''' unsigned int channel, RppiChnFormat chnFormat)
{
    return RPP_SUCCESS;
}
'''

header_code = r'''
#include <rppdefs.h>
#include "rppi_validate.hpp"

#ifdef HIP_COMPILE
#include <hip/rpp_hip_common.hpp>

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

rpp_src_dir = "/home/mcw/AMD_RPP_shobi/ktnotes/AMDRPP/src/"

local_path = rpp_src_dir

modules = []
header_file_names = []
for dirs in os.listdir(rpp_src_dir):
    modules.append(dirs)

time_info = 0

with open('/home/mcw/AMD_RPP_shobi/ktnotes/scripts/RPP_Automation/process_ms4.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    basic_function(csv_reader, 0)
with open('/home/mcw/AMD_RPP_shobi/ktnotes/scripts/RPP_Automation/process_ms4.csv') as csv_file1:
    csv_reader1 = csv.reader(csv_file1, delimiter=',')
    basic_function(csv_reader1, 1)
for each_file in header_file_names:
    f = open(each_file,"a+")
    f.write("\n "+header_guards_end)
   
	
