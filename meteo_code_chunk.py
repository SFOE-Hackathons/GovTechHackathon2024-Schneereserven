# kpi-wetter-3
# Skript laeuft taeglich da es zwei Datenquellen gibt: Monatliche und taegliche Niederschlags-Daten
# Monatliche Daten des Vormonats liegen immer am 6. und am 21. (definitiv) vor
# Taegliche Daten liegen am naechsten Tag vor
# Tag 1-5: Vormonat anhand taeglichen Daten, aktueller Monat anhand taeglichen Daten
# Tag 6-31: Vormonat anhand monatlichen Daten, aktueller Monat anhand taeglichen Daten

import os
import urllib.request
import urllib.parse
import json
import pandas as pd
import csv
import io
import datetime
from datetime import timedelta, date
import numpy as np
import matplotlib.pyplot as plt
import boto3
from botocore.exceptions import NoCredentialsError
#%matplotlib inline
#%config InlineBackend.figure_format='retina'

output = "Wetter/kpi-wetter-3_meteoswiss_niederschlag_V1.csv"
output2 = "Wetter/kpi-wetter-3_meteoswiss_niederschlag_V2.csv"

stations = ["BAS","BER","CHD","CHM","DAV","ENG","GVE","LUG","SAE","SIA","SIO","SMA"]
stations_names = ['Basel / Binningen','Bern / Zollikofen',"Château-d'Oex",'Chaumont','Davos',"Engelberg",'Genève / Cointrin', 'Lugano','Säntis','Segl-Maria','Sion','Zürich / Fluntern']

today = int(pd.to_datetime("today").strftime('%d'))
last_month = datetime.datetime.today().replace(day=1).replace(hour=23).replace(minute=59) - datetime.timedelta(days=1)
last_month_first_day = last_month.replace(day=1).replace(hour=0).replace(minute=0)
this_month_first_day = pd.to_datetime("today").replace(day=1).replace(hour=0).replace(minute=0)


# Auth on API
token = os.environ["METEOSCHWEIZ_TOKEN"]
kodart_url = 'https://service.meteoswiss.ch/kodart-public/api/v1/'
token_url = 'https://service.meteoswiss.ch/auth/realms/meteoswiss.ch/protocol/openid-connect/token'
with urllib.request.urlopen(urllib.request.Request(
        method='POST',
        url=token_url,
        data=urllib.parse.urlencode((('grant_type', 'refresh_token'), ('client_id', 'api-token'),
                                     ('refresh_token', token)
                                     )).encode())) as f:
    auth_header = 'Bearer ' + json.loads(f.read().decode())['access_token']
    
# Bestellte Produkte abfragen
#url = "https://service.meteoswiss.ch/kodart-public/api/v1/products/" # this shows the available product(s)
#req = urllib.request.Request(url=url)
#req.add_header('Authorization', auth_header)
#with urllib.request.urlopen(req) as f:
#    response = f.read()
#    y = json.loads(response)
#y


###############
# Produkt "PRODUKT_API_daily_BFE_surface" abfragen und Staging nachfuehren
# Taegliche Daten
###############

# API call
url = "https://service.meteoswiss.ch/kodart-public/api/v1/products/realizations?productId=6120" # this shows the available product(s)
req = urllib.request.Request(url=url)
req.add_header('Authorization', auth_header)
with urllib.request.urlopen(req) as f:
    response = f.read()
    with open("Wetter/staging_ms_6120.csv", 'wb') as f:
        f.write(response) # binary answer, we have to write to disk
        
        
###############
# Produkt "PRODUKT_API_monthly_BFE_surface" abfragen und Staging nachfuehren
# Monatliche Daten. Werden am 5. (erste Schaetzung) und 20. (definitiv) des Folgemonats aufdatiert.
# Produkt kann nur 7 Tagen nach dem 5. und 20. abgerufen werden.
###############

# API call
url = "https://service.meteoswiss.ch/kodart-public/api/v1/products/realizations?productId=6780" # this shows the available product(s)
req = urllib.request.Request(url=url)
req.add_header('Authorization', auth_header)
with urllib.request.urlopen(req) as f:
    response = f.read()
    if len(response) > 0:
        with open("Wetter/staging_ms_6780.csv", 'wb') as f:
            f.write(response) # binary answer, we have to write to disk
            
