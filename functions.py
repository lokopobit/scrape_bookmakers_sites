# -*- coding: utf-8 -*-

"""
Created on Fri Nov 29 11:22:04 2019

@author: lokopobit
"""

# Load external libreries
from datetime import date
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import os

#Create json object for dumping and loading. Dont forget close().
def create_json(website, data_path):
    data_path = os.path.join(data_path, website)
    extraction_date = str(date.today()).replace('-', '_')
    data_path = os.path.join(data_path, extraction_date)
    f = open(data_path + '.json', 'w')
    return f

#Load data from stored json.
def load_data(website, data_path, day):
    #dia = '2019_11_17' example
    data_path = os.path.join(data_path, website)
    data_path = os.path.join(data_path, day)
    f = open(data_path + '.json', 'r')
    data = json.load(f)
    return data

#Lanzar navegador con url 
def start_url_driver(url, driver_path, is_headless=True):
    try:
        if is_headless:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(executable_path=driver_path, options=options)
        else:
            driver = webdriver.Firefox(executable_path=driver_path)
        driver.implicitly_wait(10)
        driver.get(url)
        return driver
    except:
        print('ERROR: LOADING PAGE ', url)
    