import tkinter as tk
from tkinter import ttk
import serial
import random
import time
from scipy.optimize import curve_fit


ser = serial.Serial('/dev/cu.usbmodem11301', 9600)

arduino_port = '/dev/cu.usbmodem11301'
baud_rate = 9600



def send_command(command):
    ser.write(command.encode())

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs, className=' Gantt Gang')

        # creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (menu, weight, etalonnage, choix):

            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(menu)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class menu(tk.Frame):
    def __init__(self, parent, controller):
        #tk.Frame.__init__(self, parent)
        super().__init__(parent)
        self.controller = controller
        # tk.Tk.title("Menu principale")
        # tk.Tk.geometry("400x200")

        self.frame_poids = ttk.Frame(self)
        self.frame_poids.pack(side="top", padx=20, pady=20)
        self.poids_label = ttk.Label(self.frame_poids, text="Menu principal", font=("Arial", 30))
        self.poids_label.pack()

        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='top',padx=20, pady=20)

        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Masse", command = lambda : controller.show_frame(weight))
        self.bouton_fonction1.pack(pady=10)

        self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Étalonnage", command=lambda : controller.show_frame(etalonnage))
        self.bouton_fonction2.pack(pady=10)

        self.bouton_fonction3 = ttk.Button(self.frame_boutons, text="Compter les pièces", command=lambda : controller.show_frame(choix))
        self.bouton_fonction3.pack(pady=10)


class weight(tk.Frame):
    # correction = -1 * float(ser.readline().decode().strip())
    correction = -1 * float(0)
    unité = 0
    def __init__(self, parent, controller):
        # tk.Frame.__init__(self, parent)
        super().__init__(parent)
        self.controller = controller
        # self.title("Menu de Pesée")
        # self.geometry('400x200')
        self.frame_poids = ttk.Frame(self)
        self.frame_poids.pack(side="top", padx=20, pady=20)
        self.poids_label = ttk.Label(self.frame_poids, text="Masse mesuré:", font=("Arial", 14))
        self.poids_label.pack()

        self.poids_valeur = tk.StringVar()
        self.poids_valeur.set("0")
        self.poids_affichage = ttk.Label(self.frame_poids, textvariable=self.poids_valeur, font=("Arial", 20))
        self.poids_affichage.pack()



        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='bottom',padx=20, pady=20)

        self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Tare", command= self.tarer)
        self.bouton_fonction2.pack(pady=10)

        self.bouton_fonction3 = ttk.Button(self.frame_boutons, text="Grammes <--> onces", command = self.changement_unité)
        self.bouton_fonction3.pack(pady=10)

        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Menu", command = lambda : controller.show_frame(menu))
        self.bouton_fonction1.pack(pady=10)

        self.lire_poids_arduino()

    def lire_poids_arduino(self):
        poids = self.lire_poids_aleatoire() + weight.correction
        # poids = ser.readline().decode().strip() + weight.correction
        if weight.unité == 0:
            self.poids_valeur.set(f'{str(round(poids, 1))} g')
        elif weight.unité ==1:
            self.poids_valeur.set(f'{str(round((poids*0.0353), 3))} oz')
        self.after(1000, self.lire_poids_arduino)

    def lire_poids_aleatoire(self):
        # Simulation de la lecture du poids
        return round(random.uniform(0, 100), 2)

    def tarer(self):
        # send_command('t')
        # weight.correction = -1 * float(ser.readline().decode().strip())
        weight.correction = -1* self.lire_poids_aleatoire()
        print('Tare effectué')

    def changement_unité(self):
        if weight.unité == 0:
            weight.unité = 1
        elif weight.unité == 1:
            weight.unité = 0



