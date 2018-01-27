# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:17:19 2018

@author: Ania
"""

import pyodbc
import datetime

server = 'ud-project.database.windows.net' 
database = 'UD_Project' 
username = 'ud_admin@ud-project' 
password = '' 

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};'
    r'SERVER='+server+';'
    r'DATABASE='+database+';'
    r'UID='+username+';'
    r'PWD='+password, autocommit = True
    )


cursor = conn.cursor()


sql_end_date = """ update MAIN 
    set DATE_END = ?
    where MAIN.id not in (
            select id  
            from new_offers) 
    and DATE_END is null """

cursor.execute(sql_end_date,datetime.datetime.now().date())



select_data_sql = 'SELECT * FROM NEW_OFFERS LEFT JOIN MAIN ON NEW_OFFERS.ID=MAIN.ID'
cursor.execute(select_data_sql)
sql_insert= """ INSERT INTO MAIN (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
for row in cursor.fetchall():
    cursor.execute(sql_insert,(row.ID,row.LINK,row.LOCATION,row.LAT,row.LONG,row.COMPANY,row.TITLE, row.EMPLOY_TYPE, row.DATE_BEGIN, None, row.DATE_VALID, row.SALARY, row.SPONSORED, row.LANGUAGE, row.KEYWORDS, row.OFFER_DES))




sql_update_query = """ INSERT INTO QUERY (id,query)
                        SELECT NEW_OFFERS.id,NEW_OFFERS.query FROM NEW_OFFERS
                        LEFT JOIN QUERY 
                        ON NEW_OFFERS.ID=QUERY.ID
                        AND
                        NEW_OFFERS.QUERY=QUERY.QUERY """
                        
cursor.execute(sql_update_query)