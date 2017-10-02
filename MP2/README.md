## README

1. This program was created using Anaconda2 v4.4.0. However, this should
work on any standard installations of python 2.7.x+
2. To install the packages required to run the program, please find the
requirements.txt file. This file contains all the packages used by the
program. To install, do the following:

    **pip install -r requirements.txt**
3. The program was developed on a flavour of Ubuntu 16.04 (elementary OS 0.4.1 Loki)
with Kernel version as Linux 4.10.0-33-generic. The code tends to be
cross-platform, however this has not been tested on a Windows or Mac
machine.

4. The program is launched by typing the following on the command line:

   **python OsamaIqbal_MiniProject2.py**

5. The program accepts two country names from the following:
  * US
  * UK
  * France
  * Hongkong
  * Japan

    It then goes and loads the market (indices) data for the past 10 years, starting today,
  for these particular countries, finds its correlation and plots it as a heatmap.
  It errors out when one tries to load the same country twice

6. Another step performed by the script is to find the correlation between all the aforementioned indices
and plot them as a heatmap, just to give a better picture to the end user. Therefore, this last step can
be thought of a birds-eye view, while the two-market comparision phase can be considered as an isolation
view to get better sense of correlation between the indices

7. Sometimes, Yahoo Finance bugs out, and hence, cannot find the data for the Ticker/Index. Please re-run the
program again to get the data. This is a known issue