# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:17:19 2018

@author: Ania
"""

import pyodbc
import datetime
import parse_text

server = 'ud-project.database.windows.net' 
database = 'UD_Project' 
username = 'ud_admin@ud-project' 
password = '95f6d74684f884b4d841e5b9b700!' 

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};'
    r'SERVER='+server+';'
    r'DATABASE='+database+';'
    r'UID='+username+';'
    r'PWD='+password, autocommit = True
    )


cursor = conn.cursor()

cursor1 = conn.cursor()
    

sql_end_date = """ update MAIN 
    set DATE_END = ?
    where MAIN.id not in (
            select id  
            from new_offers) 
    and DATE_END is null """

cursor.execute(sql_end_date,datetime.datetime.now().date())



select_data_sql = """SELECT 
        NEW_OFFERS.ID,NEW_OFFERS.LINK,NEW_OFFERS.LOCATION,NEW_OFFERS.LAT,
        NEW_OFFERS.LONG,NEW_OFFERS.COMPANY,NEW_OFFERS.TITLE,
        NEW_OFFERS.EMPLOY_TYPE,NEW_OFFERS.DATE_BEGIN,NEW_OFFERS.DATE_VALID,
        NEW_OFFERS.SPONSORED,NEW_OFFERS.LANGUAGE,NEW_OFFERS.KEYWORDS,
        NEW_OFFERS.OFFER_DES 
        FROM NEW_OFFERS 
        LEFT JOIN MAIN 
        ON NEW_OFFERS.ID=MAIN.ID WHERE MAIN.ID IS NULL"""
        
cursor.execute(select_data_sql)
sql_insert= """ INSERT INTO 
    MAIN (ID,LINK,LOCATION,LAT,LONG,COMPANY,
    TITLE,EMPLOY_TYPE,DATE_BEGIN,DATE_VALID,
    SPONSORED,LANGUAGE, KEYWORDS,OFFER_DES) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

for row in cursor.fetchall():
    cursor1.execute(sql_insert,(row.ID,row.LINK,row.LOCATION,row.LAT,row.LONG,row.COMPANY,row.TITLE, row.EMPLOY_TYPE, row.DATE_BEGIN, row.DATE_VALID, row.SPONSORED, row.LANGUAGE, row.KEYWORDS, row.OFFER_DES))
    parse_text.main(row.ID, row.OFFER_DES)



sql_update_query = """ INSERT INTO QUERY (id,query)
                        SELECT NEW_OFFERS.id,NEW_OFFERS.query FROM NEW_OFFERS
                        LEFT JOIN QUERY 
                        ON NEW_OFFERS.ID=QUERY.ID
                        AND
                        NEW_OFFERS.QUERY=QUERY.QUERY
                        WHERE QUERY.ID IS NULL"""
                        
cursor.execute(sql_update_query)