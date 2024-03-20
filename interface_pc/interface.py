import tkinter as tk
from tkinter import ttk
import time
import serial


arduino_port = '/dev/cu.usbmodem21301'  # Ports: Sim = '/dev/cu.usbmodem21301', Loic = '/dev/cu.usbmodem1301', Dan = ''
baud_rate = 9600  # Make sure it matches the baud rate in your Arduino sketch

root = tk.Tk()
root.title("Arduino Control")

try:
    ser = serial.Serial(arduino_port, baud_rate)
except serial.SerialException:
    print("Failed to connect to Arduino.")

def send_command(command):
    ser.write(command.encode())

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
        
        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Tare", command=self.tarer)
        self.bouton_fonction1.pack(pady=10)
        
        self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Étalonnage", command=self.etalon)
        self.bouton_fonction2.pack(pady=10)
        
        self.bouton_fonction3 = ttk.Button(self.frame_boutons, text="Choisir une dénomination", command=self.compter)
        self.bouton_fonction3.pack(pady=10)
        
        self.peser()

    def peser(self):
        send_command('p')


    def tarer(self):
        send_command('t')

    def etalon(self):
        send_command('e')

    def compter(self):
        send_command('c')


if __name__ == "__main__":
    app = InterfaceGraphique()
    app.mainloop()

root.mainloop()