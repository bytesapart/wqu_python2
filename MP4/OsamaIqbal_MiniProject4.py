"""
Created on Mon October 02 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Elementary OS with Ubuntu 16.04 variant, with a Linux 4.10.0-33-generic as the Kernel.

Project 4:
-- Steps:
1.Create a csv file with a list of all presidents, their parties from 1920 onwards
2.Using Pandas load the .csv file into a Pandas dataframe.
3.Download data from an appropriate financial website such as Google Finance, Yahoo Finance, Quandl, CityFALCON, or another similar source
4.Calculate yearly returns for both the downloaded indices from 1920 onwards
5.Calculate measures of central tendency (mean return, median return, variance of returns) for each of the two groups
6.Represent the findings through suitable comparative graphical studies
"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import logging  # Logging class for logging in the case of an error, makes debugging easier
import sys  # For exiting gracefully
import quandl  # For fetching the Market Data
import pandas as pd  # For fetching the data in a DataFrame
import matplotlib.pyplot as plt


def plot_group_bar_chart(plotting_dataframe):
    """
    This function is used for plotting a grouped bar chart
    :param plotting_dataframe: The DataFrame to plot
    :return: None
    """
    # Setting the positions and width for the bars
    pos = list(range(len(plotting_dataframe['Mean Annual Return'])))
    width = 0.25

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10, 5))

    # Create a bar with Mean Annual Return data,
    # in position pos,
    plt.bar(pos, plotting_dataframe['Mean Annual Return'], width, alpha=0.5,
            color='#EE3224', label=plotting_dataframe['Party'][0])

    # Create a bar with Annual Median Return data,
    # in position pos + some width buffer,
    plt.bar([p + width for p in pos], plotting_dataframe['Median Annual Return'], width, alpha=0.5,
            color='#F78F1E', label=plotting_dataframe['Party'][1])

    # Create a bar with Annual Variance data,
    # in position pos + some width buffer,
    plt.bar([p + width * 2 for p in pos], plotting_dataframe['Annual Variance'], width, alpha=0.5,
            color='#FFC222', label=plotting_dataframe['Party'][2])

    # Set the y axis label
    ax.set_ylabel('Values')

    # Set the chart's title
    ax.set_title('Annual Equity Index Performance since 1920 - Democrats vs Republicans')

    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(plotting_dataframe['Party'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos) - width, max(pos) + width * 4)
    plt.ylim([0, max(plotting_dataframe['Mean Annual Return'] + plotting_dataframe['Median Annual Return']
                     + plotting_dataframe['Annual Variance'])])

    # Adding the legend and showing the plot
    plt.legend(['Mean Annual Return', 'Median Annual Return', 'Annual Variance'], loc='upper left')
    plt.grid()
    plt.show()


def main():
    """
        This function is called from the main block. The purpose of this function is to contain all the calls to
        business logic functions
        :return: int - Return 0 or 1, which is used as the exist code, depending on successful or erroneous flow
        """
    # Wrap in a try block so that we catch any exceptions thrown by other functions and return a 1 for graceful exit
    try:
        # ===== Step 1: Load the CSV as a pandas DataFrame =====
        presidents_dataframe = pd.DataFrame.from_csv('presidents.csv')
        # Convert the Start and End columns to DateTime objects
        presidents_dataframe['Start'] = pd.to_datetime(presidents_dataframe['Start'])
        presidents_dataframe['End'] = pd.to_datetime(presidents_dataframe['End'])

        # ===== Step 2: Download the two Indices =====
        # By using the collapse parameter, we directly get yearly data instead fetching daily/monthly
        # data and performing calculations on that dataset
        djia_dataframe = quandl.get("BCB/UDJIAD1", collapse='annual')
        snp_dataframe = quandl.get("MULTPL/SP500_REAL_PRICE_MONTH", collapse='annual')

        # Filter so that they are 1920 onwards
        djia_dataframe = djia_dataframe.loc['1920':]
        snp_dataframe= snp_dataframe.loc['1920':'2016']  # Because the DJIA datasource does not have 2017's data

        # ===== Step 2: Calculate the yearly returns  =====
        # Since our data is already in yearly format, we need to call pct_change() with 1 as the
        # parameter. Assuming our data would have been daily or monthly, then we would have called
        # pct_change(252) for yearly returns from daily, and pct_change(21) for yearly returns from monthly data
        djia_yearly_returns = djia_dataframe['Value'].pct_change(1)
        snp_yearly_returns = snp_dataframe['Value'].pct_change(1)
        # Join the DataFrames
        djia_dataframe = djia_dataframe.join(djia_yearly_returns, rsuffix='_Yearly_Returns')
        snp_dataframe = snp_dataframe.join(snp_yearly_returns, rsuffix='_Yearly_Returns')
        # Drop the first year since it contains a NaN value
        djia_dataframe.dropna(inplace=True)
        snp_dataframe.dropna(inplace=True)

        # ===== Step 4: Segregate returns in terms of Presidency  =====
        presidency_list = []
        for index, date_value in enumerate(snp_dataframe.index):
            for p_index in range(0, len(presidents_dataframe)):
                if presidents_dataframe.iloc[p_index]['End'] > date_value > presidents_dataframe.iloc[p_index]['Start']:
                    presidency_list.append(presidents_dataframe.iloc[p_index]['Party'])
                    break
        # Map Yearly Returns to Party
        djia_dataframe = djia_dataframe.join(pd.DataFrame(presidency_list, columns=['Party']).set_index(
            djia_dataframe.index))
        snp_dataframe = snp_dataframe.join(pd.DataFrame(presidency_list, columns=['Party']).set_index(
            snp_dataframe.index))
        # Combine SnP and DJIA frame
        combined_dataframe = pd.DataFrame({'DJIA': djia_dataframe['Value_Yearly_Returns'],
                                           'SNP': snp_dataframe['Value_Yearly_Returns'],
                                           'Party': snp_dataframe['Party']}).reset_index(drop=True)

        democrats_dataframe = combined_dataframe[combined_dataframe['Party'] == 'Democratic']
        republicans_dataframe = combined_dataframe[combined_dataframe['Party'] == 'Republican']

        # ===== Step 4: Calculate Central Tendency for each of the groups  =====
        democrats_central_tendency = democrats_dataframe.describe()
        republicans_central_tendency = republicans_dataframe.describe()
        # Create Plotting DataFrame
        plotting_dataframe = pd.DataFrame([['Democrats-DJIA', democrats_central_tendency.loc['mean']['DJIA'],
                                            democrats_central_tendency.loc['50%']['DJIA'],
                                            democrats_central_tendency.loc['std']['DJIA'] ** 2],
                                           ['Democrats-SnP', democrats_central_tendency.loc['mean']['SNP'],
                                            democrats_central_tendency.loc['50%']['SNP'],
                                            democrats_central_tendency.loc['std']['SNP'] ** 2],
                                           ['Republicans-DJIA', republicans_central_tendency.loc['mean']['DJIA'],
                                            republicans_central_tendency.loc['50%']['DJIA'],
                                            republicans_central_tendency.loc['std']['DJIA'] ** 2],
                                           ['Republicans-SNP', republicans_central_tendency.loc['mean']['SNP'],
                                            republicans_central_tendency.loc['50%']['SNP'],
                                            republicans_central_tendency.loc['std']['SNP'] ** 2]],
                                          columns=
                                          ['Party', 'Mean Annual Return', 'Median Annual Return', 'Annual Variance'])
        # Plot the data
        plot_group_bar_chart(plotting_dataframe)
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

