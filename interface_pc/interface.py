import tkinter as tk
from tkinter import ttk
import time
import serial
import random
import time


ser = serial.Serial('/dev/cu.usbmodem11301', 9600)

arduino_port = '/dev/cu.usbmodem11301'
baud_rate = 9600



# def send_command(command):
#     ser.write(command.encode())

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

        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='top',padx=20, pady=20)
        
        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Poids", command = lambda : controller.show_frame(weight))
        self.bouton_fonction1.pack(pady=10)
        
        self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Étalonnage", command=lambda : controller.show_frame(etalonnage))
        self.bouton_fonction2.pack(pady=10)
        
        self.bouton_fonction3 = ttk.Button(self.frame_boutons, text="Compter les pièce", command=lambda : controller.show_frame(choix))
        self.bouton_fonction3.pack(pady=10)


class weight(tk.Frame):
    def __init__(self, parent, controller):
        # tk.Frame.__init__(self, parent)
        super().__init__(parent)
        self.controller = controller
        # self.title("Menu de Pesée")
        # self.geometry('400x200')
        self.frame_poids = ttk.Frame(self)
        self.frame_poids.pack(side="left", padx=20, pady=20)
        self.poids_label = ttk.Label(self.frame_poids, text="Poids mesuré:", font=("Arial", 14))
        self.poids_label.pack()
        
        self.poids_valeur = tk.StringVar()
        self.poids_valeur.set("0")
        self.poids_affichage = ttk.Label(self.frame_poids, textvariable=self.poids_valeur, font=("Arial", 20))
        self.poids_affichage.pack()



        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='bottom',padx=20, pady=20)
        
        self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Tare", command= self.tarer)
        self.bouton_fonction2.pack(pady=10)

        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Menu", command = lambda : controller.show_frame(menu))
        self.bouton_fonction1.pack(pady=10)

        self.lire_poids_arduino()

    def lire_poids_arduino(self):
        #poids = self.lire_poids_aleatoire()  # Remplacer par la lecture réelle depuis l'Arduino
        poids = ser.readline().decode().strip()
        self.poids_valeur.set(str(poids))
        self.after(100, self.lire_poids_arduino)

    def lire_poids_aleatoire(self):
        # Simulation de la lecture du poids
        return round(random.uniform(0, 100), 2)

    
    def tarer(self):
        # send_command('t')
        print('tare effectué')

class etalonnage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='bottom',padx=20, pady=20)
        
        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Menu", command = lambda : controller.show_frame(menu))
        self.bouton_fonction1.pack(pady=10)

class choix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='bottom',padx=20, pady=20)
        
        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Menu", command = lambda : controller.show_frame(menu))
        self.bouton_fonction1.pack(pady=10)

if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()





# class InterfaceGraphique(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Interface Graphique avec Arduino")
#         self.geometry("400x200")
        
#         self.frame_poids = ttk.Frame(self)
#         self.frame_poids.pack(side="left", padx=20, pady=20)
        
#         self.poids_label = ttk.Label(self.frame_poids, text="Poids mesuré:", font=("Arial", 14))
#         self.poids_label.pack()
        
#         self.poids_valeur = tk.StringVar()
#         self.poids_valeur.set("0")
#         self.poids_affichage = ttk.Label(self.frame_poids, textvariable=self.poids_valeur, font=("Arial", 20))
#         self.poids_affichage.pack()
        
#         self.frame_boutons = ttk.Frame(self)
#         self.frame_boutons.pack(side="right", padx=20, pady=20)
        
#         self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Tare", command=self.activer_fonction1)
#         self.bouton_fonction1.pack(pady=10)
        
#         self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Étalonnage", command=self.activer_fonction2)
#         self.bouton_fonction2.pack(pady=10)
        
#         self.bouton_fonction3 = ttk.Button(self.frame_boutons, text="Choisir une dénomination", command=self.activer_fonction3)
#         self.bouton_fonction3.pack(pady=10)
        
#         self.lire_poids_arduino()

#     def lire_poids_arduino(self):
#         poids = ser.readline().decode().strip()
#         # poids = self.lire_poids_aleatoire()  # Remplacer par la lecture réelle depuis l'Arduino
#         self.poids_valeur.set(str(poids))
#         self.after(500, self.lire_poids_arduino)

#     def lire_poids_aleatoire(self):
#         # Simulation de la lecture du poids
#         return round(random.uniform(0, 100), 2)

#     def activer_fonction1(self):
#         # Appeler la fonction 1 sur l'Arduino
#         print("Fonction 1 activée")

#     def activer_fonction2(self):
#         # Appeler la fonction 2 sur l'Arduino
#         print("Fonction 2 activée")

#     def activer_fonction3(self):
#         # Appeler la fonction 3 sur l'Arduino
#         print("Fonction 3 activée")

# if __name__ == "__main__":
#     app = InterfaceGraphique()
#     app.mainloop()
