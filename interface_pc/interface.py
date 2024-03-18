import tkinter as tk
from tkinter import ttk
import random
import time
from serial import Serial

class InterfaceGraphique(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface Graphique avec Arduino")
        self.geometry("400x200")
        
        self.frame_poids = ttk.Frame(self)
        self.frame_poids.pack(side="left", padx=20, pady=20)
        
        self.poids_label = ttk.Label(self.frame_poids, text="Poids mesuré:", font=("Arial", 14))
        self.poids_label.pack()
        
        self.poids_valeur = tk.StringVar()
        self.poids_valeur.set("0")
        self.poids_affichage = ttk.Label(self.frame_poids, textvariable=self.poids_valeur, font=("Arial", 20))
        self.poids_affichage.pack()
        
        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side="right", padx=20, pady=20)
        
        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Tare", command=self.activer_fonction1)
        self.bouton_fonction1.pack(pady=10)
        
        self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Étalonnage", command=self.activer_fonction2)
        self.bouton_fonction2.pack(pady=10)
        
        self.bouton_fonction3 = ttk.Button(self.frame_boutons, text="Choisir une dénomination", command=self.activer_fonction3)
        self.bouton_fonction3.pack(pady=10)
        
        self.lire_poids_arduino()

    def lire_poids_arduino(self):
        poids = self.lire_poids_aleatoire()  # Remplacer par la lecture réelle depuis l'Arduino
        self.poids_valeur.set(str(poids))
        self.after(500, self.lire_poids_arduino)

    def lire_poids_aleatoire(self):
        # Simulation de la lecture du poids
        return round(random.uniform(0, 100), 2)

    def activer_fonction1(self):
        # Appeler la fonction 1 sur l'Arduino
        print("Tare")

    def activer_fonction2(self):
        # Appeler la fonction 2 sur l'Arduino
        print("Étalonnage")

    def activer_fonction3(self):
        # Appeler la fonction 3 sur l'Arduino
        print("dénomination")
    
    def lire_valeur_serial():
    # Ouvrir la connexion série
        ser = Serial('COM1', 9600)  # Remplacer 'COM1' par le port série utilisé par votre Arduino

        while True:
            # Lire une ligne de données depuis le port série
            valeur = ser.readline().decode().strip()
            valeur_label.config(text=valeur)  # Mettre à jour l'étiquette Tkinter avec la valeur lue

        # Fermer la connexion série
        ser.close()

if __name__ == "__main__":
    app = InterfaceGraphique()
    app.mainloop()
