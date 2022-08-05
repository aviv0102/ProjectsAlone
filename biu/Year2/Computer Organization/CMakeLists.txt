cmake_minimum_required(VERSION 3.8)
project(C_files)

set(CMAKE_C_STANDARD 99)

set(SOURCE_FILES main.c ex1.c ex1.h)
add_executable(C_files ${SOURCE_FILES})