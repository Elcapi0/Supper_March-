import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from generateur_achats import generer_achats
from analyse_achats import (histogramme_achats_par_client, repartition_prix_articles, 
                            evolution_achats_temps, repartition_achats_par_article, 
                            total_depenses_par_client)
from database import lire_achats, sauvegarder_achat, supprimer_achat, modifier_achat

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Achats")
        self.geometry("1000x750")
        
        # Section des filtres
        filter_frame = tk.Frame(self)
        filter_frame.pack(side=tk.TOP, pady=10)

        # Champ pour entrer le nom du client
        tk.Label(filter_frame, text="Client:").pack(side=tk.LEFT, padx=5)
        self.client_entry = tk.Entry(filter_frame, width=20)
        self.client_entry.pack(side=tk.LEFT, padx=5)
        
        # Sélecteurs de dates pour la plage de dates
        tk.Label(filter_frame, text="Date de début:").pack(side=tk.LEFT, padx=5)
        self.date_debut = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_debut.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="Date de fin:").pack(side=tk.LEFT, padx=5)
        self.date_fin = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_fin.pack(side=tk.LEFT, padx=5)
        
        # Bouton de filtre
        tk.Button(filter_frame, text="Filtrer", command=self.filtrer_achats).pack(side=tk.LEFT, padx=5)
        
        # Section de recherche dynamique
        search_frame = tk.Frame(self)
        search_frame.pack(side=tk.TOP, pady=10)

        tk.Label(search_frame, text="Recherche:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.recherche_achats)

        # Section supérieure des boutons d'action
        action_frame = tk.Frame(self)
        action_frame.pack(side=tk.TOP, pady=10)
        
        # Boutons pour générer et afficher les achats
        tk.Button(action_frame, text="Générer Achats", command=self.generer_achats).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Afficher Tous les Achats", command=self.afficher_tous_achats).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Ouvrir Graphiques", command=self.ouvrir_fenetre_graphiques).pack(side=tk.LEFT, padx=5)
        
        # Nouveau bouton "Ajouter un Achat"
        tk.Button(action_frame, text="Ajouter un Achat", command=self.ouvrir_fenetre_ajout_achat).pack(side=tk.LEFT, padx=5)
        
        # Boutons "Modifier" et "Supprimer"
        tk.Button(action_frame, text="Modifier Achat", command=self.modifier_achat).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Supprimer Achat", command=self.supprimer_achat).pack(side=tk.LEFT, padx=5)
        
        # Cadre pour le Treeview et la barre de défilement
        treeview_frame = tk.Frame(self)
        treeview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Barre de défilement verticale
        scrollbar = tk.Scrollbar(treeview_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Zone de tableau pour afficher les achats avec une barre de défilement
        # self.treeview = ttk.Treeview(treeview_frame, columns=("ID", "Client", "Articles", "Date"), show="headings", yscrollcommand=scrollbar.set)
        # self.treeview.heading("ID", text="ID")
        self.treeview = ttk.Treeview(treeview_frame, columns=("Client", "Articles", "Date"), show="headings", yscrollcommand=scrollbar.set)
        self.treeview.heading("Client", text="Client")
        self.treeview.heading("Articles", text="Articles")
        self.treeview.heading("Date", text="Date")
        self.treeview.pack(fill=tk.BOTH, expand=True)
        
        # Configuration de la barre de défilement
        scrollbar.config(command=self.treeview.yview)

    def generer_achats(self):
        generer_achats()
        messagebox.showinfo("Succès", "Achats générés et stockés dans la base de données.")
    
    def afficher_tous_achats(self):
        self.afficher_achats()  # Afficher tous les achats sans filtre

    def filtrer_achats(self):
        # Récupérer les valeurs des filtres
        client = self.client_entry.get().strip() or None
        date_debut = self.date_debut.get_date().strftime('%Y-%m-%d')
        date_fin = self.date_fin.get_date().strftime('%Y-%m-%d')
        
        # Filtrer les achats et mettre à jour l'affichage
        self.afficher_achats(client=client, date_debut=date_debut, date_fin=date_fin)

    def afficher_achats(self, client=None, date_debut=None, date_fin=None):
        # Effacer l'affichage actuel dans le Treeview
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        
        # Charger les achats filtrés
        achats = lire_achats(client=client, date_debut=date_debut, date_fin=date_fin)
        for achat in achats:
            client, articles, date = achat
            self.treeview.insert("", "end", values=(client, articles, date))
    
    def recherche_achats(self, event=None):
        # Texte de recherche
        texte_recherche = self.search_entry.get().strip().lower()
        
        # Charger tous les achats pour effectuer la recherche
        achats = lire_achats()
        
        # Effacer l'affichage actuel
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        # Filtrer les achats en fonction du texte de recherche
        for achat in achats:
            client, articles, date = achat
            # Vérifier si le texte de recherche est dans le nom du client ou les articles
            if texte_recherche in client.lower() or texte_recherche in articles.lower():
                self.treeview.insert("", "end", values=(client, articles, date))

    def ouvrir_fenetre_ajout_achat(self):
        # Fenêtre d'ajout manuel d'un nouvel achat
        FenetreAjoutAchat(self)
    
    def modifier_achat(self):
        # Obtenir la sélection dans le Treeview
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un achat à modifier.")
            return

        achat_values = self.treeview.item(selected_item)["values"]
        client, articles, date = achat_values

        # Ouvrir la fenêtre de modification
        FenetreModificationAchat(self, client, articles, date)

    def supprimer_achat(self):
        # Obtenir la sélection dans le Treeview
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un achat à supprimer.")
            return

        achat_id = self.treeview.item(selected_item)["values"][0]
        
        # Confirmation de suppression
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet achat ?"):
            supprimer_achat(achat_id)
            messagebox.showinfo("Succès", "Achat supprimé avec succès.")
            self.afficher_tous_achats()

    def ouvrir_fenetre_graphiques(self):
        # Ouvrir une fenêtre pour afficher les graphiques
        GraphiquesWindow(self)

class FenetreAjoutAchat(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajouter un Achat")
        self.geometry("400x300")
        
        # Champs du formulaire pour entrer les informations de l'achat
        tk.Label(self, text="Client:").pack(pady=5)
        self.client_entry = tk.Entry(self, width=30)
        self.client_entry.pack(pady=5)

        tk.Label(self, text="Articles:").pack(pady=5)
        self.articles_entry = tk.Entry(self, width=30)
        self.articles_entry.pack(pady=5)

        tk.Label(self, text="Prix:").pack(pady=5)
        self.prix_entry = tk.Entry(self, width=30)
        self.prix_entry.pack(pady=5)

        tk.Label(self, text="Date:").pack(pady=5)
        self.date_entry = DateEntry(self, width=27, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)

        # Bouton pour enregistrer l'achat
        tk.Button(self, text="Enregistrer", command=self.enregistrer_achat).pack(pady=10)

    def enregistrer_achat(self):
        # Récupérer les informations du formulaire
        client = self.client_entry.get().strip()
        articles = self.articles_entry.get().strip()
        prix = self.prix_entry.get().strip()
        date = self.date_entry.get_date().strftime('%Y-%m-%d')
        
        # Vérifier que tous les champs sont remplis
        if not client or not articles or not prix or not date:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
            return
        
        # Ajouter l'achat dans la base de données
        try:
            sauvegarder_achat(client, [(articles, prix)], date)
            messagebox.showinfo("Succès", "Achat ajouté avec succès.")
            self.destroy()  # Fermer la fenêtre après l'ajout
            self.master.afficher_tous_achats()  # Rafraîchir l'affichage dans le Treeview
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ajouter l'achat : {e}")

class FenetreModificationAchat(tk.Toplevel):
    def __init__(self, parent, client, articles, date):
        super().__init__(parent)
        self.title("Modifier un Achat")
        self.geometry("400x300")
        
        # Champs du formulaire pour modifier les informations de l'achat
        tk.Label(self, text="Client:").pack(pady=5)
        self.client_entry = tk.Entry(self, width=30)
        self.client_entry.insert(0, client)
        self.client_entry.pack(pady=5)

        tk.Label(self, text="Articles:").pack(pady=5)
        self.articles_entry = tk.Entry(self, width=30)
        self.articles_entry.insert(0, articles)
        self.articles_entry.pack(pady=5)

        tk.Label(self, text="Date:").pack(pady=5)
        self.date_entry = DateEntry(self, width=27, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(date)
        self.date_entry.pack(pady=5)

        # Bouton pour enregistrer les modifications
        tk.Button(self, text="Enregistrer", command=self.enregistrer_modification).pack(pady=10)

    def enregistrer_modification(self):
        # Récupérer les informations mises à jour
        client = self.client_entry.get().strip()
        articles = self.articles_entry.get().strip()
        date = self.date_entry.get_date().strftime('%Y-%m-%d')
        
        if not client or not articles or not date:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
            return

        # Mettre à jour l'achat dans la base de données
        try:
            modifier_achat(self.achat_id, client, [(articles,)], date)
            messagebox.showinfo("Succès", "Achat modifié avec succès.")
            self.destroy()  # Fermer la fenêtre après la modification
            self.master.afficher_tous_achats()  # Rafraîchir l'affichage dans le Treeview
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de modifier l'achat : {e}")

class GraphiquesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Graphiques des Achats")
        self.geometry("800x600")
        
        # Dropdown pour sélectionner le type de graphique
        self.type_graphique = tk.StringVar()
        options = ["Histogramme par Client", "Répartition des Prix", "Évolution des Achats", 
                   "Répartition par Article", "Dépenses par Client"]
        ttk.Label(self, text="Choisir le type de graphique :").pack(pady=5)
        self.combo_graphiques = ttk.Combobox(self, textvariable=self.type_graphique, values=options, state="readonly")
        self.combo_graphiques.pack(pady=10)
        self.combo_graphiques.bind("<<ComboboxSelected>>", self.afficher_graphique)

        # Zone de dessin pour le graphique
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = None

    def afficher_graphique(self, event=None):
        choix = self.type_graphique.get()
        achats = lire_achats()
        
        # Supprimer le graphique précédent
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        # Créer un nouveau graphique selon le choix
        plt.figure()
        if choix == "Histogramme par Client":
            histogramme_achats_par_client()
        elif choix == "Répartition des Prix":
            repartition_prix_articles()
        elif choix == "Évolution des Achats":
            evolution_achats_temps()
        elif choix == "Répartition par Article":
            repartition_achats_par_article()
        elif choix == "Dépenses par Client":
            total_depenses_par_client()

        # Intégrer le graphique dans Tkinter
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