# read staging
df_staging = pd.read_csv("Wetter/staging_ms_6780.csv", sep=";")
df_staging.rename(columns={"Station/Location": "abbr", "Date": "time"}, inplace=True)

# read full history
df_history = pd.read_csv("Wetter/MeteoSchweiz_Niederschlag.csv", sep=",")
df_history.rre150m0 = pd.to_numeric(df_history.rre150m0, errors="coerce")

# concat
df_new = pd.concat([df_history, df_staging])
df_new = df_new.drop_duplicates()

# save
df_new.to_csv("Wetter/MeteoSchweiz_Niederschlag.csv", index=False)

###############
# Lade die Norm-Werte und leite Schweizer-Mittel pro Kalenderonat ab
###############

df_norm = pd.read_csv("Wetter/climate-reports-normtables_rre150m0_1991-2020_de.txt", skiprows=8, sep='\t')
df_norm = df_norm[df_norm['Station'].isin(stations_names)]
df_norm.drop(columns=['Stationshöhe [m]', 'Jahr'], inplace=True)
df_norm.rename(columns={"Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4", "Mai": "5", "Jun": "6", "Jul": "7", "Aug": "8", "Sep": "9", "Okt": "10", "Nov": "11", "Dez": "12"}, inplace=True)
df_norm = df_norm.mean(numeric_only=True, axis=0).to_frame()
df_norm.reset_index(inplace=True)
df_norm.rename(columns={"index": "Monat", 0: "Niederschlag_CH_Norm_mean"}, inplace=True)
df_norm.Monat = df_norm.Monat.astype('int64')
df_norm.set_index('Monat', inplace=True)

###############
# Lade die ganze Zeitreihe der monatlichen Daten und leite Schweizer-Mittel ab
###############

df_history = pd.read_csv("Wetter/MeteoSchweiz_Niederschlag.csv")
df_history.time = pd.to_datetime(df_history.time, format='%Y%m')
df_history.rre150m0 = pd.to_numeric(df_history.rre150m0, errors="coerce")
df_history = df_history[df_history['abbr'].isin(stations)]
df_history = df_history[df_history.time > "2020-12-31"]
df_history = df_history.drop_duplicates()
df_history.sort_values(by="time")
df_history = df_history.groupby('time').mean(numeric_only=True)
df_history.reset_index(inplace=True)
df_history.rename(columns={"time": "Datum", "rre150m0": "Niederschlag_CH_gemessen_mean"}, inplace=True)
df_history["Monat"] = pd.DatetimeIndex(df_history["Datum"]).month


###############
# Hinzufuegen des letzten Monats anhand der taeglichen Daten
###############

# read staging
df_staging = pd.read_csv("Wetter/staging_ms_6120.csv", sep=";")
df_staging.rename(columns={"Station/Location": "abbr", "Date": "time"}, inplace=True)
df_staging = df_staging[["abbr", "time", "rre150d0"]].copy()
df_staging.drop(df_staging[df_staging['rre150d0'] == "-"].index, inplace = True)
df_staging.time = pd.to_datetime(df_staging.time, format='%Y%m%d')
df_staging.rre150d0 = pd.to_numeric(df_staging.rre150d0, errors="coerce")
df_staging = df_staging[df_staging['abbr'].isin(stations)]

# In Abhaengigkeit des Tages die Daten filtern

# Tag 1-5: Vormonat anhand taeglichen Daten, aktueller Monat anhand taeglichen Daten
if today < 6:
    df_staging = df_staging[df_staging.time >= last_month_first_day.strftime('%Y-%m-%d')]
    
    
# Tag 6-31: Vormonat anhand monatlichen Daten, aktueller Monat anhand taeglichen Daten
else:
    df_staging = df_staging[df_staging.time >= this_month_first_day.strftime('%Y-%m-%d')]
    
    
