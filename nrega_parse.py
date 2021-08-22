#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 13:03:05 2021
@author: alexandranava
"""
#------------------------libraries--------------------------
from bs4 import BeautifulSoup
import pandas as pd
import os
#------------------------user inputs--------------------------
state = "bihar"
project_path = "/Users/alexandranava/Desktop/Code/Income Dynamics Lab/NREGA/" + state + "/"
#--------------------------------------------------
html_data_path = project_path + "data/"
number_files = (len(os.listdir(html_data_path)))
No_data_list = [] #sites recorded without data
counter = 0
text_rows =[]

for file in os.listdir(html_data_path): #for each html file name
    f = open(html_data_path+file)
    if  file[0] == '.' or len(f.readlines()) <= 3: #record empty files names
        No_data_list.append(file)
        continue
    for year in ["2017-2018", "2018-2019", "2019-2020", "2020-2021"]:
        if year in file:
            file_year = year
            file_wo_year = file.replace(year,"")
    file_split = file_wo_year.split('--')
    district, district_code, block, block_code, Panchayat, panchayat_code, none_ = file_split
    counter += 1
    print("Currently working on "+ str(counter)+ " of "+ str(number_files) + file + "\n---------------------------------------------------")
    soup = BeautifulSoup(open(html_data_path+file), "html.parser")
    data_table = soup("div", {"id":"ContentPlaceHolder1_divRep"})[0]
    rows = data_table.find_all("tr")
    for  row in (rows):
        data_cells = row.findAll("td")
        text_row = []
        text_row.extend([year,district,district_code,block,block_code,Panchayat,panchayat_code])
        for cell in data_cells:
            cell = cell.text.strip()
            text_row.append(cell)
        text_rows.append(text_row)
df = pd.DataFrame(text_rows)

df.columns =  ['Year', 'District', "District Code" , 'Block', "Block Code", 'Panchayat', "Panchayat Code"] + text_rows[0][7:]
df.drop(df.loc[df['Work Name(Work Code)']=='Work Name(Work Code)'].index, inplace=True)
df.to_csv(project_path + state + "_data.csv")

print("Double check for data:", No_data_list)
