# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 08:28:01 2017

@author: Ania
"""

import getopt
import os
from glob import glob
import sys
import os.path
import urllib.request
from bs4 import BeautifulSoup as BS
from langdetect import detect
import pyodbc 
import datetime


def main():
    query = "it - rozwoj oprogramowania"
    location = "wroclaw"
    cc = '5016'
    URL="https://www.pracuj.pl/praca/{0};wp/{1};cc,{2}"
    try:
        opts, args = getopt.getopt(sys.argv[1:],"q:l:c:")
    except getopt.GetoptError:
        print ("pracujjobsearch.py -q <query> -l <location> -c <cc>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-q"):
            query = arg
        elif opt in ("-l"):
            location = arg
        elif opt in ("-c"):
            cc = arg
    url = URL.format(location,query.replace(" ","%20"),cc)
    print(url)
    Next_page = True
    
    while Next_page:
        try:
            wp=urllib.request.urlopen(url)
            html=BS(wp,'html.parser')
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            Next_page = False
        parse_html(html,query,location)
        pom = html.find_all('li',class_='desktopPagin_item')
        try:
            url = "https://www.pracuj.pl" + pom[-1].find('a').get('href')
            print(url)
        except:
            Next_page = False


def parse_html(soup,query,location):
    soup=soup.find_all('li', class_='o-list_item')
    for i in soup:
            id=i.find(class_='o-list_item_link_name').get('data-gtm-offer')
            link="https://www.pracuj.pl"+i.find(class_='o-list_item_link_name').get('href')
            company=i.find(class_='o-list_item_link_emp o-list_item_link_emp--hover seolink').string
            if i.find(class_='label superOfferLabel'):
                sponsored= True
            else:
                sponsored= False 
            job_title=i.find(class_="o-list_item_link_name").string
            salary=i.find(class_="label salaryLabel")
            if salary:
                salary=salary.string
            else:
                salary=''
            keywords,lat,long,employ_type,date_posted,validThrough,offer_description,language = get_data(link)
            if language=='en':
                save_to_database(id,link,location,lat,long,query,company,job_title,employ_type,date_posted,validThrough,salary,sponsored,language,keywords,offer_description)
            
            
def get_data(link):
    try:
        wp = urllib.request.urlopen(link)
        html = BS(wp, 'html.parser')
    except:
        print("Unexpected error:", sys.exc_info()[0])
    keywords = html.find('meta', attrs={'name':'Keywords'}).get('content')
    soup = html.find('div', class_='main')
    adress = soup.find('span', attrs={'class':'o-main__right_offer_cnt_details_item_text ico-location latlng'})
    lat = adress.get('data-lat')
    long = adress.get('data-lng')
    employ_type = soup.find('span', attrs={'itemprop':'employmentType'}).text.replace('\n',' ')
    date_posted = soup.find('span', attrs={'itemprop':'datePosted'}).text
    if '.' in date_posted:
        date_posted = datetime.datetime.strptime(date_posted, "%d.%m.%Y" )
    else:
        date_posted = datetime.datetime.strptime(date_posted, "%Y-%m-%d" )
    validThrough = soup.find('span', attrs={'itemprop':'validThrough'}).string.replace(')','')
    if '.' in validThrough:
        validThrough = datetime.datetime.strptime(validThrough, "%d.%m.%Y" )
    else:
        validThrough = datetime.datetime.strptime(validThrough, "%Y-%m-%d" )
    offer_description = soup.find('div', attrs={'id':'description'})
    if offer_description:
        offer_description = offer_description.text
    else:
        offer_description = soup.find('div', attrs={'class':'o-main__left_table uploaded'}).text
    try:
        language = detect(offer_description)
    except:
        language = '0'
    return keywords,lat,long,employ_type,date_posted,validThrough,offer_description,language

    
def save_to_database(id,link,location,lat,long,query,company,job_title,employ_type,date_posted,validThrough,salary,sponsored,language,keywords,offer_description):
    
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
    insert_data_sql = '''INSERT into NEW_OFFERS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    try:
        cursor.execute(insert_data_sql,(id,link,location,lat,long,query,company,job_title,employ_type,date_posted,validThrough,salary,sponsored,language,keywords,offer_description))    
    except:
        pass
    
if __name__ == "__main__":
    main()