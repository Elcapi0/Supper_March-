import matplotlib.pyplot as plt  # On importe une bibliothèque pour créer des graphiques
from collections import Counter  # On importe un outil qui compte combien de fois chaque élément apparaît
import ast  # On importe un outil qui transforme du texte en structure de données Python
from database import lire_achats  # On importe la fonction pour lire les achats depuis une base de données

# Fonction pour créer un graphique montrant combien d'achats chaque client a fait
def histogramme_achats_par_client():
    achats = lire_achats()  # On lit les achats depuis la base de données
    clients = [achat[0] for achat in achats]  # On récupère le nom de chaque client (premier élément de chaque achat)
    compteur = Counter(clients)  # On compte combien d'achats chaque client a faits
    # On dessine un graphique en barres où chaque barre représente un client et montre son nombre d'achats
    plt.bar(compteur.keys(), compteur.values(), color='skyblue')  
    plt.xlabel('Clients')  # On nomme l'axe horizontal "Clients"
    plt.ylabel('Nombre d\'achats')  # On nomme l'axe vertical "Nombre d'achats"
    plt.title('Nombre d\'achats par client')  # On met le titre du graphique
    plt.xticks(rotation=45, ha="right")  # On tourne les noms des clients pour qu'ils soient plus lisibles
    plt.tight_layout()  # On ajuste l'espace autour du graphique
    plt.show()  # On affiche le graphique

# Fonction pour montrer la répartition des prix des articles achetés
def repartition_prix_articles():
    achats = lire_achats()  # On lit les achats depuis la base de données
    prix = []  # On crée une liste vide pour stocker les prix des articles
    for achat in achats:  # Pour chaque achat dans la liste :
        # On évalue chaque article pour extraire son nom et son prix
        for article, prix_article in ast.literal_eval(achat[1]):  
            prix.append(float(prix_article))  # On ajoute le prix de l'article (en nombre) à la liste des prix
    # On crée un histogramme pour montrer la distribution des prix
    plt.hist(prix, bins=10, color='lightgreen', edgecolor='black')  # bins=10 divise les prix en 10 catégories
    plt.xlabel('Prix')  # On nomme l'axe horizontal "Prix"
    plt.ylabel('Nombre d\'articles')  # On nomme l'axe vertical "Nombre d'articles"
    plt.title('Répartition des prix des articles')  # On met le titre du graphique
    plt.tight_layout()  # On ajuste l'espace pour que tout soit bien visible
    plt.show()  # On affiche le graphique

# Fonction pour montrer comment le nombre d'achats évolue au fil du temps
def evolution_achats_temps():
    achats = lire_achats()  # On lit les achats depuis la base de données
    dates = [achat[2] for achat in achats]  # On extrait la date de chaque achat (3ème élément de chaque achat)
    compteur = Counter(dates)  # On compte combien d'achats ont été faits chaque jour
    # On dessine un graphique en ligne où chaque point représente une date et le nombre d'achats ce jour-là
    plt.plot(list(compteur.keys()), list(compteur.values()), marker='o', linestyle='-', color='orange')  
    plt.xlabel('Date')  # On nomme l'axe horizontal "Date"
    plt.ylabel('Nombre d\'achats')  # On nomme l'axe vertical "Nombre d'achats"
    plt.title('Évolution des achats dans le temps')  # On met le titre du graphique
    plt.xticks(rotation=45, ha="right")  # On tourne les dates pour qu'elles soient plus lisibles
    plt.tight_layout()  # On ajuste l'espace autour du graphique
    plt.show()  # On affiche le graphique

# Fonction pour montrer combien de fois chaque article a été acheté
def repartition_achats_par_article():
    achats = lire_achats()  # On lit les achats depuis la base de données
    articles = []  # On crée une liste vide pour stocker les articles
    for achat in achats:  # Pour chaque achat dans la liste :
        # On évalue chaque article pour en extraire le nom et le prix
        for article, prix_article in ast.literal_eval(achat[1]):  
            articles.append(article)  # On ajoute le nom de l'article à la liste des articles
    compteur = Counter(articles)  # On compte combien de fois chaque article a été acheté
    # On dessine un graphique en barres où chaque barre représente un article et montre combien de fois il a été acheté
    plt.bar(compteur.keys(), compteur.values(), color='purple')  
    plt.xlabel('Articles')  # On nomme l'axe horizontal "Articles"
    plt.ylabel('Nombre d\'achats')  # On nomme l'axe vertical "Nombre d'achats"
    plt.title('Répartition des achats par article')  # On met le titre du graphique
    plt.xticks(rotation=45, ha="right")  # On tourne les noms des articles pour qu'ils soient plus lisibles
    plt.tight_layout()  # On ajuste l'espace autour du graphique
    plt.show()  # On affiche le graphique

# Fonction pour calculer combien chaque client a dépensé au total
def total_depenses_par_client():
    achats = lire_achats()  # On lit les achats depuis la base de données
    depenses_par_client = {}  # On crée un dictionnaire vide pour stocker les dépenses totales de chaque client
    for achat in achats:  # Pour chaque achat dans la liste :
        client = achat[0]  # On récupère le nom du client (premier élément de l'achat)
        # On calcule combien ce client a dépensé pour cet achat en faisant la somme des prix des articles achetés
        total = sum([float(prix_article) for article, prix_article in ast.literal_eval(achat[1])])  
        # On ajoute le total des dépenses au montant déjà existant pour ce client
        depenses_par_client[client] = depenses_par_client.get(client, 0) + total  
    # On dessine un graphique en barres où chaque barre montre le total des dépenses de chaque client
    plt.bar(depenses_par_client.keys(), depenses_par_client.values(), color='red')  
    plt.xlabel('Clients')  # On nomme l'axe horizontal "Clients"
    plt.ylabel('Total des dépenses (FCFA)')  # On nomme l'axe vertical "Total des dépenses (FCFA)"
    plt.title('Total des dépenses par client')  # On met le titre du graphique
    plt.xticks(rotation=45, ha="right")  # On fait tourner les noms des clients pour qu'ils soient plus lisibles
    plt.tight_layout()  # On ajuste l'espace autour du graphique
    plt.show()  # On affiche le graphique
