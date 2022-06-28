/*
 * hof.cpp
 *
 *  Created on: Dec 2, 2010
 *      Author: Ozy_Sjahputera
 */

#include "HoF_Raster.hpp"

/*==============================================================================
   FRHistogram_CrispRaster | Computation of the Fr-histogram
                             associated with a pair of crisp objects
							 (raster data).
--------------------------------------------------------------------------------
   See hof.hpp for argument details.
==============================================================================*/

void hof::HoF_Raster::FRHistogram_CrispRaster (double *histogram,
							  	  int numberDirections, double typeForce,
							  	  unsigned char *imageA, unsigned char *imageB,
							  	  int width, int height)
{
	int methode;
	double p0, p1;

	if(fabs(typeForce)<=ZERO_FORCE_TYPE)
		methode=7;
	else
		methode=2;
	p0=0.01; /* doesn't matter here */
	p1=3.0;  /* doesn't matter here */

	if(width>=height)
		computeHistogram(histogram,
			             numberDirections,typeForce,
						 imageA,imageB,width,height,
						 methode,p0,p1);

	else
	{
		/* Currently, 'computeHistogram' assumes that
				      'width' is greater than or equal to 'height.
				      If this is not the case, the image is rotated
				      by 90 degree using the rotateImage() method.
				      The resulting histogram will be shifted to undo
				      the effect of image rotation.
		 */

		int i, j;
		unsigned char *rotImageA;
		unsigned char *rotImageB;
		double *auxHistogram;

		rotImageA=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		rotImageB=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		auxHistogram=(double *)malloc((numberDirections+1)*sizeof(double));

		/*
		std::vector<unsigned char> rotImageA(static_cast<unsigned int>(width*height),0);
		std::vector<unsigned char> rotImageB(static_cast<unsigned int>(width*height),0);
		std::vector<double> auxHistogram(static_cast<unsigned int>(numberDirections+1),0);
		*/

		rotateImage(imageA,width,height,rotImageA);
		rotateImage(imageB,width,height,rotImageB);
		computeHistogram(auxHistogram,
			             numberDirections,typeForce,
						 rotImageA,rotImageB,height,width,
						 methode,p0,p1);

		/*
		rotateImage(imageA,width,height,&rotImageA[0]);
		rotateImage(imageB,width,height,&rotImageB[0]);
		computeHistogram(&auxHistogram[0],
			             numberDirections,typeForce,
						 &rotImageA[0],&rotImageB[0],height,width,
						 methode,p0,p1);
		*/

		for(i=0,j=numberDirections/4;i<=numberDirections;i++,j++)
			histogram[i]=auxHistogram[j%numberDirections];

		free(rotImageA);
		free(rotImageB);
		free(auxHistogram);
	}
}

/*==============================================================================
   F02Histogram_CrispRaster | Computation of the histogram of hybrid forces
                              associated with a pair of crisp objects
							  (raster data).
--------------------------------------------------------------------------------
   See hof.hpp for argument details.
==============================================================================*/

void hof::HoF_Raster::F02Histogram_CrispRaster (double *histogram, int numberDirections,
									unsigned char *imageA, unsigned char *imageB,
									int width, int height, double p0, double p1)
{
	int methode;
	double typeForce;

	methode=3;
	typeForce=2.0; /* doesn't matter here */

	if(width>=height)
		computeHistogram(histogram,
			             numberDirections,typeForce,
						 imageA,imageB,width,height,
						 methode,p0,p1);
	else
	{
		/* Currently, 'computeHistogram' assumes that
				      'width' is greater than or equal to 'height.
				      If this is not the case, the image is rotated
				      by 90 degree using the rotateImage() method.
				      The resulting histogram will be shifted to undo
				      the effect of image rotation.
		 */

		int i, j;
		unsigned char *rotImageA;
		unsigned char *rotImageB;
		double *auxHistogram;

		rotImageA=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		rotImageB=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		auxHistogram=(double *)malloc((numberDirections+1)*sizeof(double));

		rotateImage(imageA,width,height,rotImageA);
		rotateImage(imageB,width,height,rotImageB);
		computeHistogram(auxHistogram,
			             numberDirections,typeForce,
						 rotImageA,rotImageB,height,width,
						 methode,p0,p1);

		for(i=0,j=numberDirections/4;i<=numberDirections;i++,j++)
			histogram[i]=auxHistogram[j%numberDirections];

		free(rotImageA);
		free(rotImageB);
		free(auxHistogram);
	}
}

/*==============================================================================
   FRHistogram_FuzzyRaster | Computation of the Fr-histogram
                             associated with a pair of fuzzy objects
							 (raster data).
--------------------------------------------------------------------------------
  See hof.hpp for argument details.
==============================================================================*/

void hof::HoF_Raster::FRHistogram_FuzzyRaster (double *histogram,
							  int numberDirections, double typeForce,
				 			  unsigned char *imageA, unsigned char *imageB,
							  int width, int height,
							  int fuzzyMethod) {

	double p0, p1;
	int methode;

	p0=0.01; /* doesn't matter here */
	p1=3.0;  /* doesn't matter here */

	switch(fuzzyMethod) {
		case SIMPLE_CUTS: /* only possibility right now */
		default: methode=8;
	}

	if(width>=height)
		computeHistogram(histogram,
			             numberDirections,typeForce,
						 imageA,imageB,width,height,
						 methode,p0,p1);

	else {
		/* Currently, 'computeHistogram' assumes that
				      'width' is greater than or equal to 'height.
				      If this is not the case, the image is rotated
				      by 90 degree using the rotateImage() method.
				      The resulting histogram will be shifted to undo
				      the effect of image rotation.
		 */
		int i, j;
		unsigned char *rotImageA;
		unsigned char *rotImageB;
		double *auxHistogram;

		rotImageA=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		rotImageB=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		auxHistogram=(double *)malloc((numberDirections+1)*sizeof(double));

		rotateImage(imageA,width,height,rotImageA);
		rotateImage(imageB,width,height,rotImageB);
		computeHistogram(auxHistogram,
			             numberDirections,typeForce,
						 rotImageA,rotImageB,height,width,
						 methode,p0,p1);

		for(i=0,j=numberDirections/4;i<=numberDirections;i++,j++)
			histogram[i]=auxHistogram[j%numberDirections];

		free(rotImageA);
		free(rotImageB);
		free(auxHistogram);
	}
}

/*==============================================================================
   F02Histogram_FuzzyRaster | Computation of the histogram of hybrid forces
                              associated with a pair of fuzzy objects
							  (raster data).
--------------------------------------------------------------------------------
   See hof.hpp for argument details.
==============================================================================*/

void hof::HoF_Raster::F02Histogram_FuzzyRaster (double *histogram, int numberDirections,
				 			   unsigned char *imageA, unsigned char *imageB,
							   int width, int height, double p0, double p1,
							   int fuzzyMethod) {

	int methode;
	double typeForce;

	typeForce=2.0; /* doesn't matter here */
	switch(fuzzyMethod) {
		case MIN_PIXELS: methode=4; break;
		case DOUBLE_CUTS: methode=6; break;
		case SIMPLE_CUTS: /* default value */
		default: methode=5; break;
	}

	if(width>=height)
		computeHistogram(histogram,
			             numberDirections,typeForce,
						 imageA,imageB,width,height,
						 methode,p0,p1);

	else { /* Currently, 'computeHistogram' assumes that
		      'width' is greater than or equal to 'height. */

		int i, j;
		unsigned char *rotImageA;
		unsigned char *rotImageB;
		double *auxHistogram;

		rotImageA=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		rotImageB=(unsigned char *)malloc(width*height*sizeof(unsigned char));
		auxHistogram=(double *)malloc((numberDirections+1)*sizeof(double));

		rotateImage(imageA,width,height,rotImageA);
		rotateImage(imageB,width,height,rotImageB);
		computeHistogram(auxHistogram,
			             numberDirections,typeForce,
						 rotImageA,rotImageB,height,width,
						 methode,p0,p1);

		for(i=0,j=numberDirections/4;i<=numberDirections;i++,j++)
			histogram[i]=auxHistogram[j%numberDirections];

		free(rotImageA);
		free(rotImageB);
		free(auxHistogram);
	}
}

/*======================================================================

     Function Options
     -------------------

     methode 7 --> F0-histogram  (any crisp objects)
     methode 8 --> F0-histogram  (fuzzy objects using SIMPLE_CUTS)
     methode 2 --> Fr-histogram  (disjoint crisp objects)
     methode 3 --> F02-histogram (crisp objects)
     methode 4 --> F02-histogram (fuzzy objects using MIN_PIXELS)
     methode 5 --> F02-histogram (fuzzy objects using SIMPLE_CUTS)
     methode 6 --> F02-histogram (fuzzy objects using DOUBLE_CUTS)

=====================================================================*/

