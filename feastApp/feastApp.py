import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import csv


FICHIER_JSON = "evenements.json"

def charger_evenements():
    try:
        with open(FICHIER_JSON, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def sauvegarder_evenements(evenements):
    with open(FICHIER_JSON, "w") as f:
        json.dump(evenements, f, indent=2)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FASO SPORT & CULTURE EVENTS")
        self.geometry("1080x720")
        self.configure(bg="#2c3e50")
        self.evenements = charger_evenements()

        self.font_title = ("Helvetica", 24, "bold")
        self.font_btn = ("Helvetica", 12)
        self.font_list = ("Consolas", 12)

        label_title = tk.Label(self, text="FASO SPORT & CULTURE EVENTS", font=self.font_title, fg="white", bg="#2c3e50")
        label_title.pack(pady=20)

        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        frame_btn = tk.Frame(main_frame, bg="#2c3e50")
        frame_btn.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        # Bouton MENU qui va disparaître après clic
        self.menu_btn = tk.Button(frame_btn, text="MENU", font=self.font_btn,
                                  bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
                                  relief=tk.FLAT, padx=15, pady=8, command=self.afficher_actions)
        self.menu_btn.pack(fill=tk.X, pady=10)

        # Frame qui contiendra les boutons d'action, caché au départ
        self.actions_frame = tk.Frame(frame_btn, bg="#2c3e50")

        # Les boutons à afficher après clic sur MENU
        self.btn_creer = tk.Button(self.actions_frame, text="Créer un événement", command=self.creer_evenement, font=self.font_btn,
                                   bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
                                   relief=tk.FLAT, padx=15, pady=8)
        self.btn_ajouter = tk.Button(self.actions_frame, text="Ajouter un inscrit", command=self.ajouter_inscrit, font=self.font_btn,
                                     bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
                                     relief=tk.FLAT, padx=15, pady=8)
        self.btn_rechercher = tk.Button(self.actions_frame, text="Rechercher", command=self.rechercher_evenement, font=self.font_btn,
                                        bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
                                        relief=tk.FLAT, padx=15, pady=8)
        self.btn_exporter = tk.Button(self.actions_frame, text="Exporter des inscrits", command=self.exporter_inscrits, font=self.font_btn,
                                      bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
                                      relief=tk.FLAT, padx=15, pady=8)
        self.btn_rafraichir = tk.Button(self.actions_frame, text="Rafraîchir la liste", command=self.afficher_evenements, font=self.font_btn,
                                        bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
                                        relief=tk.FLAT, padx=15, pady=8)

        # Cadre pour la liste des événements (à droite)
        frame_list = tk.Frame(main_frame, bg="#9273c2")
        frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listebox = tk.Listbox(frame_list, width=80, height=20, font=self.font_list, yscrollcommand=scrollbar.set,
                                  bg="#ecf0f1", fg="#2c3e50", selectbackground="#2980b9", selectforeground="white", bd=0)
        self.listebox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listebox.yview)

        self.afficher_evenements()

    def afficher_actions(self):
        self.menu_btn.pack_forget()  # Retirer le bouton MENU

        # Afficher les boutons d'action
        self.actions_frame.pack(fill=tk.X, pady=5)
        self.btn_creer.pack(fill=tk.X, pady=5)
        self.btn_ajouter.pack(fill=tk.X, pady=5)
        self.btn_rechercher.pack(fill=tk.X, pady=5)
        self.btn_exporter.pack(fill=tk.X, pady=5)
        self.btn_rafraichir.pack(fill=tk.X, pady=5)

    def afficher_evenements(self):
        self.listebox.delete(0, tk.END)
        for i, event in enumerate(self.evenements):
            ligne = f"{i}. {event['type'].capitalize()} - {event['date']} à {event['lieu']} ({len(event['inscrits'])} inscrit(s))"
            self.listebox.insert(tk.END, ligne)

    def creer_evenement(self):
        type_event = simpledialog.askstring("Type", "Type d'événement (sportif/culturel) :", parent=self)
        date = simpledialog.askstring("Date", "Date (AAAA-MM-JJ) :", parent=self)
        lieu = simpledialog.askstring("Lieu", "Lieu de l’événement :", parent=self)
        if type_event and date and lieu:
            self.evenements.append({"type": type_event, "date": date, "lieu": lieu, "inscrits": []})
            sauvegarder_evenements(self.evenements)
            self.afficher_evenements()
            messagebox.showinfo("Succès", "Événement créé.")
        else:
            messagebox.showwarning("Incomplet", "Tous les champs sont obligatoires.")

    def ajouter_inscrit(self):
        selection = self.listebox.curselection()
        if not selection:
            messagebox.showwarning("Aucun événement", "Sélectionnez un événement.", parent=self)
            return
        index = selection[0]
        nom = simpledialog.askstring("Nom", "Nom de l’inscrit :", parent=self)
        if nom:
            self.evenements[index]["inscrits"].append(nom)
            sauvegarder_evenements(self.evenements)
            self.afficher_evenements()
            messagebox.showinfo("Succès", "Inscrit ajouté.", parent=self)

    def rechercher_evenement(self):
        critere = simpledialog.askstring("Critère", "Rechercher par 'type' ou 'date' :", parent=self)
        valeur = simpledialog.askstring("Valeur", "Valeur à rechercher :", parent=self)
        if critere and valeur:
            resultats = [e for e in self.evenements if e.get(critere) == valeur]
            self.listebox.delete(0, tk.END)
            if resultats:
                for i, event in enumerate(resultats):
                    ligne = f"{event['type'].capitalize()} - {event['date']} à {event['lieu']} ({len(event['inscrits'])} inscrit(s))"
                    self.listebox.insert(tk.END, ligne)
            else:
                self.listebox.insert(tk.END, "Aucun événement trouvé.")

    def exporter_inscrits(self):
        selection = self.listebox.curselection()
        if not selection:
            messagebox.showwarning("Aucun événement", "Sélectionnez un événement.", parent=self)
            return
        index = selection[0]
        nom_fichier = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if nom_fichier:
            with open(nom_fichier, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Nom des inscrits"])
                for nom in self.evenements[index]["inscrits"]:
                    writer.writerow([nom])
            messagebox.showinfo("Export", "Inscrits exportés avec succès.", parent=self)

if __name__ == "__main__":
    app = Application()
    app.mainloop()