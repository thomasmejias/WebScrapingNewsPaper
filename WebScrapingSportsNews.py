from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

#Function Set Up Chrome Driver
def setUpDriver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

#Function Close the Website
def closeWebsite(driverWebsite):
    driverWebsite.quit()

#Function where charge all the pages with the news of the last month
def getInfoWebsite(driverWebsite):
    driverWebsite.get("https://www.lateja.cr/deportes/")
    time.sleep(3)

    currentMonth = "05 de julio 2025"
        
    continueCycle = True
    clics = 0

    while continueCycle: 

        html_content = driverWebsite.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        dateNew = soup.find_all('time')

        for date in dateNew:
            dateText = date.get_text(strip=True)

            if(currentMonth in dateText):
                continueCycle = False

        try:
            buttonWebsite = WebDriverWait(driverWebsite, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ver más')]"))
            )
            buttonWebsite.click()
            clics += 1
            #time.sleep(10)
        except:
            continueCycle = False

    appendInfoToLists(driverWebsite,soup)

#Function which extract all the sports news from lateja newspaper and saved on the CSV File
def appendInfoToLists(driverWebsite,contentWebsite):
    listNews = []
    listDates = []
    listAuthors = []

    titlesLG = contentWebsite.find_all('a', class_='lg-promo-headline')
    titlesH3 = contentWebsite.find_all('h3', class_='c-heading headline-text')
    authorA = contentWebsite.find_all('span', class_='ts-byline__names')
    dateNew = contentWebsite.find_all('time')
    
    for author in authorA:
        listAuthors.append(author.text.strip())

    for titleLG in titlesLG:
        listNews.append(titleLG.text.strip())

    for titleH3 in titlesH3:
        listNews.append(titleH3.text.strip())

    for date in dateNew:
        listDates.append(date.get_text(strip=True))
    
    createCSV(listAuthors, listNews, listDates)
    closeWebsite(driverWebsite)

#Function which Create a CSV File
def createCSV(vListAuthors, vListNews, vListDates):

    min_len = min(len(vListNews), len(vListDates), len(vListAuthors))

    infoNews = []
    for i in range(min_len):
        infoNews.append({
            'New': vListNews[i],
            'Date': vListDates[i],
            'Author': vListAuthors[i]
        })

    df = pd.DataFrame(infoNews)
    df.to_csv('news_website.csv', index=False, encoding='utf-8-sig')