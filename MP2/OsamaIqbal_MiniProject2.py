"""
Created on Mon October 02 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Elementary OS with Ubuntu 16.04 variant, with a Linux 4.10.0-33-generic as the Kernel.

Project 1:
-- Steps:
1.	Write a python program that prompts the user to choose any five stock exchanges of the world (whose data is available on Google Finance, Yahoo Finance, Quandl, CityFALCON, or another similar source.
2.	For each such market, let the program automatically choose the relevant Market Index (say S&P500 for USA, CNXNIFTY for India, HANGSENG Index for Hong Kong etc)
3.	Download data for the last 10 years for each of the Indices.
4.	Calculate Correlation Coefficients of monthly returns between each pair of indices
5.  Plot the results in a suitable graphical format that represents the trends in the data and their interdependence
"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import logging  # Logging class for logging in the case of an error, makes debugging easier
import sys  # For gracefully notifying whether the script has ended or not
from pandas_datareader import data as pdr  # The pandas Data Module used for fetching data from a Data Source
import pandas as pd  # For calculating coefficient of correlation
import warnings  # For removing Deprecation Warning w.r.t. Yahoo Finance Fix
import datetime  # For setting correct dates from today up to a year in the past to get data from YF
import time
import numpy as np  # For numerical operations
import seaborn as sns  # For plotting the graphs

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fix_yahoo_finance import pdr_override  # For overriding Pandas DataFrame Reader not connecting to YF


def yahoo_finance_bridge():
    """
        This function fixes problems w.r.t. fetching data from Yahoo Finance
        :return: None
        """
    logging.info('Correcting Yahoo Finance')
    pdr_override()


def get_countries_from_user():
    """
    This function prompts the user to enter markets that it needs to load. It then returns a dictionary consisting
    of the values of the markets that the user needs to load
    :return: dictionary: Returns a dictionary consisting of the markets that the user wants to load
    """
    # Create an empty dictionary for mapping the markets that need to be loaded
    countires_to_load = {'CountryOne': None, 'CountryTwo': None}
    # Prompt the user to enter a market for the first market
    countires_to_load['CountryOne'] = str(raw_input(
        'Please enter the first market to load. '
        'Valid values are US, UK, France, HongKong, Japan. (case insensitive):')).lower()
    if countires_to_load['CountryOne'].lower() not in ['us', 'uk', 'france', 'hongkong', 'japan']:
        raise ValueError('Market is not US, UK, France, HongKong or Japan. Please enter a valid Market.')
        # Prompt the user to enter a market for the first market
    countires_to_load['CountryTwo'] = str(raw_input(
        'Please enter the second market to load. '
        'Valid values are US, UK, France, HongKong, Japan. (case insensitive):')).lower()
    if countires_to_load['CountryTwo'].lower() not in ['us', 'uk', 'france', 'hongkong', 'japan']:
        raise ValueError('Market is not US, UK, france, HongKong or Japan. Please enter a valid Market.')

    return countires_to_load


def get_market_map():
    """
    Returns a map of countries to their respective markets/indices
    :return: dictionary
    """
    return {
        'us': '^GSPC',
        'uk': '^FTSE',
        'france': '^FCHI',
        'hongkong': '^HSI',
        'japan': '^N225'
    }


def get_market_names_from_countries(countries):
    """
    This function returns a dictionary containing a map of the country names to the markets that need to be loaded
    :param countries: Dictionary containing the countries to load
    :return: dictionary: A dictionary consisting of the markets to load
    """
    # Get the markets map
    markets_map = get_market_map()

    # Create an empty dictionary to return
    markets_from_countries = {}

    for key, value in countries.items():
        if value in markets_map:
            markets_from_countries[value] = markets_map[value]

    # Return the map
    if len(markets_from_countries) != 2:
        raise ValueError(
            'Only 2 different markets can be loaded. The input to the script contained a redundant market.')
    else:
        return markets_from_countries


def get_data_from_yahoo_finance(market_ticker):
    """
    This function fetches data from Yahoo Finance in the form of a Pandas DataFrame
    :param market_ticker: The Ticker symbol for which data needs to be fetched
    :return: pd.DataFrame - Returns a DataFrame containing the data fetched from Yahoo Finance
    """
    today = datetime.datetime.now().date()
    ten_years_ago = today.replace(year=today.year - 10)
    time.sleep(2)
    data = pdr.get_data_yahoo(market_ticker, start=str(ten_years_ago), end=str(today), auto_adjust=True)
    if data.empty:
        logging.info('No Data found for Ticker %s. The ticker does not exist' % market_ticker)
        raise ValueError('No Data found for Ticker %s. The ticker does not exist' % market_ticker)
    else:
        return data


def get_monthly_return(index):
    """
    Calculate the Monthly Return of the data based on Monthly Return calculations given at:
    (http://bit.ly/2hHNHuV)
    :param index: The index whose monthly return needs to be calculated
    :return: pd.DataFrame: Consisting of values with the monthly return
    """
    monthly = index.asfreq('M').ffill()
    monthly_pc = monthly / monthly.shift(1) - 1
    # Drop na rows and return
    return monthly_pc.dropna()


def main():
    """
    This function is called from the main block. The purpose of this function is to contain all the calls to
    business logic functions
    :return: int - Return 0 or 1, which is used as the exist code, depending on successful or erroneous flow
    """
    # Wrap in a try block so that we catch any exceptions thrown by other functions and return a 1 for graceful exit
    try:
        # ===== Step 0: Sanitation =====
        # Fix Pandas Datareader's Issues with Yahoo Finance (Since yahoo abandoned it's API)
        yahoo_finance_bridge()
        # ===== Step 1: Get the two markets from the user =====
        # Prompt the user to input the data that needs to be downloaded
        countries = get_countries_from_user()

        # ===== Step 2: Automatically choose the right market =====
        markets_to_load = get_market_names_from_countries(countries)

        # ===== Step 3: Download the 10 Year data for the Ticker =====
        indices_to_load_list = list(markets_to_load.values())
        index_one = get_data_from_yahoo_finance(str(indices_to_load_list[0]))
        index_two = get_data_from_yahoo_finance(str(indices_to_load_list[1]))

        # ===== Step 4: Calculate Correlation Coefficients of monthly returns between each pair of indices =====
        # Get monthly returns for the indices
        monthly_return_index_one = get_monthly_return(index_one)
        monthly_return_index_two = get_monthly_return(index_two)
        # Combine the monthly returns into a single DataFrame
        monthly_return_combo = pd.DataFrame({indices_to_load_list[0]: monthly_return_index_one['Close'].tolist(),
                                             indices_to_load_list[1]: monthly_return_index_two['Close'].tolist()})
        # Convert Decimal Values to percentage values
        monthly_return_combo = monthly_return_combo * 100
        # Calculate the correlation
        correl = monthly_return_combo.corr(method='pearson', min_periods=1)

        # ===== Step 5: Plot the results in a suitable graphical format =====
        sns.heatmap(correl,
                    xticklabels=correl.columns.values,
                    yticklabels=correl.columns.values)
        sns.plt.show()
        sns.pairplot(monthly_return_combo)
        sns.plt.show()

        # ===== Additional Step: Calculate Correl between all the indices =====
        # Get the rest of the indices that are pending
        other_indices_to_load = [val for val in get_market_map().values() if val not in indices_to_load_list]

        index_three = get_data_from_yahoo_finance(str(other_indices_to_load[0]))
        index_four = get_data_from_yahoo_finance(str(other_indices_to_load[1]))
        index_five = get_data_from_yahoo_finance(str(other_indices_to_load[2]))

        monthly_return_index_three = get_monthly_return(index_three)
        monthly_return_index_four = get_monthly_return(index_four)
        monthly_return_index_five = get_monthly_return(index_five)

        other_monthly_return_combo = pd.DataFrame({
            other_indices_to_load[0]: monthly_return_index_three['Close'].tolist(),
            other_indices_to_load[1]: monthly_return_index_four['Close'].tolist(),
            other_indices_to_load[2]: monthly_return_index_five['Close'].tolist()})

        other_monthly_return_combo = other_monthly_return_combo * 100

        total_combo = pd.concat([monthly_return_combo, other_monthly_return_combo], axis=1)

        total_correl = total_combo.corr(method='pearson', min_periods=1)

        sns.heatmap(total_correl,
                    xticklabels=total_correl.columns.values,
                    yticklabels=total_correl.columns.values)
        sns.plt.show()
        sns.pairplot(total_combo)
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
