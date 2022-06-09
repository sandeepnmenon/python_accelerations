#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
namespace py = pybind11;

// Get sum of array elements
long long get_array_sum(const std::vector<long> array) {
    long long sum = 0;
    for (int i=0; i < array.size(); ++i ) {
        sum += array[i];
    }
    return sum;
}

PYBIND11_MODULE(py_vector, m) {
    m.def("get_array_sum", &get_array_sum, "Get sum of array elements", py::arg("array"));
}