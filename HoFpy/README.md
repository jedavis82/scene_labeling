# HoFpy

This package provides Python bindings for the Histogram of Forces code written by Pascal Matsakis, with a C++ wrapper provided by Ozy Sjahputera. The code is based on the following work:

> [1] P. Matsakis, Relations spatiales structurelles et interpretation d'images, Ph.D. dissertation, IRIT, Universite Paul Sabatier, Toulouse, France, 1998.

> [2] P. Matsakis, L. Wendling, "A New Way to Represent the Relative Position of Areal Objects", PAMI, vol. 21, no. 7, pp. 634-643, 1999.

Python bindings are provided only for the crisp raster implementation using NumPy arrays. The following functions are available:

__Histogram of Constant Forces (F0)__
```
F0Hist(imageA: numpy.ndarray[numpy.uint8], imageB: numpy.ndarray[numpy.uint8], numberDirections: int = 180) -> numpy.ndarray[numpy.float64]
```

__Histogram of Gravitational Forces (F2)__
```
F2Hist(imageA: numpy.ndarray[numpy.uint8], imageB: numpy.ndarray[numpy.uint8], numberDirections: int = 180) -> numpy.ndarray[numpy.float64]
```

__General Histogram of Forces (FR)__
```
FRHist(imageA: numpy.ndarray[numpy.uint8], imageB: numpy.ndarray[numpy.uint8], typeForce: float, numberDirections: int = 180) -> numpy.ndarray[numpy.float64]
```

__Histogram of Hybrid Forces (F02)__
```
F02Hist(imageA: numpy.ndarray[numpy.uint8], imageB: numpy.ndarray[numpy.uint8], numberDirections: int = 180, p0: float = 0.01, p1: float = 3.0) -> numpy.ndarray[numpy.float64]
```

## Installation

Clone the repo to a local directory and run the following commands to build and install the `hofpy` package.

```
pip install -r requirements.txt
pip install .
```

## Usage

An example script is provided in `test.py`.