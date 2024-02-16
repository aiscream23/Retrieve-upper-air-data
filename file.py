import time
import calendar
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

import argparse

parser = argparse.ArgumentParser(description='Download upper air data.')

parser.add_argument('year', type=int, help='Tahun, contohnya 2023.')
parser.add_argument('station', type=str, help='kode stasiun WMOID. contoh 96749 (STAMET Soekarno Hatta')


args = parser.parse_args()
year = args.year
station = args.station


for month in range(1,13):
    try:
        url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM=0100&TO=3112&STNM={station}" 
        driver.get(url)
        
        tag_body = driver.find_elements(By.TAG_NAME, "body")
        # Menyimpan data ke dalam file
        file_path = f'download/data_{year}_{month:02d}.txt'
        with open(file_path, 'w') as file:
            for body in tag_body:
                file.write(body.text)
        
        if driver.find_elements(By.TAG_NAME, "pre")[0].text == "Invalid TIME parameter." :
            # untuk bulan dengan jumlah tanggal 30
            url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM=0100&TO=3012&STNM={station}"
            driver.get(url)

            tag_body = driver.find_elements(By.TAG_NAME, "body")
            # Menyimpan data ke dalam file
            file_path = f'download/data_{year}_{month:02d}.txt'
            with open(file_path, 'w') as file:
                for body in tag_body:
                    file.write(body.text)
            
            if driver.find_elements(By.TAG_NAME, "pre")[0].text == "Invalid TIME parameter.":
                # untuk bulan dengan jumlah tanggal 29
                url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM=0100&TO=2912&STNM={station}"
                driver.get(url)

                tag_body = driver.find_elements(By.TAG_NAME, "body")
                # Menyimpan data ke dalam file
                file_path = f'download/data_{year}_{month:02d}.txt'
                with open(file_path, 'w') as file:
                    for body in tag_body:
                        file.write(body.text)           

                if driver.find_elements(By.TAG_NAME, "pre")[0].text == "Invalid TIME parameter.":
                    # untuk bulan dengan jumlah tanggal 28
                    url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM=0100&TO=2812&STNM={station}"
                    driver.get(url)

                    tag_body = driver.find_elements(By.TAG_NAME, "body")
                    # Menyimpan data ke dalam file
                    file_path = f'download/data_{year}_{month:02d}.txt'
                    with open(file_path, 'w') as file:
                        for body in tag_body:
                            file.write(body.text)

                else:
                    pass
            else:
                pass
        else:
            pass
    except:
        pass

time.sleep(1)
driver.close()

# bagian menyusun dataframenya dari kumpulan download file txtnya
# Nama folder output
output_folder = 'output'

os.makedirs(output_folder, exist_ok=True)

# bisa diatasi dengan mengganti nama file saat download kalau mau simpel untuk sortednya
file_names = os.listdir("download/")
sorted_file_names = sorted(file_names, key=lambda x: (int(x.split('_')[2][:2]), int(x.split('_')[1])))
with open(os.path.join(output_folder, 'coba.txt'), 'w') as outfile:
    for fname in sorted_file_names:
        with open(os.path.join("download", fname)) as infile:
            for line in infile:
                outfile.write(line)

with open(os.path.join(output_folder, 'coba.txt'), 'r') as file:
    text = file.read()

lines = text.strip().split('\n')
data = []

for line in lines:
    if "Station information and sounding indices" in line:
        station_data = {}
    if ":" in line:
        key, value = line.split(':')
        station_data[key.strip()] = value.strip()
        # Jika sudah mencapai SWEAT index, tambahkan data stasiun ke list dan reset dict
        if "SWEAT index" in key:
            data.append(station_data)
# Buat DataFrame dari list data
df = pd.DataFrame(data)

# save filenya
df.to_excel('output/hasil.xlsx')
