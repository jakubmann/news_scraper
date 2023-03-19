from bs4 import BeautifulSoup
import urllib.request, sys, time
import requests
import pandas as pd

def getArticleList(url):
    articlelist = getPage(url)
    if articlelist:
        soup = BeautifulSoup(articlelist.text, 'xml')
        return soup.find_all('loc') 
    return False

def getPage(url):
    try:
        page = requests.get(url)
        return page
    except Exception:
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
        print ('error for ',url)
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
        return False

def getArticleText(rawText, source):
    soup = BeautifulSoup(rawText, 'html.parser')
    text = ''
    match source:
        case 'denikn':
            paragraphs = soup.find_all('p')
        case 'seznamzpravy':
            paragraphs = soup.find_all('p', class_='e_ae')
        case 'idnes':
            paragraphs = soup.find_all('div', class_='opener')
            paragraphs.append(soup.find_all('div', class_='bbtext'))
        case _:
            return
    for paragraph in paragraphs:
        text += paragraph.text.strip() + '\n'
    return text

def writeFile(filename, articlelist):
    with open(filename, 'w', encoding='utf-8') as file:
        for articleUrl in articlelist:
            page = getPage(articleUrl.text.strip())
            if (page):
                #print(page.text)
                file.write(getArticleText(page.text, 'denikn'))
            print(articleUrl.text.strip())


denikn = getArticleList('https://static.novydenik.com/sitemap.year.2023.xml')
seznamzpravy = getArticleList('https://www.seznamzpravy.cz/sitemaps/sitemap_articles_0.xml')
idnes = getArticleList('https://www.idnes.cz/zpravy/sitemap')


'''
if idnes:
    for articleUrl in idnes:
        page = getPage(articleUrl.text.strip())
        if (page):
            print(getArticleText(page.text, 'idnes'))
  '''

if denikn:
    writeFile('denikn.txt', denikn)
