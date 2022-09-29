from genericpath import isfile
import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse



load_dotenv()

class Scrapper():
    scrapped_datas = {
        'pointer_post-datas'
    }
    
    pointers = {
        'pointer_post-datas': { # Ne pas utiliser de "_" mise à part pour séparer le mot pointer qui est obligatoir
        
            '.posts-container-card': {
                '.user-post':{
                    'name': 'user post', # name est une var priotaire c'est à dire quel sert qu'a donner un nom à l'objet scrapper 
                    '.author-name': 'text',
                    '.publication-date': 'datetime YY-mm-dd',
                    '.post-msg-content': 'text',
                }
            },

            '#sidebar': {
                '.article':{
                    # 'name': 'article', Si aucun nom n'est spécifier alors le nom du conteneur de la données scrapper est le nom de l'objet qui le contient ici 'article'
                    '.publication-date': 'datetime',
                    '.article-content': 'text'
                }
            },
            # ...
        }
    }


    def __init__(self):
        # Config var
        self.use_db  = os.getenv('SCR_use_db')
        self.db_type = os.getenv('SCR_db_type')
        self.db_user = os.getenv('SCR_db_user')
        self.db_pwd  = os.getenv('SCR_pwd')

        self.pointers_json_file = os.getenv('SCR_pointers_file_path')
        self.real_JSONFile_path     = ''
        self.useJsonFile        = False

        self.url_to_scrap = os.getenv('SCR_url_to_scrap')



        # Class var
        self.scrapped_datas = {}
        self.pointers = {}
        self.have_page = {
            'have': True,
            'page_pointers': {
                
            }
        }
        self.page_to_scrap_infos = {
            'url': '',
            'domain': '',
            'url_path': '',
            'page_requested': '',

            'souped_page': ''
        }

    def start(self):
        if self.checkConf() == False:
            return None
            
        self.page_to_scrap_infos['souped_page'] = self.GetPageContent()

        if self.useJsonFile:
            self.readElInJson()
        # print(self.page_to_scrap_infos['souped_page'])

    def readElInJson(self):
        for pointer, value in self.pointers['pointer'].items():
            if type(value) is dict:
                print('get-in: ', pointer)

    def getElement(el):
        print(el)

    def checkConf(self):
        if self.url_to_scrap is  None:
            print('Erreur une url de la page à scrapper est requis')
            return False

        self.page_to_scrap_infos['domain']   =  urlparse(self.url_to_scrap).netloc
        self.page_to_scrap_infos['url_path'] =  urlparse(self.url_to_scrap).path    

        if self.pointers_json_file is not None:
            self.useJsonFile = True
            Folder_file_path = os.path.dirname(os.path.realpath(__file__))
            self.real_JSONFile_path = Folder_file_path + '/' + self.pointers_json_file
            
            if os.path.isfile(self.real_JSONFile_path):
                self.loadJsonFile()


        return True
            

    def GetPageContent(self):
        #construct the url to access the posts for each thread
        page_url = urlunparse(('https', self.page_to_scrap_infos['domain'], self.page_to_scrap_infos['url_path'], "", "", "")) 
        page = requests.get(page_url)
        souped_page = BeautifulSoup(page._content, "html.parser")
        return souped_page


    def haveNextDataToScrap():
        print('')

    def ElExist(el):
        print(el)


    def loadJsonFile(self):
        print('json file in load')
        file = open(self.real_JSONFile_path)
        jsonData = json.load(file)
        self.pointers = jsonData
        return jsonData

    
scr = Scrapper().start()