void hof::HoF_Raster::computeHistogram (double *Histo, int Taille, double typeForce,
								unsigned char *Image_A, unsigned char *Image_B,
								int Xsize, int Ysize,
								int methode, double p0, double p1)
{
  /* Structure pour l'image */
  struct Adresse *Tab_A, *Tab_B;
  double *tab_ln;
  int *Chaine;
  int deb_chaine, case_dep, case_dep_neg, case_op, case_op_neg;
  int x1,x2,y1,y2;
  double Sum_LN_C1,Sum_LN_C2;
  double angle;
  double Pas_Angle;
  int tempCut[256], Cut[256];
  unsigned char *ptrA, *ptrB;

    for(x1=0;x1<256;x1++) tempCut[x1]=Cut[x1]=0;
	for(x1=0;x1<=Taille;x1++) Histo[x1]=0.0;
	x2=y2=y1=0;

	for(ptrA=Image_A,ptrB=Image_B,x1=Xsize*Ysize-1;x1>=0;x1--,ptrA++,ptrB++)
		if(*ptrA) {
			if(*ptrB) {
				y2+=(*ptrB); /* y2 is the area of B (times 255) */
				if(*ptrB<*ptrA) y1+=(*ptrB);
				else y1+=(*ptrA); /* y1 is the area of the intersection (times 255) */
			}
			x2+=(*ptrA); /* x2 is the area of A (times 255) */
			tempCut[static_cast<unsigned int>(*ptrA)]=1;
		} else if(*ptrB) {
			y2+=(*ptrB);
			tempCut[static_cast<unsigned int>(*ptrB)]=1;
		}

	for(x1=1;x1<256;x1++) if(tempCut[x1]) Cut[++Cut[0]]=x1;
	if(x2>y2) p0*=2*sqrt(y2/(PI*255));
	else p0*=2*sqrt(x2/(PI*255));
	p1*=2*sqrt(y1/(PI*255));
	if(p0<p1) p0=p1;

  Tab_A=(struct Adresse *)malloc(Ysize*sizeof(struct Adresse));
  Tab_B=(struct Adresse *)malloc(Ysize*sizeof(struct Adresse));

  Cree_Tab_Pointeur(Image_A, Tab_A, Xsize, Ysize);
  Cree_Tab_Pointeur(Image_B, Tab_B, Xsize, Ysize);

  /* Tableau de ln constante */
  tab_ln=(double *)malloc(Xsize*sizeof(double));

  Cree_Tab_ln(tab_ln, Xsize);

  Chaine=(int *)malloc((2*Xsize+1)*sizeof(int));

  Pas_Angle = 2*PI/Taille; /* PI/(Taille+1) */

  /************* Angle = 0 *****************/
  angle=0;
  x1=y1=y2=0;
  x2=Xsize;
  Bresenham_X(x1, y1, x2, y2, Xsize, Chaine);
  case_dep=Taille/2;
  case_op=0;
  case_dep_neg=Taille/2;
  case_op_neg=Taille;
  deb_chaine=1;

  Sum_LN_C1=Sum_LN_C2=0;

  for (y1=0;y1<Ysize;y1++)
    Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, 1, Xsize, Ysize,
	       case_dep, case_op, Chaine, deb_chaine, Cut, tab_ln, p0,
	       &Sum_LN_C1,&Sum_LN_C2,typeForce);

  if (methode>=3 && methode<=6) /* F02 (flou ou pas) */
    {
      Histo[case_dep] = Histo[case_dep]/(p0*p0) + Sum_LN_C1;
      Histo[case_op]  = Histo[case_op]/(p0*p0) + Sum_LN_C2;
    }

  /********** angle in [-pi/4,pi/4]-{0} ***************/
  /*      (projection suivant l'axe des X)            */

  angle+=Pas_Angle;
  x2 = Xsize + 200;

  while (angle<PI/4+0.0001) /* Arghhhhhh.... */
    {
      y2 = (int) (x2 * tan (angle));
      x1=0;
      y1=0;

      case_dep++;
      case_op++;

      /* On determine la droite a translater... */
      Bresenham_X(x1, y1, x2, y2, Xsize, Chaine);

      /* Vertical */
      deb_chaine=1;

      Sum_LN_C1=Sum_LN_C2=0;

      for (y1=0;y1<Ysize;y1++)
	Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, 1, Xsize, Ysize,
		   case_dep, case_op, Chaine, deb_chaine, Cut, tab_ln,
		   p0*cos(angle), &Sum_LN_C1, &Sum_LN_C2,typeForce);



      /* Horizontal */
      y1=0;
      while (x1<Xsize)
	{
	  x1+=Chaine[deb_chaine];
	  deb_chaine+=2;
	  Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, 1, Xsize, Ysize,
		     case_dep, case_op, Chaine, deb_chaine, Cut, tab_ln,
		     p0*cos(angle), &Sum_LN_C1, &Sum_LN_C2,typeForce);
	}

      if (methode>=3 && methode<=6) /* F02 (flou ou pas) */
	{
	  Histo[case_dep] = Histo[case_dep]/(cos(angle)*p0*p0) +
	    Sum_LN_C1*cos(angle);
	  Histo[case_op]  = Histo[case_op]/(cos(angle)*p0*p0) +
	    Sum_LN_C2*cos(angle);
	}

      /************* Angle negatif oppose *******/
      case_dep_neg--;
      case_op_neg--;

      /* Vertical */
      deb_chaine=1;

      Sum_LN_C1=Sum_LN_C2=0;

      x1=0;

      /*for (y1=0;y1<Ysize;y1++) // AR Ysize...
	 Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, -1, Xsize, -1,
		    case_op_neg, case_dep_neg, Chaine, deb_chaine, Cut,
		    tab_ln, p0*cos(angle), &Sum_LN_C1,&Sum_LN_C2,typeForce);

       // Horizontal
       deb_chaine=1;
       y1=Ysize-1;
       x1=Xsize;
        while (x1>0)
	{
	   x1-=Chaine[deb_chaine];
	   deb_chaine+=2;
	   Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, -1, -1, Ysize,
		      case_op_neg, case_dep_neg, Chaine, deb_chaine, Cut,
		      tab_ln, p0*cos(angle),&Sum_LN_C1,&Sum_LN_C2,typeForce);

	}
	*/
	if (case_dep_neg >= (Taille/2-Taille/8))
	{
          x1=0;
          for (y1=0;y1<Ysize;y1++) /* AR Ysize... */
	    Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, -1, Xsize, -1,
		    case_dep_neg, case_op_neg, Chaine, deb_chaine, Cut,
		    tab_ln, p0*cos(angle),&Sum_LN_C1, &Sum_LN_C2,typeForce);

	  /* Horizontal */
         deb_chaine=1;
         y1=Ysize-1;
         while (x1<Xsize)
	  {
	    x1+=Chaine[deb_chaine];
	    deb_chaine+=2;
	    Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, -1, Xsize, -1,
		     case_dep_neg, case_op_neg, Chaine, deb_chaine, Cut,
		     tab_ln, p0*cos(angle),&Sum_LN_C1, &Sum_LN_C2,typeForce);

	  }

         if (methode>=3 && methode<=6) /* F02 (flou ou pas) */
	  {
	    Histo[case_dep_neg] = Histo[case_dep_neg]/(cos(angle)*p0*p0) +
	      Sum_LN_C1*cos(angle);
	    Histo[case_op_neg]  = Histo[case_op_neg]/(cos(angle)*p0*p0) +
	      Sum_LN_C2*cos(angle);
	  }

          angle+=Pas_Angle;
         }
      else
        {
           x1=0;
           deb_chaine=1;

           for (y1=0;y1<Ysize;y1++) /* AR Ysize...*/
	     Calcul_Seg_X(Tab_A, Tab_B, Histo, methode, x1, y1, 1, -1, Xsize, -1,
			case_dep_neg, case_op_neg, Chaine, deb_chaine, Cut,
			tab_ln, p0*cos(angle), &Sum_LN_C1,
			&Sum_LN_C2, typeForce);

	   /* Horizontal */
          deb_chaine=1;
          y1=Ysize-1;
            while (x1<Xsize)
	   {
	     x1+=Chaine[deb_chaine];
	     deb_chaine+=2;
	     Calcul_Seg_X   (Tab_A, Tab_B, Histo, methode, x1, y1, 1, -1, Xsize,
			   -1, case_dep_neg, case_op_neg, Chaine, deb_chaine,
	       Cut, tab_ln, p0*cos(angle),&Sum_LN_C1,&Sum_LN_C2,typeForce);
	   }

          if (methode>=3 && methode<=6) /* F02 (flou ou pas) */
	  {
	    Histo[case_dep_neg] = Histo[case_dep_neg]/(cos(angle)*p0*p0) +
	      Sum_LN_C1*cos(angle);
	    Histo[case_op_neg]  = Histo[case_op_neg]/(cos(angle)*p0*p0) +
	      Sum_LN_C2*cos(angle);
	  }
	  angle+=Pas_Angle;
      }
}


  /*********** angle in ]-PI/2,-PI/4[ or ]PI/4,PI/2[ ***************/
  /*              (projection suivant l'axe des Y)                 */

  while (angle<PI/2-0.0001)   /* another Aaaarrggggghhh....... */
    {
      y2 = (int) (x2 * tan (angle));
      x1=0;
      y1=0;
      case_dep++;
      case_op++;

      /* On determine la droite a translater... */
        Bresenham_Y(x1, y1, x2, y2, Ysize, Chaine);

      /* Horizontal */
      Sum_LN_C1=Sum_LN_C2=0;

      deb_chaine=1;
      for (x1=0;x1<Xsize;x1++)
	Calcul_Seg_Y(Tab_A, Tab_B, Histo, methode, x1, y1, 1, 1, Xsize,
		     Ysize, case_dep, case_op, Chaine, deb_chaine, Cut, tab_ln,
		     p0*sin(angle), &Sum_LN_C1, &Sum_LN_C2, typeForce);

      /* Vertical */
      x1=0;
      y1=0;
      while (y1<Ysize)
	{
	  y1+=Chaine[deb_chaine];
	  deb_chaine+=2;
	  Calcul_Seg_Y(Tab_A, Tab_B, Histo, methode, x1, y1, 1, 1, Xsize,Ysize,
		       case_dep, case_op, Chaine, deb_chaine, Cut, tab_ln,
		       p0*sin(angle), &Sum_LN_C1, &Sum_LN_C2, typeForce);
	}

      if (methode>=3 && methode<=6) /* F02 (flou ou pas) */
	{
	  Histo[case_dep] = Histo[case_dep]/(sin(angle)*p0*p0) +
	    Sum_LN_C1*sin(angle);
	  Histo[case_op]  = Histo[case_op]/(sin(angle)*p0*p0) +
	    Sum_LN_C2*sin(angle);
	}

      /******** Partie oppose ***************/
      case_dep_neg--;
      case_op_neg--;

      /* Horizontal */
      Sum_LN_C1=Sum_LN_C2=0;
      deb_chaine=1;
      y1=0;  /*  y1=Ysize-1 est envisageable aussi... */

      for (x1=0;x1<Xsize;x1++)
	Calcul_Seg_Y(Tab_A, Tab_B, Histo, methode, x1, y1, -1, 1, -1, Ysize,
		     case_op_neg, case_dep_neg, Chaine, deb_chaine,Cut, tab_ln,
		     p0*sin(angle), &Sum_LN_C2, &Sum_LN_C1, typeForce);

      /* Vertical */
      x1=Xsize-1;
      y1=0;
      while (y1<Ysize)
	{
	  y1+=Chaine[deb_chaine];
	  deb_chaine+=2;
	  Calcul_Seg_Y(Tab_A, Tab_B, Histo, methode, x1, y1, -1, 1, -1, Ysize,
		       case_op_neg, case_dep_neg,Chaine,deb_chaine,Cut, tab_ln,
		       p0*sin(angle), &Sum_LN_C2, &Sum_LN_C1, typeForce);
	}

      if (methode>=3 && methode<=6) /* F02 (flou ou pas) */
	{
	  Histo[case_dep_neg] = Histo[case_dep_neg]/(sin(angle)*p0*p0) +
	    Sum_LN_C1*sin(angle);
	  Histo[case_op_neg]  = Histo[case_op_neg]/(sin(angle)*p0*p0) +
	    Sum_LN_C2*sin(angle);
	}

      angle+=Pas_Angle;
    }

  /************* Angle = PI/2 *****************/
  y1=x1=x2=0;
  y2=Ysize;
  case_dep++;
  case_op++;
  Bresenham_Y(x1, y1, x2, y2, Ysize, Chaine);

  deb_chaine=1;
  Sum_LN_C1=Sum_LN_C2=0;

  for (x1=0;x1<Xsize;x1++)
    Calcul_Seg_Y(Tab_A, Tab_B, Histo, methode, x1, y1, 1, 1, Xsize,
		 Ysize, case_dep, case_op, Chaine, deb_chaine,
		 Cut, tab_ln, p0, &Sum_LN_C1, &Sum_LN_C2, typeForce);

  if (methode>=3 && methode<=6) /* F02 (flou ou pas) */
    {
      Histo[case_dep] = Histo[case_dep]/(p0*p0) + Sum_LN_C1;
      Histo[case_op]  = Histo[case_op]/(p0*p0) + Sum_LN_C2;
    }

  /* Atribution de la valeur associee a -PI */
  Histo[Taille] += Histo[0];
  Histo[0] = Histo[Taille];

  if (methode<3 || methode>6) /* Fr quelconque (mais pas hybride) */
    Angle_Histo(Histo, Taille, typeForce);

  free(Tab_A);
  free(Tab_B);
  free(tab_ln);
  free(Chaine);
}


