# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.8

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
CMAKE_COMMAND = /home/magshimim/Desktop/clion-2017.2.3/bin/cmake/bin/cmake

# The command to remove a file.
RM = /home/magshimim/Desktop/clion-2017.2.3/bin/cmake/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/home/magshimim/Desktop/C files"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/home/magshimim/Desktop/C files/cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/C_files.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/C_files.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/C_files.dir/flags.make

CMakeFiles/C_files.dir/main.c.o: CMakeFiles/C_files.dir/flags.make
CMakeFiles/C_files.dir/main.c.o: ../main.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/home/magshimim/Desktop/C files/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/C_files.dir/main.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/C_files.dir/main.c.o   -c "/home/magshimim/Desktop/C files/main.c"

CMakeFiles/C_files.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/C_files.dir/main.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E "/home/magshimim/Desktop/C files/main.c" > CMakeFiles/C_files.dir/main.c.i

CMakeFiles/C_files.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/C_files.dir/main.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S "/home/magshimim/Desktop/C files/main.c" -o CMakeFiles/C_files.dir/main.c.s

CMakeFiles/C_files.dir/main.c.o.requires:

.PHONY : CMakeFiles/C_files.dir/main.c.o.requires

CMakeFiles/C_files.dir/main.c.o.provides: CMakeFiles/C_files.dir/main.c.o.requires
	$(MAKE) -f CMakeFiles/C_files.dir/build.make CMakeFiles/C_files.dir/main.c.o.provides.build
.PHONY : CMakeFiles/C_files.dir/main.c.o.provides

CMakeFiles/C_files.dir/main.c.o.provides.build: CMakeFiles/C_files.dir/main.c.o


CMakeFiles/C_files.dir/ex1.c.o: CMakeFiles/C_files.dir/flags.make
CMakeFiles/C_files.dir/ex1.c.o: ../ex1.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/home/magshimim/Desktop/C files/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/C_files.dir/ex1.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/C_files.dir/ex1.c.o   -c "/home/magshimim/Desktop/C files/ex1.c"

CMakeFiles/C_files.dir/ex1.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/C_files.dir/ex1.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E "/home/magshimim/Desktop/C files/ex1.c" > CMakeFiles/C_files.dir/ex1.c.i

CMakeFiles/C_files.dir/ex1.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/C_files.dir/ex1.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S "/home/magshimim/Desktop/C files/ex1.c" -o CMakeFiles/C_files.dir/ex1.c.s

CMakeFiles/C_files.dir/ex1.c.o.requires:

.PHONY : CMakeFiles/C_files.dir/ex1.c.o.requires

CMakeFiles/C_files.dir/ex1.c.o.provides: CMakeFiles/C_files.dir/ex1.c.o.requires
	$(MAKE) -f CMakeFiles/C_files.dir/build.make CMakeFiles/C_files.dir/ex1.c.o.provides.build
.PHONY : CMakeFiles/C_files.dir/ex1.c.o.provides

CMakeFiles/C_files.dir/ex1.c.o.provides.build: CMakeFiles/C_files.dir/ex1.c.o


# Object files for target C_files
C_files_OBJECTS = \
"CMakeFiles/C_files.dir/main.c.o" \
"CMakeFiles/C_files.dir/ex1.c.o"

# External object files for target C_files
C_files_EXTERNAL_OBJECTS =

C_files: CMakeFiles/C_files.dir/main.c.o
C_files: CMakeFiles/C_files.dir/ex1.c.o
C_files: CMakeFiles/C_files.dir/build.make
C_files: CMakeFiles/C_files.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/home/magshimim/Desktop/C files/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_3) "Linking C executable C_files"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/C_files.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/C_files.dir/build: C_files

.PHONY : CMakeFiles/C_files.dir/build

CMakeFiles/C_files.dir/requires: CMakeFiles/C_files.dir/main.c.o.requires
CMakeFiles/C_files.dir/requires: CMakeFiles/C_files.dir/ex1.c.o.requires

.PHONY : CMakeFiles/C_files.dir/requires

CMakeFiles/C_files.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/C_files.dir/cmake_clean.cmake
.PHONY : CMakeFiles/C_files.dir/clean

CMakeFiles/C_files.dir/depend:
	cd "/home/magshimim/Desktop/C files/cmake-build-debug" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/home/magshimim/Desktop/C files" "/home/magshimim/Desktop/C files" "/home/magshimim/Desktop/C files/cmake-build-debug" "/home/magshimim/Desktop/C files/cmake-build-debug" "/home/magshimim/Desktop/C files/cmake-build-debug/CMakeFiles/C_files.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/C_files.dir/depend

