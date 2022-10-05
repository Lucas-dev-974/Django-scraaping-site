from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlunparse
from Site.models import Threads,Threads_Replys, History
from .dtb import dtb


def SaveInHistory(thread):
    history_item = History.objects.create(
        target_site_id = 1  ,
        author = thread['author'],
        content = thread['content'],
        publication_date = thread['publication_date'],
        scrapped_date = thread['scrapped_date']
    )

    return history_item

def saveThread(thread, tgsite_id):
    thread_ = Threads.objects.create(
        target_id_id=1, 
        title = thread['title'],
        author = thread['author'],
        publication_date = thread['publication_date'],
        scrapped_date = thread['scrapped_date'],
        content = thread['content'],
        number_of_replys = thread['number_of_replys']
    )

    return thread_

def saveThreadReplys(thread, thread_id):
    thread_ = Threads.objects.create(
        thread_id = thread_id, 
        # title = thread['title'],
        author = thread['author'],
        publication_date = thread['publication_date'],
        scrapped_date = thread['scrapped_date'],
        content = thread['content']
    )

    return thread_

def getPage(domain, url_path):
    # print('site id: -- ', siteid)
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

    # boucle sur les article récuperer
    iteration = 0
    # for thread in thread_results:
    while iteration != 2:
        first_element = thread_results[iteration].find("div") # get first children - the div
        link          = first_element.find("a")
        
        title = link["title"] # get the title and save it 
        url   = link["href"] # get the link towards the post of the thread 
    
        domain = pageContent.find('meta', property='og:site_name')['content']
        
        threads.append(getParsedThreadsAndReplys(title, domain, url)) 
        iteration += 1

    return threads

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
    
def getParsedThreadsAndReplys(thread_title, thread_domain, thread_path):
    
    # Define parsed Thread object
    thread_datas = {
        'title': thread_title,
        'content': '',
        'author':  '',
        'replys': [],
        'link': thread_domain + thread_path,
        'scrapped_date': datetime.now(),
        'publication_date': ''
    }

    
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
    
    # Here we get replys of the thread
    

    # get html publication date and convert it to datetime Y-m-d
    pb_date_str = StarterThread.find(class_ = 'DateTime lia-message-posted-on lia-component-common-widget-date').find('span', class_ = 'local-date').text
    pb_date     = pb_date_str.split('-')
    pb_date[0] = pb_date[0][1:3]
    pb_converted_to_datetime = datetime(int(pb_date[2]), int(pb_date[1]), int(pb_date[0]))
    thread_datas['publication_date'] = pb_converted_to_datetime

    # Get replys and save them
    
    thread_datas['number_of_replys'] = len(thread_datas['replys'])
    # # Save thread in database get id of Thread
    # thread_id = dtb().insert('Site_threads', {
    #         'target_id_id': 1,
    #         'title': thread_datas['title'],
    #         'number_of_replys': 0,
    #         'author':  thread_datas['author'],
    #         'content': thread_datas['content'],
    #         'publication_date': pb_converted_to_datetime,
    #         'scrapped_date': thread_datas['scrapped_date'],
    #         'link': thread_datas['link']
    #     })

    # Here define the thread id just created and then get and save all replys

    thr = saveThread(thread=thread_datas, tgsite_id=1)
    thread_datas['id'] = thr.id
    thread_datas['replys'] = getReplyOfThread(soup_thread_page, thread_datas)   
    # print
    SaveInHistory(thread_datas)
    return thread_datas

def getReplyOfThread(thread_page, parent):
    replysComponents  = thread_page.find_all(class_ = 'lia-thread-reply')
    _replys = [] # Parsed replys

    # Todo Remove Limit
    # Limit of thread to get
    blockage = len(replysComponents)
    if(blockage > 1):
        blockage = 3
    
    iteration = 0
    while iteration != blockage - 1:
        # Get Author
        author  = replysComponents[iteration].find(class_ = 'lia-user-name-link').get_text()

        # Get html and convert publication date html as datetime
        pb_date_str = replysComponents[iteration].find(class_ = 'DateTime lia-message-posted-on lia-component-common-widget-date').find('span', class_ = 'local-date').text
        pb_date     = pb_date_str.split('-')
        pb_date[0] = pb_date[0][1:3]
        pb_converted_to_datetime = datetime(int(pb_date[2]), int(pb_date[1]), int(pb_date[0]))

        # Get Content
        content = replysComponents[iteration].find(class_ = 'lia-message-body-content').get_text()
        _replys.append({
            'author': author,
            'content': content,
            'publication_date': pb_converted_to_datetime,
            'scrapped_date': parent['scrapped_date'],
            'link': parent['link'],
            'thread_id': parent['id']
        })

        # thread_id = dtb().insert('Site_threads_replys', {
        #     'thread_id': parent['id'],
        #     'author':  author,
        #     'content': content,
        #     'publication_date': pb_converted_to_datetime,
        #     'scrapped_date': datetime.now(),
        #     'link': parent['link']
        # })
        
        iteration += 1
    
    return _replys
