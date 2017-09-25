"""
Created on Mon Aug 14 09:54:10 2017

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Elementary OS with Ubuntu 16.04 variant, with a Linux 4.10.0-33-generic as the Kernel.

Project 1:
-- Steps:
1.	Write a python program that prompts the user to enter any valid stock symbol available in Google Finance, Yahoo Finance, Quandl, CityFALCON, or another similar source for NYSE & NASDAQ. Ensure proper error handling for wrong user inputs..
2.	Download data for last 1 month for user entered ticker from Google Finance, Yahoo Finance, Quandl, CityFALCON, or another similar source
3.	Using Interpolation techniques, fit a quadratic line through the data points and plot the same
4.	Choose a quadratic equation of your choice and using SciPy leastsq() optimization method calculate the best fit line with respect to the downloaded data 5. Plot the best fit line and the actual data points together with error bars.
"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import logging  # Logging class for logging in the case of an error, makes debugging easier
import sys  # For gracefully notifying whether the script has ended or not
from pandas_datareader import data as pdr  # The pandas Data Module used for fetching data from a Data Source
import warnings  # For removing Deprication Warning w.r.t. Yahoo Finance Fix
import datetime  # For setting correct dates from today up to a year in the past to get data from YF
import numpy as np  # For numerical operations
import scipy.interpolate  # For fitting quadratic curve
import pylab  # For plotting the graphs

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


def get_ticker_from_user():
    """
    This function prompts a user for an input, and returns it as the ticker
    :return:
    """
    logging.info('Prompting user to enter a ticker symbol')
    print('Note: Data up to 1 month from today will be fetched from Yahoo Finance')
    return raw_input('Enter a Symbol Ticker (case insensitive): ')


def get_data_from_yahoo_finance(stock_ticker):
    """
    This function fetches data from Yahoo Finance in the form of a Pandas DataFrame
    :param stock_ticker: The Ticker symbol for which data needs to be fetched
    :return: pd.DataFrame - Returns a DataFrame containing the data fetched from Yahoo Finance
    """
    today = datetime.datetime.now().date()
    previous_month = today.replace(month=today.month - 1)
    data = pdr.get_data_yahoo(stock_ticker, start=str(previous_month), end=str(today), auto_adjust=True)
    if data.empty:
        logging.info('No Data found for Ticker %s. The ticker does not exist' % stock_ticker)
        raise ValueError('No Data found for Ticker %s. The ticker does not exist' % stock_ticker)
    else:
        return data


def quadratic_interpolation_with_plot(x_array_dim, y_array_dim, x_label):
    """
    Perform Quadratic Interpolation with plotting of the graph
    :param x_array: The x array value for the interpolation
    :param y_array: The y array value for the interpolation
    :return:
    """
    interp = scipy.interpolate.interp1d(x_array_dim, y_array_dim, kind='quadratic')
    pylab.plot(x_array_dim, y_array_dim, 'o', label='Actual Data Values (%s)' % x_label)
    pylab.plot(x_array_dim, interp(x_array_dim), label='Quadratic Fit (%s)' % x_label)
    pylab.legend()
    pylab.xlabel(x_label)
    pylab.show()


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

        # ===== Step 1: Get the Ticker From user =====
        # Prompt the user to input the data that needs to be downloaded
        stock_ticker = get_ticker_from_user()
        logging.debug('Stock Ticker is: %s' % str(stock_ticker))

        # ===== Step 2: Download the data for the Ticker =====
        # Get the data fetched from Yahoo Finance
        stock_data = get_data_from_yahoo_finance(str(stock_ticker))

        # ===== Step 3: Fit a quadratic line =====
        # Convert pandas DataFrame to Numpy Array, and drop the 'Volume' column
        x_array = np.array(stock_data)[:, :4]
        x_array = x_array.mean(axis=1)
        # Get the y part of the function, that is y = f(x)
        y_array = x_array ** 2  # Quadratic Function to fit
        # Interpolate and plot the result
        quadratic_interpolation_with_plot(x_array, y_array, 'Mean Values')

        # ===== Step 4: Fit a quadratic line =====



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
