from cProfile import run
from datetime import datetime
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .functions import getNextPageUrl, getPage, getPostsFromPage, Threads
from .dtb import dtb

def runScrap(_siteid):
    # global siteid
    # siteid = _siteid
    print(_siteid)
    scrap_limit = 0
    URL = "https://community.o2.co.uk/t5/Discussions-Feedback/bd-p/4"
    domain = urlparse(URL).netloc
    page = requests.get(URL)
    pageContent = BeautifulSoup(page.content, "html.parser")

    all_threads = []

    Threads.objects.all().delete()

    # On récupere le chemin de la page
    currentPagePath   = urlparse(URL).path
    
    while  scrap_limit != 4:
        threads = []
        print('\niteration: ', scrap_limit, ' ', currentPagePath)
        currentPage   = getPage(domain, currentPagePath)
        threads.append(getPostsFromPage(currentPage))
        currentPagePath   = urlparse(getNextPageUrl(currentPage)).path
        scrap_limit = scrap_limit + 1
        all_threads.append(threads)



    print("the scrapping task is finished")
