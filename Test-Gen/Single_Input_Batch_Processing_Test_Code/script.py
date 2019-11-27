# IMPORTS
import subprocess
import csv
import shlex, subprocess
import os

# IO FOLDERS LOCATIONS
local_folder = '/home/lokeswara/Desktop/AMD-RPP/AMDRPP-Scripts/Test-Gen/Single_Input_Batch_Processing_Test_Code/' # CURRENT SCRIPT CODE LOCATION + '/'
csv_name = '/home/lokeswara/Desktop/AMD-RPP/AMDRPP-Scripts/Test-Gen/Single_Input_Batch_Processing_Test_Code/batch_script.csv' # CSV FILE LOCATION
code_folder = '/home/lokeswara/Desktop/AMD-RPP/AMDRPP-Scripts/dummy/' # FOLDER LOCATION TO DUMP SCRIPT GENERATED CODE + '/'

# GENERAL
IP_shell_name = "/shell.sh"
IP_build = "/build"
IP_cmake_location = "/CMakeLists.txt"
IP_cmake_name = "CMakeLists.txt"
IP_shell_1 = "cd\ncd "
IP_shell_2 = "/build\ncmake ..\nmake\n"
IP_host = "_HOST"
IP_ocl = "_OCL"
IP_hip = "_HIP"
IP_pln = "_PLN.cpp"
IP_pkd = "_PKD.cpp"
IP_1 = "INPUT%1"
IP_2 = "INPUT%2"
IP_3 = "INPUT%3"
IP_4 = "INPUT%4"
IP_5 = "INPUT%5"
IP_tab = "\t"
IP_min = "min"
IP_max = "max"
IP_cmake_1 = "add_executable("
IP_cmake_2 = ")\n"
IP_cmake_3 = "\ntarget_link_libraries("
IP_cmake_4 = " ${OpenCV_LIBS} -I/opt/rocm/rpp/include -L/opt/rocm/rpp/lib/ -lamd_rpp -L/opt/rocm/opencl/lib/x86_64/ -lOpenCL pthread  -lboost_filesystem -lboost_system )"
IP_cmake_3_hip = "\ntarget_link_libraries("
IP_cmake_4_hip = " ${OpenCV_LIBS} -I/opt/rocm/rpp/include/ -I/opt/rocm/opencl/include/ -I/opt/rocm/include/ -L/opt/rocm/rpp/lib/ -lamd_rpp -lboost_filesystem -lboost_system -L/opt/rocm/hip/lib/ -lhiprtc)"


