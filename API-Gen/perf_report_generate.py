import csv
import os
cur_directory = os.path.dirname(os.path.realpath(__file__))
image_file = open(cur_directory + "/image_name.csv","r")
time_file = open(cur_directory+"/gdf_files/rpp_time.csv","a+")
perf_report = open(cur_directory + "/final_perf_report.csv","a+")
perf_report_list = perf_report.readlines()
p_len = len(perf_report_list)
image_csv_reader = csv.reader(image_file, delimiter=',')
time_csv_reader = csv.reader(time_file, delimiter=',')
valid = 1
for idx,row in enumerate(time_csv_reader):
    if(p_len == 0):
        valid = 0
        for time_info in row:
            if("_") in time_info:
                time_info = time_info.replace("_",",")
                perf_report.write(time_info)
                perf_report.write(',')
            else:
                perf_report.write(time_info)
                perf_report.write(',')
    elif(idx == p_len):
        valid = 0
        for time_info in row:
            if("_") in time_info:
                time_info = time_info.replace("_",",")
                perf_report.write(time_info)
                perf_report.write(',')
            else:
                perf_report.write(time_info)
                perf_report.write(',')
if valid:
    perf_report.write('Invalid parameters ,')
    time_file.write('Invalid parameters \n')

for idx, row in enumerate(image_csv_reader):
    if idx == 0:
        if(p_len == 0):
            for image_info in row:
                perf_report.write(image_info)
                perf_report.write(',')
            perf_report.write('\n')
    elif(idx == p_len):
        for image_info in row:
            perf_report.write(image_info)
            perf_report.write(',')
        perf_report.write('\n')


image_file.close()
time_file.close()
perf_report.close()
