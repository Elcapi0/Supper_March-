import ast
import matplotlib.pyplot as plt
from database import lire_achats

def repartition_prix_articles():
    achats = lire_achats()  # On lit les achats depuis la base de données
    prix = []  # On crée une liste vide pour stocker les prix des articles

    for achat in achats:  # Pour chaque achat dans la liste :
        try:
            # Tente d'évaluer chaque article pour extraire son nom et son prix
            articles = ast.literal_eval(achat[1])
            for article, prix_article in articles:
                prix.append(float(prix_article))  # On ajoute le prix de l'article à la liste des prix
        except (ValueError, SyntaxError) as e:
            print(f"Erreur de format dans les articles pour l'achat {achat}: {e}")
            continue  # Ignorer cet enregistrement et continuer avec les autres

    # On crée un histogramme pour montrer la distribution des prix
    plt.hist(prix, bins=10, color='lightgreen', edgecolor='black')  # bins=10 divise les prix en 10 catégories
    plt.xlabel('Prix')  # On nomme l'axe horizontal "Prix"
    plt.ylabel('Nombre d\'articles')  # On nomme l'axe vertical "Nombre d'articles"
    plt.title('Répartition des prix des articles')  # On met le titre du graphique
    plt.tight_layout()  # On ajuste l'espace pour que tout soit bien visible
    plt.show()  # On affiche le graphique