class etalonnage(tk.Frame):
    # Compteur d'étape étalonnage
    étapes = 0
    valeur_mesure = []
    def __init__(self, parent, controller):
        # tk.Frame.__init__(self, parent)
        super().__init__(parent)
        self.controller = controller

        self.frame_poids = ttk.Frame(self)
        self.frame_poids.pack(side="top", padx=20, pady=20)
        self.poids_label = ttk.Label(self.frame_poids, text="Étalonnage", font=("Arial", 30))
        self.poids_label.pack()


        # Affichage commande
        self.frame_phrase = ttk.Frame(self)
        self.frame_phrase.pack(side="top", padx=20, pady=20)
        self.phrase_label = ttk.Label(self.frame_phrase)
        self.phrase_label.pack()

        self.phrase_valeur = tk.StringVar()
        self.phrase_valeur.set("Début de l'étalonnage. \n Appuyez sur start pour passer à la première étape")
        self.phrase_affichage = ttk.Label(self.frame_phrase, textvariable=self.phrase_valeur, font=("Arial", 20))
        self.phrase_affichage.pack()



        # bouton start
        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='left',padx=20, pady=20)

        self.bouton_fonction4 = ttk.Button(self.frame_boutons, text="Start", command = self.phrase)
        self.bouton_fonction4.pack(pady=10)

        # Bouton next
        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Next", command = self.next)
        self.bouton_fonction1.pack(pady=10)

        # Bouton fin
        self.bouton_fonction3 = ttk.Button(self.frame_boutons, text="Fin", command = self.fin)
        self.bouton_fonction3.pack(pady=10)

        self.frame_boutons_2 = ttk.Frame(self)
        self.frame_boutons_2.pack(side='right',padx=20, pady=20)

        # Bouton menu
        self.bouton_fonction2 = ttk.Button(self.frame_boutons_2, text="Menu", command = lambda : controller.show_frame(menu))
        self.bouton_fonction2.pack(pady=10)


    def phrase(self):
        phrases = ["""Déposez 1 gramme sur la balance puis appuyez sur next""", """Déposez 2 grammes sur la balance puis appuyez sur next""",
                    """Déposez 5 grammes sur la balance puis appuyez sur next""", """Déposez 10 grammes sur la balance puis appuyez sur next""",
                    """Déposez 20 grammes sur la balance puis appuyez sur next""", """Déposez 50 grammes sur la balance puis appuyez sur next""",
                    """Déposez 70 grammes sur la balance puis appuyez sur next""", """Déposez 100 grammes sur la balance puis appuyez sur next""",
                    """Fin de l'étalonnage. \n Appuyez sur le bouton fin."""]
        try:
            self.phrase_valeur.set(phrases[etalonnage.étapes])
            etalonnage.étapes += 1
        except:
            self.fin()

    def next(self):
        # ajouter l'enregistrement du courant
        # etalonnage.valeur_mesure.append(float(ser.readline().decode().strip()))
        
        self.phrase()



    def fin(self):
        force = [0.00981, 0.01962, 0.04905, 0.0981, 0.1962, 0.4905, 0.6867, 0.981]
        etalonnage.valeur_mesure = [1, 2, 5, 10, 20, 50, 70, 100]
        k_f = self.mon_curve_fit(self.droite, force, etalonnage.valeur_mesure)
        # Envoyer k_f[0][0] et k_f[0][1] à l'arduino
        try:
            ser = serial.Serial(arduino_port, baud_rate)
        except serial.SerialException:
            print("Failed to connect to Arduino.")
        send_command(f'a{k_f[0][0]}, {k_f[0][1]}')
        print(f'{k_f[0][0]}, {k_f[0][1]}')

        self.phrase_valeur.set("Début de l'étalonnage. \n Appuyez sur start pour passer à la première étape")
        etalonnage.étapes = 0

    # fonction pour curve fit
    def mon_curve_fit(self, fct, liste_var_indep, liste_var_dep):
        parameters, covariance = curve_fit(fct, liste_var_indep, liste_var_dep)
        return [parameters, covariance]

# Fonction d'une droite pour curve fit
    def droite(self, x, m, b):
        y = (m*x)+b
        return y


