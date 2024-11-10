import random
from config import FICHIER_ACHATS, FICHIER_CLIENTS, FICHIER_ARTICLES, FICHIER_PRIX, FICHIER_DATES
from database import creer_table_achats, sauvegarder_achat

def lire_fichier(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        return [ligne.strip() for ligne in fichier.readlines()]

def generer_achats():
    # Lecture des données depuis les fichiers
    clients = lire_fichier(FICHIER_CLIENTS)
    articles = lire_fichier(FICHIER_ARTICLES)
    prix = lire_fichier(FICHIER_PRIX)
    dates = lire_fichier(FICHIER_DATES)
    
    # Création de la table d'achats si elle n'existe pas
    creer_table_achats()
    
    # Enregistrement des achats générés
    with open(FICHIER_ACHATS, 'w') as fichier:
        for client in clients:
            nb_articles = random.randint(1, 3)
            articles_choisis = random.sample(list(zip(articles, prix)), nb_articles)
            date_achat = random.choice(dates)
            achat = (client, articles_choisis, date_achat)
            fichier.write(str(achat) + '\n')
            sauvegarder_achat(client, articles_choisis, date_achat)
