import sqlite3
from config import DATABASE_NAME

def creer_table_achats():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS achats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT,
            articles TEXT,
            date TEXT,
            UNIQUE(client, articles, date)
        )
        """
    )
    connection.commit()
    connection.close()

def sauvegarder_achat(client, articles, date):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO achats (client, articles, date) VALUES (?, ?, ?)", (client, str(articles), date))
    connection.commit()
    connection.close()

def lire_achats(client=None, date_debut=None, date_fin=None):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    
    # Construction de la requête SQL avec filtres optionnels
    query = "SELECT client, articles, date FROM achats WHERE 1=1"
    params = []
    
    if client:
        query += " AND client = ?"
        params.append(client)
    
    if date_debut:
        query += " AND date >= ?"
        params.append(date_debut)
    
    if date_fin:
        query += " AND date <= ?"
        params.append(date_fin)
    
    cursor.execute(query, params)
    achats = cursor.fetchall()
    connection.close()
    return achats

def supprimer_achat(achat_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM achats WHERE id = ?", (achat_id,))
    connection.commit()
    connection.close()

def modifier_achat(achat_id, client, articles, date):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE achats SET client = ?, articles = ?, date = ? WHERE id = ?",
        (client, str(articles), date, achat_id)
    )
    connection.commit()
    connection.close()