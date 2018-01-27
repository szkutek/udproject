# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:13:06 2018

@author: Ania
"""


import pyodbc

server = 'ud-project.database.windows.net' 
database = 'UD_Project' 
username = 'ud_admin@ud-project' 
password = 'aoud_project!1311' 

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};'
    r'SERVER='+server+';'
    r'DATABASE='+database+';'
    r'UID='+username+';'
    r'PWD='+password, autocommit = True
    )

cursor = conn.cursor()


create_table_main = """
    CREATE TABLE MAIN(
            ID int NOT NULL PRIMARY KEY,
            LINK VARCHAR(300),
            LOCATION VARCHAR(20),
            LAT VARCHAR(20),
            LONG VARCHAR(20),
            COMPANY VARCHAR(100),
            TITLE VARCHAR(300),
            EMPLOY_TYPE VARCHAR(200),
            DATE_BEGIN DATE,
            DATE_END DATE,
            DATE_VALID DATE,
            SALARY VARCHAR(50),
            SPONSORED BIT,
            LANGUAGE CHAR(2),
            KEYWORDS VARCHAR(400),
            OFFER_DES VARCHAR(8000))
    """
    
create_table_query = """
    CREATE TABLE QUERY(
            ID INT,
            QUERY VARCHAR (150),
            PRIMARY KEY (ID, QUERY),
            CONSTRAINT FK_QueryID FOREIGN KEY (ID)
            REFERENCES MAIN(ID))
    """
    
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
            SPONSORED BIT,
            LANGUAGE CHAR(2),
            KEYWORDS VARCHAR(400),
            OFFER_DES VARCHAR(8000))
    """
    
cursor.execute(create_table_main)
cursor.execute(create_table_query)
cursor.execute(create_table_new_offers)




