# Praesepe-Tails
This repository contains files used to create color vs period and color vs magnitude plots for selected stars. 

This code is licensed under the MIT License, copyright the authors. See the LICENSE file for details. 

## Files
* The Cumulative Praesepe Tails Table file is a csv containing quality ratings for the stars' measured periods, based on Causal Pixel Modeling (CPM) and Simple Aperture Photometry (SAP).
* The Final Table file includes all of the information about the tidal tail candidates necessary for the creation of plots.
* The Color vs Absolute Magnitude and Color vs Apparent Magnitude files contain scripts to create both plots. 
* The Period vs Color plot file creates a period color plot without any outlier adjustments. The period color plot with the outlier fix includes vertical lines to indicate the doubled periods of select outliers.
* the RNAAS_plot file combines the previous two files to create a single figure for the Research Note
* The copy_panels file retrieves visual inspection plots corresponding to the final period selections

## Figures
* The Panels/ subdirectory contains the visual inspection plots used to determine whether a period was present or not
