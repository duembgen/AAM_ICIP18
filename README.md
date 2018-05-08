# AAM - A SIMPLE ASSESSMENT METRIC OF AXIAL CHROMATIC ABERRATION

## Authors

- Majed El Helou
- Frederike Dümbgen
- Sabine Süsstrunk

Created on May 7, 2018.

## Description 

This repository contains the modules and scripts necessary to reproduce the results from the paper "AAM - A Simple Assessment Metric of Axial Chromatic Aberration". 

## Structure

### data/

Due to the size of the full experimental image data (12GB+), we only upload the extracted features. We provide data for two different camera settings: Canon EF 50mm f/2.5 (experiment ID 4) and Canon EF 50mm f/1.8 I (experiment ID 7).

For each camera X={4,7} (experiment IDs), we provide:

distances_X.mat
contains the distances of data capture for the experiment, these distances are the separation between the camera lens and the captured edge.

GaussStd2Color_X.mat
contains the estimated Gaussian standard deviation (the blur circle explained in the paper) at every distance, for the color channels.

GaussStd2Nir_X.mat
contains the estimated Gaussian standard deviation (the blur circle explained in the paper) at every distance, for the NIR channel.

### matlab/

This folder contains the Matlab script used to read the above data and create the plots shown in Figure 3 in the paper. 

### python/

This folder contains source code to compute the AAM metric. The code is best understood by looking at the provided notebook _demo_AAM.ipynb_. In particular, it contains the code necessary to reproduce the results in tables 1 and 2. 

## License 

This code is provided under the BSD license. 
