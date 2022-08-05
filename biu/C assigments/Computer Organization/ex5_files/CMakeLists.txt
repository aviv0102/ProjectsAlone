cmake_minimum_required(VERSION 3.8)
project(ex5_files)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        Blur.bmp
        Blur_correct.bmp
        gibson_500.bmp
        Makefile
        myfunction.c
        readBMP.c
        readBMP.h
        Sharpen.bmp
        Sharpen_correct.bmp
        showBMP.c
        writeBMP.c
        writeBMP.h)

add_executable(ex5_files ${SOURCE_FILES})