/*==============================================================
	Creation of a table ln of constants (fuzzy case).
==============================================================*/

void hof::HoF_Raster::Cree_Tab_ln (double *Tab, int Xsize)
{
  int i;
  for(i=1;i<Xsize;i++)
    *(Tab+i)=log((double)(i+1)*(i+1)/(i*(i+2)));
}

/*==============================================================
	Creation of a pointer list of the beginnning of each image line.
==============================================================*/

void hof::HoF_Raster::Cree_Tab_Pointeur (unsigned char *Image, struct Adresse *Tab, int Xsize, int Ysize)
{
  int i,j;
  i=Xsize*Ysize;
  for (j=0; j<Ysize; j++)
    {
      i-=Xsize;
      Tab[j].adr=Image+i;
    }
}

/*==============================================================
 Bresenham line along the X-axis and backup range in structure of the changes.
==============================================================*/

void hof::HoF_Raster::Bresenham_X (int x1, int y1, int x2, int y2, int Borne_X, int *chaine)
{
  int Tmp,e,change,x,y,Delta_x,Delta_y,s1,s2,x_prec,y_prec;
  x=x1;
  y=y1;
  Delta_x = abs(x2-x1);
  Delta_y = abs(y2-y1);
  s1 = sign<int>(x2-x1);
  s2 = sign<int>(y2-y1);
  x_prec=x;
  y_prec=y;
  chaine[0]=0;

  /* Permutation of delta_x and delta_y following the slope of seg. */
  if (Delta_y>Delta_x)
    {
      Tmp     = Delta_x;
      Delta_x = Delta_y;
      Delta_y = Tmp;
      change = 1;
    }
  else
    change = 0;
  /* Init. of e (case inters. with -1/2) */
  e=2*Delta_y-Delta_x;

  while (x < Borne_X)
    {
      while (e>=0)
	{
	  if (change)
	    {
	      x=x+s1;
	      chaine[0]++;
	      chaine[chaine[0]]=abs(y-y_prec)+1;
	      chaine[0]++;
	      chaine[chaine[0]]=1;
	      y_prec=y+1;
	    }
	  else
	    {
	      y=y+s2;
	      chaine[0]++;
	      chaine[chaine[0]]=abs(x-x_prec)+1;
	      chaine[0]++;
	      chaine[chaine[0]]=1;
	      x_prec=x+1;
	    }
	  e=e-2*Delta_x;
	}
      if (change)
	y=y+s2;
      else
	x=x+s1;
      e=e+2*Delta_y;
    }
  if (change)
    if (y_prec!=y)
      {
	chaine[0]++;
	chaine[chaine[0]]=abs(y-y_prec)+1;
      }
    else {}
  else
    if (x_prec!=x)
      {
	chaine[0]++;
	chaine[chaine[0]]=abs(x-x_prec)+1;
      }
}

/*==============================================================
 Same thing but following the y-axis.
==============================================================*/

void hof::HoF_Raster::Bresenham_Y (int x1, int y1, int x2, int y2, int Borne_Y, int *chaine)
{
  int Tmp,e,change,x,y,Delta_x,Delta_y,s1,s2,x_prec,y_prec;
  x=x1;
  y=y1;
  Delta_x = abs(x2-x1);
  Delta_y = abs(y2-y1);
  s1 = sign(x2-x1);
  s2 = sign(y2-y1);
  x_prec=x;
  y_prec=y;
  chaine[0]=0;

  /* Permutation de delta_x et delta_y suivant la pente de seg. */
  if (Delta_y>Delta_x)
    {
      Tmp     = Delta_x;
      Delta_x = Delta_y;
      Delta_y = Tmp;
      change = 1;
    }
  else
    change = 0;
  /* init. de e (cas inters. avec -1/2) */
  e=2*Delta_y-Delta_x;

  while (y < Borne_Y)
    {
      while (e>=0)
	{
	  if (change)
	    {
	      x=x+s1;
	      chaine[0]++;
	      chaine[chaine[0]]=abs(y-y_prec)+1;
	      chaine[0]++;
	      chaine[chaine[0]]=1;
	      y_prec=y+1;
	    }
	  else
	    {
	      y=y+s2;
	      chaine[0]++;
	      chaine[chaine[0]]=abs(x-x_prec)+1;
	      chaine[0]++;
	      chaine[chaine[0]]=1;
	      x_prec=x+1;
	    }
	  e=e-2*Delta_x;
	}
      if (change)
	y=y+s2;
      else
	x=x+s1;
      e=e+2*Delta_y;
    }
  if (change)
    if (y_prec!=y)
      {
	chaine[0]++;
	chaine[chaine[0]]=abs(y-y_prec)+1;
      }
    else {}
  else
    if (x_prec!=x)
      {
	chaine[0]++;
	chaine[chaine[0]]=abs(x-x_prec)+1;
      }
}

/*==============================================================
 On trace une ligne d'apres Bresenham.
 Decalage en X, et coupe de niveau.
==============================================================*/

