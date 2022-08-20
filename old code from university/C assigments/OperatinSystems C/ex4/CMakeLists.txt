cmake_minimum_required(VERSION 3.8)
project(ex4)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pthread")
set(SOURCE_FILES main.c osqueue.c threadPool.c)
add_executable(ex4 ${SOURCE_FILES})