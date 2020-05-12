# GTest Samples

## Two Example Cases
  1. Compare Scalar with function output
  2. Compare outputs of two functions

## Install GTests
```
$ sudo apt-get install libgtest-dev
$ cd /usr/src/gtest
$ sudo apt-get install cmake # install cmake
$ sudo cmake CMakeLists.txt
$ sudo make
$ sudo cp *.a /usr/lib  # copy or symlink libgtest.a and libgtest_main.a to your /usr/lib folderst
```
## Build and Run
1. Clone the repository
2. go to the GTest folder
3. mkdir build; cmake .., make 
4. ./runTests

## References
[http://www.eriksmistad.no/getting-started-with-google-test-on-ubuntu/](http://www.eriksmistad.no/getting-started-with-google-test-on-ubuntu/) 