struct hof::Segment* hof::HoF_Raster::ligne_x (struct Adresse *Tab, int x, int y,
					  	  	  	  int Borne_X, int Borne_Y,
					  	  	  	  int *Chaine, int deb,
					  	  	  	  int pas_x, int pas_y, int Cut)
{
  int i;
  int S;
  struct hof::Segment *Liste_Seg, *Deb_liste, *Seg;
  int paspasser; /* pas bo ! a optimiser (gestion diff. des TWL)... */
  int xtmp=0,ytmp=0, xprec=0, yprec=0;
  paspasser=1;
  S=0;
  Liste_Seg=Deb_liste=NULL;

  while (((x!=Borne_X)&&(y!=Borne_Y)) && (deb<=Chaine[0]))
    {
      i=0;
      while ((i<Chaine[deb])&&((x!=Borne_X)&&(y!=Borne_Y)))
	{
	  if (*(Tab[y].adr+x)>=Cut)
	    if (!S)
	      {
		S=1;
		xtmp=xprec=x;
		ytmp=yprec=y;
	      }
	    else {xprec=x; yprec=y;}
	  else
	    if (S)
	      {
		S=0;
		Seg=(struct hof::Segment *)malloc(sizeof(struct hof::Segment));
		Seg->x1=xtmp;
		Seg->y1=ytmp;
		Seg->x2=xprec;
		Seg->y2=yprec;
		if (paspasser==1)
		  {
		    Liste_Seg=Deb_liste=Seg;
		    Liste_Seg->suivant=NULL;
		    paspasser=0;
		  }
		else
		  {
		    Liste_Seg->suivant=Seg;
		    Liste_Seg=Liste_Seg->suivant;
		    Liste_Seg->suivant=NULL;
		  }
	      }
	  i++;
	  x+=pas_x;
	}
      deb++;
      y+=pas_y;
      deb++;
    }
  /* hof::Segment limitrophe a la fenetre */
 if (S)
    {
      Seg=(struct hof::Segment *)malloc(sizeof(struct hof::Segment));
      Seg->x1=xtmp;
      Seg->y1=ytmp;
      Seg->x2=xprec;
      Seg->y2=yprec;
      if (paspasser==1)
	{
	  Liste_Seg=Deb_liste=Seg;
	  Liste_Seg->suivant=NULL;
	  paspasser=0;
	}
      else
	{
	  Liste_Seg->suivant=Seg;
	  Liste_Seg=Liste_Seg->suivant;
	  Liste_Seg->suivant=NULL;
        }
    }
  return(Deb_liste);
}

/*==============================================================
 On trace une ligne.
 Cas flou, decalage en X, sauvegarde pt a pt.
==============================================================*/

struct hof::Segment* hof::HoF_Raster::ligne_x_floue (struct Adresse *Tab, int x, int y,
										int Borne_X, int Borne_Y,
										int *Chaine, int deb,
										int pas_x, int pas_y)
{
  int i;
  struct hof::Segment *Liste_Seg, *Deb_liste, *Seg;
  int paspasser; /* pas bo ! a optimiser... */
  paspasser=1;
  Liste_Seg=Deb_liste=NULL;

  while (((x!=Borne_X)&&(y!=Borne_Y)) && (deb<=Chaine[0]))
    {
      i=0;
      while ((i<Chaine[deb])&&((x!=Borne_X)&&(y!=Borne_Y)))
	{
	  if (*(Tab[y].adr+x)!=0)
	    {
	      Seg=(struct hof::Segment *)malloc(sizeof(struct hof::Segment));
	      Seg->x1=x;
	      Seg->y1=y;
	      Seg->x2=x;
	      Seg->y2=y;
	      Seg->Val=(int) *(Tab[y].adr+x);
		if (paspasser==1)
		  {
		    Liste_Seg=Deb_liste=Seg;
		    Liste_Seg->suivant=NULL;
		    paspasser=0;
		  }
		else
		  {
		    Liste_Seg->suivant=Seg;
		    Liste_Seg=Liste_Seg->suivant;
		    Liste_Seg->suivant=NULL;
		  }
	    }
	  i++;
	  x+=pas_x;
	}
      deb++;
      y+=pas_y;
      deb++;
    }
  return(Deb_liste);
}

/*==============================================================
 Idem mais decalage en Y.
==============================================================*/

struct hof::Segment* hof::HoF_Raster::ligne_y (struct Adresse *Tab, int x, int y,
					  	  	  	  int Borne_X, int Borne_Y,
					  	  	  	  int *Chaine, int deb,
					  	  	  	  int pas_x, int pas_y, int Cut)
{
  int i;
  int S=0;
  struct hof::Segment *Liste_Seg, *Deb_liste, *Seg;
  int paspasser; /* pas bo ! a optimiser... */
  int xtmp=0, ytmp=0, xprec=0, yprec=0;
  paspasser=1;
  Liste_Seg=Deb_liste=NULL;

  while (((x!=Borne_X)&&(y!=Borne_Y)) && (deb<=Chaine[0]))
    {
      i=0;
      while ((i<Chaine[deb])&&((x!=Borne_X)&&(y!=Borne_Y)))
	{
	  if (*(Tab[y].adr+x)>=Cut)
	    if (!S)
	      {
		S=1;
		xtmp=xprec=x;
		ytmp=yprec=y;
	      }
	    else {xprec=x;yprec=y;}
	  else
	    if (S)
	      {
		S=0;
		Seg=(struct hof::Segment *)malloc(sizeof(struct hof::Segment));
		/* permut. de x et y - projection suivant y - */
		Seg->x1=ytmp;
		Seg->y1=xtmp;
		Seg->x2=yprec;
		Seg->y2=xprec;
		if (paspasser==1)
		  {
		    Liste_Seg=Deb_liste=Seg;
		    Liste_Seg->suivant=NULL;
		    paspasser=0;
		  }
		else
		  {
		    Liste_Seg->suivant=Seg;
		    Liste_Seg=Liste_Seg->suivant;
		    Liste_Seg->suivant=NULL;
		  }
	      }
	  i++;
	  y+=pas_y;
	}
      deb++;
      x+=pas_x;
      deb++;
    }
  /* hof::Segment limitrophe a la fenetre */
  if (S)
    {
      Seg=(struct hof::Segment *)malloc(sizeof(struct hof::Segment));
      Seg->x1=ytmp;
      Seg->y1=xtmp;
      Seg->x2=yprec;
      Seg->y2=xprec;
      if (paspasser==1)
	{
	  Liste_Seg=Deb_liste=Seg;
	  Liste_Seg->suivant=NULL;
	  paspasser=0;
	}
      else
	{
	  Liste_Seg->suivant=Seg;
	  Liste_Seg=Liste_Seg->suivant;
	  Liste_Seg->suivant=NULL;
	}
    }
  return(Deb_liste);
}


/*==============================================================
 Cas flou, decalage en Y.
==============================================================*/

struct hof::Segment* hof::HoF_Raster::ligne_y_floue (struct Adresse *Tab, int x, int y,
						  	  	  	  	  int Borne_X, int Borne_Y,
						  	  	  	  	  int *Chaine, int deb,
						  	  	  	  	  int pas_x, int pas_y)
{
  int i;
  struct hof::Segment *Liste_Seg, *Deb_liste, *Seg;
  int paspasser; /* pas bo ! a optimiser... */
  paspasser=1;
  Liste_Seg=Deb_liste=NULL;

  while (((x!=Borne_X)&&(y!=Borne_Y)) && (deb<=Chaine[0]))
    {
      i=0;
      while ((i<Chaine[deb])&&((x!=Borne_X)&&(y!=Borne_Y)))
	{
	  if (*(Tab[y].adr+x)!=0)
	    {
	      Seg=(struct hof::Segment *)malloc(sizeof(struct hof::Segment));
	      /* permut. de x et y - projection suivant y - */
	      Seg->x1=y;
	      Seg->y1=x;
	      Seg->x2=y;
	      Seg->y2=x;
	      Seg->Val=(int) *(Tab[y].adr+x);
	      if (paspasser==1)
		{
		  Liste_Seg=Deb_liste=Seg;
		  Liste_Seg->suivant=NULL;
		  paspasser=0;
		}
	      else
		{
		  Liste_Seg->suivant=Seg;
		  Liste_Seg=Liste_Seg->suivant;
		  Liste_Seg->suivant=NULL;
		}
	    }
	  i++;
	  y+=pas_y;
	}
      deb++;
      x+=pas_x;
      deb++;
    }
  return(Deb_liste);
}

/*==============================================================
 Creation du Fr-histogramme, objets (nets) disjoints.
==============================================================*/

void hof::HoF_Raster::F0_disjoints (double *Histo,
				  	  	  	  struct hof::Segment *List_Seg_A,
				  	  	  	  struct hof::Segment *List_Seg_B,
				  	  	  	  int Case1, int Case2)
{
  double Som_Seg_Pos;
  double Som_Seg_Neg;
  double d1,d2;

  struct hof::Segment *Seg_A, *Seg_B, *pt_L_A, *pt_L_B;

  Som_Seg_Pos = Som_Seg_Neg = 0;

  pt_L_A=List_Seg_A;

  while (pt_L_A)
    {
      Seg_A=pt_L_A;
      d1=fabs(Seg_A->x2-Seg_A->x1)+1;
      /* premier segment */
      pt_L_B=List_Seg_B;
      while (pt_L_B)
	{
	  Seg_B=pt_L_B;
	  d2=fabs(Seg_B->x2-Seg_B->x1)+1;
	  if (Seg_A->x2 < Seg_B->x1) Som_Seg_Pos += d1*d2;
	  else Som_Seg_Neg += d1*d2;
	  pt_L_B=pt_L_B->suivant;
	}
      pt_L_A=pt_L_A->suivant;
    }
  /* Attribution de la somme a l'histo. */
  Histo[Case1] += Som_Seg_Pos;
  /* Angle oppose. */
  Histo[Case2] += Som_Seg_Neg;
}

/*============================================================*/

