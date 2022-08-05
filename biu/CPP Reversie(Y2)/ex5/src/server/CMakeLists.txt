cmake_minimum_required(VERSION 3.8)
project(server)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        Command.h
        CommandManeger.cpp
        CommandManeger.h
        GameMap.cpp
        GameMap.h
        GameRoom.cpp
        GameRoom.h
        JoinGame.cpp
        JoinGame.h
        ListGames.cpp
        ListGames.h
        main.cpp
        Server.cpp
        Server.h
        StartGame.cpp
        StartGame.h)

add_executable(server ${SOURCE_FILES})