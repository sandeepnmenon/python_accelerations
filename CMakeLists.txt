cmake_minimum_required(VERSION 3.4...3.18)
project(python_accelerations)

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_subdirectory(extern/pybind11)
pybind11_add_module(py_vector cxx_src/py_vector.cpp)
pybind11_add_module(py_opencv cxx_src/py_opencv.cpp)

target_link_libraries( py_opencv PRIVATE ${OpenCV_LIBS} )
