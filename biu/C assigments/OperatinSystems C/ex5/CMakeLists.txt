cmake_minimum_required(VERSION 3.8)
project(ex5)

set(CMAKE_C_STANDARD 99)

set(SOURCE_FILES ex52.c ex51.c)
add_executable(ex5 ${SOURCE_FILES})