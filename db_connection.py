# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 21:13:06 2018

@author: Ania
"""


import pyodbc

server = 'ud-project.database.windows.net' 
database = 'UD_Project' 
username = '' 
password = '' 

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};'
    r'SERVER='+server+';'
    r'DATABASE='+database+';'
    r'UID='+username+';'
    r'PWD='+password, autocommit = True
    )

cursor = conn.cursor()

cursor.execute("DROP TABLE QUERY")
cursor.execute("DROP TABLE MAIN")
cursor.execute("DROP TABLE NEW_OFFERS")


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
            SPONSORED BIT,
            LANGUAGE CHAR(2),
            KEYWORDS VARCHAR(400),
            OFFER_DES VARCHAR(8000))
    """
    
jobs = """CREATE TABLE Jobs (
  job_id          INT NOT NULL,
  salary_low      INT,
  salary_up       INT,
  salary_currency VARCHAR(10),
  contract_type   VARCHAR(20),
  relocate        INT,
  PRIMARY KEY (job_id),
  FOREIGN KEY (job_id) REFERENCES MAIN (ID)
)"""

JobResp = """CREATE TABLE JobResps (
  job_id INT         NOT NULL,
  resp   VARCHAR(50) NOT NULL,
  PRIMARY KEY (job_id, resp),
  FOREIGN KEY (job_id) REFERENCES Jobs (job_id)
)"""

JobQuals = """CREATE TABLE JobQuals (
  job_id INT         NOT NULL,
  qual   VARCHAR(50) NOT NULL,
  PRIMARY KEY (job_id, qual),
  FOREIGN KEY (job_id) REFERENCES Jobs (job_id)
)"""


JobTechs ="""CREATE TABLE JobTechs (
  job_id INT         NOT NULL,
  tech   VARCHAR(50) NOT NULL,
  PRIMARY KEY (job_id, tech),
  FOREIGN KEY (job_id) REFERENCES Jobs (job_id)
)"""

cursor.execute(create_table_main)
cursor.execute(create_table_query)
cursor.execute(create_table_new_offers)
cursor.execute(jobs)
cursor.execute(resp)
cursor.execute(qual)
cursor.execute(JobResp)
cursor.execute(JobQuals)
cursor.execute(JobTechs)



