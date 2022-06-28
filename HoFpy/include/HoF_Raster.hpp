/*
 * hof.hpp
 *
 *  Created on: Dec 2, 2010
 *      Author: Ozy_Sjahputera
 *
 *  This is a C++ class wrapper for Matsakis's original HoF functions for raster objects (v2.01, March 2001).
 */

#ifndef HOF_RASTER_HPP_
#define HOF_RASTER_HPP_

#include "constants.hpp"
#include <cmath>
#include <cstdlib>
#include <iostream>

namespace hof{

/*
 * Don't like these structs, but okay for now.
 */

struct Adresse
{
  unsigned char *adr;
};

/* Possibly used in a forward linked list */

struct Segment
{
  int x1;
  int y1;
  int x2;
  int y2;
  int Val;
  struct Segment *suivant; // pointing to next segment
};

/* Trying to collect all these HoF functions in a class */

class HoF_Raster{
public:
	HoF_Raster()
	{
		;
	}
	~HoF_Raster()
	{
		;
	}
	/*
	 * Histogram of Forces (HoF) concept is based on the following work:
	 *
	 [1] P. Matsakis, Relations spatiales structurelles et interpretation d'images,
		 Ph.D. dissertation, IRIT, Universite Paul Sabatier, Toulouse, France, 1998.
	 [2] P. Matsakis, L. Wendling, "A New Way to Represent the Relative Position of
	     Areal Objects", PAMI, vol. 21, no. 7, pp. 634-643, 1999.

	=======================================================================================
	 ARGUMENTS | These are the arguments accepted by the functions
		       | FRHistogram_CrispRaster(), FRHistogram_FuzzyRaster(),
			   | F02Histogram_CrispRaster(), F02Histogram_FuzzyRaster().
	---------------------------------------------------------------------------------------

	double typeForce
	----------------
	The type of force to be considered (i.e., any real number).
	0.0 for constant forces, 2.0 for gravitational forces, etc.

	int numberDirections
	--------------------
	It is a positive multiple of 4 (e.g., 16, 32, 64, 120, 180, 360).
	Forces will be considered in 'numberDirections' directions.

	double *histogram
	-----------------
	'numberDirections+1' values will be stored in the memory space pointed by 'histogram'.
	For instance, 'histogram[0]' will be the resultant of forces in direction 0 ("to the
	right"), and 'histogram[numberDirections]' the resultant of forces in direction
	2PI (i.e., equal to 'histogram[0]'). 'histogram[numberDirections/4]' will be the
	resultant of forces in direction PI/2 ("above") and 'histogram[numberDirections/2]'
	the resultant of forces in direction PI ("to the left").

	unsigned char *imageA
	---------------------
	The image that represents the argument object (sequential ordering, from top-left
	to bottom-right). Gray levels are values between 0 and 255. The value 0 means that
	the pixel does not belong at all to the object, and the value 255 that it totally
	belongs to the object. The object is fuzzy if there exists a pixel whose gray
	level g is such that 0<g<255. Otherwise, it is crisp.

	unsigned char *imageB
	---------------------
	The image that represents the referent object.

	int width, height
	-----------------
	The width and height of the two images.

	int fuzzyMethod
	---------------
	For the computation of histograms associated with fuzzy objects only.
	Either  1 (simple sum scheme, see Krishnapuram, Keller and Ma, 1993),
	        2 (double sum scheme, see Dubois and Jaulent, 1987),
		   -1 (equivalent to the simple sum scheme, but pairs
		       of pixels are processed instead of alpha-cuts),
		   -2 (equivalent to the double sum scheme).

	double p0, p1
	-------------
	For the computation of histograms of hybrid forces only. See [1].
	'p0' is related to the size of the smallest object, and 'p1' to the size of
	the intersection. If the objects are "not too close" (according to 'p0'), only
	gravitational forces are exerted. When the objects intersect, or are "very close",
	constant forces appear. We should have: 0<p0<p1. Typical values are p0=0.01 and p1=3.
	*/

	/*************************************
	 * Methods for handling crisp objects.
	 *************************************/

	/* F-r histogram, where r = typeForce (0=Constant, 2=Gravitational, etc.) */
	void FRHistogram_CrispRaster (double *histogram,
								  int numberDirections, double typeForce,
					 		 	  unsigned char *imageA, unsigned char *imageB,
								  int width, int height);

	/* F-hybrid histogram, common values for p0=0.01 and p1=3 */
	void F02Histogram_CrispRaster (double *histogram, int numberDirections,
					 			   unsigned char *imageA, unsigned char *imageB,
								   int width, int height, double p0, double p1);
	/*************************************
	 * Methods for handling fuzzy objects.
	 *************************************/

	/* F-r histogram, where r = typeForce (0=Constant, 2=Gravitational, etc.) */
	void FRHistogram_FuzzyRaster (double *histogram,
								  int numberDirections, double typeForce,
					 			  unsigned char *imageA, unsigned char *imageB,
								  int width, int height,
								  int fuzzyMethod);

	/* F-hybrid histogram, common values for p0=0.01 and p1=3 */
	void F02Histogram_FuzzyRaster (double *histogram, int numberDirections,
					 			   unsigned char *imageA, unsigned char *imageB,
								   int width, int height, double p0, double p1,
								   int fuzzyMethod);

private:
	void rotateImage (unsigned char *image, int width, int height, unsigned char *rotatedImage);

