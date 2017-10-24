"""
Created on Mon October 16 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Windows 10.

Final Project: The Misbehaviour of Markets
1.	Write a python program(s) to download end-of-day data last 25 years the major global stock market indices from Google Finance, Yahoo Finance, Quandl, CityFALCON, or another similar source.
2.	It is a common assumption in quantitative finance that stock returns follow a normal distribution whereas prices follow a lognormal distribution For all these indices check how closely price movements followed a log-normal distribution.
3.	Verify whether returns from these broad market indices followed a normal distribution?
4.	For each of the above two parameters (price movements and stock returns) come up with specific statistical measures that clearly identify the degree of deviation from the ideal distributions. Graphically represent the degree of correspondence.
5.	One of the most notable hypothesis about stock market behavior is the "Efficient market hypothesis" which also internally assume that market price follows a random-walk process. Assuming that Stock Index prices follow a geometric Brownian motion and hence index returns were normally distributed with about 20% historical volatility, write a program sub-module to calculate the probability of an event like the 1987 stock market crash happening ? Explain in simple terms what the results imply.
6.	What does "fat tail" mean? Plot the distribution of price movements for the downloaded indices (in separate subplot panes of a graph) and identify fat tail locations if any.
7.	It is often claimed that fractals and multi-fractals generate a more realistic picture of market risks than log-normal distribution. Considering last 10 year daily price movements of NASDAQ, write a program to check whether fractal geometrics could have better predicted stock market movements than log-normal distribution assumption. Explain your findings with suitable graphs.

Indexes to be used:
    - S&P 500 (USA)
    - DAX (Germany)
    - FTSE (UK)
    - KOSPI (Korea)
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
import numpy as np  # For getting log values from prices
import warnings  # For removing Deprecation Warning w.r.t. Yahoo Finance Fix
import matplotlib.pyplot as plt
import scipy.stats
import statsmodels.graphics.gofplots as sm
import math

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


# Main block of the program. The program begins execution from this block when called from a cmd
def lognormal_check_markets(dataframe_dictionary):
    """
    This function takes in markets and does a check to find out whether they the price movements follow
    a Log Normal Distribution

    :param: dataframe_dictionary: Consist of a Dictionary Mapping of Market Name to Maket Data DataFrame
    :type: dict

    :return: dict
    """
    print('\n\nCheck whether Price Movements follow a Log-Normal Distribution')
    print('H0: The price movements of the indices follow a Log-Normal Distribution')
    print('H1: The movements of the indices do not follow a Log-Normal Distribution\n')

    for key, value in dataframe_dictionary.items():
        under_test = scipy.stats.kstest(value['Close'], "lognorm", scipy.stats.lognorm.fit(value['Close']))
        # Populate Return Dictionary
        if under_test.pvalue < 0.05:
            print('The p-value for ' + key + '\'s Price Movements is less than 0.05, '
                                             'therefore it does not follow Log-Normal Distribution.')
        else:
            print(key + '\'s Price Movements follow a Log-Normal Distribution')


def lognormal_check_deviation(data_dict):
    """
    This function takes a dictionary containing Markets DataFrame, and does a np.log() on the closing
    prices. Then it gives skewness, kurtosis, mean, median std, min and max of the values
    :param data_dict: The dictionary containing the DataFrames
    :return: dict
    """
    # Iterate through every market
    for key, value in data_dict.items():
        # Take the log of close prices
        close_price = np.log(value['Close'])
        print('\n===== Calculating Statistic for Prices for %s =====' % key)
        skew = scipy.stats.skewtest(close_price)
        print('Skew for %s is : %f' % (key, skew.statistic))
        kurt = scipy.stats.kurtosistest(close_price)
        print('Kurtosis for %s is : %f' % (key, kurt.statistic))
        t_test = scipy.stats.ttest_1samp(close_price, 0)
        print('T-Statistic for %s is : %f' % (key, t_test.statistic))
        desc = close_price.describe()
        print('Mean for %s is : %f' % (key, desc.iloc[1]))
        print('Median for %s is : %f' % (key, desc.iloc[5]))
        print('Standard Deviation for %s is : %f' % (key, desc.iloc[2]))
        print('Min for %s is : %f' % (key, desc.iloc[3]))
        print('Max for %s is : %f' % (key, desc.iloc[7]))
        print('========================================\n')


def normal_check_market_returns(data_dict):
    """
    This function takes a Data Dictionary and and calculates daily returns of each of the index in the dictionary.
    Then, it checks if the it is normally distributed or not
    :param data_dict: Dictionary ocntaining market historical data's DataFrame
    :return:None
    """
    print('\n\nCheck whether Price Movements follow a Log-Normal Distribution')
    print('H0: The returns of the indices follow a Normal Distribution')
    print('H1: The returns of the indices do not follow a Normal Distribution\n')

    for key, value in data_dict.items():
        # Get Daily Returns and Backfill
        daily_return = value['Close'].pct_change().fillna(method='backfill')
        under_test = scipy.stats.normaltest(daily_return)
        # Populate Return Dictionary
        if under_test.pvalue < 0.05:
            print('The p-value for ' + key + '\'s Stock Returns is less than 0.05, '
                                             'therefore it does not follow Normal Distribution.')
        else:
            print(key + '\'s Stock Returns follow a Normal Distribution')


def normal_check_deviation(data_dict):
    """
    This function takes a dictionary containing Markets DataFrame, calculates the returns.
    Then it gives skewness, kurtosis, mean, median std, min and max of the values
    :param data_dict: The dictionary containing the DataFrames
    :return: dict
    """
    # Iterate through every market
    for key, value in data_dict.items():
        # Take the log of close prices
        daily_return = value['Close'].pct_change().fillna(method='backfill')
        print('\n===== Calculating Statistic for Stock Returns for %s =====' % key)
        skew = scipy.stats.skewtest(daily_return)
        print('Skew for %s is : %f' % (key, skew.statistic))
        kurt = scipy.stats.kurtosistest(daily_return)
        print('Kurtosis for %s is : %f' % (key, kurt.statistic))
        t_test = scipy.stats.ttest_1samp(daily_return, 0)
        print('T-Statistic for %s is : %f' % (key, t_test.statistic))
        desc = daily_return.describe()
        print('Mean for %s is : %f' % (key, desc.iloc[1]))
        print('Median for %s is : %f' % (key, desc.iloc[5]))
        print('Standard Deviation for %s is : %f' % (key, desc.iloc[2]))
        print('Min for %s is : %f' % (key, desc.iloc[3]))
        print('Max for %s is : %f' % (key, desc.iloc[7]))
        print('========================================\n')


def plot_qq_plot(data, both=True):
    """
    This function plots QQ Plots for both the stock returns and the log of the prices
    :param data: The DataFrame dictionary containing market indices
    :return: None
    """
    # ===== Plot the returns =====
    if both:
        f, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)
            ) = plt.subplots(4, 2, figsize=(12, 24))
        f = sm.qqplot(data['^DJI']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax1)
        ax1.grid(True)
        ax1.set_title('Dow Jones Index')
        f = sm.qqplot(data['^GSPC']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax2)
        ax2.grid(True)
        ax2.set_title('SnP 500')
        f = sm.qqplot(data['^IXIC']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax3)
        ax3.grid(True)
        ax3.set_title('NASDAQ')
        f = sm.qqplot(data['^GDAXI']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax4)
        ax4.grid(True)
        ax4.set_title('German DAX')
        f = sm.qqplot(data['^FTSE']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax5)
        ax5.grid(True)
        ax5.set_title('FTSE')
        f = sm.qqplot(data['^HSI']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax6)
        ax6.grid(True)
        ax6.set_title('HSI')
        f = sm.qqplot(data['^KS11']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax7)
        ax7.grid(True)
        ax7.set_title('KOSPI')
        f = sm.qqplot(data['^NSEI']['Close'].pct_change().fillna(method='backfill'), dist='norm', line='s', fit=True,
                      ax=ax8)
        ax8.grid(True)
        ax8.set_title('India Nifty')
        plt.suptitle('Returns QQ Plot')
        plt.show()
    # ===== Plot the prices =====
    f, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)
        ) = plt.subplots(4, 2, figsize=(12, 24))
    f = sm.qqplot(np.log(data['^DJI']['Close']), dist='norm', ax=ax1)
    ax1.grid(True)
    ax1.set_title('Dow Jones Index')
    f = sm.qqplot(np.log(data['^GSPC']['Close']), dist='norm', ax=ax2)
    ax2.grid(True)
    ax2.set_title('SnP 500')
    f = sm.qqplot(np.log(data['^IXIC']['Close']), dist='norm', ax=ax3)
    ax3.grid(True)
    ax3.set_title('NASDAQ')
    f = sm.qqplot(np.log(data['^GDAXI']['Close']), dist='norm', ax=ax4)
    ax4.grid(True)
    ax4.set_title('German DAX')
    f = sm.qqplot(np.log(data['^FTSE']['Close']), dist='norm', ax=ax5)
    ax5.grid(True)
    ax5.set_title('FTSE')
    f = sm.qqplot(np.log(data['^HSI']['Close']), dist='norm', ax=ax6)
    ax6.grid(True)
    ax6.set_title('HSI')
    f = sm.qqplot(np.log(data['^KS11']['Close']), dist='norm', ax=ax7)
    ax7.grid(True)
    ax7.set_title('KOSPI')
    f = sm.qqplot(np.log(data['^NSEI']['Close']), dist='norm', ax=ax8)
    ax8.grid(True)
    ax8.set_title('India Nifty')
    plt.suptitle('Prices QQ Plot')
    plt.show()


def market_crash_probability(snp_data):
    """
    This function calculates the probability of a stock market crash using GBM
    :param sp_data: the snp500 close price data
    :return: None
    """
    # Calculate Yearly Returns
    snp_yearly = snp_data['Close'].pct_change(259).dropna()[0]
    # start at the final day of the data to be starting point this assumes that when running GBM it will give daily next year forecast
    snp0 = math.log(snp_data['Close'][-1])
    m = snp_yearly  # Expected Return
    sigma = 0.20  # Anuallized Volatility
    T = 1 / 252.0  # Maturity Date in years
    dt = .00001
    N = 10
    steps = round(T / dt)  # number of steps
    snp = np.zeros([int(N), int(steps)], dtype=float)
    x = range(0, int(steps), 1)
    storage = []  # For storing simulated values, to calc. probability
    for j in range(0, N, 1):
        snp[j, 0] = snp0
        for i in x[:-1]:
            snp[j, i + 1] = snp[j, i] + (m - 0.5 * pow(sigma, 2)) * dt + sigma * scipy.sqrt(
                dt) * np.random.standard_normal()
        storage.append(np.exp(snp)[j])
        plt.plot(x, np.exp(snp)[j])
    plt.xlabel('Steps')
    plt.ylabel('SnP500 Prices')
    plt.show()

    # For calculating probability
    # Get the returns for each day from simulated set, minus
    storage = pd.DataFrame(storage)
    storage_returns = storage.T.pct_change()
    # Where returns are less than a 20.3% drop, which was a single day crash in 19887
    prob = storage_returns < -0.203
    probability_of_crash = prob.sum()
    for index, row in probability_of_crash.iteritems():
        print('The probability of a 1987 crash of SnP500, where a single intraday crash was 20.3%, '
              'using GBM with the ' + str(index) + ' simulation is: ' + str(row))


def hurst(size, nasdaq_close_price):
    nasdaq_close_price = nasdaq_close_price[0:size]  # NASDAQ prices for n period
    yn = nasdaq_close_price - np.mean(nasdaq_close_price)  # Calculation of mean adjusted series for this period
    zn = np.cumsum(yn)  # Calculation of the cumulative sum
    Rn = np.max(zn) - np.min(zn)  # Calculation of range
    Sn = np.std(nasdaq_close_price)  # Calculation of std deviation
    En = Rn / Sn  # Calculation of the rescaled range
    return np.log(En)


def generateYn(x, results):
    yn = []
    interCept = results.params[0]
    x1 = results.params[1]
    for i in range(len(x)):
        yn.append(interCept + x1 * x[i])
    return yn


def hurst_ts(ts):
    """Returns the Hurst Exponent of the time series vector ts"""
    # Create the range of lag values
    lags = range(2, 100)

    # Calculate the array of the variances of the lagged differences
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    # Use a linear fit to estimate the Hurst Exponent
    poly = np.polyfit(np.log(lags), np.log(tau), 1)

    # Return the Hurst exponent from the polyfit output
    return poly[0] * 2.0


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

        # ===== Step 1: Fetching end of day data for the last 25 years for the four indexes in play =====
        data = pdr.get_data_yahoo(['^DJI', '^GSPC', '^IXIC', '^GDAXI', '^FTSE', '^HSI', '^KS11', '^NSEI'],
                                  start="1991-10-01", end="2017-10-01", as_panel=False, group_by='index',
                                  auto_adjust=True)
        # Assign them to variables,
        # Interpolate holes, using a simple Linear Interpolation,
        # and drop NaN rows that could not be interpolated, since backfilling could skew results
        DJI = data['^DJI'].interpolate().dropna()
        SP500 = data['^GSPC'].interpolate().dropna()
        NASDAQ = data['^IXIC'].interpolate().dropna()
        DAX = data['^GDAXI'].interpolate().dropna()
        FTSE = data['^FTSE'].interpolate().dropna()
        HSI = data['^HSI'].interpolate().dropna()
        KOSPI = data['^KS11'].interpolate().dropna()
        CNXNIFTY = data['^NSEI'].interpolate().dropna()

        # ===== Step 2:  Using a Normality test for the prices of the stock market indexes to find out their distribution =====
        # Create DataFrame Dictionary
        data_dict = {'DJI': DJI, 'SP500': SP500, 'NASDAQ': NASDAQ, 'DAX': DAX, 'FTSE': FTSE, 'HSI': HSI, 'KOSPI': KOSPI,
                     'CNXNIFTY': CNXNIFTY}
        lognormal_check_markets(data_dict)
        # Check the distributions deviation from log-normal distribution
        lognormal_check_deviation(data_dict)

        # ===== Step 3:  Using a Normality test for the returns of the stock market indexes to find out their distribution =====
        # Check for normality of the returns
        normal_check_market_returns(data_dict)

        # ===== Step 4: For prices and returns, show statistic and plot their correspondence =====
        # Check the distributions deviation from log-normal distribution
        lognormal_check_deviation(data_dict)
        # Check the distributions deviation from Normal distribution
        normal_check_deviation(data_dict)
        # PLot QQ plot
        plot_qq_plot(data)

        # ===== Step 5: GBM stock market crash probability =====
        market_crash_probability(SP500.loc['2016':'2016'].interpolate())

        # ===== Step 6: Plot distribution to identify fat tails =====
        plot_qq_plot(data, both=False)

        # ===== Step 7: Plot distribution to identify fat tails =====
        nasdaq_10_years = data['^IXIC']['2006':'2016']
        nasdaq_close_price = nasdaq_10_years['Close'].interpolate().dropna()
        y = [hurst(np.size(nasdaq_close_price), nasdaq_close_price),
             hurst(np.size(nasdaq_close_price) / 2, nasdaq_close_price),
             hurst(np.size(nasdaq_close_price) / 4, nasdaq_close_price),
             hurst(np.size(nasdaq_close_price) / 8, nasdaq_close_price),
             hurst(np.size(nasdaq_close_price) / 16, nasdaq_close_price),
             hurst(np.size(nasdaq_close_price) / 32, nasdaq_close_price)]
        x = [np.log(np.size(nasdaq_close_price)),
             np.log(np.size(nasdaq_close_price) / 2),
             np.log(np.size(nasdaq_close_price) / 4),
             np.log(np.size(nasdaq_close_price) / 8),
             np.log(np.size(nasdaq_close_price) / 16),
             np.log(np.size(nasdaq_close_price) / 32)]
        xx = sm.add_constant(x)
        model = sm.OLS(y, xx)
        results = model.fit()
        print(results.summary())
        yn = generateYn(xx, results)
        plt.plot(xx, np.reshape(yn, (6, 2)), '-')
        plt.scatter(x, y)
        plt.grid(True)
        plt.title("Rescaled Range Analysis for NASDAQ Prices for 10 Years")
        plt.show()

        # Get the Hurst Exponent of the Series:
        nasdaq_hurst = results.params[1]
        print("Hurst(NASDAQ Close Prices):    %s" % str(nasdaq_hurst))
        fractal_dim = 2 - nasdaq_hurst
        print("Fractal Dimension: %s" % str(fractal_dim))
        if nasdaq_hurst > 0.5 and fractal_dim < 1.5:
            print('The given Hurst expression is Trending')
        elif nasdaq_hurst < 0.5 and fractal_dim > 1.5:
            print('The given Hurst expression is anti-persisting, that is, it is mean reverting')

        print('\n========== Alternative Hurst Exponent Calculation ==========')
        nasdaq_hurst = hurst_ts(np.log(nasdaq_close_price))
        print("Hurst(NASDAQ Close Prices):    %s" % str(nasdaq_hurst))
        fractal_dim = 2 - nasdaq_hurst
        print("Fractal Dimension: %s" % str(fractal_dim))

        if nasdaq_hurst > 0.5 and fractal_dim < 1.5:
            print('The given Hurst expression is Trending')
        elif nasdaq_hurst < 0.5 and fractal_dim > 1.5:
            print('The given Hurst expression is anti-persisting, that is, it is mean reverting')

    except BaseException, e:
        # Casting a wide net to catch all exceptions
        print('\n%s' % str(e))
        return 1


if __name__ == '__main__':
    # Initialize Logger
    logging.basicConfig(format='%(asctime)s %(message)s: ')
    logging.info('Application Started')
    exit_code = main()
    logging.info('Application Ended')
    sys.exit(exit_code)
