# Class representing a company stock, with financial data

from selenium import webdriver

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker 
        self.stock_url = "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)
        self.financial_url = "https://finance.yahoo.com/quote/{0}/financials?p={0}".format(ticker)

        self.updateData()




    def updateData(self):
        self._get_raw_data()
        self._process_data()



    def _get_raw_data(self):
        '''Download raw data from Yahoo Finance'''
        driver = webdriver.Chrome()
        driver.get(self.stock_url)
        # SCRAPE STOCK DATA
        driver.get(self.financial_url)
        # SCRAPE FINANCE DATA


    def _process_data(self):
        '''Process raw data to create meaningful up-to-date data points'''
        pass
        
    