from oauth2client.service_account import ServiceAccountCredentials
import re
import time
import gspread
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
GOOGLE_SHEET_SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds = [ServiceAccountCredentials.from_json_keyfile_name('test-key.json', GOOGLE_SHEET_SCOPE)]
credentials = creds[0]
client = gspread.authorize(credentials)
SHEET = client.open('api').sheet1 # worksheet('Sheet_name')
print("Authorisation Successful Moving to Scraper")
#Scraper Function for getting emails for the company
def cin(text):
    text=str(text)
    abc=re.sub(' ','+',text)
    url='https://www.quickcompany.in/company?q='
    link=url+abc
    page=requests.get(link)
    content=soup(page.content,'html.parser')
    cin=content.findAll('div',attrs={'class':'lighter'})
    if len(cin)>0:
        bc=cin[0].text
        bc=re.sub('CIN: ','',bc)
    else:
        bc=str(cin)
    web='https://www.zaubacorp.com/company//'
    link=web+bc
    page=requests.get(link)
    content=soup(page.content,'html.parser')
    para=content.text
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", para)
    if len(emails)>0:
        mail=emails[0]
    else:
        mail=str(emails)
    return mail



# The Main Data Scraper
def main():
    q=int(input("Type No of pages to be Scrapped="))
    print("Scraper is on the Process please wait")
    url='https://www.myamcat.com/jobs/page/'
    a=b=c=d=e=f=2
    for i in range(1,(q+1),1):
        we=i
        abc=url+str(i)
        page=requests.get(abc)
        content=soup(page.content,'html.parser')
        Job=content.findAll('a',attrs={'class':'profile-name'})
        Comp=content.findAll('div',attrs={'class':'company_name'})
        Sal=content.findAll('span',attrs={'class':'jobText'})
        for i in range(1,len(Job),1):
            abc=Job[i].text
            bc=re.sub("\n",' ',abc)
            SHEET.update_cell(a,1, bc)
            a=a+1
            time.sleep(0.5)
        time.sleep(1)
        
        for i in range(5,len(Sal),3):
            loc=Sal[i].text
            SHEET.update_cell(b,2, loc)
            b=b+1
            time.sleep(0.5)
        time.sleep(1)
        for i in range(3,len(Sal),3):
            Dur=Sal[i].text
            SHEET.update_cell(c,3, Dur)
            c=c+1
            time.sleep(0.5)
        time.sleep(1)
        for i in range(4,len(Sal),3):
            sal=Sal[i].text
            SHEET.update_cell(d,4, sal)
            d=d+1
            time.sleep(0.5)
        for i in range(1,len(Comp),1):
            abc=Comp[i].text
            bc=re.sub("\n",' ',abc)
            SHEET.update_cell(e,5, bc)
            e=e+1
            email=cin(bc)
            SHEET.update_cell(f,6, email)
            f=f+1
            time.sleep(0.5)
        print('Successfully Scraped Page No is:',we)
        time.sleep(2)

if __name__ == '__main__':
    main()
