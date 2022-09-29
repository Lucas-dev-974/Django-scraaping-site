from asyncio.windows_events import NULL
from datetime import date, datetime
import requests
import Site.ScrapCore.functions as fn
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from Site.ScrapCore.dtb import dtb

from .Scrapper import Scrapper

db = dtb()


URL = "https://community.o2.co.uk/t5/Discussions-Feedback/bd-p/4"
domain = urlparse(URL).netloc
page = requests.get(URL)

pageContent = BeautifulSoup(page.content, "html.parser")

all_threads = []

# On récupere le chemin de la page
currentPagePath   = urlparse(URL).path


compteur = 0



#TODO mettre cette boucle dans une fonction pour l'appeler avec les boutons scrap
"""while  compteur != 1:
    threads = []
    print('\niteration: ', compteur, ' ', currentPagePath)
    currentPage   = fn.getPage(domain, currentPagePath)
    
    threads.append(fn.getPostsFromPage(currentPage)['threads'])

    currentPagePath   = urlparse(fn.getNextPageUrl(currentPage)).path
    compteur = compteur + 1
    all_threads.append(threads)

print("the scrapping task is finished")"""



def saveThread(thread, is_reply=False):
    
    author           = thread['author']
    content          = thread['content']
    # publication_date = thread['publication_date']
    scrapped_date    = thread['scrapped_date']


    pb_date = thread['publication_date'][1:].split('-')
    pb_converted_to_datetime = datetime(int(pb_date[2]), int(pb_date[1]), int(pb_date[0]))
    if is_reply == False:
        title     = thread['title']
        target_id = 1
        number_of_replys = 0

        thread_id = dtb().insert('Site_threads', {
            'target_id_id': target_id,
            'title': title,
            'number_of_replys': number_of_replys,
            'author':  author,
            'content': content.replace("'", "''"),
            'publication_date': pb_converted_to_datetime,
            'scrapped_date': datetime.now(),
        })

        for reply in thread['replys']:
            reply['thread_id_id'] = thread_id
            saveThread(reply, True)
    else:
        thread_id = dtb().insert('Site_threads_replys', {
            'thread_id': thread['thread_id_id'],
            'author':  author,
            'content': content.replace("'", "''"),
            'publication_date': pb_converted_to_datetime,
            'scrapped_date': datetime.now(),
        })
    # if 'replys' in thread:
    #     reply = thread['replys']

    # print(thread['title'])
    # dtb().insert('threads', {
    #     'target_id': 1,
        
    # })

"""jsonThread = fn.JsonEncoder(all_threads)

decodedJsonThreadsPerPage = fn.JsonDecode(jsonThread)[0] # Get the first page
# print(decodedJsonThreadsPerPage)
for page in decodedJsonThreadsPerPage:
    print('\n')
    for thread in page:
        saveThread(thread)"""