# Zuerst pro Station und Monat summieren
df_month = df_staging.groupby([df_staging.time.dt.month, df_staging.time.dt.year, df_staging.abbr])['rre150d0'].sum().to_frame()
# rename MultiIndex damit man index reseten kann
df_month.index.set_names(['Monat', 'Jahr', 'abbr'], inplace=True)
df_month.reset_index(inplace=True)
# Nun pro Monat ueber alle Stationen mitteln
df_month = df_month.groupby([df_month.Monat, df_month.Jahr])['rre150d0'].mean().to_frame()
df_month.reset_index(inplace=True)
df_month['Datum'] = pd.to_datetime(dict(year=df_month.Jahr, month=df_month.Monat, day="01"))
df_month.rename(columns={"rre150d0": "Niederschlag_CH_gemessen_mean"}, inplace=True)
df_month = df_month[["Datum", "Niederschlag_CH_gemessen_mean", "Monat"]].copy()

# Hinzufuegen zu df_history
df_history = pd.concat([df_history, df_month])


###############
# Join der monatlichen Daten und der Normwerte der Kalendermonate
###############

df = df_history.join(df_norm, on='Monat', validate='m:1', lsuffix='_caller', rsuffix='_other')
df.drop(columns=['Monat'], inplace=True)
df["Niederschlag_CH_gemessen_relativ_zu_Norm"] = round(df["Niederschlag_CH_gemessen_mean"]/df["Niederschlag_CH_Norm_mean"]*100,1)
df["Niederschlag_CH_norm_relativ"] = 100

df = df.tail(14)

# Test-Plot 1
#df[["Datum", 
#    "Niederschlag_CH_gemessen_relativ_zu_Norm", 
#    "Niederschlag_CH_norm_relativ"]].plot(kind="bar", 
#                                          xlabel="Monat",
#                                          ylabel="%",
#                                          x="Datum",
#                                          figsize=(15,5),
#                                          title="Niederschlag Schweiz (Monatssumme) im Vergleich zur Norm")
#plt.show()

df_plot = df.copy()
df_plot = df_plot[["Datum", "Niederschlag_CH_gemessen_relativ_zu_Norm"]]
#df_plot["Differenz_zu_Norm_Prozent"] = round(df_plot["Niederschlag_CH_gemessen_relativ_zu_Norm"]-100,1)
df_plot["Differenz_zu_Norm_Prozent"] = df_plot["Niederschlag_CH_gemessen_relativ_zu_Norm"]

if today == 1:
    diff_ist_soll = df_plot["Niederschlag_CH_gemessen_relativ_zu_Norm"].iloc[-1] - (100/30*today)
else:
    diff_ist_soll = df_plot["Niederschlag_CH_gemessen_relativ_zu_Norm"].iloc[-1] - (100/30*(today-1))

df_plot["Trend"] = np.nan  
df_plot["TrendRating"] = np.nan

# Trend
s=pd.Series([-1000,-25,-10,10,25,1000])
trendNumber = len(s)
Trend = pd.cut([diff_ist_soll], s, trendNumber, labels=["down_strong", "down_mild", "neutral", "up_mild", "up_strong"])
TrendRating = pd.cut([diff_ist_soll], s, trendNumber, labels=["negativ", "negativ", "neutral", "positiv", "positiv"], ordered=False)

df_plot.iloc[-1, df_plot.columns.get_loc('Trend')] = Trend
df_plot.iloc[-1, df_plot.columns.get_loc('TrendRating')] = TrendRating

#df_plot.drop(columns={"soll"}, inplace=True)

df_plot.drop_duplicates(subset=['Datum'], keep='last', inplace=True)

df_plot2 = df_plot.drop(columns={"Differenz_zu_Norm_Prozent"})

# Test-Plot 2
# data
#threshold = 100
#values = df_plot["Niederschlag_CH_gemessen_relativ_zu_Norm"]
#x = range(len(values))

# split it up
#above_threshold = np.maximum(values - threshold, 0)
#below_threshold = np.minimum(values, threshold)

# and plot it
#fig, ax = plt.subplots()
#ax.bar(x, below_threshold, 0.8, color="#964B00")
#ax.bar(x, above_threshold, 0.8, color="blue",
#        bottom=below_threshold)

#fig.set_size_inches(15, 5)

# horizontal line indicating the threshold
#ax.plot([-1, 14], [threshold, threshold], "k--")

#ax.set_title('Niederschlag Schweiz (Monatssumme) im Vergleich zur Norm')
#ax.set_xlabel('Monat')
#ax.set_ylabel('%')
#plt.show()

# write kpi-wetter-1_meteoswiss_temp_prognose.csv
df_plot.to_csv(output, index=False)
df_plot2.to_csv(output2, index=False)