void hof::HoF_Raster::F1_disjoints (double *Histo,
      			  	  	  	  struct hof::Segment *List_Seg_A,
      			  	  	  	  struct hof::Segment *List_Seg_B,
      			  	  	  	  int Case1, int Case2)
{
  double Som_Seg_Pos;
  double Som_Seg_Neg;
  double d1,d2,D;

  struct hof::Segment *Seg_A, *Seg_B, *pt_L_A, *pt_L_B;

  Som_Seg_Pos = Som_Seg_Neg = 0;

  pt_L_A=List_Seg_A;

  while (pt_L_A)
    {
      Seg_A=pt_L_A;
      d1=fabs(Seg_A->x2-Seg_A->x1)+1;
      /* premier segment */
      pt_L_B=List_Seg_B;
      while (pt_L_B)
	{
	  Seg_B=pt_L_B;
	  d2=fabs(Seg_B->x2-Seg_B->x1)+1;
	  /* d'abord => Pas de chevauchement */
	  if (Seg_A->x2 < Seg_B->x1)
	    {
	      D=fabs(Seg_B->x1-Seg_A->x2)-1;
	      Som_Seg_Pos += D*log(D)+(D+d1+d2)*log(D+d1+d2)
		-(D+d1)*log(D+d1)-(D+d2)*log(D+d2);
	    }
	  else
	    {
	      D=fabs(Seg_B->x2-Seg_A->x1)-1;
	      Som_Seg_Neg += D*log(D)+(D+d1+d2)*log(D+d1+d2)
		-(D+d1)*log(D+d1)-(D+d2)*log(D+d2);
	    }
	  pt_L_B=pt_L_B->suivant;
	}
      pt_L_A=pt_L_A->suivant;
    }
  /* Attribution de la somme a l'histo. */
  Histo[Case1] += Som_Seg_Pos;
  /* Angle oppose. */
  Histo[Case2] += Som_Seg_Neg;
}


/*============================================================*/

void hof::HoF_Raster::F2_disjoints (double *Histo,
				  	  	  	  struct hof::Segment *List_Seg_A,
				  	  	  	  struct hof::Segment *List_Seg_B,
				  	  	  	  int Case1, int Case2)
{
  double Som_Seg_Pos;
  double Som_Seg_Neg;
  double d1,d2,D;

  struct hof::Segment *Seg_A, *Seg_B, *pt_L_A, *pt_L_B;

  Som_Seg_Pos = Som_Seg_Neg = 0;

  pt_L_A=List_Seg_A;

  while (pt_L_A)
    {
      Seg_A=pt_L_A;
      d1=fabs(Seg_A->x2-Seg_A->x1)+1;
      /* premier segment */
      pt_L_B=List_Seg_B;
      while (pt_L_B)
	{
	  Seg_B=pt_L_B;
	  d2=fabs(Seg_B->x2-Seg_B->x1)+1;
	  if (Seg_A->x2 < Seg_B->x1)
	    {
	      D=fabs(Seg_B->x1-Seg_A->x2)-1;
	      Som_Seg_Pos += log(((d1+D)*(D+d2))/(D*(d1+D+d2)));
	    }
	  else
	    {
	      D=fabs(Seg_B->x2-Seg_A->x1)-1;
	      Som_Seg_Neg += log(((d1+D)*(D+d2))/(D*(d1+D+d2)));
	    }
	  pt_L_B=pt_L_B->suivant;
	}
      pt_L_A=pt_L_A->suivant;
    }
  /* Attribution de la somme a l'histo. */
  Histo[Case1] += Som_Seg_Pos;
  /* Angle oppose. */
  Histo[Case2] += Som_Seg_Neg;
}

/* Par hypothese : r!=0 et r!=1 et r!=2.
==============================================================*/

void hof::HoF_Raster::Fr_disjoints (double *Histo,
				  	  	  	  struct hof::Segment *List_Seg_A,
				  	  	  	  struct hof::Segment *List_Seg_B,
				  	  	  	  int Case1, int Case2, double r)
{
  double Som_Seg_Pos;
  double Som_Seg_Neg;
  double d1,d2,D;

  struct hof::Segment *Seg_A, *Seg_B, *pt_L_A, *pt_L_B;

  Som_Seg_Pos = Som_Seg_Neg = 0;

  pt_L_A=List_Seg_A;

  while (pt_L_A)
    {
      Seg_A=pt_L_A;
      d1=fabs(Seg_A->x2-Seg_A->x1)+1;
      /* premier segment */
      pt_L_B=List_Seg_B;
      while (pt_L_B)
	{
	  Seg_B=pt_L_B;
	  d2=fabs(Seg_B->x2-Seg_B->x1)+1;
	  /* d'abord => Pas de chevauchement */
	  if ((Seg_A->x2==Seg_B->x2)&&(Seg_A->x1==Seg_B->x1))
	    {
	      D=fabs(Seg_A->x1-Seg_A->x2)+1;
	      Som_Seg_Neg += (1.0/((1-r)*(2-r)))*pow(D,2-r);
	      Som_Seg_Pos += (1.0/((1-r)*(2-r)))*pow(D,2-r);
	    }
	  else
	  if (Seg_A->x2 < Seg_B->x1)
	    {
	      D=fabs(Seg_B->x1-Seg_A->x2)-1;
	      Som_Seg_Pos += (1.0/((1-r)*(2-r)))*
		                 (pow(D,2-r)-pow(d1+D,2-r)-pow(d2+D,2-r)+pow(D+d1+d2,2-r));
	    }
	  else
	    {
	      D=fabs(Seg_B->x2-Seg_A->x1)-1;
	      Som_Seg_Neg += (1.0/((1-r)*(2-r)))*
		                 (pow(D,2-r)-pow(d1+D,2-r)-pow(d2+D,2-r)+pow(D+d1+d2,2-r));
	    }
	  pt_L_B=pt_L_B->suivant;
	}
      pt_L_A=pt_L_A->suivant;
    }
  /* Attribution de la somme a l'histo. */
  Histo[Case1] += Som_Seg_Pos;
  /* Angle oppose. */
  Histo[Case2] += Som_Seg_Neg;
}

/*==============================================================
 Relation "before" pour forces hybrides F02.
==============================================================*/

void hof::HoF_Raster::Before (double *H, double x, double y, double z,
			  	  	  double Y0, int Case, double Poids, double *Som_LN)
{
  if (Y0<=y)
    (*Som_LN) += log((x+y)*(y+z)/(y*(x+y+z))) * Poids; /* Y0^2 en fac... */
  /*H[Case].Val +=Y0*Y0*log((x+y)*(y+z)/(y*(x+y+z))) * Poids;  */
  else
    if (Y0>=x+y+z)
      H[Case] += x*z*Poids;
    else
      if ((Y0<=x+y)&&(Y0<=y+z))
	H[Case] += (Y0*Y0 * log((y+z)*(x+y)/(Y0*(x+y+z)))+
			(y-3*Y0)*(y-Y0)/2)*Poids;
      else
	if ((Y0>=x+y)&&(Y0<=y+z))
	  H[Case] += (Y0*Y0 * log((y+z)/(x+y+z))-(x/2+y-2*Y0)*x)*Poids;
	else
	  if (((Y0>=x+y)&&(Y0>=y+z))&&(Y0<=x+y+z))
	    H[Case] += (Y0*Y0 * log(Y0/(x+y+z))-
	      (x+y+z-3*Y0)*(x+y+z-Y0)/2+x*z)*Poids;
	  else
	    /*   if ((Y0>=x+y)&&(Y0>=y+z)) */
	    H[Case] += (Y0*Y0 * log((y+x)/(x+y+z))-(z/2+y-2*Y0)*z)*Poids;
}

/*==============================================================
 Relation "overlaps" pour forces hybrides F02.
==============================================================*/

void hof::HoF_Raster::Overlaps (double *H, double x, double y, double z,
			    		double Y0, int Case, double Poids)
{
  if ((Y0<=x+y)&&(Y0<=y+z))
    H[Case] += (Y0*Y0 * log((x+y)*(y+z)/(Y0*(x+y+z)))-
		    2*Y0*(y-3*Y0/4))*Poids;
  else
    if (((Y0<=x+y)&&(y+z<=Y0))&&(0<=y+z))
      H[Case] += (Y0*Y0 * log((y+x)/(x+y+z))+2*Y0*z-(y+z)*(y+z)/2)*Poids;
    else
      if (((x+y<=Y0)&&(Y0<=y+z))&&(0<=x+y))
	H[Case] += (Y0*Y0 * log((y+z)/(x+y+z))+2*Y0*x-(y+x)*(y+x)/2)*Poids;
      else
	if (((x+y<=Y0)&&(y+z<=Y0))&&(Y0<=x+y+z))
	  H[Case] += (Y0*Y0 * log(Y0/(x+y+z))-(x+y+z-3*Y0)*(x+y+z-Y0)/2+
			  x*z-y*y/2)*Poids;
	else
	  H[Case] += (x*z-y*y/2)*Poids;
}

/*==============================================================
 Relation "overlapped by" pour forces hybrides F02.
==============================================================*/

void hof::HoF_Raster::Overlapped_By (double *H, double x, double y, double z,
				   	   	   	   double Y0, int Case, double Poids)
{
  if (Y0>=x+y+z)
    H[Case] += ((x+y+z)*(x+y+z)/2)*Poids;
  else
    H[Case] += (Y0*Y0 * log(Y0/(x+y+z))+2*Y0*(x+y+z-3*Y0/4))*Poids;
}

/*==============================================================
 Relation "contains" pour forces hybrides F02.
==============================================================*/

