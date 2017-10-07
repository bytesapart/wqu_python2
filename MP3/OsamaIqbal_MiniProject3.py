"""
Created on Mon October 02 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Elementary OS with Ubuntu 16.04 variant, with a Linux 4.10.0-33-generic as the Kernel.

Project 3:
-- Steps:
1.Check out the nutrient-db python utility from GitHub from https://github.com/schirinos/nutrient-db.git
2.Run the main program with python nutrientdb.py -e > nutrients.json to convert the USDA data to JSON format. For further details, check https://github.com/schirinos/nutrient-db. You might have to install the python utility for MongoDB interface via pip install pymongo
3.Load the JSON dataset into Pandas dataframe using the built in python json class. Extract values of the following fields in to the dataframe - food names, group, id, and manufacturer
4.For the 'Amino Acids' nutrient group output a table showing the different constituents of the group (Alanine, Glycine, Histidine etc) and the foods in which they are present (Gelatins, dry powder, beluga, meat etc)
5.For all the different nutrient group (beef Products, Pork Products, dairy and egg products etc.) calculate the median Zinc content (median of the zinc content in all the foods that constitute the nutrient group)
6.Plot the distribution of median Zinc Content for different nutrient groups as a bar chart.
"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import logging  # Logging class for logging in the case of an error, makes debugging easier
import sys  # For gracefully notifying whether the script has ended or not
import os  # For joining of paths
import pandas as pd  # For calculating coefficient of correlation
import seaborn as sns  # For plotting the graphs


def main():
    """
    This function is called from the main block. The purpose of this function is to contain all the calls to
    business logic functions
    :return: int - Return 0 or 1, which is used as the exist code, depending on successful or erroneous flow
    """
    # Wrap in a try block so that we catch any exceptions thrown by other functions and return a 1 for graceful exit
    try:
        # ===== Step 1: Load the JSON dataset into Pandas dataframe =====
        # Load the DataFrame
        # NOTE: The default json method is called as an underlyer by read_json.
        raw_dataframe = pd.read_json(os.path.join('nutrient-db', 'nutrients.json'), lines=True)

        # ===== Step 2: Output Amino Acid and Food Group Table =====
        # List of Amino Acids - From Wikipedia (https://en.wikipedia.org/wiki/Amino_acid#Table_of_standard_amino_acid_abbreviations_and_properties)
        amino_dict = {
            "Alanine": [],
            "Arginine": [],
            "Asparagine": [],
            "Aspartic acid": [],
            "Cysteine": [],
            "Glutamic acid": [],
            "Glutamine": [],
            "Glycine": [],
            "Histidine": [],
            "Isoleucine": [],
            "Leucine": [],
            "Lysine": [],
            "Methionine": [],
            "Phenylalanine": [],
            "Proline": [],
            "Serine": [],
            "Threonine": [],
            "Tryptophan": [],
            "Tyrosine": [],
            "Valine": [],
        }
        amino_list = amino_dict.keys()
        # Create List of Food Groups
        for index in xrange(0, len(raw_dataframe)):
            food_item = raw_dataframe.iloc[index]['name']['long']
            if index % 1000 == 0:
                print('Processing Item between %s and %s out of %s' % (str(index), str(index + 1000), str(len(raw_dataframe))))
            for n_index in xrange(0,len(raw_dataframe.iloc[index]['nutrients'])):
                if raw_dataframe.iloc[index]['nutrients'][n_index]['name'] in amino_list:
                    if food_item in amino_dict[raw_dataframe.iloc[index]['nutrients'][n_index]['name']]:
                        continue
                    else:
                        amino_dict[raw_dataframe.iloc[index]['nutrients'][n_index]['name']].append(food_item)

        amino_dataframe = pd.DataFrame.from_dict(amino_dict, orient='index').transpose()
        print(amino_dataframe.head())
        print(amino_dataframe.tail())
        amino_dataframe.to_csv()

        # ===== Step 3: Output Bar Chart for Median of Zinc Content =====
        # Initialize an empty dictionary of unique 'group' elements, with key as group and value as a list
        group_dict = {key: [] for key in raw_dataframe['group'].unique()}
        group_list = group_dict.keys()

        for index in xrange(0, len(raw_dataframe)):
            group_item = raw_dataframe.iloc[index]['group']
            if index % 1000 == 0:
                print('Processing Item between %s and %s out of %s' % (str(index), str(index + 1000), str(len(raw_dataframe))))
            for n_index in xrange(0, len(raw_dataframe.iloc[index]['nutrients'])):
                if raw_dataframe.iloc[index]['nutrients'][n_index]['name'] == u'Zinc, Zn':
                    group_dict[group_item].append(raw_dataframe.iloc[index]['nutrients'][n_index]['value'])
                    break

        zinc_dataframe = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in group_dict.items()]))
        sns.barplot(data=zinc_dataframe, orient='h', ci=None)
        sns.plt.show()

    except BaseException, e:
        # Casting a wide net to catch all exceptions
        print('\n%s' % str(e))
        return 1


# Main block of the program. The program begins execution from this block when called from a cmd
if __name__ == '__main__':
    # Initialize Logger
    logging.basicConfig(format='%(asctime)s %(message)s: ')
    logging.info('Application Started')
    exit_code = main()
    logging.info('Application Ended')
    sys.exit(exit_code)
