import os
from dotenv import load_dotenv

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

        pointers_json_file = os.getenv('SCR_pointers_file_path')

        if pointers_json_file is not None:
            print(os.getenv('test'))


        # Class var
        self.scrapped_datas = {}
        self.have_page = {
            'have': True,
            'page_pointers': {
                
            }
        }
        self.page_to_scrap_infos = {
            'url': '',
            'domain': '',
            'page_requested': '',

            'souped_page': ''
        }

    # def config_urls(url)

scr = Scrapper()
