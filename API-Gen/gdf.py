import subprocess
import csv
import shlex, subprocess
import os
import time

#Gettting started! 

#Folder Deatils
#output : Stores final output
#gdf_files : stores gdf files.

#Input Format : Node name, no of inputs,no of outputs(0/1),[paramter type, paramter datatype, value]
#org.rpp.XOR,2,1,scalar,float,1

#Make sure the current path csv files and the python script are present in the same folder.
#Chaneg image directory path.
#Export mivisionx library, rpp library and runvx path in local terminal.

start = r'''
import vx_rpp
'''

#org.rpp.Brightness,1,480,360,U008,480,360,U008,scalar,float,1,scalar,int,10
#org.rpp.Brightness,1,1,scalar,float,1,scalar,int,10
#lady.png,480,360,U008
cur_directory = os.path.dirname(os.path.realpath(__file__))
img_directory = "/home/mcw/AMD_RPP_shobi/ktnotes/gdf/images/"
modules = []
for dirs in os.listdir(cur_directory):
    modules.append(dirs)
if "output" not in modules:
    os.mkdir(cur_directory + '/output')
if "gdf_files" not in modules:
    os.mkdir(cur_directory + '/gdf_files')

counter = 0
image_name_csv = open(cur_directory + "/image_name.csv","a")
with open(cur_directory +'/gdf.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    run= open("run.sh","w")
    for row in csv_reader:
        function = row[0].split(".")
        arguments = (len(row))
        if row[1] == '1':
            images_file = open(cur_directory + "/gdf_single_input.csv","r")
            images = images_file.readlines()
            for idx, image in enumerate(images):
                image_params = image.split(",")
                #print(image_params)
                if "Hue" in function:
                    if "U008" in image_params[-1].strip():
                        print(image_params)
                        print("encountered HUE")
                        continue
                elif "Saturation" in function:
                    if "U008" in image_params[-1].strip():
                        print(image_params)
                        print("encountered Saturation")
                        continue
                image_name = image_params[0].split(".")
                image_extension = image_name[1]
                image_name = image_name[0]
                output_name_params = ""
                execute_call = ""
                params = ''
                counter = counter + 1
                f= open("gdf_files/" + "run_" + str(counter) + ".gdf","w")      
                run.write("runvx " + "gdf_files/" + "run_" + str(counter) + ".gdf" + "\n" )
                run.write(" python perf_report_generate.py \n")
                if idx == 0:
                    image_name_csv.write(image.rstrip())
                else:
                    image_name_csv.write(image.rstrip())
                f.write("\n" + start)                          
                for j in range(3, arguments-1,3) :
                    extra_parameters = "data " + "temp" + str(j) + " = " + row[j] + ":" 
                    params = params + " " + "temp" + str(j)
                    output_name_params = output_name_params + "_" + row[j+2]           
                    if row[j + 1] == "float" :
                        extra_parameters = extra_parameters + "FLOAT32," + row[j+2]
                        image_name_csv.write(",FLOAT32,")
                        image_name_csv.write(row[j+2])
                    if row[j + 1] == "float64" :
                        extra_parameters = extra_parameters + "FLOAT64," + row[j+2]
                        image_name_csv.write(",FLOAT64,")
                        image_name_csv.write(row[j+2])
                    if row[j + 1] == "uint":
                        extra_parameters = extra_parameters + "UINT32," + row[j+2] 
                        image_name_csv.write(",UINT32,")
                        image_name_csv.write(row[j+2])
                    if row[j + 1] == "int":
                        extra_parameters = extra_parameters + "INT32," + row[j+2]
                        image_name_csv.write(",INT32,")
                        image_name_csv.write(row[j+2])
                    f.write(extra_parameters + "\n")

                output_name = "output_" + function[2] + "_" + image_name + output_name_params + "_" + str(counter) + "." + image_extension
                input = "\ndata input1 = image" + ':' + image_params[1] + ',' + image_params[2] + ',' + image_params[3] 
                f.write(input)
                core_params = " input1"
                f.write("\nread input1 " + img_directory  + image_name + "." + image_extension + "\n")
                if row[2] == '1':
                    output = "\ndata output = image" + ':' + image_params[1] + ',' + image_params[2] + ',' + image_params[3]
                    f.write(output)
                    core_params = core_params + " output"
                    f.write("\nwrite output " + "../output/" + output_name + "\n")
                if row[2] == '0':      
                    f.write("\nwrite input1 " + "../output/" + output_name + "\n") 
                execute_call = "\nnode " + row[0] + core_params + params
                image_name_csv.write("\n")
                f.write(execute_call)
                f.close
        else:
            images_file = open(cur_directory + "/gdf_double_input.csv","r+")
            images = images_file.readlines()
            for idx, double_images in enumerate(images):
                image_count = 0 
                params = ""
                execute_call = ""
                output_name_params = ""
                core_params= ""
                double_image = double_images.split(",")
                images_names = [double_image[0].split(".")[0], double_image[4].split(".")[0] ]
                images_extension = [double_image[0].split(".")[1], double_image[4].split(".")[1] ]   
                counter = counter + 1
                f= open("gdf_files/" + "run_" + str(counter) + ".gdf","w")                
                run.write("runvx " + "gdf_files/" + "run_" + str(counter) + ".gdf" + "\n" )
                run.write("python perf_report_generate.py \n")
                if idx == 0:
                    image_name_csv.write(double_images.rstrip())
                else:
                    image_name_csv.write(double_images.rstrip())
                f.write("\n" + start)   
                for j in range(3, arguments-1,3) :
                    extra_parameters = "data " + "temp" + str(j) + " = " + row[j] + ":" 
                    params = params + " " + "temp" + str(j)
                    output_name_params = output_name_params + "_" + row[j+2]           
                    if row[j + 1] == "float" :
                        extra_parameters = extra_parameters + "FLOAT32," + row[j+2]
                        image_name_csv.write(",FLOAT32,")
                        image_name_csv.write(row[j+2])
                    if row[j + 1] == "float64" :
                        extra_parameters = extra_parameters + "FLOAT64," + row[j+2]
                        image_name_csv.write(",FLOAT64,")
                        image_name_csv.write(row[j+2])
                    if row[j + 1] == "uint":
                        extra_parameters = extra_parameters + "UINT32," + row[j+2]
                        image_name_csv.write(",UINT32,")
                        image_name_csv.write(row[j+2])
                    if row[j + 1] == "int":
                        extra_parameters = extra_parameters + "INT32," + row[j+2]
                        image_name_csv.write(",INT32,")
                        image_name_csv.write(row[j+2])
                    f.write(extra_parameters + "\n")
                
                output_name = "output_" + function[2] + "_" + images_names[0] + "_" + images_names[1] + output_name_params + "_" + str(counter) + "." + images_extension[0]
                
                for image in images_names:
                    image_count = image_count + 1
                    for i in range (1 + (image_count - 1) * 4, 1 + (image_count * 3), 3):
                        input = "\ndata input" + str(image_count) +  " = image" + ':' + double_image[i] + ',' + double_image[i+1] + ',' + double_image[i+2]
                        core_params = core_params + " input" + str(image_count) + " "
                        f.write(input + "\n")
                        f.write("\nread input" + str(image_count) + " " + img_directory + image + "." + images_extension[image_count-1] +  "\n")
                
                if row[2] == '1':      
                    output = "\ndata output = image" + ':' + double_image[i] + ',' + double_image[i+1] + ',' + double_image[i+2]
                    core_params = core_params + " output"
                    f.write(output + "\n")
                    f.write("\nwrite output " + "../output/" + output_name + "\n")
                if row[2] == '0':      
                    f.write("\nwrite input1 " + "../output/" + output_name + "\n")                    
                
                execute_call = "node " + row[0] + core_params + params
                image_name_csv.write("\n")
                f.write(execute_call)
                f.close
                

    f_exec = "chmod +x run.sh"
    p = subprocess.Popen(f_exec, shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
    (out,err) = p.communicate()
    if p.returncode == 0:
        print ("command '' succeeded, returned: %s" \
        % (str(out)))
    else:
        print ("command '' failed, exit-code=%d error = %s" \
                % (p.returncode, str(err)))
image_name_csv.close()   

