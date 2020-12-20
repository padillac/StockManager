### This program 

# Imports
# from selenium import webdriver

# from tqdm import tqdm

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime, date
import time

from threading import Thread

# import re

# Local Imports
from src.stock import Stock






if __name__ == "__main__":
    print("Starting")

    crwd = Stock("CRWD")
    aapl = Stock("AAPL")
    asti = Stock("ASTI")
    tsla = Stock("TSLA")


    x1 = Thread(target=crwd.updateData)
    x2 = Thread(target=aapl.updateData)
    x3 = Thread(target=asti.updateData)
    x4 = Thread(target=tsla.updateData)
    
    x1.start()
    x2.start()

    x1.join()
    x2.join()

    x3.start()
    x4.start()
    
    x3.join()
    x4.join()


    print(crwd)
    print(aapl)
    print(asti)
    print(tsla)