void hof::HoF_Raster::Contains (double *H, double x, double y, double z,
			    		double Y0, int Case, double Poids)
{
  if (Y0<=x+y)
    H[Case] += (Y0*Y0 * log((y+x)/(x+y+z))+2*Y0*z)*Poids;
  else
    if ((y+x<=Y0)&&(Y0<=x+y+z))
      H[Case] += (Y0*Y0 * log(Y0/(x+y+z))+2*Y0*z-(x+y-3*Y0)
		      *(y+x-Y0)/2)*Poids;
    else
      /*if (x+y+z<=Y0)*/
      H[Case] += (z/2+y+x)*z*Poids;
}

/*==============================================================
 Relation "during" pour forces hybrides F02.
==============================================================*/

void hof::HoF_Raster::During (double *H, double x, double y, double z,
			  	  	  double Y0, int Case, double Poids)
{
  if (Y0<=z+y)
    H[Case] += (Y0*Y0 * log((y+z)/(x+y+z))+2*Y0*x)*Poids;
  else
    if ((y+z<=Y0)&&(Y0<=x+y+z))
      H[Case] += (Y0*Y0 * log(Y0/(x+y+z))+2*Y0*x-(z+y-3*Y0)*
		      (y+z-Y0)/2)*Poids;
    else
      /*if (x+y+z<=Y0)*/
      H[Case] += (x/2+y+z)*x*Poids;
}

/*==============================================================
 Forces hybrides F02, pour objets (nets) quelconques.
==============================================================*/

void hof::HoF_Raster::F02 (double *Histo,
		     	 	 struct hof::Segment *List_Seg_A,
		     	 	 struct hof::Segment *List_Seg_B,
		     	 	 int Case1, int Case2, double Poids, double Y0,
		     	 	 double *Sum_LN_C1, double *Sum_LN_C2)
{
  double x,y,z;
  struct hof::Segment *Seg_A, *Seg_B, *pt_L_A, *pt_L_B;

  pt_L_A=List_Seg_A;

  /* Attention a gerer avec les angles apres */
  while (pt_L_A)
    {
      /* premier segment */
      Seg_A=pt_L_A;

      pt_L_B=List_Seg_B;
      while (pt_L_B)
	{
	  Seg_B=pt_L_B;
	  /* d'abord Case 1 ... Optimisable */
	  if (Seg_A->x1 <= Seg_B->x2)
	    {
	      if (Seg_A->x2 < Seg_B->x1)
		{
		  x=fabs(Seg_A->x2-Seg_A->x1)+1;
		  z=fabs(Seg_B->x2-Seg_B->x1)+1;
		  y=fabs(Seg_B->x1-Seg_A->x2)-1;
		  Before(Histo, x, y, z, Y0, Case1, Poids, Sum_LN_C1 );
		}
	      else
		if ((Seg_A->x2<Seg_B->x2)&&(Seg_A->x1<Seg_B->x1))
		  {
		    x=fabs(Seg_A->x2-Seg_A->x1)+1;
		    z=fabs(Seg_B->x2-Seg_B->x1)+1;
		    y=-(fabs(Seg_A->x2-Seg_B->x1)+1);
		    Overlaps(Histo, x, y, z, Y0, Case1, Poids);
		  }
		else
		  if ((Seg_B->x1>Seg_A->x1)&&(Seg_A->x2>=Seg_B->x2))
		    {
		      x=fabs(Seg_B->x2-Seg_A->x1)+1;
		      z=fabs(Seg_B->x2-Seg_B->x1)+1;
		      y=-z;
		      Contains(Histo, x, y, z, Y0, Case1, Poids);
		    }
		  else
		    if ((Seg_B->x1<=Seg_A->x1)&&(Seg_B->x2>Seg_A->x2))
		      {
			x=fabs(Seg_A->x2-Seg_A->x1)+1;
			z=fabs(Seg_B->x2-Seg_A->x1)+1;
			y=-x;
			During(Histo, x, y, z, Y0, Case1, Poids);
		      }
		    else
		      {
			x=z=fabs(Seg_B->x2-Seg_A->x1)+1;
			y=-x;
			Overlapped_By(Histo, x, y, z, Y0, Case1, Poids);
		      }
	    }

	  /* droite dans l'autre sens attention au = */
	  if (Seg_B->x1 <= Seg_A->x2)
	    {
	      if (Seg_B->x2 < Seg_A->x1)
		{
		  x=fabs(Seg_A->x2-Seg_A->x1)+1;
		  z=fabs(Seg_B->x2-Seg_B->x1)+1;
		  y=fabs(Seg_A->x1-Seg_B->x2)-1;
		  Before(Histo, x, y, z, Y0, Case2, Poids, Sum_LN_C2);
		}
	      else
		if ((Seg_A->x2>Seg_B->x2)&&(Seg_A->x1>Seg_B->x1))
		  {
		    x=fabs(Seg_A->x2-Seg_A->x1)+1;
		    z=fabs(Seg_B->x2-Seg_B->x1)+1;
		    y=-(fabs(Seg_B->x2-Seg_A->x1)+1);
		    Overlaps(Histo, x, y, z, Y0, Case2, Poids);
		  }
		else
		  if ((Seg_A->x1>Seg_B->x1)&&(Seg_B->x2>=Seg_A->x2))
		    {
		      x=fabs(Seg_A->x2-Seg_A->x1)+1;
		      z=fabs(Seg_A->x2-Seg_B->x1)+1;
		      y=-x;
		      During(Histo, x, y, z, Y0, Case2, Poids);
		    }
		  else
		    if ((Seg_A->x1<=Seg_B->x1)&&(Seg_A->x2>Seg_B->x2))
		      {
			z=fabs(Seg_B->x2-Seg_B->x1)+1;
			x=fabs(Seg_A->x2-Seg_B->x1)+1;
			y=-z;
			Contains(Histo, x, y, z, Y0, Case2, Poids);
		      }
		    else
		      {
			x=z=fabs(Seg_A->x2-Seg_B->x1)+1;
			y=-z;
			Overlapped_By(Histo, x, y, z, Y0, Case2, Poids);
		      }
	    }

	  pt_L_B=pt_L_B->suivant;
	}
      pt_L_A=pt_L_A->suivant;
    }
}

/*==============================================================
 Forces constantes F0, pour objets (nets) quelconques.
==============================================================*/


void hof::HoF_Raster::F0 (double *Histo,
		    		struct hof::Segment *List_Seg_A, struct hof::Segment *List_Seg_B,
		    		int Case1, int Case2, double Poids)
{
  double x,y,z;
  struct hof::Segment *Seg_A, *Seg_B, *pt_L_A, *pt_L_B;

  pt_L_A=List_Seg_A;

  /* Attention a gerer avec les angles apres */
  while (pt_L_A)
    {
      Seg_A=pt_L_A;
      /* premier segment */
      pt_L_B=List_Seg_B;
      while (pt_L_B)
	{
	  Seg_B=pt_L_B;
	  /* d'abord Case 1 ... Optimisable */
	  if (Seg_A->x1 <= Seg_B->x2)
	    {
	      if (Seg_A->x2 < Seg_B->x1)
		{
		  x=fabs(Seg_A->x2-Seg_A->x1)+1;
		  z=fabs(Seg_B->x2-Seg_B->x1)+1;
		  Histo[Case1]+=Poids*x*z;
		}
	      else
		if ((Seg_A->x2<Seg_B->x2)&&(Seg_A->x1<Seg_B->x1))
		  {
		    x=fabs(Seg_A->x2-Seg_A->x1)+1;
		    z=fabs(Seg_B->x2-Seg_B->x1)+1;
		    y=-(fabs(Seg_A->x2-Seg_B->x1)+1);
		    Histo[Case1]+=Poids*(x*z-y*y/2);
		  }
		else
		  if ((Seg_B->x1>Seg_A->x1)&&(Seg_A->x2>=Seg_B->x2))
		    {
		      x=fabs(Seg_B->x2-Seg_A->x1)+1;
		      z=fabs(Seg_B->x2-Seg_B->x1)+1;
		      y=-z;
		      Histo[Case1]+=Poids*(x+y+z/2)*z;
		    }
		  else
		    if ((Seg_B->x1<=Seg_A->x1)&&(Seg_B->x2>Seg_A->x2))
		      {
			x=fabs(Seg_A->x2-Seg_A->x1)+1;
			z=fabs(Seg_B->x2-Seg_A->x1)+1;
			y=-x;
			Histo[Case1]+=Poids*(x/2+y+z)*x;
		      }
		    else
		      {
			x=z=fabs(Seg_B->x2-Seg_A->x1)+1;
			y=-x;
			Histo[Case1]+=Poids*(x+y+z)*(x+y+z)/2;
		      }
	    }

	  /* droite dans l'autre sens attention au = */
	  if (Seg_B->x1 <= Seg_A->x2)
	    {
	      if (Seg_B->x2 < Seg_A->x1)
		{
		  x=fabs(Seg_A->x2-Seg_A->x1)+1;
		  z=fabs(Seg_B->x2-Seg_B->x1)+1;
		  Histo[Case2]+=Poids*x*z;
		}
	      else
		if ((Seg_A->x2>Seg_B->x2)&&(Seg_A->x1>Seg_B->x1))
		  {
		    x=fabs(Seg_A->x2-Seg_A->x1)+1;
		    z=fabs(Seg_B->x2-Seg_B->x1)+1;
		    y=-(fabs(Seg_B->x2-Seg_A->x1)+1);
		    Histo[Case2]+=Poids*(x*z-y*y/2);
		  }
		else
		  if ((Seg_A->x1>Seg_B->x1)&&(Seg_B->x2>=Seg_A->x2))
		    {
		      x=fabs(Seg_A->x2-Seg_A->x1)+1;
		      z=fabs(Seg_A->x2-Seg_B->x1)+1;
		      y=-x;
		      Histo[Case2]+=Poids*(x/2+y+z)*x;
		    }
		  else
		    if ((Seg_A->x1<=Seg_B->x1)&&(Seg_A->x2>Seg_B->x2))
		      {
			z=fabs(Seg_B->x2-Seg_B->x1)+1;
			x=fabs(Seg_A->x2-Seg_B->x1)+1;
			y=-z;
			Histo[Case2]+=Poids*(x+y+z/2)*z;
		      }
		    else
		      {
			x=z=fabs(Seg_A->x2-Seg_B->x1)+1;
			y=-z;
			Histo[Case2]+=Poids*(x+y+z)*(x+y+z)/2;
		      }
	    }
	  pt_L_B=pt_L_B->suivant;
	}
      pt_L_A=pt_L_A->suivant;
    }
}

