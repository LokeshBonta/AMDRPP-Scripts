# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ulagammai/ocl-Unit-Testing

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ulagammai/ocl-Unit-Testing/build

# Include any dependencies generated for this target.
include CMakeFiles/Single.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/Single.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/Single.dir/flags.make

CMakeFiles/Single.dir/Single.cpp.o: CMakeFiles/Single.dir/flags.make
CMakeFiles/Single.dir/Single.cpp.o: ../Single.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ulagammai/ocl-Unit-Testing/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/Single.dir/Single.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/Single.dir/Single.cpp.o -c /home/ulagammai/ocl-Unit-Testing/Single.cpp

CMakeFiles/Single.dir/Single.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Single.dir/Single.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ulagammai/ocl-Unit-Testing/Single.cpp > CMakeFiles/Single.dir/Single.cpp.i

CMakeFiles/Single.dir/Single.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Single.dir/Single.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ulagammai/ocl-Unit-Testing/Single.cpp -o CMakeFiles/Single.dir/Single.cpp.s

CMakeFiles/Single.dir/Single.cpp.o.requires:

.PHONY : CMakeFiles/Single.dir/Single.cpp.o.requires

CMakeFiles/Single.dir/Single.cpp.o.provides: CMakeFiles/Single.dir/Single.cpp.o.requires
	$(MAKE) -f CMakeFiles/Single.dir/build.make CMakeFiles/Single.dir/Single.cpp.o.provides.build
.PHONY : CMakeFiles/Single.dir/Single.cpp.o.provides

CMakeFiles/Single.dir/Single.cpp.o.provides.build: CMakeFiles/Single.dir/Single.cpp.o


# Object files for target Single
Single_OBJECTS = \
"CMakeFiles/Single.dir/Single.cpp.o"

# External object files for target Single
Single_EXTERNAL_OBJECTS =

Single: CMakeFiles/Single.dir/Single.cpp.o
Single: CMakeFiles/Single.dir/build.make
Single: /usr/local/lib/libopencv_dnn.so.3.4.0
Single: /usr/local/lib/libopencv_ml.so.3.4.0
Single: /usr/local/lib/libopencv_objdetect.so.3.4.0
Single: /usr/local/lib/libopencv_shape.so.3.4.0
Single: /usr/local/lib/libopencv_stitching.so.3.4.0
Single: /usr/local/lib/libopencv_superres.so.3.4.0
Single: /usr/local/lib/libopencv_videostab.so.3.4.0
Single: /usr/local/lib/libopencv_calib3d.so.3.4.0
Single: /usr/local/lib/libopencv_features2d.so.3.4.0
Single: /usr/local/lib/libopencv_flann.so.3.4.0
Single: /usr/local/lib/libopencv_highgui.so.3.4.0
Single: /usr/local/lib/libopencv_photo.so.3.4.0
Single: /usr/local/lib/libopencv_video.so.3.4.0
Single: /usr/local/lib/libopencv_videoio.so.3.4.0
Single: /usr/local/lib/libopencv_imgcodecs.so.3.4.0
Single: /usr/local/lib/libopencv_imgproc.so.3.4.0
Single: /usr/local/lib/libopencv_core.so.3.4.0
Single: CMakeFiles/Single.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ulagammai/ocl-Unit-Testing/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable Single"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Single.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/Single.dir/build: Single

.PHONY : CMakeFiles/Single.dir/build

CMakeFiles/Single.dir/requires: CMakeFiles/Single.dir/Single.cpp.o.requires

.PHONY : CMakeFiles/Single.dir/requires

CMakeFiles/Single.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/Single.dir/cmake_clean.cmake
.PHONY : CMakeFiles/Single.dir/clean

CMakeFiles/Single.dir/depend:
	cd /home/ulagammai/ocl-Unit-Testing/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ulagammai/ocl-Unit-Testing /home/ulagammai/ocl-Unit-Testing /home/ulagammai/ocl-Unit-Testing/build /home/ulagammai/ocl-Unit-Testing/build /home/ulagammai/ocl-Unit-Testing/build/CMakeFiles/Single.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/Single.dir/depend

