# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 08:28:01 2017

@author: Ania
"""

import datetime 
import getopt
import os
from glob import glob
import string
import sys
import re
import logging
import os.path
import urllib.request
from bs4 import BeautifulSoup as BS
import math



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
            data=i.find(itemprop="datePosted").string
            if i.find(class_='label superOfferLabel'):
                sponsored='true'
            else:
                sponsored='false'
            snippet=i.find(class_="o-list_item_text_details clearfix acc_cnt").string
            job_title=i.find(class_="o-list_item_link_name").string
            salary=i.find(class_="label salaryLabel")
            if salary:
                salary=salary.string
            else:
                salary=''
            get_data(link)
                
            
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
    employ_type = soup.find('span', attrs={'itemprop':'employmentType'}).text
    date_posted = soup.find('span', attrs={'itemprop':'datePosted'}).string
    validThrough = soup.find('span', attrs={'itemprop':'validThrough'}).string
    company_description = soup.find('div', attrs={'id':'company'}).text
    offer_description = soup.find('div', attrs={'id':'description'}).text
    
    
    
    
if __name__ == "__main__":
    main()