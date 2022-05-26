#include <opencv2/opencv.hpp>
#include <string>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
namespace py = pybind11;
using namespace std;

// Checkerborad detection for given file
py::array get_checkerboard_corners(const string image_file_path, int num_columns, int num_rows)
{
    // Read image
    cv::Mat image = cv::imread(image_file_path, cv::IMREAD_COLOR);
    if (image.empty())
    {
        cout << "Image not found" << endl;
        return py::array();
    }

    // Convert to grayscale
    cv::Mat gray_image;
    cv::cvtColor(image, gray_image, cv::COLOR_BGR2GRAY);

    // Detect checkerboard
    cv::Size board_size(num_columns, num_rows);
    vector<cv::Point2f> corners;
    bool found = cv::findChessboardCorners(gray_image, board_size, corners, cv::CALIB_CB_ADAPTIVE_THRESH | cv::CALIB_CB_NORMALIZE_IMAGE);

    // If checkerboard is found, refine the corner locations
    if (found)
    {
        cv::cornerSubPix(gray_image, corners, cv::Size(11, 11), cv::Size(-1, -1), cv::TermCriteria(cv::TermCriteria::EPS + cv::TermCriteria::COUNT, 30, 0.1));
    
        // Convert corners to vector array
        vector<vector<float>> corners_vector;
        for (int i=0; i < corners.size(); ++i)
        {
            vector<float> corner_vector;
            corner_vector.push_back(corners[i].x);
            corner_vector.push_back(corners[i].y);
            corners_vector.push_back(corner_vector);
        }

        return py::cast(corners_vector);
    }
    else
    {
        return py::array_t<float>();
    }
}

PYBIND11_MODULE(py_opencv, m)
{
    m.def("get_checkerboard_corners", &get_checkerboard_corners, "Get checkerboard corners", py::arg("image_file_path"), py::arg("num_columns"), py::arg("num_rows"));
}