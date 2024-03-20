import tkinter as tk
from tkinter import ttk
import time
import serial


arduino_port = '/dev/cu.usbmodem21301'  # Ports: Sim = '/dev/cu.usbmodem21301', Loic = '/dev/cu.usbmodem11301', Dan = ''
baud_rate = 9600  # Make sure it matches the baud rate in your Arduino sketch

# root = tk.Tk()
# root.title("Arduino Control")

# try:
#     ser = serial.Serial(arduino_port, baud_rate)
# except serial.SerialException:
#     print("Failed to connect to Arduino.")

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
        tk.Frame.__init__(self, parent)
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
        tk.Frame.__init__(self, parent)
        # self.title("Menu de Pesée")
        # self.geometry('400x200')
        self.frame_boutons = ttk.Frame(self)
        self.frame_boutons.pack(side='bottom',padx=20, pady=20)
        
        self.bouton_fonction1 = ttk.Button(self.frame_boutons, text="Menu", command = lambda : controller.show_frame(menu))
        self.bouton_fonction1.pack(pady=10)

        self.bouton_fonction2 = ttk.Button(self.frame_boutons, text="Tare", command= self.tarer)
        self.bouton_fonction2.pack(pady=10)
    
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