# SCRIPTING CODE
def process_csv(csv_reader,numline):
    shell_text = "" # STORES THE COMMANDS TO GET EXECUTED AFTER SCRIPTING
    shell_script = open(code_folder + IP_shell_name,"a+") # CREATES SHELL SCRIPT INSEDE OP LOCATION

    # TRAVERSE EACH AND EVERY FUNCTION IN THE CSV 
    for count,row in enumerate(csv_reader):
        
        writeFuncName = row[4]
        if(row[1] == '0'):
            writeFuncName = writeFuncName + IP_host
        elif(row[1] == '1'):
            writeFuncName = writeFuncName + IP_ocl
        else:
            writeFuncName = writeFuncName + IP_hip
        
        os.mkdir(code_folder + writeFuncName) # CREATE A FOLDER INSIDE THE OP LOCATION WITH THE FUNCTION NAME
        os.mkdir(code_folder + writeFuncName + IP_build) # CREATE THE BUILD FOLDER INSIDE THE SPECIFIED LOCATION
        
        cm = open(code_folder + writeFuncName + IP_cmake_location, "a+") # CREATE A 'CMakeList.txt' INSIDE THE FUNCTION FOLDER
        c = open(local_folder + IP_cmake_name, "r") # OPEN TEMPLATE CMAKE FILE IN THE CURRENT FOLDER
        cmake = c.read() # READ CONTENTS OF THE TEMPLATE CMAKE FILES
        # SET COMPILE FLAGS IN CMAKE ACCORDING TO HIP OR OCL
        if(row[1] == 0) or (row[1] == 1):
            cmake = cmake + "\n" + """set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DOCL_COMPILE=1 -DRPP_BACKEND_OPENCL=1 ")"""
        else:
            cmake = cmake + "\n" + """set(COMPILER_FOR_HIP /opt/rocm/bin/hipcc)"""
            cmake = cmake + "\n" + """set(CMAKE_CXX_COMPILER ${COMPILER_FOR_HIP})"""
            cmake = cmake + "\n" + """set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHIP_COMPILE=1 -DRPP_BACKEND_HIP=1 -fopenmp -std=c++14") """

        shell_text = shell_text + IP_shell_1 + code_folder + writeFuncName + IP_shell_2
        
        # """ """ """ """ """ FUNCTION 1 Batch_DD_D_C """ """ """ """ """

        # CREATE NEW 'Batch_DD_D_C<MODE>.cpp' FILE INSIDE OP FUNCTION LOCATION
        fileName = '/Batch_DD_D_C'
        if(row[1] == '0'):
            fileName = fileName + IP_host
        elif(row[1] == '1'):
            fileName = fileName + IP_ocl
        else:
            fileName = fileName + IP_hip
        if(row[0] == '1'):
            fileName = fileName + IP_pln
        else:
            fileName = fileName + IP_pkd
        DD_D_C = open(code_folder + writeFuncName + fileName,"a+")
        
        code1 = open(local_folder + 'Batch_DD_D_C.cpp',"r") # OPEN TEMPLATE FILE
        Batch_DD_D_C = code1.read() # READ Batch_DD_D_C.cpp

        # WRITE IN CMAKE
        index_cmake = cmake.index('set(')
        cmake = cmake[:index_cmake] + IP_cmake_1 + "Batch_DD_D_C Batch_DD_D_C.cpp" + IP_cmake_2 + cmake[index_cmake:]
        if(row[1] == '2'):
            cmake = cmake + IP_cmake_3_hip + "Batch_DD_D_C" + IP_cmake_4_hip
        else:
            cmake = cmake + IP_cmake_3 + "Batch_DD_D_C" + IP_cmake_4

        if(row[1] == '2'):
            index_temp = Batch_DD_D_C.index('using namespace cv;')  
            Batch_DD_D_C = Batch_DD_D_C[:index_temp] + """void check_hip_error(void)\n{\n\thipError_t err = hipGetLastError();\n\tif (err != hipSuccess)\n\t{\n\t\tstd::cerr\n\t\t\t<< "Error: "\n\t\t\t<< hipGetErrorString(err)\n\t\t\t<< std::endl;\n\t\texit(err);\n\t}\n}\n""" + Batch_DD_D_C[index_temp:]
        # UPDATE INITIAL PARAMETERS IN THE FILE
        Batch_DD_D_C = Batch_DD_D_C.replace(IP_1,row[0])
        Batch_DD_D_C = Batch_DD_D_C.replace(IP_2,row[1])
        Batch_DD_D_C = Batch_DD_D_C.replace(IP_3,row[2])
        Batch_DD_D_C = Batch_DD_D_C.replace(IP_4,row[3])
        Batch_DD_D_C = Batch_DD_D_C.replace(IP_5,row[4])

        # MAIN CODE AND FUNCTION CALL
        Batch_DD_D_C_Main_Code = ''
        i = 6
        for x in range(int(row[5])):
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\t' + row[i] + ' min' + row[i+1] + ' = ' + row[i+2] + ', max' + row[i+1] + ' = ' + row[i+3] + ', ' + row[i+1] + '[images];\n'
            i = i + 4
        i = 6
        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\t' + 'for(i = 0 ; i < images ; i++)\n\t{\n'
        for x in range(int(row[5])):
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\t\t' + row[i+1] + '[i] = ((max' + row[i+1] + ' - min' + row[i+1] + ') / images) * i + min' + row[i+1] + ';\n' 
            i = i + 4
        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\t}\n'
        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\n\trppHandle_t handle;\n'
        if(row[1] == '0'):
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\trppCreateWithBatchSize(&handle, noOfImages);\n'
        elif(row[1] == '1'):
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + """   
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages);
\tcl_mem d_input, d_output;
\tcl_platform_id platform_id;
\tcl_device_id device_id;
\tcl_context theContext;
\tcl_command_queue theQueue;
\tcl_int err;
\tif(mode == 1)
\t\t{
\t\terr = clGetPlatformIDs(1, &platform_id, NULL);
\t\terr = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_GPU, 1, &device_id, NULL);
\t\ttheContext = clCreateContext(0, 1, &device_id, NULL, NULL, &err);
\t\ttheQueue = clCreateCommandQueue(theContext, device_id, 0, &err);
\t\td_input = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\td_output = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\terr = clEnqueueWriteBuffer(theQueue, d_input, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), input, 0, NULL, NULL);
\t}\n 
"""
        else:
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + """ 
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages); 
\tint *d_input, *d_output;
\thipMalloc(&in, ioBufferSize * sizeof(Rpp8u));
\thipMalloc(&out, ioBufferSize * sizeof(Rpp8u));
\tcheck_hip_error();
\thipMemcpy(in,input,ioBufferSize * sizeof(Rpp8u),hipMemcpyHostToDevice);
\tcheck_hip_error();\n
"""
        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + """ 
\tclock_t start, end;'    
\tdouble cpu_time_used;
\tstart = clock();\n 
"""
        if(row[1] == '0'):
            if(row[0] == 3):
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        else:    
            if(row[0] == 3):
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_host(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_host(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + """\tend = clock();
\tcpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
\tcout<<"Batch_DD_D_C TIME"<<cpu_time_used<<endl; """
        if(row[1] == '1'):
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + """
\tclEnqueueReadBuffer(theQueue, d_output, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), output, 0, NULL, NULL);

\trppDestroyGPU(handle);\n
"""
        elif(row[1] == '2'):
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + """
\thipMemcpy(output,out,ioBufferSize * sizeof(Rpp8u),hipMemcpyDeviceToHost);

\trppDestroyGPU(handle);\n
"""
        else:
            Batch_DD_D_C_Main_Code = Batch_DD_D_C_Main_Code + "\n\trppDestroyHost(handle);"
        
        # insert code into the temp program code
        index_Batch_DD_D_C = Batch_DD_D_C.index('/* CODE ENDS HERE */')
        Batch_DD_D_C = Batch_DD_D_C[:index_Batch_DD_D_C] + Batch_DD_D_C_Main_Code + Batch_DD_D_C[index_Batch_DD_D_C:]
        
        # Write the template Batch_DD_D_C.cpp into new Batch_DD_D_C.cpp
        DD_D_C.write(Batch_DD_D_C) 
        shell_text = shell_text + "./Batch_DD_D_C\n"
        # """ """ """ """ """ """ """  """ """ """ """ """ """ """
        
        # Write the template cmake into new cmake
        cm.write(cmake)

  # """ """ """ """ """ FUNCTION 1 Batch_SS """ """ """ """ """

        # CREATE NEW 'Batch_SS<MODE>.cpp' FILE INSIDE OP FUNCTION LOCATION
        fileName = '/Batch_SS'
        if(row[1] == '0'):
            fileName = fileName + IP_host
        elif(row[1] == '1'):
            fileName = fileName + IP_ocl
        else:
            fileName = fileName + IP_hip
        if(row[0] == '1'):
            fileName = fileName + IP_pln
        else:
            fileName = fileName + IP_pkd
        SS = open(code_folder + writeFuncName + fileName,"a+")
        
        code1 = open(local_folder + 'Batch_SS.cpp',"r") # OPEN TEMPLATE FILE
        Batch_SS = code1.read() # READ Batch_DD_D_C.cpp

        # WRITE IN CMAKE
        index_cmake = cmake.index('set(')
        cmake = cmake[:index_cmake] + IP_cmake_1 + "Batch_SS Batch_SS.cpp" + IP_cmake_2 + cmake[index_cmake:]
        if(row[1] == '2'):
            cmake = cmake + IP_cmake_3_hip + "Batch_SS" + IP_cmake_4_hip
        else:
            cmake = cmake + IP_cmake_3 + "Batch_SS" + IP_cmake_4

        if(row[1] == '2'):
            index_temp = Batch_SS.index('using namespace cv;')  
            Batch_SS = Batch_SS[:index_temp] + """void check_hip_error(void)\n{\n\thipError_t err = hipGetLastError();\n\tif (err != hipSuccess)\n\t{\n\t\tstd::cerr\n\t\t\t<< "Error: "\n\t\t\t<< hipGetErrorString(err)\n\t\t\t<< std::endl;\n\t\texit(err);\n\t}\n}\n""" + Batch_SS[index_temp:]
        # UPDATE INITIAL PARAMETERS IN THE FILE
        Batch_SS = Batch_SS.replace(IP_1,row[0])
        Batch_SS = Batch_SS.replace(IP_2,row[1])
        Batch_SS = Batch_SS.replace(IP_3,row[len(row) - 1])
        Batch_SS = Batch_SS.replace(IP_4,row[3])
        Batch_SS = Batch_SS.replace(IP_5,row[4])

        # MAIN CODE AND FUNCTION CALL
        Batch_SS_Main_Code = ''
        i = 6
        for x in range(int(row[5])):
            Batch_SS_Main_Code = Batch_SS_Main_Code + '\t' + row[i] + ' min' + row[i+1] + ' = ' + row[i+2] + ', max' + row[i+1] + ' = ' + row[i+3] + ', ' + row[i+1] + '[images];\n'
            i = i + 4
        i = 6
        for x in range(int(row[5])):
            Batch_SS_Main_Code = Batch_SS_Main_Code + '\t' + row[i+1] + ' = rand() % (max' + row[i+1] + ' - min' + row[i+1] + ') + min' + row[i+1] + ';\n' 
            i = i + 4

        Batch_SS_Main_Code = Batch_SS_Main_Code + '\n\trppHandle_t handle;\n'
        if(row[1] == '0'):
            Batch_SS_Main_Code = Batch_SS_Main_Code + '\trppCreateWithBatchSize(&handle, noOfImages);\n'
        elif(row[1] == '1'):
            Batch_SS_Main_Code = Batch_SS_Main_Code + """   
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages);
\tcl_mem d_input, d_output;
\tcl_platform_id platform_id;
\tcl_device_id device_id;
\tcl_context theContext;
\tcl_command_queue theQueue;
\tcl_int err;
\tif(mode == 1)
\t\t{
\t\terr = clGetPlatformIDs(1, &platform_id, NULL);
\t\terr = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_GPU, 1, &device_id, NULL);
\t\ttheContext = clCreateContext(0, 1, &device_id, NULL, NULL, &err);
\t\ttheQueue = clCreateCommandQueue(theContext, device_id, 0, &err);
\t\td_input = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\td_output = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\terr = clEnqueueWriteBuffer(theQueue, d_input, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), input, 0, NULL, NULL);
\t}\n 
"""
        else:
            Batch_SS_Main_Code = Batch_SS_Main_Code + """ 
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages); 
\tint *d_input, *d_output;
\thipMalloc(&in, ioBufferSize * sizeof(Rpp8u));
\thipMalloc(&out, ioBufferSize * sizeof(Rpp8u));
\tcheck_hip_error();
\thipMemcpy(in,input,ioBufferSize * sizeof(Rpp8u),hipMemcpyHostToDevice);
\tcheck_hip_error();\n
"""
        Batch_SS_Main_Code = Batch_SS_Main_Code + """ 
\tclock_t start, end;'    
\tdouble cpu_time_used;
\tstart = clock();\n 
"""
        if(row[1] == '0'):
            if(row[0] == 3):
                Batch_SS_Main_Code = Batch_SS_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_SS_Main_Code = Batch_SS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_SS_Main_Code = Batch_SS_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_SS_Main_Code = Batch_SS_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_SS_Main_Code = Batch_SS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_SS_Main_Code = Batch_SS_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        else:    
            if(row[0] == 3):
                Batch_SS_Main_Code = Batch_SS_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_gpu(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_SS_Main_Code = Batch_SS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_SS_Main_Code = Batch_SS_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_SS_Main_Code = Batch_SS_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_gpu(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_SS_Main_Code = Batch_SS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_SS_Main_Code = Batch_SS_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        Batch_SS_Main_Code = Batch_SS_Main_Code + """\tend = clock();
\tcpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
\tcout<<"Batch_SS TIME"<<cpu_time_used<<endl; """
        if(row[1] == '1'):
            Batch_SS_Main_Code = Batch_SS_Main_Code + """
\tclEnqueueReadBuffer(theQueue, d_output, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), output, 0, NULL, NULL);

\trppDestroyGPU(handle);\n
"""
        elif(row[1] == '2'):
            Batch_SS_Main_Code = Batch_SS_Main_Code + """
\thipMemcpy(output,out,ioBufferSize * sizeof(Rpp8u),hipMemcpyDeviceToHost);

\trppDestroyGPU(handle);\n
"""
        else:
            Batch_SS_Main_Code = Batch_SS_Main_Code + "\n\trppDestroyHost(handle);"
        
        # insert code into the temp program code
        index_Batch_SS = Batch_SS.index('/* CODE ENDS HERE */')
        Batch_SS = Batch_SS[:index_Batch_SS] + Batch_SS_Main_Code + Batch_SS[index_Batch_SS:]
        
        # Write the template Batch_SS.cpp into new Batch_SS.cpp
        SS.write(Batch_SS) 
        shell_text = shell_text + "./Batch_SS\n"
        # """ """ """ """ """ """ """  """ """ """ """ """ """ """

# """ """ """ """ """ FUNCTION 3 Batch_DS """ """ """ """ """

        # CREATE NEW 'Batch_DS<MODE>.cpp' FILE INSIDE OP FUNCTION LOCATION
        fileName = '/Batch_DS'
        if(row[1] == '0'):
            fileName = fileName + IP_host
        elif(row[1] == '1'):
            fileName = fileName + IP_ocl
        else:
            fileName = fileName + IP_hip
        if(row[0] == '1'):
            fileName = fileName + IP_pln
        else:
            fileName = fileName + IP_pkd
        DS = open(code_folder + writeFuncName + fileName,"a+")
        
        code1 = open(local_folder + 'Batch_DS.cpp',"r") # OPEN TEMPLATE FILE
        Batch_DS = code1.read() # READ Batch_DD_D_C.cpp

        # WRITE IN CMAKE
        index_cmake = cmake.index('set(')
        cmake = cmake[:index_cmake] + IP_cmake_1 + "Batch_DS Batch_DS.cpp" + IP_cmake_2 + cmake[index_cmake:]
        if(row[1] == '2'):
            cmake = cmake + IP_cmake_3_hip + "Batch_DS" + IP_cmake_4_hip
        else:
            cmake = cmake + IP_cmake_3 + "Batch_DS" + IP_cmake_4

        if(row[1] == '2'):
            index_temp = Batch_DS.index('using namespace cv;')  
            Batch_DS = Batch_DS[:index_temp] + """void check_hip_error(void)\n{\n\thipError_t err = hipGetLastError();\n\tif (err != hipSuccess)\n\t{\n\t\tstd::cerr\n\t\t\t<< "Error: "\n\t\t\t<< hipGetErrorString(err)\n\t\t\t<< std::endl;\n\t\texit(err);\n\t}\n}\n""" + Batch_DS[index_temp:]
        # UPDATE INITIAL PARAMETERS IN THE FILE
        Batch_DS = Batch_DS.replace(IP_1,row[0])
        Batch_DS = Batch_DS.replace(IP_2,row[1])
        Batch_DS = Batch_DS.replace(IP_3,row[2])
        Batch_DS = Batch_DS.replace(IP_4,row[3])
        Batch_DS = Batch_DS.replace(IP_5,row[4])

        # MAIN CODE AND FUNCTION CALL
        Batch_DS_Main_Code = ''
        i = 6
        for x in range(int(row[5])):
            Batch_DS_Main_Code = Batch_DS_Main_Code + '\t' + row[i] + ' min' + row[i+1] + ' = ' + row[i+2] + ', max' + row[i+1] + ' = ' + row[i+3] + ', ' + row[i+1] + '[images];\n'
            i = i + 4
        i = 6
        for x in range(int(row[5])):
            Batch_DS_Main_Code = Batch_DS_Main_Code + '\t' + row[i+1] + ' = rand() % (max' + row[i+1] + ' - min' + row[i+1] + ') + min' + row[i+1] + ';\n' 
            i = i + 4

        Batch_DS_Main_Code = Batch_DS_Main_Code + '\n\trppHandle_t handle;\n'
        if(row[1] == '0'):
            Batch_DS_Main_Code = Batch_DS_Main_Code + '\trppCreateWithBatchSize(&handle, noOfImages);\n'
        elif(row[1] == '1'):
            Batch_DS_Main_Code = Batch_DS_Main_Code + """   
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages);
\tcl_mem d_input, d_output;
\tcl_platform_id platform_id;
\tcl_device_id device_id;
\tcl_context theContext;
\tcl_command_queue theQueue;
\tcl_int err;
\tif(mode == 1)
\t\t{
\t\terr = clGetPlatformIDs(1, &platform_id, NULL);
\t\terr = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_GPU, 1, &device_id, NULL);
\t\ttheContext = clCreateContext(0, 1, &device_id, NULL, NULL, &err);
\t\ttheQueue = clCreateCommandQueue(theContext, device_id, 0, &err);
\t\td_input = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\td_output = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\terr = clEnqueueWriteBuffer(theQueue, d_input, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), input, 0, NULL, NULL);
\t}\n 
"""
        else:
            Batch_DS_Main_Code = Batch_DS_Main_Code + """ 
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages); 
\tint *d_input, *d_output;
\thipMalloc(&in, ioBufferSize * sizeof(Rpp8u));
\thipMalloc(&out, ioBufferSize * sizeof(Rpp8u));
\tcheck_hip_error();
\thipMemcpy(in,input,ioBufferSize * sizeof(Rpp8u),hipMemcpyHostToDevice);
\tcheck_hip_error();\n
"""
        Batch_DS_Main_Code = Batch_DS_Main_Code + """ 
\tclock_t start, end;'    
\tdouble cpu_time_used;
\tstart = clock();\n 
"""
        if(row[1] == '0'):
            if(row[0] == 3):
                Batch_DS_Main_Code = Batch_DS_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DS_Main_Code = Batch_DS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DS_Main_Code = Batch_DS_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_DS_Main_Code = Batch_DS_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DS_Main_Code = Batch_DS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DS_Main_Code = Batch_DS_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        else:    
            if(row[0] == 3):
                Batch_DS_Main_Code = Batch_DS_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_gpu(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DS_Main_Code = Batch_DS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DS_Main_Code = Batch_DS_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_DS_Main_Code = Batch_DS_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_gpu(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DS_Main_Code = Batch_DS_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DS_Main_Code = Batch_DS_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        Batch_DS_Main_Code = Batch_DS_Main_Code + """\tend = clock();
\tcpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
\tcout<<"Batch_DS TIME"<<cpu_time_used<<endl; """
        if(row[1] == '1'):
            Batch_DS_Main_Code = Batch_DS_Main_Code + """
\tclEnqueueReadBuffer(theQueue, d_output, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), output, 0, NULL, NULL);

\trppDestroyGPU(handle);\n
"""
        elif(row[1] == '2'):
            Batch_DS_Main_Code = Batch_DS_Main_Code + """
\thipMemcpy(output,out,ioBufferSize * sizeof(Rpp8u),hipMemcpyDeviceToHost);

\trppDestroyGPU(handle);\n
"""
        else:
            Batch_DS_Main_Code = Batch_DS_Main_Code + "\n\trppDestroyHost(handle);"
        
        # insert code into the temp program code
        index_Batch_DS = Batch_DS.index('/* CODE ENDS HERE */')
        Batch_DS = Batch_DS[:index_Batch_DS] + Batch_DS_Main_Code + Batch_DS[index_Batch_DS:]
        
        # Write the template Batch_DS.cpp into new Batch_DS.cpp
        DS.write(Batch_DS) 
        shell_text = shell_text + "./Batch_DS\n"
        # """ """ """ """ """ """ """  """ """ """ """ """ """ """

# """ """ """ """ """ FUNCTION 4 Batch_DD """ """ """ """ """

        # CREATE NEW 'Batch_DD<MODE>.cpp' FILE INSIDE OP FUNCTION LOCATION
        fileName = '/Batch_DD'
        if(row[1] == '0'):
            fileName = fileName + IP_host
        elif(row[1] == '1'):
            fileName = fileName + IP_ocl
        else:
            fileName = fileName + IP_hip
        if(row[0] == '1'):
            fileName = fileName + IP_pln
        else:
            fileName = fileName + IP_pkd
        DD = open(code_folder + writeFuncName + fileName,"a+")
        
        code1 = open(local_folder + 'Batch_DD.cpp',"r") # OPEN TEMPLATE FILE
        Batch_DD = code1.read() # READ Batch_DD_D_C.cpp

        # WRITE IN CMAKE
        index_cmake = cmake.index('set(')
        cmake = cmake[:index_cmake] + IP_cmake_1 + "Batch_DD Batch_DD.cpp" + IP_cmake_2 + cmake[index_cmake:]
        if(row[1] == '2'):
            cmake = cmake + IP_cmake_3_hip + "Batch_DD" + IP_cmake_4_hip
        else:
            cmake = cmake + IP_cmake_3 + "Batch_DD" + IP_cmake_4

        if(row[1] == '2'):
            index_temp = Batch_DD.index('using namespace cv;')  
            Batch_DD = Batch_DD[:index_temp] + """void check_hip_error(void)\n{\n\thipError_t err = hipGetLastError();\n\tif (err != hipSuccess)\n\t{\n\t\tstd::cerr\n\t\t\t<< "Error: "\n\t\t\t<< hipGetErrorString(err)\n\t\t\t<< std::endl;\n\t\texit(err);\n\t}\n}\n""" + Batch_DD[index_temp:]
        # UPDATE INITIAL PARAMETERS IN THE FILE
        Batch_DD = Batch_DD.replace(IP_1,row[0])
        Batch_DD = Batch_DD.replace(IP_2,row[1])
        Batch_DD = Batch_DD.replace(IP_3,row[len(row) - 1])
        Batch_DD = Batch_DD.replace(IP_4,row[3])
        Batch_DD = Batch_DD.replace(IP_5,row[4])

        # MAIN CODE AND FUNCTION CALL
        Batch_DD_Main_Code = ''
        i = 6
        Batch_DD_Main_Code = Batch_DD_Main_Code + '\t' + 'for(i = 0 ; i < images ; i++)\n\t{\n'
        for x in range(int(row[5])):
            Batch_DD_Main_Code = Batch_DD_Main_Code + '\t\t' + row[i+1] + '[i] = ((max' + row[i+1] + ' - min' + row[i+1] + ') / images) * i + min' + row[i+1] + ';\n' 
            i = i + 4
        Batch_DD_Main_Code = Batch_DD_Main_Code + '\t}\n'

        i = 6
        for x in range(int(row[5])):
            Batch_DD_Main_Code = Batch_DD_Main_Code + '\t' + row[i+1] + ' = rand() % (max' + row[i+1] + ' - min' + row[i+1] + ') + min' + row[i+1] + ';\n' 
            i = i + 4

        Batch_DD_Main_Code = Batch_DD_Main_Code + '\n\trppHandle_t handle;\n'
        if(row[1] == '0'):
            Batch_DD_Main_Code = Batch_DD_Main_Code + '\trppCreateWithBatchSize(&handle, noOfImages);\n'
        elif(row[1] == '1'):
            Batch_DD_Main_Code = Batch_DD_Main_Code + """   
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages);
\tcl_mem d_input, d_output;
\tcl_platform_id platform_id;
\tcl_device_id device_id;
\tcl_context theContext;
\tcl_command_queue theQueue;
\tcl_int err;
\tif(mode == 1)
\t\t{
\t\terr = clGetPlatformIDs(1, &platform_id, NULL);
\t\terr = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_GPU, 1, &device_id, NULL);
\t\ttheContext = clCreateContext(0, 1, &device_id, NULL, NULL, &err);
\t\ttheQueue = clCreateCommandQueue(theContext, device_id, 0, &err);
\t\td_input = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\td_output = clCreateBuffer(theContext, CL_MEM_READ_ONLY, ioBufferSize * sizeof(Rpp8u), NULL, NULL);
\t\terr = clEnqueueWriteBuffer(theQueue, d_input, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), input, 0, NULL, NULL);
\t}\n 
"""
        else:
            Batch_DD_Main_Code = Batch_DD_Main_Code + """ 
\trppCreateWithStreamAndBatchSize(&handle, theQueue, noOfImages); 
\tint *d_input, *d_output;
\thipMalloc(&in, ioBufferSize * sizeof(Rpp8u));
\thipMalloc(&out, ioBufferSize * sizeof(Rpp8u));
\tcheck_hip_error();
\thipMemcpy(in,input,ioBufferSize * sizeof(Rpp8u),hipMemcpyHostToDevice);
\tcheck_hip_error();\n
"""
        Batch_DD_Main_Code = Batch_DD_Main_Code + """ 
\tclock_t start, end;'    
\tdouble cpu_time_used;
\tstart = clock();\n 
"""
        if(row[1] == '0'):
            if(row[0] == 3):
                Batch_DD_Main_Code = Batch_DD_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_Main_Code = Batch_DD_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_Main_Code = Batch_DD_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_DD_Main_Code = Batch_DD_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_host(input, srcSize, output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_Main_Code = Batch_DD_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_Main_Code = Batch_DD_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        else:    
            if(row[0] == 3):
                Batch_DD_Main_Code = Batch_DD_Main_Code + '\trppi_' + row[4] + '_u8_pkd3_batchDD_ROID_gpu(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_Main_Code = Batch_DD_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_Main_Code = Batch_DD_Main_Code + 'roiPoints, noOfImages, handle);\n'
            else:
                Batch_DD_Main_Code = Batch_DD_Main_Code + '\trppi_' + row[4] + '_u8_pln1_batchDD_ROID_gpu(d_input, srcSize, d_output, '
                if len(row) > 5:
                    i = 6
                    for x in range(int(row[5])):    
                        Batch_DD_Main_Code = Batch_DD_Main_Code + row[i+1] + ', ' 
                        i = i + 4
                Batch_DD_Main_Code = Batch_DD_Main_Code + 'roiPoints, noOfImages, handle);\n\n' 
        Batch_DD_Main_Code = Batch_DD_Main_Code + """\tend = clock();
\tcpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
\tcout<<"Batch_DD TIME"<<cpu_time_used<<endl; """
        if(row[1] == '1'):
            Batch_DD_Main_Code = Batch_DD_Main_Code + """
\tclEnqueueReadBuffer(theQueue, d_output, CL_TRUE, 0, ioBufferSize * sizeof(Rpp8u), output, 0, NULL, NULL);

\trppDestroyGPU(handle);\n
"""
        elif(row[1] == '2'):
            Batch_DD_Main_Code = Batch_DD_Main_Code + """
\thipMemcpy(output,out,ioBufferSize * sizeof(Rpp8u),hipMemcpyDeviceToHost);

\trppDestroyGPU(handle);\n
"""
        else:
            Batch_DD_Main_Code = Batch_DD_Main_Code + "\n\trppDestroyHost(handle);"
        
        # insert code into the temp program code
        index_Batch_DD = Batch_DD.index('/* CODE ENDS HERE */')
        Batch_DD = Batch_DD[:index_Batch_DD] + Batch_DD_Main_Code + Batch_DD[index_Batch_DD:]
        
        # Write the template Batch_DD.cpp into new Batch_DD.cpp
        DD.write(Batch_DD) 
        shell_text = shell_text + "./Batch_DD\n"
        # """ """ """ """ """ """ """  """ """ """ """ """ """ """

        # Write the template cmake into new cmake
        cm.write(cmake)
      
            
    # SUB PROCESS
    shell_script.write(shell_text)
    # s = subprocess.Popen("cd " + code_folder + ";chmod +x shell.sh;./shell.sh",stdin = None, stdout = None, stderr = None, close_fds = True, shell = True)

# MAIN CODE
with open(csv_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',') # CREATE CSV READER
    f = open(csv_name) # OPEN CSV
    numline = len(f.readlines()) # READ NUMBER OF LINES IN CSV (NUMBER OF LINES = NUMBER OF FUNCTIONS TO BE TESTED)
    print (numline)
    process_csv(csv_reader,numline) # ACTUAL GENERATION OF TEST CODE BEGINE HERE