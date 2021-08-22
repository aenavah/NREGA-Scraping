#requires state and state/"data" directories within cwd, and ukrescrapes data csv in state directory

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:11:43 2021

@author: alexandranava
"""

#------------------------- libraries -------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import csv
import time
from os import path
import os
chrome_options = Options()
#------------------------- user inputs -------------------------
driver = webdriver.Chrome(executable_path = "/Users/alexandranava/Desktop/CODE/Income Dynamics Lab/NREGA/Chrome Driver 91/chromedriver91", options = chrome_options )
state = "bihar"
folder_path = "/Users/alexandranava/Desktop/CODE/Income Dynamics Lab/NREGA/" + state + "/"
wait_hours = 8 #hours to wait if site breaks to try again
wait_seconds = wait_hours* 60 * 60 #overwrite for debug
basepage_url = "https://mnregaweb2.nic.in/netnrega/"

timestorun = 3
#-------------------------------------------------------------
clicked_csv = folder_path + "clicked_links.csv"
all_url_path = folder_path + "ukrescrape" + state + "_links.csv" #list of clicked
#-------------------------------------------------------------
#if page is closed, have to end code and rerun
print("*******************************************")

def save_pagesource(browser, pathh, filename): #save html for individul years for each panchayat to folder "data"
    if "/" in filename:
        filename = filename.replace("/","")
    with codecs.open(pathh + filename, "w+", "utf-8-sig") as temp:
        temp.write(browser.page_source)

def retrieve_codes(url): #break down url into district and code, block and code,panchayat and code into a list "data"
    full_id = ""
    url = url.replace(basepage_url + "IndexFrame.aspx?lflag=local&","")
    url = url.split("&")
    district_code = url[0].replace("District_Code=","")
    district_name = url[1].replace("district_name=","")
    state_name = url[2].replace("state_name=","")
    state_code = url[3].replace("state_Code=","")
    block_name = url[4].replace("block_name=","")
    block_code = url[5].replace("block_code=","")
    panchayat_name = url[8].replace("Panchayat_name=","")
    panchayat_code = url[9].replace("Panchayat_Code=","")
    data = [district_name, district_code, block_name, block_code, panchayat_name, panchayat_code]
    for cell in data:
        full_id = full_id + cell + "--"
    data.append(full_id)
    return data

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
def main_script():
    #initialize
    basepage_number = 0

    #make list of panchayat base page from csv, including done ones
    basepagelinks = [] #all links to be clicked through including already done ones
    with codecs.open(all_url_path, 'r', encoding= 'unicode_escape') as links: ###
        pd_links = csv.reader(links)
        for line in pd_links:
           full_url = basepage_url + line[0].strip("../")
           basepagelinks.append(full_url)
    #removes urls that its already done
    if path.exists(folder_path + "clicked_links.csv"):
        print("Obtaining Remaining Panchayats...")
        clicked_urls = [] #links that have been done already if code stopped previously
        with codecs.open( folder_path + "clicked_links.csv") as clicked_csv_:
            clicked_object = csv.reader(clicked_csv_)
            for line in clicked_object:
                clicked_urls.append(line[1])
        for clicked in clicked_urls:
            basepagelinks.remove(clicked)
        print("*******************************************")

    #now go through remaining urls and scrape
    for basepage in basepagelinks: #each basepage is the full url
        #initialize
        panchayat_id = retrieve_codes(basepage)
        file_name = panchayat_id[-1]
        basepage_number += 1
        print("Currently Working on... ", str(basepage_number) + " of " + str(len(basepagelinks)) + "\n" + file_name)
        driver.get(basepage)
        soup = BeautifulSoup(driver.page_source, features="html5lib")
        driver.find_element_by_partial_link_text("Material Register").click()
        for year in ["2017-2018", "2018-2019", "2019-2020", "2020-2021"]:
            if year == "2018-2019" and file_name == "24+PARAGANS+SOUTH--3216--KULTALI--3216013--KUNDAKHALI+GODABAR--3216013006--":
                continue
            select_year =  driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$ddl_finyr']/option[text()='"+year+"']").click()
            print(year, end = '') #prints after clicking the year
            save_pagesource(driver, folder_path + "data/", file_name + year)
            print("...", end = " ") #prints once year is saved
        print('\n ----------------------------------') #prints once all years done
        url_completed = [[file_name,basepage]]
        df = pd.DataFrame(url_completed)
        df.to_csv(folder_path + "clicked_links.csv", header = False, index = False, mode = 'a')

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

#------------------------- error handler -------------------------
def tryagain(count):
    try:
        if count == 0:
            print("--------First Try--------")
            os.mkdir(folder_path)
            os.mkdir(folder_path + "data/")
            print("Created " + state + " folder in cwd...")
        main_script()

    except:
        driver = webdriver.Chrome(executable_path = "/Users/alexandranava/Desktop/CODE/Income Dynamics Lab/NREGA/Chrome Driver 91/chromedriver91", options = chrome_options )
        time.sleep(wait_seconds)
        print("Trying Again...")
        if count < timestorun:
            tryagain(count+1)

#main_script() #use for debugging
tryagain(0) #use to automatically rerun script if exception occurs
