cmake_minimum_required(VERSION 3.4...3.18)
project(python_accelerations)

add_subdirectory(extern/pybind11)
pybind11_add_module(py_vector cxx_src/py_vector.cpp)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(py_vector
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})