# AAM - AN ASSESSMENT METRIC OF AXIAL CHROMATIC ABERRATION

## Authors

- Majed El Helou
- Frederike Dümbgen
- Sabine Süsstrunk

Created on May 7, 2018.

## Description 

This repository contains the modules and scripts necessary to reproduce the results from the paper "AAM - A Simple Assessment Metric of Axial Chromatic Aberration". 

## Structure

- matlab

Due to the size of the full experimental image data (12GB+), we only upload the extracted features.

For X={4,7} (experiment IDs):


distances_X.mat
contains the distances of data capture for the experiment, these distances are the separation between the camera lens and the captured edge.


GaussStd2Color_X.mat
contains the estimated Gaussian standard deviation (the blur circle explained in the paper) at every distance, for the color channels.


GaussStd2Nir_X.mat
contains the estimated Gaussian standard deviation (the blur circle explained in the paper) at every distance, for the NIR channel.


makeFigs.m
reads the data and generates the 2 figures presented in the paper.



- python

