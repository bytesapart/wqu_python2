Mini Project III - Readme
=========================
Python Version: 2.7

Author: Osama Iqbal

Date: 7th October, 2017

Description
----------------
This Python module takes a JSON file, which consists of
Nutrient Information from the USDA National Nutrient Database for Standard Reference (http://www.ars.usda.gov/ba/bhnrc/ndl)
and performs the following analysis:
* Classifies food groups according to the Amino Acids it provides.
* Gets Median of Zinc Content provided by all food groups and visualizes it in a barplot.

Platforms
----------------
This application is platform agnostic. This program was created using Anaconda2 v4.4.0. However, this should
work on any standard installations of python 2.7.x+. The program was developed on a flavour of Ubuntu 16.04 (elementary OS 0.4.1 Loki)
with Kernel version as Linux 4.10.0-33-generic. The code tends to be
cross-platform, however this has not been tested on a Windows or Mac
machine.

Installation
--------------
1. Install Python 2.7.0 - https://www.python.org/downloads/
2. Unzip files to local drive in desired folder (example: C:\MP3).
3. Open cmd prompt / shell.
4. Navigate to created folder.
5. Install requirements:
   1. Type “pip install -r requirements.txt” in cmd prompt/shell.
   2. Install all requirements.
6. To get the nutrient-db folder, perfrom **either** of the following:
   1. By downloading the zip:
       * Download the zip file from https://github.com/schirinos/nutrient-db and extract it in the MP3 folder
       * Navigate to the nutrients-db folder, and execute "nutrientdb.py -e > nutrients.json" in a cmd prompt window
   2. Programmatically via git:
       * Download and install git from https://git-scm.com/downloads
       * Navigate to MP3 folder, and type "git init"
       * After successful initialization, type "git submodule add https://github.com/schirinos/nutrient-db.git
       * Navigate to the nutrients-db folder, and execute "nutrientdb.py -e > nutrients.json" in a cmd prompt window
7. Run “OsamaIqbal_MiniProject3.py” by typing python OsamaIqbal_MiniProject3.py in command prompt/shell.

Main Requirements
---------------------------
Python version 2.7 - See https://www.continuum.io/downloads for installation.
pip - Is included with Python 2.7. See https://pip.pypa.io/en/stable/installing/ for more.


Pandas - see https://pandas.pydata.org/pandas-docs/stable/ for more information.
Seaborn - see https://seaborn.pydata.org/ for more information.

