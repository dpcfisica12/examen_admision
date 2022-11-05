from django.http import HttpResponse
import pandas as pd
import sqlite3
def read():
    cnx = sqlite3.connect('examen_admision/db.sqlite3')
    df_season = pd.read_sql_query("SELECT * FROM SEASON", cnx)
    df_customer_order = pd.read_sql_query("SELECT * FROM Customer_Order", cnx)
    df_detecting_change = pd.read_sql_query("SELECT * FROM Detecting_Change", cnx)
    return df_season, df_customer_order, df_detecting_change


def Season(df):
    df = df[['ORDER_ID','ORDER_DT']]
    df['ORDER_DT'] = pd.to_datetime(df['ORDER_DT'])
    def season_of_date(date_UTC):
        year = str(date_UTC.year)
        seasons = {'spring': pd.date_range(start= year +'-03-19 00:00:00', end=year + '-06-19 00:00:00'),
                'summer': pd.date_range(start= year + '-06-20 00:00:00', end= year + '-09-21 00:00:00'),
                'fall': pd.date_range(start= year + '-09-23 00:00:00', end= year + '-12-20 00:00:00')}
        if date_UTC in seasons['spring']:
            return 'spring'
        if date_UTC in seasons['summer']:
            return 'summer'
        if date_UTC in seasons['autumn']:
            return 'fall'
        else:
            return 'winter'

    df['season'] = df.Date.map(season_of_date)
    return HttpResponse(df)

def Customer_Order(df):
    df = df.drop_duplicates(subset=['order_number','status'])
    def func(x):
        if x == 'PENDING':
            return 2
        elif x == 'SHIPPED':
            return 1
        elif x == 'CANCELED':
            return 0
    def func_inversa(x):
        if x >1 :
            return 'PENDING'
        elif x == 1:
            return 'SHIPPED'
        elif x == 0:
            return 'CANCELED'
    df['status_number'] = df['status'].apply(func)
    df = df.groupby(by='order_number').sum()
    df['order_number'] = df.index
    df['status'] = df['status_number'].apply(func_inversa)
    return HttpResponse(df)

def detecting_changes(df):
    df['C'] = df['was_rainy'].diff()
    df = df[df['C']==True]
    df = df[['date','was_rainy']]
    return HttpResponse(df)

def run():
    df_season, df_customer_order, df_detecting_change = read()
    Season(df_season)
    Customer_Order(df_customer_order)
    detecting_changes(df_detecting_change)
