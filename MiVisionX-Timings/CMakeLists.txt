#MI	T License
#
# Copyright (c) 2018 Advanced Micro Devices, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################

cmake_minimum_required (VERSION 2.8)
project (ovx_test)
set (CMAKE_CXX_STANDARD 11)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(OpenCV )

include_directories (${OpenCV_INCLUDE_DIRS})
include_directories (/opt/rocm/mivisionx/include/)
include_directories (/opt/rocm/opencl/include/)
include_directories (/opt/rocm/include)
link_directories    (/opt/rocm/mivisionx/lib/)
link_directories    (/opt/rocm/lib)
link_directories    (/opt/rocm/rpp/lib/)



add_executable(ovx_test ovx_test_old.cpp)
target_compile_definitions(ovx_test PUBLIC )
target_link_libraries(ovx_test -g ${OpenCV_LIBRARIES})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ")
target_link_libraries(ovx_test -g openvx vx_rpp ${OpenCV_LIBRARIES} -L/opt/rocm/opencl/lib/x86_64/ -g -lOpenCL pthread  -L/usr/lib/x86_64-linux-gnu/  -lboost_filesystem -lboost_system)

cmake_minimum_required (VERSION 2.8)
project (rali)
set (CMAKE_CXX_STANDARD 11)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(OpenCV )

include_directories (${OpenCV_INCLUDE_DIRS})
include_directories (/opt/rocm/mivisionx/include/)
include_directories (/opt/rocm/opencl/include/)
include_directories (/opt/rocm/include)
link_directories    (/opt/rocm/mivisionx/lib/)
link_directories    (/opt/rocm/lib)
link_directories    (/opt/rocm/rpp/lib/)



# add_executable(rppTest ovx_test_old.cpp)
# # add_executable(rppTestGauss rpp_test.cpp)
# # add_executable(rppTestErode rpp_test_erode.cpp)
# # add_executable(rppTestDilate rpp_test_erode.cpp)
# # add_executable(rppTestBox rpp_test_box.cpp)
# #add_executable(rpp_timings rpp_timings.cpp)




# if (OpenCV_FOUND)
#   target_compile_definitions(rppTest PUBLIC ENABLE_OPENCV=1)

#   target_link_libraries(rppTest ${OpenCV_LIBRARIES})
# else(OpenCV_FOUND)
#   target_compile_definitions(rppTest PUBLIC ENABLE_OPENCV=0)
# endif(OpenCV_FOUND)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ")
# target_link_libraries(rppTest -g openvx ${OpenCV_LIBRARIES} -L/opt/rocm/opencl/lib/x86_64/ -lOpenCL pthread)
# # target_link_libraries(rppTestGauss -g openvx ${OpenCV_LIBRARIES} -L/opt/rocm/opencl/lib/x86_64/ -lOpenCL pthread)
# # target_link_libraries(rppTestErode -g openvx ${OpenCV_LIBRARIES} -L/opt/rocm/opencl/lib/x86_64/ -lOpenCL pthread)
# # target_link_libraries(rppTestDilate -g openvx ${OpenCV_LIBRARIES} -L/opt/rocm/opencl/lib/x86_64/ -lOpenCL pthread)
# # target_link_libraries(rppTestBox -g openvx ${OpenCV_LIBRARIES} -L/opt/rocm/opencl/lib/x86_64/ -lOpenCL pthread)
# #target_link_libraries(rpp_timings -g openvx ${OpenCV_LIBRARIES} -L/opt/rocm/opencl/lib/x86_64/ -lOpenCL pthread)






























