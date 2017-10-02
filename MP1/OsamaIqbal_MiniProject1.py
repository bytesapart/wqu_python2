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
4.	Choose a quadratic equation of your choice and using SciPy leastsq() optimization method calculate the best fit line with respect to the downloaded data
5.  Plot the best fit line and the actual data points together with error bars.
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
import scipy.optimize  # For Optimization Problems
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


def quadratic_interpolation_with_plot(x_array_dim, x_label):
    """
    Perform Quadratic Interpolation with plotting of the graph
    :param x_array_dim: The x array value for the interpolation
    :param x_label: The X axis label value
    :return: None
    """
    granular_time_step = np.linspace(0, 20, 100)
    time_step = np.arange(0, len(x_array_dim))
    interpreted = scipy.interpolate.interp1d(time_step, x_array_dim, kind='quadratic')
    y1 = interpreted(granular_time_step)
    pylab.plot(x_array_dim, 'o', label='Actual Data Values (%s)' % x_label)
    pylab.plot(granular_time_step, y1, label='Quadratic Fit (%s)' % x_label)
    pylab.legend()
    pylab.xlabel(x_label)
    pylab.show()


def fitfunc(p, t):
    """This is the equation"""
    return p[0] * t ** 2 + p[1] * t


def errfunc(p, t, y):
    return fitfunc(p, t) - y


def best_fit_with_plot(close_price):
    """
    Plots best fitting quadratic equation
    :param close_price: The array to fit
    :return: None
    """
    x_data = np.arange(1, len(close_price) + 1)
    y_data = close_price

    guess = np.array([close_price.max(), close_price.min()])
    output, preds = scipy.optimize.leastsq(errfunc, guess, args=(x_data, y_data))
    y_error = fitfunc(output, x_data) - y_data  # residuals
    pylab.errorbar(x_data, y_data, yerr=y_error, fmt='ro', label="Actual stock price")
    pylab.plot(fitfunc(output, x_data), 'b--', label="Best Fit - Quadratic Function")
    pylab.legend(loc='best')
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
        # Use only the close prices of the stocks
        x_close = x_array[:, 3]
        # Interpolate and plot the result
        quadratic_interpolation_with_plot(x_close, 'Close Values')

        # ===== Step 4 and 5: Calculate Best Fit =====
        best_fit_with_plot(x_close)

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