/*==============================================================
 Forces hybrides F02, pour objets flous quelconques.
 Methode MIN_PIXELS (traitement des paires de pixels,
 min des membership grades).
==============================================================*/

void hof::HoF_Raster::F02_flous (double *Histo,
			     struct hof::Segment *List_Seg_A, struct hof::Segment *List_Seg_B,
			     int Case1, int Case2, double *Tab, double Y0,
			     double *Sum_LN_C1, double *Sum_LN_C2)
{
  double x,z,y;

  struct hof::Segment *Seg_A, *Seg_B, *pt_L_A, *pt_L_B;

  pt_L_A=List_Seg_A;

  /* Attention a gerer avec les angles apres */
  while (pt_L_A)
    {
      Seg_A=pt_L_A;
      /* premier segment */
      pt_L_B=List_Seg_B;
      while (pt_L_B)
	{
	  Seg_B=pt_L_B;
	  /* d'abord => Pas de chevauchement */
	  if (Seg_A->x1 <= Seg_B->x1)
	    if (Seg_A->x2 < Seg_B->x1)
	      {
		y=fabs(Seg_B->x1-Seg_A->x2)-1;
		if (Y0<=y)
		  /*(*Sum_LN_C1) +=min255(Seg_A->Val,Seg_B->Val)*Tab[(int)y]; */
		  Histo[Case1]+=Y0*Y0*min255<double>(static_cast<double>(Seg_A->Val),static_cast<double>(Seg_B->Val))*Tab[static_cast<int>(y)];
	       	else
		  {
		    x=1;z=1;
		    Before(Histo, x, y, z, Y0, Case1,
			   min255(Seg_A->Val,Seg_B->Val), Sum_LN_C1);
		  }
		/* Temporaire
		//x=1;z=1;Histo[Case1]+=min255(Seg_A->Val,Seg_B->Val)*x*z; */
	      }
	    else
	      {
		x=z=1;y=-1;

		Overlapped_By(Histo, x, y, z, Y0, Case1, min255<double>(static_cast<double>(Seg_A->Val),static_cast<double>(Seg_B->Val)));
		Overlapped_By(Histo, x, y, z, Y0, Case2, min255<double>(static_cast<double>(Seg_A->Val),static_cast<double>(Seg_B->Val)));
		/* Histo[Case1]+=min255(Seg_A->Val,Seg_B->Val)*(x+y+z)*
		  (x+y+z)/2;
		Histo[Case2]+=min255(Seg_A->Val,Seg_B->Val)*(x+y+z)*
		  (x+y+z)/2; */
	      }
	  else
	    if (Seg_B->x2 <= Seg_A->x1)
	      {
		y=fabs(Seg_B->x1-Seg_A->x2)-1;
		if (Y0<=y)
 		  (*Sum_LN_C2)+=min255<double>(static_cast<double>(Seg_A->Val),static_cast<double>(Seg_B->Val))*Tab[static_cast<int>(y)];
		/* Histo[Case2]+=Y0*Y0*min255(Seg_A->Val,Seg_B->Val)*Tab[(int)y]; */
	       	else
		  {
		    x=1;z=1;
		    Before(Histo, x, y, z, Y0, Case2, min255<double>(static_cast<double>(Seg_A->Val),static_cast<double>(Seg_B->Val)), Sum_LN_C2);
		  }
		/*Temporaire
		// x=1;z;Histo[Case2]+=min255(Seg_A->Val,Seg_B->Val)*x*z; */
	      }
	    else
	      {
		/* cout << " on ne doit passer la... " << endl; */
		x=z=1;y=-1;
		Overlapped_By(Histo, x, y, z, Y0, Case1, min255<double>(static_cast<double>(Seg_A->Val),static_cast<double>(Seg_B->Val)));
		Overlapped_By(Histo, x, y, z, Y0, Case2, min255<double>(static_cast<double>(Seg_A->Val),static_cast<double>(Seg_B->Val)));
		/* Histo[Case1]+=min255(Seg_A->Val,Seg_B->Val)*(x+y+z)*
		  (x+y+z)/2;
		Histo[Case2]+=min255(Seg_A->Val,Seg_B->Val)*(x+y+z)*(x+y+z)/2;*/
	      }
	  pt_L_B=pt_L_B->suivant;
	}
      pt_L_A=pt_L_A->suivant;
    }
}

/*==============================================================
 Choix de la methode a appliquer.
==============================================================*/

void hof::HoF_Raster::Choix_Methode (double *Histo,
				   struct hof::Segment *List_Seg_A,
				   struct hof::Segment *List_Seg_B,
				   int Case1, int Case2, int methode, double Y0,
				   double *Sum_LN_C1, double *Sum_LN_C2, double r)
{

  switch (methode)
    {
    case 2:
	  if(fabs(r)<=ZERO_FORCE_TYPE)
		F0_disjoints(Histo, List_Seg_A, List_Seg_B, Case1, Case2);
	  else if(fabs(r-1)<=ZERO_FORCE_TYPE)
		F1_disjoints(Histo, List_Seg_A, List_Seg_B, Case1, Case2);
	  else if(fabs(r-2)<=ZERO_FORCE_TYPE)
		F2_disjoints(Histo, List_Seg_A, List_Seg_B, Case1, Case2);
	  else
		Fr_disjoints(Histo, List_Seg_A, List_Seg_B, Case1, Case2, r);
      break;
    case 3:
      F02(Histo, List_Seg_A, List_Seg_B, Case1, Case2, 1.0, Y0, Sum_LN_C1, Sum_LN_C2);
      break;
    case 7:
      F0(Histo, List_Seg_A, List_Seg_B, Case1, Case2, 1.0);
      break;
    }
}

/*==============================================================
 Fr-histogrammes avec r quelconque mais objets disjoints.
 Prise en consideration du facteur multiplicatif
 qui depend de l'angle.
==============================================================*/

void hof::HoF_Raster::Angle_Histo (double *Histo, int Taille, double r)
{
  int case_dep,case_op, case_dep_neg, case_op_neg;
  double angle;
  double Pas_Angle=2*PI/Taille;
  case_dep=case_dep_neg=Taille/2;
  case_op=0;
  case_op_neg=Taille;
  angle=Pas_Angle;
  /* Case concernee */
  case_dep++;
  case_op++;
  case_dep_neg--;
  case_op_neg--;

  if(fabs(r)<=ZERO_FORCE_TYPE)
    {
      while (angle<PI/4+0.0001)
	{
	  Histo[case_dep]/=cos(angle);
	  Histo[case_op]/=cos(angle);
	  Histo[case_dep_neg]/=cos(angle);
	  Histo[case_op_neg]/=cos(angle);
	  angle+=Pas_Angle;
	  case_dep++;
	  case_op++;
	  case_dep_neg--;
	  case_op_neg--;
	}
      while (angle<PI/2)
	{
	  Histo[case_dep]/=sin(angle);
	  Histo[case_op]/=sin(angle);
	  Histo[case_dep_neg]/=sin(angle);
	  Histo[case_op_neg]/=sin(angle);
	  angle+=Pas_Angle;
	  case_dep++;
	  case_op++;
	  case_dep_neg--;
	  case_op_neg--;
	}
    }
  else if(fabs(r-2)<=ZERO_FORCE_TYPE)
    {
      while (angle<PI/4+0.0001)
	{
	  Histo[case_dep]*=cos(angle);
	  Histo[case_op]*=cos(angle);
	  Histo[case_dep_neg]*=cos(angle);
	  Histo[case_op_neg]*=cos(angle);
	  angle+=Pas_Angle;
	  case_dep++;
	  case_op++;
	  case_dep_neg--;
	  case_op_neg--;
	}
      while (angle<PI/2)
	{
	  Histo[case_dep]*=sin(angle);
	  Histo[case_op]*=sin(angle);
	  Histo[case_dep_neg]*=sin(angle);
	  Histo[case_op_neg]*=sin(angle);
	  angle+=Pas_Angle;
	  case_dep++;
	  case_op++;
	  case_dep_neg--;
	  case_op_neg--;
	}
    }
  else if(fabs(r-1)>ZERO_FORCE_TYPE)
	{
      while (angle<PI/4+0.0001)
	{
	  Histo[case_dep]/=pow(cos(angle),1-r);
	  Histo[case_op]/=pow(cos(angle),1-r);
	  Histo[case_dep_neg]/=pow(cos(angle),1-r);
	  Histo[case_op_neg]/=pow(cos(angle),1-r);
	  angle+=Pas_Angle;
	  case_dep++;
	  case_op++;
	  case_dep_neg--;
	  case_op_neg--;
	}
      while (angle<PI/2)
	{
	  Histo[case_dep]/=pow(sin(angle),1-r);
	  Histo[case_op]/=pow(sin(angle),1-r);
	  Histo[case_dep_neg]/=pow(sin(angle),1-r);
	  Histo[case_op_neg]/=pow(sin(angle),1-r);
	  angle+=Pas_Angle;
	  case_dep++;
	  case_op++;
	  case_dep_neg--;
	  case_op_neg--;
	}
    }
}

