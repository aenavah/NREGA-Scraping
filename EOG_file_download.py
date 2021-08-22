
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import wget
chrome_options = Options()
import time

site = "https://eogdata.mines.edu/nighttime_light/monthly/v10/"
driver = webdriver.Chrome(executable_path = "/Users/alexandranava/Desktop/CODE/Income Dynamics Lab/NREGA/Chrome Driver 91/chromedriver91", options = chrome_options )
driver.get(site)
year_list = ["2021"] #include last year found if not done with all the months
for year in year_list:
    driver.find_element_by_partial_link_text(year).click()
    #time.sleep(3)
    if year == "2013":
        month_list = ["05"] ###change here if not the first run, do not include last found month
    if year == "2018":
        month_list = ["09", "10", "11", "12"]
    if year == "2019": #remove current year
        month_list = ["09"]
    if year == "2020":
        month_list = ["10", "11", "12"]
    if year == "2021":
        month_list = ["01", "02", "03"]
    for month in month_list:
        driver.find_element_by_partial_link_text(year + month).click()
        #time.sleep(3)
        driver.find_element_by_partial_link_text("vcmcfg").click()
        #time.sleep(3)
        soup = BeautifulSoup(driver.page_source,"html.parser")  #beautiful soup object of second page html
        driver.find_element_by_partial_link_text("75N060E").click()
        print("Found " + year + "/" + month)
        if year + month == year_list[0] + month_list[0]:
            print("log in...")
            time.sleep(240)
            driver.back()
        else:
            time.sleep(240)
        driver.back()
        driver.back()
    driver.back()
