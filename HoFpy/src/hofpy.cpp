#include <iostream>
#include "hofpy.h"
#include "HoF_Raster.hpp"


py::array_t<double> FHist(py::array_t<unsigned char>& imageA, py::array_t<unsigned char>& imageB, 
                          int numberDirections, bool useHybrid, double typeForce, double p0, double p1) {

    py::buffer_info bufA = imageA.request();
    py::buffer_info bufB = imageB.request();

    if (bufA.ndim != 2 || bufB.ndim != 2)
    {
        throw std::runtime_error("Image dimensions must be 2");
    }
    if ((bufA.shape[0] != bufB.shape[0]) || (bufA.shape[1] != bufB.shape[1]))
    {
        throw std::runtime_error("Images must have same shape");
    }

    auto histogram = py::array_t<double>(numberDirections + 1);

    py::buffer_info buf_histogram = histogram.request();

    unsigned char* ptrA = (unsigned char*)bufA.ptr;
    unsigned char* ptrB = (unsigned char*)bufB.ptr;
    double* ptr_histogram = (double*)buf_histogram.ptr;

    int M = bufA.shape[1];
    int N = bufA.shape[0];

    hof::HoF_Raster raster_obj;

    if (useHybrid) {
        raster_obj.F02Histogram_CrispRaster(ptr_histogram, numberDirections, ptrA, ptrB, M, N, p0, p1);
    }
    else {
        raster_obj.FRHistogram_CrispRaster(ptr_histogram, numberDirections, typeForce, ptrA, ptrB, M, N);
    }

    return histogram;
}


py::array_t<double> FRHist(py::array_t<unsigned char>& imageA, py::array_t<unsigned char>& imageB, double typeForce, int numberDirections) {
    return FHist(imageA, imageB, numberDirections, false, typeForce, 0.01, 3.0);
}

py::array_t<double> F0Hist(py::array_t<unsigned char>& imageA, py::array_t<unsigned char>& imageB, int numberDirections) {
    return FRHist(imageA, imageB, 0.0, numberDirections);
}

py::array_t<double> F2Hist(py::array_t<unsigned char>& imageA, py::array_t<unsigned char>& imageB, int numberDirections) {
    return FRHist(imageA, imageB, 2.0, numberDirections);
}

py::array_t<double> F02Hist(py::array_t<unsigned char>& imageA, py::array_t<unsigned char>& imageB, int numberDirections, double p0, double p1) {
    return FHist(imageA, imageB, numberDirections, true, 0.0, p0, p1);
}