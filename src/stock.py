# Class representing a company stock, with financial data


# IMPORTS
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


# GLOBALS
NUMERIC_CHARACTERS = {
    'M': 1000000,
    'B': 1000000000,
    'T': 1000000000000
}


class Stock:
    def __init__(self, ticker):
        print("Creating Stock object with ticker '{}'...".format(ticker))
        self.ticker = ticker 
        self.stock_url = "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)
        self.statistics_url = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)
        self.income_statement_url = "https://finance.yahoo.com/quote/{0}/financials?p={0}".format(ticker)
        self.balance_sheet_url = "https://finance.yahoo.com/quote/{0}/balance-sheet?p={0}".format(ticker)
        self.cash_flow_url = "https://finance.yahoo.com/quote/{0}/cash-flow?p={0}".format(ticker)
        self.current_price = None
        self.dollar_change = None
        self.percent_change = None
        self.market_cap = None
        self.volume = None
        self.avg_volume = None
        self.total_assets = None
        self.current_assets = None
        self.total_liabilities = None
        self.equity = None
        self.outstanding_shares = None
        
        self.NCAV = None
        self.NCAV_per_share = None
        self.NAV_per_share = None
        self.PE_ratio = None
        self.EPS = None
        self.one_year_growth_rate = None
        self.pe_ratio_entry_price = "N/A"
        self.net_net_entry_price = "N/A"
        self.price_to_book_entry_price = "N/A"
        self.pe_ratio_entry_price = "N/A"
        self.graham_value = "N/A"
        self.graham_entry_price = "N/A"




    def __str__(self):
        return "Stock Object [\"{}\"] :\n\
            Stock Price:  ${:,}\n\
            $ Change:     ${:,}\n\
            % Change:     {:,}%\n\
            1-yr Growth:  {:,}%\n\
            Market Cap:   ${:,}\n\
            Volume:       {:,}\n\
            Avg. Volume:  {:,}\n\
            Out. Shares:  {:,}\n\
            Tot. Assets:  ${:,}\n\
            Cur. Assets:  ${:,}\n\
            Tot. Liabil:  ${:,}\n\
            Book Value:   ${:,}\n\
            NCAV:         ${:,}\n\
            NCAV / share: ${:,}\n\
            NAV / share:  ${:,}\n\
            PE Ratio:     {}\n\
            EPS:          {}\n\
\
        Analysis:\n\
            Net-Net Valuation Entry Price: ${}\n\
            Price to Book Entry Price:     ${}\n\
            PE Ratio Entry Price:          ${}\n\
            Graham Growth Value:           ${}\n\
            Graham Growth Entry Price:     ${}\n\
            ".format(
                self.ticker, 
                self.current_price, 
                self.dollar_change, 
                self.percent_change,
                self.one_year_growth_rate,
                self.market_cap,
                self.volume,
                self.avg_volume,
                self.outstanding_shares,
                self.total_assets,
                self.current_assets,
                self.total_liabilities,
                self.equity,
                self.NCAV,
                self.NCAV_per_share,
                self.NAV_per_share,
                self.PE_ratio,
                self.EPS,
                self.net_net_entry_price,
                self.price_to_book_entry_price,
                self.pe_ratio_entry_price,
                self.graham_value,
                self.graham_entry_price)



    def updateData(self):
        self._get_raw_data()
        self._process_data()




    def _get_raw_data(self):
        '''Download raw data from Yahoo Finance'''
        caps = DesiredCapabilities().CHROME
        caps['pageLoadStrategy'] = 'eager'
        driver = webdriver.Chrome(desired_capabilities=caps)
        # SCRAPE STOCK DATA
        driver.get(self.stock_url)
        self.current_price = float(driver.find_element_by_xpath('//span[@data-reactid="50"]').text)
        change = driver.find_element_by_xpath('//span[@data-reactid="51"]').text.split()
        self.dollar_change, self.percent_change = float(change[0]), float(change[1].lstrip('(').rstrip('%)'))
        raw_market_cap = driver.find_element_by_xpath('//td[@data-test="MARKET_CAP-value"]').text
        self.market_cap = int(float(raw_market_cap[:-1]) * NUMERIC_CHARACTERS[raw_market_cap[-1]])
        self.volume = int(driver.find_element_by_xpath('//td[@data-test="TD_VOLUME-value"]').text.replace(',', ''))
        self.avg_volume = int(driver.find_element_by_xpath('//td[@data-test="AVERAGE_VOLUME_3MONTH-value"]').text.replace(',', ''))
        raw_pe_ratio = driver.find_element_by_xpath('//td[@data-test="PE_RATIO-value"]').text
        self.PE_ratio = float(raw_pe_ratio) if raw_pe_ratio != "N/A" else "N/A"
        raw_eps = driver.find_element_by_xpath('//td[@data-test="EPS_RATIO-value"]').text
        self.EPS = float(raw_eps) if raw_eps != "N/A" else "N/A"

        # SCRAPE STATS DATA
        driver.get(self.statistics_url)
        raw_outstanding_shares = driver.find_element_by_xpath('//span[contains(text(), "Shares Outstanding")]/../../td[2]').text
        self.outstanding_shares = int(float(raw_outstanding_shares[:-1]) * NUMERIC_CHARACTERS[raw_outstanding_shares[-1]])
        self.one_year_growth_rate = float(driver.find_element_by_xpath('//span[contains(text(), "52-Week Change")]/../../td[2]').text[:-1])

        # SCRAPE FINANCE DATA
        driver.get(self.income_statement_url)

        driver.get(self.balance_sheet_url)
        driver.find_element_by_xpath('//span[contains(text(), "Expand All")]').click()
        time.sleep(.4)
        driver.find_element_by_xpath('//span[contains(text(), "Quarterly")]').click()
        time.sleep(.4)
        table_rows = driver.find_elements_by_xpath('//div[@data-test="fin-row"]')
        self.total_assets = int(1000 * float(table_rows[0].find_elements_by_xpath('.//div[@data-test="fin-col"]')[0].text.replace(',', '')))
        self.current_assets = int(1000 * float(table_rows[1].find_elements_by_xpath('.//div[@data-test="fin-col"]')[0].text.replace(',', '')))
        self.total_liabilities = int(1000 * float(table_rows[31].find_elements_by_xpath('.//div[@data-test="fin-col"]')[0].text.replace(',', '')))
        self.equity = int(1000 * float(table_rows[50].find_elements_by_xpath('.//div[@data-test="fin-col"]')[0].text.replace(',', '')))


        driver.get(self.cash_flow_url)
        
        


    def _process_data(self):
        '''Process raw data to create meaningful up-to-date data points'''
        #Net-Net Valuation
        self.NCAV = self.current_assets - self.total_liabilities
        self.NCAV_per_share = self.NCAV / self.outstanding_shares
        self.net_net_entry_price = self.NCAV_per_share * 2/3

        # Price to Book Valuation
        self.NAV_per_share = self.equity / self.outstanding_shares
        self.price_to_book_entry_price = self.NAV_per_share * .8

        # Price to Earnings Ratio Valuation
        if type(self.PE_ratio) == float:
            self.target_PE_ratio = self.PE_ratio * .7
            self.pe_ratio_entry_price = self.EPS * self.target_PE_ratio

        # Graham Growth Formula Valuation
        self.graham_value = self.EPS * (8.5 + 2 * self.one_year_growth_rate)
        self.graham_entry_price = self.graham_value * .7
        

    
    
