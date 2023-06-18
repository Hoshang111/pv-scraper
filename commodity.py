import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
from datetime import datetime
import ssl
import requests

todays_date = datetime.now().strftime("%d-%m-%Y")
#################################################################################
'''
Trading Economics
'''

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

r = requests.get('https://tradingeconomics.com/commodities', headers=HEADERS)
outdir = '/dbfs/FileStore/commodities_api/'

table_commodity = pd.read_html(r.text, match='Price')
energy_df = table_commodity[0]
energy_df['Date'] = todays_date
energy_df = energy_df.set_index('Date')
energy = outdir+ 'energy_' + todays_date + '.csv'
energy_df.to_csv(energy, index=True, encoding="utf-8")

metals_df = table_commodity[1]
metals_df['Date'] = todays_date
metals_df = metals_df.set_index('Date')
metals = outdir+ 'metals_' + todays_date + '.csv'
metals_df.to_csv(metals, index=True, encoding="utf-8")

agricultural_df = table_commodity[2]
agricultural_df['Date'] = todays_date
agricultural_df = agricultural_df.set_index('Date')
agricultural = outdir+ 'agricultural_' + todays_date + '.csv'
agricultural_df.to_csv(agricultural, index=True, encoding="utf-8")

industrial_df = table_commodity[3]
industrial_df['Date'] = todays_date
industrial_df = industrial_df.set_index('Date')
industrial = outdir+ 'industrial_' + todays_date + '.csv'
industrial_df.to_csv(industrial, index=True, encoding="utf-8")

livestock_df = table_commodity[4]
livestock_df['Date'] = todays_date
livestock_df = livestock_df.set_index('Date')
livestock = outdir+ 'livestock_' + todays_date + '.csv'
livestock_df.to_csv(livestock, index=True, encoding="utf-8")

index_df = table_commodity[5]
index_df['Date'] = todays_date
index_df = index_df.set_index('Date')
index = outdir+ 'index_' + todays_date + '.csv'
index_df.to_csv(index, index=True, encoding="utf-8")

electricity_df = table_commodity[6]
electricity_df['Date'] = todays_date
electricity_df = electricity_df.set_index('Date')
electricity = outdir+ 'electricity_' + todays_date + '.csv'
electricity_df.to_csv(electricity, index=True, encoding="utf-8")

string = "Hey Jock, the run has finished for today: " + todays_date
print(string)