class choix(tk.Frame):
    correction = -1 * float(0)
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.frame_poids = ttk.Frame(self)
        self.frame_poids.pack(side="top", padx=20, pady=20)
        self.poids_label = ttk.Label(self.frame_poids, text="Comptage de pièces", font=("Arial", 30))
        self.poids_label.pack()

        # 0,05$
        self.frame_poids_1 = ttk.Frame(self)
        self.frame_poids_1.pack(side="left", padx=20, pady=20)
        self.poids_label_1 = ttk.Label(self.frame_poids_1, text="0,05$:", font=("Arial", 14))
        self.poids_label_1.pack()

        self.poids_valeur_1 = tk.StringVar()
        self.poids_valeur_1.set("0")
        self.poids_affichage_1 = ttk.Label(self.frame_poids_1, textvariable=self.poids_valeur_1, font=("Arial", 20))
        self.poids_affichage_1.pack()


        # 0,10$
        self.frame_poids_2 = ttk.Frame(self)
        self.frame_poids_2.pack(side="left", padx=20, pady=20)
        self.poids_label_2 = ttk.Label(self.frame_poids_2, text="0,10$:", font=("Arial", 14))
        self.poids_label_2.pack()

        self.poids_valeur_2 = tk.StringVar()
        self.poids_valeur_2.set("0")
        self.poids_affichage_2 = ttk.Label(self.frame_poids_2, textvariable=self.poids_valeur_2, font=("Arial", 20))
        self.poids_affichage_2.pack()

        # 0,25$
        self.frame_poids_3 = ttk.Frame(self)
        self.frame_poids_3.pack(side="left", padx=20, pady=20)
        self.poids_label_3 = ttk.Label(self.frame_poids_3, text="0,25$:", font=("Arial", 14))
        self.poids_label_3.pack()

        self.poids_valeur_3 = tk.StringVar()
        self.poids_valeur_3.set("0")
        self.poids_affichage_3 = ttk.Label(self.frame_poids_3, textvariable=self.poids_valeur_3, font=("Arial", 20))
        self.poids_affichage_3.pack()

        # 1$
        self.frame_poids_4 = ttk.Frame(self)
        self.frame_poids_4.pack(side="left", padx=20, pady=20)
        self.poids_label_4 = ttk.Label(self.frame_poids_4, text="1$:", font=("Arial", 14))
        self.poids_label_4.pack()

        self.poids_valeur_4 = tk.StringVar()
        self.poids_valeur_4.set("0")
        self.poids_affichage_4 = ttk.Label(self.frame_poids_4, textvariable=self.poids_valeur_4, font=("Arial", 20))
        self.poids_affichage_4.pack()

        # 2$
        self.frame_poids_5 = ttk.Frame(self)
        self.frame_poids_5.pack(side="left", padx=20, pady=20)
        self.poids_label_5 = ttk.Label(self.frame_poids_5, text="2$:", font=("Arial", 14))
        self.poids_label_5.pack()

        self.poids_valeur_5 = tk.StringVar()
        self.poids_valeur_5.set("0")
        self.poids_affichage_5 = ttk.Label(self.frame_poids_5, textvariable=self.poids_valeur_5, font=("Arial", 20))
        self.poids_affichage_5.pack()

        # Bouton
        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='bottom',padx=20, pady=20)

        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Menu", command = lambda : controller.show_frame(menu))
        self.bouton_fonction1.pack(pady=10)

        self.multiple()

    def multiple(self):
        ref = {'0,05':3.95, '0,10':1.75, '0,25':4.4, '1':6.27, '2':6.92}
        poids = self.lire_poids_aleatoire()
        # poids = ser.readline().decode().strip()
        self.poids_valeur_1.set(f'{round((poids-choix.correction)/ref["0,05"])}')
        self.poids_valeur_2.set(f'{round((poids-choix.correction)/ref["0,10"])}')
        self.poids_valeur_3.set(f'{round((poids-choix.correction)/ref["0,25"])}')
        self.poids_valeur_4.set(f'{round((poids-choix.correction)/ref["1"])}')
        self.poids_valeur_5.set(f'{round((poids-choix.correction)/ref["2"])}')
        self.after(1000, self.multiple)

    def lire_poids_aleatoire(self):
        # Simulation de la lecture du poids
        return round(random.uniform(0, 100), 2)

    def tare(self):
        # choix.correction = -1 * float(ser.readline().decode().strip())
        choix.correction = -1* self.lire_poids_aleatoire()
        print('Tare effectué')

if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()
