# Class representing a company stock, with financial data

from selenium import webdriver

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker 
        self.stock_url = "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)
        self.financial_url = "https://finance.yahoo.com/quote/{0}/financials?p={0}".format(ticker)

        self._get_raw_data()


    def _get_raw_data(self):
        driver = webdriver.Chrome()
        driver.get(self.stock_url)
        