/*==============================================================
 Determination des segments suivant droite en X.
==============================================================*/


void hof::HoF_Raster::Calcul_Seg_X (struct Adresse *Tab_A, struct Adresse *Tab_B,
			        double *Histo, int methode,
				  int x1, int y1, int pas_x, int pas_y,
				  int Xsize, int Ysize, int case_dep, int case_op,
				  int *Chaine, int deb_chaine, int Cut[255],
				  double *Tab_ln, double l,
				  double *Sum_LN_C1, double *Sum_LN_C2, double r)
{

  int i,j,Prec_Cut, Prec_Cut_A, Prec_Cut_B;
  struct hof::Segment *List_Seg_A, *List_Seg_B, *aux;

  switch (methode)
    {

      /* double sigma pixel a pixel */
    case 4: /* free a realiser ds le cas classique */
      /* double sommation : cas pixel */
      List_Seg_A=ligne_x_floue(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y);
      List_Seg_B=ligne_x_floue(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y);
      if(List_Seg_A && List_Seg_B)
		       F02_flous(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
				         Tab_ln, l, Sum_LN_C1, Sum_LN_C2);
	  while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	  while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
      break;

      /* Simple sommation cas flou */
    case 5:
      /* optimisable non trivial - gestion des segments */
      /* simple sommation (Style Khrisnapuram) - segment */
      i=1; Prec_Cut = 0;
      while (i<=Cut[0])
	{
	  List_Seg_A=ligne_x(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  List_Seg_B=ligne_x(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  if(List_Seg_A && List_Seg_B)
	    {
	      F02(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
		      (double) (Cut[i]-Prec_Cut)/255.0, l, Sum_LN_C1, Sum_LN_C2) ;
	      Prec_Cut = Cut[i];
	      i++;
	    }
	  else i=Cut[0]+1;
	  while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	  while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
	}
      break;

	  /* double sommation segment a segment */
    case 6:
      /* optimisable mais non trivial */
      /* double sommation (Style Dubois) - segment */
      i=1; Prec_Cut_A = 0;
      while (i<=Cut[0])
	{
	  j=1; Prec_Cut_B = 0;
	  List_Seg_A=ligne_x(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  while (j<=Cut[0])
	    {
	      List_Seg_B=ligne_x(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[j]);
	      if(List_Seg_A && List_Seg_B)
		{
		  F02(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
		     ((double) (Cut[i]-Prec_Cut_A)/255.0)*
		     ((double) (Cut[j]-Prec_Cut_B)/255.0), l,
		     Sum_LN_C1, Sum_LN_C2);
		  Prec_Cut_B = Cut[j];
		  j++;
		}
	      else  j=Cut[0]+1;
	      while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
	    }
	  if (!List_Seg_A)
	    i=Cut[0]+1;
	  else
	    { Prec_Cut_A = Cut[i]; i++;}
	  while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	}
      break;

    case 8:
      /* optimisable non trivial - gestion des segments */
      /* simple sommation (Style Khrisnapuram) - segment */
      i=1; Prec_Cut = 0;
      while (i<=Cut[0])
	{
	  List_Seg_A=ligne_x(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  List_Seg_B=ligne_x(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  if(List_Seg_A && List_Seg_B)
	    {
	      F0(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
		 (double) (Cut[i]-Prec_Cut)/255.0) ;
	      Prec_Cut = Cut[i];
	      i++;
	    }
	  else i=Cut[0]+1;
	  while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	  while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
	}
      break;

      /* cas classiques... */
    default:
		List_Seg_A=ligne_x(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,1);
		List_Seg_B=ligne_x(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,1);
		if(List_Seg_A && List_Seg_B)
				Choix_Methode(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
								methode, l, Sum_LN_C1, Sum_LN_C2, r);
		while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
		while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
    }

}

/*==============================================================
 Determination des segments suivant droite en Y.
==============================================================*/

void hof::HoF_Raster::Calcul_Seg_Y (struct Adresse *Tab_A, struct Adresse *Tab_B,
				  double *Histo, int methode,
				  int x1, int y1, int pas_x, int pas_y,
				  int Xsize, int Ysize, int case_dep, int case_op,
				  int *Chaine, int deb_chaine,
				  int Cut[255], double *Tab_ln, double l,
				  double *Sum_LN_C1, double *Sum_LN_C2, double r)
{
  int i,j,Prec_Cut, Prec_Cut_A, Prec_Cut_B;
  struct hof::Segment *List_Seg_A, *List_Seg_B, *aux;

  switch (methode)
    {
      /* double sigma pixel a pixel */
    case 4: /* free a realiser ds le cas classique */
      /* double sommation : cas pixel */
      List_Seg_A=ligne_y_floue(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y);
      List_Seg_B=ligne_y_floue(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y);
      if(List_Seg_A && List_Seg_B)
	        F02_flous(Histo, List_Seg_A, List_Seg_B, case_dep, case_op, Tab_ln, l,
		          Sum_LN_C1, Sum_LN_C2);
      while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	  while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
      break;

      /* cas flou simple sigma */
    case 5:
      /* optimisable non trivial - gestion des segments */
      /* simple sommation (Style Khrisnapuram) - segment */
      i=1; Prec_Cut = 0;
      while (i<=Cut[0])
	{
	  List_Seg_A=ligne_y(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  List_Seg_B=ligne_y(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  if(List_Seg_A && List_Seg_B)
	    {
	      F02(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
		 (double) (Cut[i]-Prec_Cut)/255.0, l, Sum_LN_C1, Sum_LN_C2);
	      Prec_Cut = Cut[i];
	      i++;
	    }
	  else i=Cut[0]+1;
 	  while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	  while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
	}
      break;

      /* cas flou double sigma */
    case 6:
      /* optimisable non trivial */
      /* double sommation (Style Dubois) - segment */
      i=1; Prec_Cut_A = 0;
      while (i<=Cut[0])
	{
	  List_Seg_A=ligne_y(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	  j=1; Prec_Cut_B = 0;
	  while (j<=Cut[0])
	    {
	      List_Seg_B=ligne_y(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[j]);
	      if(List_Seg_A && List_Seg_B)
		{
		  F02(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
		     ((double) (Cut[i]-Prec_Cut_A)/255.0)*
		     ((double) (Cut[j]-Prec_Cut_B)/255.0), l,
		     Sum_LN_C1, Sum_LN_C2);
		  Prec_Cut_B = Cut[j];
		  j++;
		}
	      else j=Cut[0]+1;
		  while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
	    }
	  if (!List_Seg_A)
	    i=Cut[0]+1;
	  else
	    { Prec_Cut_A = Cut[i]; i++;}
	  while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	}
      break;

   case 8:
     /* optimisable non trivial - gestion des segments */
     /* simple sommation (Style Khrisnapuram) - segment */
     i=1; Prec_Cut = 0;
     while (i<=Cut[0])
       {
	 List_Seg_A=ligne_y(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	 List_Seg_B=ligne_y(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,Cut[i]);
	 if(List_Seg_A && List_Seg_B)
	   {
	     F0(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
		(double) (Cut[i]-Prec_Cut)/255.0) ;
	     Prec_Cut = Cut[i];
	     i++;
	   }
	 else i=Cut[0]+1;
	 while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
	 while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
       }
     break;

     /* cas classiques */
    default:
		List_Seg_A=ligne_y(Tab_A,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,1);
		List_Seg_B=ligne_y(Tab_B,x1,y1,Xsize,Ysize,Chaine,deb_chaine,pas_x,pas_y,1);
		if(List_Seg_A && List_Seg_B)
				Choix_Methode(Histo, List_Seg_A, List_Seg_B, case_dep, case_op,
					methode, l, Sum_LN_C1, Sum_LN_C2, r);
		while(List_Seg_A) {aux=List_Seg_A; List_Seg_A=List_Seg_A->suivant; free(aux);}
		while(List_Seg_B) {aux=List_Seg_B; List_Seg_B=List_Seg_B->suivant; free(aux);}
    }

}

/*=====================================================================================
  rotateImage | Applies a 90 degrees angle rotation to the image (counterclockwise).
---------------------------------------------------------------------------------------
  in  | The image, its width and height.
  out | The rotated image.

  'rotateImage' assumes that 'width*height' bytes have been
   allocated for the rotated image. It does not check the arguments.
=====================================================================================*/

void hof::HoF_Raster::rotateImage (unsigned char *image, int width, int height,
				  unsigned char *rotatedImage)
{
	int x, y;
	unsigned char *ptr, *ptrI;

	ptr=rotatedImage;
	for(x=width-1,ptrI=image+x;x>=0;x--,ptrI=image+x)
		for(y=0;y<height;y++,ptrI+=width,ptr++) *ptr=*ptrI;
}

