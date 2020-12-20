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

# import re

# Local Imports
from src.stock import Stock






if __name__ == "__main__":
    print("Starting")

    crwd = Stock("ASTI")
    crwd.updateData()
    print(crwd)