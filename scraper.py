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
PV Insights
'''
table_PVI = pd.read_html('http://pvinsights.com/index.php', match='Item')

polysilicon_pvi = table_PVI[2]
polysilicon_pvi = polysilicon_pvi.tail(-1)
polysilicon_pvi.columns = polysilicon_pvi.iloc[0] 
polysilicon_pvi = polysilicon_pvi.tail(-1)
polysilicon_pvi = polysilicon_pvi.head(-1)
polysilicon_pvi['Category'] = "Polysilicon"
polysilicon_pvi['Date'] = todays_date
polysilicon_pvi.set_index('Date', inplace=True)
polysilicon_pvi = polysilicon_pvi.drop(["AvgChg%", "AvgCNY"], axis=1)
polysilicon_pvi = polysilicon_pvi.rename(columns={"AvgChg": 'Change'})
                                                
wafer_pvi = table_PVI[3]
wafer_pvi = wafer_pvi.tail(-1)
wafer_pvi.columns = wafer_pvi.iloc[0] 
wafer_pvi = wafer_pvi.tail(-1)
wafer_pvi = wafer_pvi.head(-1)
wafer_pvi['Category'] = "Wafer"
wafer_pvi['Date'] = todays_date
wafer_pvi.set_index('Date', inplace=True)
wafer_pvi = wafer_pvi.drop(["AvgChg %", "AvgCNY"], axis=1)
wafer_pvi = wafer_pvi.rename(columns={"AvgChg": 'Change'})

cell_pvi = table_PVI[4]
cell_pvi = cell_pvi.tail(-1)
cell_pvi.columns = cell_pvi.iloc[0] 
cell_pvi = cell_pvi.tail(-1)
cell_pvi = cell_pvi.head(-1)
cell_pvi['Category'] = "Cell"
cell_pvi['Date'] = todays_date
cell_pvi.set_index('Date', inplace=True)
cell_pvi = cell_pvi.drop(["AvgChg %", "AvgCNY"], axis=1)
cell_pvi = cell_pvi.rename(columns={"AvgChg": 'Change'})

module_pvi = table_PVI[5]
module_pvi = module_pvi.tail(-1)
module_pvi.columns = module_pvi.iloc[0] 
module_pvi = module_pvi.tail(-1)
module_pvi = module_pvi.head(-1)
module_pvi['Category'] = "Region Module"
module_pvi['Date'] = todays_date
module_pvi.set_index('Date', inplace=True)
module_pvi = module_pvi.drop(["AvgChg %", "AvgCNY"], axis=1)
module_pvi = module_pvi.rename(columns={"AvgChg": 'Change'})

df1 = polysilicon_pvi.merge(wafer_pvi, how="outer")
df2 = df1.merge(cell_pvi, how="outer")
pvi_df = df2.merge(module_pvi, how="outer")
pvi_df['Website'] = 'PV Insights'
pvi_df['Link'] = 'http://pvinsights.com/index.php'

#################################################################################
'''
Energy Trend
'''
r = requests.get('https://www.energytrend.com/solar-price.html')
t = r.text

table_G = pd.read_html(t, match='PV Spot Price')

et_df = table_G[0]
et_df = et_df.tail(-1)
et_df = et_df.iloc[: , 1:]
et_df['Date'] = todays_date
items = []
count = 0

for row in et_df.iterrows():
    if row[1][1] == "item":
        row[1][1] = "Item"
        items.append(count)
    count += 1
items.append(count)

polysilicon_et = et_df.iloc[items[0]:items[1]]
polysilicon_et = polysilicon_et.tail(-1)
polysilicon_et['Category'] = "Polysilicon"
polysilicon_et.set_index('Date', inplace=True)
polysilicon_et = polysilicon_et.rename(columns={1: 'Item', 2: 'High', 3: 'Low', 4: 'Average', 5: 'Change'})

wafer_et = et_df.iloc[items[1]:items[2]]
wafer_et = wafer_et.tail(-1)
wafer_et['Category'] = "Wafer"
wafer_et.set_index('Date', inplace=True)
wafer_et = wafer_et.rename(columns={1: 'Item', 2: 'High', 3: 'Low', 4: 'Average', 5: 'Change'})

cell_et = et_df.iloc[items[2]:items[3]]
cell_et = cell_et.tail(-1)
cell_et['Category'] = "Cell"
cell_et.set_index('Date', inplace=True)
cell_et = cell_et.rename(columns={1: 'Item', 2: 'High', 3: 'Low', 4: 'Average', 5: 'Change'})

module_et = et_df.iloc[items[3]:items[4]]
module_et = module_et.tail(-1)
module_et['Category'] = "Region Module"
module_et.set_index('Date', inplace=True)
module_et = module_et.rename(columns={1: 'Item', 2: 'High', 3: 'Low', 4: 'Average', 5: 'Change'})

pvglass_et = et_df.iloc[items[4]:items[5]]
pvglass_et = pvglass_et.tail(-1)
pvglass_et['Category'] = "Glass"
pvglass_et.set_index('Date', inplace=True)
pvglass_et = pvglass_et.rename(columns={1: 'Item', 2: 'High', 3: 'Low', 4: 'Average', 5: 'Change'})


df1 = polysilicon_et.merge(wafer_et, how="outer")
df2 = df1.merge(cell_et, how="outer")
df3 = df2.merge(module_et, how="outer")
et = df3.merge(pvglass_et, how="outer")
et['Website'] = 'Energy Trend'
et['Link'] = 'https://www.energytrend.com/solar-price.html'
et['Change']= et['Change'].str.replace('(','', regex = True)
et['Change']= et['Change'].str.replace(')','', regex = True)
et['Change']= et['Change'].str.replace('% ','', regex = True)

#################################################################################
'''
InfoLink
'''
r = requests.get('https://www.infolink-group.com/spot-price')
t = r.text

table_I = pd.read_html(t, match='Item')

polysilicon_il = table_I[0]
polysilicon_il['Category'] = "Polysilicon"
polysilicon_il['Date'] = todays_date
polysilicon_il.set_index('Date', inplace=True)
polysilicon_il = polysilicon_il.drop(["Change($)", "Price prediction for next week"], axis=1)
polysilicon_il = polysilicon_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

wafer_il = table_I[1]
wafer_il['Category'] = "Wafer"
wafer_il['Date'] = todays_date
wafer_il.set_index('Date', inplace=True)
wafer_il = wafer_il.drop(["Change($)", "Price prediction for next week"], axis=1)
wafer_il = wafer_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

cell_il = table_I[2]
cell_il['Category'] = "Cell"
cell_il['Date'] = todays_date
cell_il.set_index('Date', inplace=True)
cell_il = cell_il.drop(["Change($)", "Price prediction for next week"], axis=1)
cell_il = cell_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})
cell_il

ncell_il = table_I[3]
ncell_il['Category'] = "Cell"
ncell_il['Date'] = todays_date
ncell_il.set_index('Date', inplace=True)
ncell_il = ncell_il.drop(["Change($)", "Price prediction for next week"], axis=1)
ncell_il = ncell_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

monofacial_il = table_I[4]
monofacial_il['Category'] = "Monfacial"
monofacial_il['Date'] = todays_date
monofacial_il.set_index('Date', inplace=True)
monofacial_il = monofacial_il.drop(["Change($)", "Price prediction for next week"], axis=1)
monofacial_il = monofacial_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

bifacial_il = table_I[5]
bifacial_il['Category'] = "Bifacial"
bifacial_il['Date'] = todays_date
bifacial_il.set_index('Date', inplace=True)
bifacial_il = bifacial_il.drop(["Change($)", "Price prediction for next week"], axis=1)
bifacial_il = bifacial_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

chinaprojects_il = table_I[6]
chinaprojects_il['Category'] = "Project"
chinaprojects_il['Date'] = todays_date
chinaprojects_il.set_index('Date', inplace=True)
chinaprojects_il = chinaprojects_il.drop(["Change($)", "Price prediction for next week"], axis=1)
chinaprojects_il = chinaprojects_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

regionmodule_il = table_I[7]
regionmodule_il['Category'] = "Region Module"
regionmodule_il['Date'] = todays_date
regionmodule_il.set_index('Date', inplace=True)
regionmodule_il = regionmodule_il.drop(["Change($)", "Price prediction for next week"], axis=1)
regionmodule_il = regionmodule_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

chinamodule_il = table_I[8]
chinamodule_il['Category'] = "Region Module"
chinamodule_il['Date'] = todays_date
chinamodule_il.set_index('Date', inplace=True)
chinamodule_il = chinamodule_il.drop(["Change($)", "Price prediction for next week"], axis=1)
chinamodule_il = chinamodule_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

modulematerials_il = table_I[9]
modulematerials_il['Category'] = "Region Module"
modulematerials_il['Date'] = todays_date
modulematerials_il.set_index('Date', inplace=True)
modulematerials_il = modulematerials_il.drop(["Change($)", "Price prediction for next week"], axis=1)
modulematerials_il = modulematerials_il.rename(columns={'Average price': 'Average', 'Change(%)': 'Change'})

df1 = pd.concat([polysilicon_il, wafer_il])
df2 = pd.concat([df1, cell_il])
df3 = pd.concat([df2, ncell_il])
df4 = pd.concat([df3, monofacial_il])
df5 = pd.concat([df4, bifacial_il])
df6 = pd.concat([df5, chinaprojects_il])
df7 = pd.concat([df6, regionmodule_il])
df8 = pd.concat([df7, chinamodule_il])
il_df = pd.concat([df8, modulematerials_il])
il_df['Website'] = 'Info Link'
il_df['Link'] = 'https://www.infolink-group.com/spot-price'

#################################################################################
'''
Create CSVs
'''
secondfinal_df = pvi_df.merge(et, how="outer")
secondfinal_df['Date'] = todays_date
secondfinal_df = secondfinal_df.set_index('Date')
final_df = pd.concat([secondfinal_df, il_df])
final_df = final_df.sort_values(by=['Category'])

polysilicon_df = final_df.loc[(final_df['Category'] == 'Polysilicon')]              
wafer_df = final_df.loc[(final_df['Category'] == 'Wafer')]
module_df = final_df.loc[(final_df['Category'] == 'Region Module')]
cell_df = final_df.loc[(final_df['Category'] == 'Cell')]
monofacial_df = final_df.loc[(final_df['Category'] == 'Monofacial')]
bifacial_df = final_df.loc[(final_df['Category'] == 'Bifacial')]
glass_df = final_df.loc[(final_df['Category'] == 'Glass')]
project_df = final_df.loc[(final_df['Category'] == 'Project')]

outdir = '/dbfs/FileStore/pv_scraper/'

poly = outdir+ 'Polysilicon_' + todays_date + '.csv'
polysilicon_df.to_csv(poly, index=False, encoding="utf-8")

waf = outdir+ 'Wafer_' + todays_date + '.csv'
wafer_df.to_csv(waf, index=False, encoding="utf-8")

mod = outdir+ 'Module_' + todays_date + '.csv'
module_df.to_csv(mod, index=False, encoding="utf-8")

cel = outdir+ 'Cell_' + todays_date + '.csv'
cell_df.to_csv(cel, index=False, encoding="utf-8")

mono = outdir+ 'Monofacial_' + todays_date + '.csv'
monofacial_df.to_csv(mono, index=False, encoding="utf-8")

bi = outdir+ 'Bifacial_' + todays_date + '.csv'
bifacial_df.to_csv(bi, index=False, encoding="utf-8")

gla = outdir+ 'Glass_' + todays_date + '.csv'
glass_df.to_csv(gla, index=False, encoding="utf-8")

proj = outdir+ 'Project_' + todays_date + '.csv'
project_df.to_csv(proj, index=False, encoding="utf-8")

DF = outdir + 'Module_Cost_Breakdown_' + todays_date + '.csv'
final_df.to_csv(DF, index=False, encoding="utf-8")

print("Executed for", todays_date)
