# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:13:06 2018

@author: Ania
"""


import pyodbc

#conn = pyodbc.connect(
#    r'DRIVER={ODBC Driver 13 for SQL Server};'
#    r'SERVER=ud-project.database.windows.net;'
#    r'DATABASE=UD_Project;'
#    r'UID=ud_admin@ud-project;'
#    r'PWD=aoud_project!1311'
#    )

conn = pyodbc.connect(
    r'DRIVER={Devart ODBC Driver for PostgreSQL};'
    r'SERVER=localhost;'
    r'DATABASE=Aoud;'
    r'UID=postgres;'
    r'PORT=5432;'
    r'PWD=sosna3894'
    )

cursor = conn.cursor()


#create_table_main = """
#    CREATE TABLE MAIN(
#            ID int NOT NULL PRIMARY KEY,
#            LINK VARCHAR(300),
#            LOCATION VARCHAR(20),
#            LAT VARCHAR(20),
#            LONG VARCHAR(20),
#            COMPANY VARCHAR(100),
#            TITLE VARCHAR(300),
#            EMPLOY_TYPE VARCHAR(200),
#            DATE_BEGIN DATE,
#            DATE_END DATE,
#            DATE_VALID DATE,
#            SALARY VARCHAR(50),
#            SPONSORED BOOLEAN,
#            LANGUAGE CHAR(2),
#            KEYWORDS VARCHAR(400),
#            SNIPPET VARCHAR(400),
#            COMPANY_DES VARCHAR(2000),
#            OFFER_DES VARCHAR(2000))
#    """
#    
#    
#create_table_query = textwrap.dedent("""
#    CREATE TABLE QUERY(
#            ID INT REFERENCES MAIN(ID),
#            QUERY VARCHAR (150))
#    """)
    
create_table_new_offers = """
    CREATE TABLE NEW_OFFERS(
            ID int NOT NULL PRIMARY KEY,
            LINK VARCHAR(300),
            LOCATION VARCHAR(20),
            LAT VARCHAR(20),
            LONG VARCHAR(20),
            QUERY VARCHAR(300),
            COMPANY VARCHAR(100),
            TITLE VARCHAR(300),
            EMPLOY_TYPE VARCHAR(200),
            DATE_BEGIN DATE,
            DATE_VALID DATE,
            SALARY VARCHAR(50),
            SPONSORED BOOLEAN,
            LANGUAGE CHAR(2),
            KEYWORDS VARCHAR(400),
            SNIPPET VARCHAR(400),
            COMPANY_DES VARCHAR(2000),
            OFFER_DES VARCHAR(2000))
    """
    
#cursor.execute(create_table_main)
#conn.commit()
#cursor.execute(create_table_query)
#conn.commit()

cursor.execute(create_table_new_offers)
#cursor.execute('DROP TABLE NEW_OFFERS')
conn.commit()