	void Cree_Tab_Pointeur (unsigned char *Image, struct Adresse *Tab,int Xsize, int Ysize);
	void Cree_Tab_ln (double *Tab, int Xsize);
	/* Bresenham methods */
	void Bresenham_X (int x1, int y1, int x2, int y2,int Borne_X, int *chaine);
	void Bresenham_Y (int x1, int y1, int x2, int y2,int Borne_Y, int *chaine);
	/* Line segments */
	struct Segment *ligne_x (struct Adresse *Tab, int x, int y,
						  	  int Borne_X, int Borne_Y,
						  	  int *Chaine, int deb,
						  	  int pas_x, int pas_y, int Cut);
	struct Segment *ligne_x_floue (struct Adresse *Tab, int x, int y,
							  int Borne_X, int Borne_Y,
							  int *Chaine, int deb,
							  int pas_x, int pas_y);
	struct Segment *ligne_y (struct Adresse *Tab, int x, int y,
						  int Borne_X, int Borne_Y,
						  int *Chaine, int deb,
						  int pas_x, int pas_y, int Cut);
	struct Segment *ligne_y_floue (struct Adresse *Tab, int x, int y,
							  int Borne_X, int Borne_Y,
							  int *Chaine, int deb,
							  int pas_x, int pas_y);

	void F0_disjoints (double *Histo,
					  struct Segment *List_Seg_A,
					  struct Segment *List_Seg_B,
					  int Case1, int Case2);
	void F1_disjoints (double *Histo,
	      			  struct Segment *List_Seg_A,
					  struct Segment *List_Seg_B,
					  int Case1, int Case2);
	void F2_disjoints (double *Histo,
					  struct Segment *List_Seg_A,
					  struct Segment *List_Seg_B,
					  int Case1, int Case2);
	void Fr_disjoints (double *Histo,
					  struct Segment *List_Seg_A,
					  struct Segment *List_Seg_B,
					  int Case1, int Case2, double r);

	void Before (double *H, double x, double y, double z, double Y0, int Case, double Poids, double *Som_LN);
	void Overlaps (double *H, double x, double y, double z, double Y0, int Case, double Poids);
	void Overlapped_By (double *H, double x, double y, double z, double Y0, int Case, double Poids);
	void Contains (double *H, double x, double y, double z, double Y0, int Case, double Poids);
	void During (double *H, double x, double y, double z, double Y0, int Case, double Poids);

	void F02 (double *Histo,
			     struct Segment *List_Seg_A,
			     struct Segment *List_Seg_B,
			     int Case1, int Case2, double Poids, double Y0,
			     double *Sum_LN_C1, double *Sum_LN_C2);
	void F0 (double *Histo,
			    struct Segment *List_Seg_A, struct Segment *List_Seg_B,
			    int Case1, int Case2, double Poids);
	void F02_flous (double *Histo,
				     struct Segment *List_Seg_A, struct Segment *List_Seg_B,
				     int Case1, int Case2, double *Tab, double Y0,
				     double *Sum_LN_C1, double *Sum_LN_C2);

	void Choix_Methode (double *Histo,
					   struct Segment *List_Seg_A,
					   struct Segment *List_Seg_B,
					   int Case1, int Case2, int methode, double Y0,
					   double *Sum_LN_C1, double *Sum_LN_C2, double r);

	void Angle_Histo (double *Histo, int Taille, double r);

	void Calcul_Seg_X (struct Adresse *Tab_A, struct Adresse *Tab_B,
				        double *Histo, int methode,
					  int x1, int y1, int pas_x, int pas_y,
					  int Xsize, int Ysize, int case_dep, int case_op,
					  int *Chaine, int deb_chaine, int Cut[255],
					  double *Tab_ln, double l,
					  double *Sum_LN_C1, double *Sum_LN_C2, double r);

	void Calcul_Seg_Y (struct Adresse *Tab_A, struct Adresse *Tab_B,
					  double *Histo, int methode,
					  int x1, int y1, int pas_x, int pas_y,
					  int Xsize, int Ysize, int case_dep, int case_op,
					  int *Chaine, int deb_chaine,
					  int Cut[255], double *Tab_ln, double l,
					  double *Sum_LN_C1, double *Sum_LN_C2, double r);

	void computeHistogram (double *Histo, int Taille, double typeForce,
						unsigned char *Image_A, unsigned char *Image_B,
					      int Xsize, int Ysize,
						int methode, double p0, double p1);

	template<typename T>
	T  sign(T x);

	template<typename T>
	T min255(T x, T y);

private:


};

template<typename T>
T  HoF_Raster::sign(T x)
{
	return (x == static_cast<T>(0) ? static_cast<T>(0) : ( x < static_cast<T>(0) ? static_cast<T>(-1) : static_cast<T>(1) ) );
}

template<typename T>
T HoF_Raster::min255(T x, T y)
{
	return ( x < y ? static_cast<T>(static_cast<double>(x)/255.0) : static_cast<T>( static_cast<double>(y) /255.0 ) );
}


} // namespace hof

#endif /* HOF_HPP_ */
