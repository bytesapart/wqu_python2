Final Project - Readme
========================
Python Version: 2.7

Author: Osama Iqbal

Date: 24th October, 2017

Description
----------------
This Python program performs the following:
* Downloads 25 Years of data for Dow, Snp500, Nasdaq, DAX, FTSE, HANGSENG, KOSPI, NIFTY, and cleans them up, if necessary.
* Checks if prices follow a log-normal distribution. Reports deviation statistics.
* Checks whether returns follow a normal distribution, and reports deviation statistics.
* Uses Geometric Brownian Motion to predict the probability of a stock market crash similar to that in 1987.
* Plots charts that help identify "Fat Tails"
* Does fractal analytics, thereby trying to prove fractals are better predictors than log-normal distribution for prices

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
2. Unzip files to local drive in desired folder (example: C:\Final).
3. Open cmd prompt / shell.
4. Navigate to created folder.
5. Make sure 'pip' has been added to environment path. Type 'where pip' on a windows machine and 'which pip' on a Unix machine to be sure
6. Execute the following command `pip install requirements.txt`. This is done so that all the requirements are installed.
5. Run “Osama_Iqbal_Final_Project.py” by typing `python Osama_Iqbal_Final_Project.py` in command prompt/shell.

Main Requirements
---------------------------
Python version 2.7 - See https://www.continuum.io/downloads for installation.
pip - Is included with Python 2.7. See https://pip.pypa.io/en/stable/installing/ for more.


Pandas - see https://pandas.pydata.org/pandas-docs/stable/ for more information.

Fix Yahoo Finance - https://github.com/ranaroussi/fix-yahoo-finance for more information.

pandas-datareader - https://pandas-datareader.readthedocs.io/en/latest/ for more information.

scipy - https://www.scipy.org/docs.html for more information.

statsmodel - http://www.statsmodels.org/stable/index.html for more information.

Matplotlib - see https://matplotlib.org/ for more information.

