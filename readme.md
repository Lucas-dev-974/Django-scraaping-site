# Scrapping-site

Scrapping-site à pour but de délivrer une interface web avec système de connexion et page privé. Cet interface vas permettre à l'utilisateur connecter d'utiliser un script de scrapping de données pour aller récuperer données tel que des Postes de publication et toutes s'est réponses.

# Prérequis 
 - Python 
 - Django

# Installation 
  - git clone https://github.com/Lucas-dev-974/Django-scraaping-site.git

# Commencer 
Dans un terminal se positionner à la racine du projet, puis exécuter les commandes suivante: 

    - .venv/Scripts/Activate.ps1
    - python manage.py migrate Site
    - python manage.py runserver

## Légère modification de l'architecture Django
### Views
Au niveaux de l'app "Site" le fichier "views.py" à été déplacer dans le dossier "views" qui lui vas contenir toutes les méthods views pour l'app "Site" par exemple: AuthentificationViews - TargetSiteViews...
 
### Formulaires
Retrouver tous les "Formulaire Django" dans le dossier "Site/Formulaires"

