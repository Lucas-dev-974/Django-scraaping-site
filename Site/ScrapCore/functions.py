from io import StringIO
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlunparse
import datetime


def getPage(domain, url_path):
    page_url = urlunparse(('https', domain, url_path, "", "", "")) # construct the url to access the posts for each thread
    page = requests.get(page_url)
    souped_page = BeautifulSoup(page._content, "html.parser")
    return souped_page

def getPostsFromPage(pageContent):
    # On instancie un tableaux qui vas contenir tous les postes de la page
    threads = []
    # print(pageContent)
    # On récupere tout les poste via le tag: article et la class: custom-message-tile 
    thread_results = pageContent.find_all("article", class_="custom-message-tile") #piege ici
    print(len(thread_results))
    # boucle sur les article récuperer
    iteration = 0
    # for thread in thread_results:
    # while iteration != 2:
    #     first_element = thread_results[iteration].find("div") # get first children - the div
    #     link          = first_element.find("a")
        
    #     title = link["title"] # get the title and save it 
    #     url   = link["href"] # get the link towards the post of the thread 
    #     domain = pageContent.find('meta', property='og:site_name')['content']
        
    #     threads.append(getParsedauthorThreadsAndReplys(title, domain, url)) 
    #     iteration += 1

    # datas = {
    #     'threads': threads,
    #     'nb_of_scrapp': iteration
    # }
    # return datas

def getNextPageUrl(page):
    page_navigation_component = page.find(class_ = "lia-paging-pager")
    next_page = page_navigation_component.find('li', class_="lia-paging-page-next")
    
    if len(next_page) == 0:
        return None
        
    next_page_link_component = next_page.find("a")
    
    if not next_page_link_component:
        return None

    # print(next_page_link_component)
    next_page_url =  next_page_link_component['href']
    # print(next_page_url)
    
    return next_page_url
    
def getParsedauthorThreadsAndReplys(thread_title, thread_domain, thread_path):
    print('get-thread: ', thread_title)
    thread_datas = {
        'title': thread_title,
        'content': '',
        'author':  '',
        'replys': [],
        'scrapped_date': datetime.datetime.now(),
        'publication_date': ''
    }

    thread_datas['scrapped_date'] = thread_datas['scrapped_date'].strftime('%x') + '-' + thread_datas['scrapped_date'].strftime('%X')
    # Firstly we get the page of the thread
    soup_thread_page = getPage(thread_domain, thread_path)
    thread_datas['author'] = soup_thread_page.find(class_ = 'UserName').find('a').get_text()
    
    # Next we search for the firts thread in the thread page to get the author, content, publication date... 
    StarterThread  = soup_thread_page.find('div', class_='lia-thread-topic')

    # Here we search for the content of body
    content = StarterThread.find(class_ = 'lia-message-body-content')

    # Check for signature if have on remove it 
    if content.find(class_ = 'UserSignature'):
        content.find(class_ = 'UserSignature').decompose()

    # Parse to string the content of the thread
    thread_datas['content'] = content.get_text()
    thread_datas['publication_date'] = StarterThread.find(class_ = 'local-date').getText()

    # Here we get replys of the thread
    thread_datas['replys'] = getReplyOfThread(soup_thread_page)

    return thread_datas

def getReplyOfThread(thread_page):
    
    replysComponents  = thread_page.find_all(class_ = 'lia-thread-reply')
    _replys = [] # Parsed replys

    # Todo Remove Limit
    # Limit of thread to get
    blockage = len(replysComponents)
    if(blockage > 1):
        blockage = 3
        
    iteration = 0
    while iteration != blockage - 1:
        author  = replysComponents[iteration].find(class_ = 'lia-user-name-link').get_text()
        print('get-replys from author: ', author)
        content = replysComponents[iteration].find(class_ = 'lia-message-body-content').get_text()
        pb_date = replysComponents[iteration].find(class_ = 'local-date').getText()
        _replys.append({
            'author': author, 
            'content': content,
            'scrapped_date': datetime.datetime.now().strftime('%x' + '-' + '%X'),
            'publication_date': pb_date
        })
        iteration += 1
    
    return _replys

def JsonEncoder(json_to_encode):
    return json.dumps(json_to_encode, indent=2, sort_keys=True)

def JsonDecode(json_to_decode):
    io = StringIO(json_to_decode)
    return json.load(io)