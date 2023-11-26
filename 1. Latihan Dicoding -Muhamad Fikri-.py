# -*- coding: utf-8 -*-
"""Templat-notebook

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmO3zH1wimHqQKx7wbt_tP_-Tazhl58x

# Proyek Analisis Data: Nama dataset
- Nama: Muhamad Fikri
- Email: fikrimuhammadhilabi@gmail.com
- Id Dicoding:

## Menentukan Pertanyaan Bisnis

- pertanyaan 1 Berapa Banyak Pinjaman sepeda per Season?
- pertanyaan 2 Bagaimana perbandingan antara pinjaman di tahun 2011 dan 2012?

## Menyaipkan semua library yang dibuthkan
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""## Data Wrangling

### Gathering Data
"""

df = pd.read_csv('hour.csv')
df

"""### Assessing Data"""

df.isnull()

df.duplicated().sum()

"""### Cleaning Data"""

df.rename(columns={
    'dteday' : 'date',
    'hr' : 'hour',
    'yr' : 'year',
    'mnth' : 'month',
},inplace=True)

df

df['datetime'] = df['date'] + " "+ df['hour'].astype(str).str.zfill(2) + ":00"
df['datetime'] = pd.to_datetime(df['datetime'])
df

df = df.drop(columns = ['date','instant'])
df

df['holiday'] = df['holiday'].map({0:False, 1 :True})
df['temp'] = df['temp'] * (39 - (-8)) + -8
list_waktu = pd.date_range(df['datetime'].min(),df['datetime'].max(),freq='1H')
list_waktu

kolom_waktu_lengkap = pd.DataFrame(list_waktu,columns=['datetime'])
kolom_waktu_lengkap

df = kolom_waktu_lengkap.merge(df,on=['datetime'],how='left')
df

# Mengisi missing value dengan nilai konstant
df['cnt'] = df['cnt'].fillna(0)

# Mengisi missing value dengan nilai di baris sebelumnya
df['temp'] = df['temp'].fillna(method ='ffill')

# Mengisi missing value dengan series
df['hour'] = df['hour'].fillna(df['datetime'].dt.hour)

df[df['casual'].isna()]

seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring', 6: 'Summer',
           7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 11: 'Fall', 12: 'Winter'}
df['season'] = df['datetime'].dt.month.map(seasons)
df

"""## Exploratory Data Analysis (EDA)

### Explore ...
"""

df.describe()

df.hist()

"""## Visualization & Explanatory Analysis

### Pertanyaan 1:
"""

pip install streamlit

import streamlit as st

st.title('My Streamlit App')
st.write('This is a Streamlit app running in Jupyter Notebook.')
season = st.selectbox("Select season:", ['Spring','Summer','Fall','Winter'])
df_plot = df.groupby(['year','season'])['registered'].sum().unstack()[['Spring','Summer','Fall','Winter']]
ax = df_plot.plot(kind='bar',color=['#D6F1C6','#F9CC87','#FF7F00','#C9F1FD'])


ax.set_title('Banyaknya peminjaman sepeda\nberdasarkan tahun dan musim')
ax.set_xlabel("Tahun")
ax.set_ylabel("Peminjaman Total")

ax.set_xticks([0,1],labels = ['2011','2012'],rotation = 45)
ax.set_yticks(np.arange(0,1000000,100000));

"""### Pertanyaan 2:"""

df.groupby(['year','month'])['registered'].sum().unstack().transpose().plot(kind='line')
ax.set_xlabel("Tahun")
ax.set_ylabel("Peminjaman Total")

"""## Conclusion

- Conclution pertanyaan 1
- conclution pertanyaan 2

Paling banyak pinjaman sepada pada musim Summer, kedua Fall, ketiga Spring, dan terakhir Winter.

Perpinjaman sepeda pada tahun 2012 meningkat dari tahun 2011.
"""