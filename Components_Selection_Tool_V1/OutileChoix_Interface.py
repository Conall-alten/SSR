# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 10:49:34 2023

@author: cpelleray2
"""

import tkinter as tk
from tkinter import ttk

import choix_moteur as ch_m

class Interface:
    
    def __init__(self):
        
        def get_selected_item(listbox):
            selected_items = []
            selected_indices = listbox.curselection()
            for index in selected_indices:
                selected_items.append(listbox.get(index))
            return selected_items

        def get_inputs():
            #input de la partie Cahier des Charges$            
            
            self.altitude = float(self.SpinAlt.get())
            self.resolution = float(self.SpinRes.get())
            self.vie = float(self.SpinVie.get())
            self.photo = float(self.SpinPhoto.get())
            self.masse = float(self.SpinMass.get())
            self.origine = self.ComboOrigin.get()
            
            self.hy1 = self.hyp_poids.get()
            self.hy2 = self.hyp_conso.get()
            self.hy3 = self.hyp_cout.get()
            self.ISP = 100
            self.POUSSEE = 0.001
            print("ready")
            return
        
        def afficher_resultat():
            self.ListeCOMP.insert(0,ch_m.CHOIX_MOTEUR(self.hy1, self.hy2, self.hy3, self.origine, self.POUSSEE, self.ISP))
        
        def clear_listbox():
            self.ListeBesoin.delete(0,tk.END)
            self.ListeCOMP.delete(0,tk.END)

        listePays=["Par Défault","Europe","France", "Allemagne","Italie","Israel","Suède","Afrique du Sud","Etats-Unis"]
        
        self.window = tk.Tk()
        self.window.geometry('950x400')
        self.window.configure(bg='#EEEEEE')
        self.window.title('Outile V1')
        
        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label='Save As')
        self.file_menu.add_command(label='Quitter',command=self.window.destroy)
        self.menubar.add_cascade(label="Fichier",menu=self.file_menu)
        #----------------------------------------------------------------------
        #déclaration des widget cahier des charges
        self.TitleCDC = tk.Label(self.window,text="Cahier des Charges :",bg="#FFFFFF",width=40)
        self.TitleCDC.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

        self.TitleEntryAlt= tk.Label(self.window,text="Altitude (km)",bg="#EEEEEE",width=20)
        self.TitleEntryAlt.grid(row=1,column=0)
        self.SpinAlt = ttk.Spinbox(self.window,from_=200,to=1000,increment=5,width=10)
        self.SpinAlt.grid(row=1,column=1)
        self.SpinAlt.set(400)
         
        self.TitleEntryRes= tk.Label(self.window,text="Résolution (m)",bg="#EEEEEE",width=20)
        self.TitleEntryRes.grid(row=2,column=0)
        self.SpinRes = ttk.Spinbox(self.window,from_=0.1,to=100,increment=0.1,width=10)
        self.SpinRes.grid(row=2,column=1)
        self.SpinRes.set(1)

        self.TitleEntryVie= tk.Label(self.window,text="Durée Vie (mois)",bg="#EEEEEE",width=20)
        self.TitleEntryVie.grid(row=3,column=0)
        self.SpinVie = ttk.Spinbox(self.window,from_=0,to=50,increment=1,width=10)
        self.SpinVie.grid(row=3,column=1)
        self.SpinVie.set(6)

        self.TitleEntryPhoto= tk.Label(self.window,text="Photo/orbite (nb)",bg="#EEEEEE",width=20)
        self.TitleEntryPhoto.grid(row=4,column=0)
        self.SpinPhoto = ttk.Spinbox(self.window,from_=1,to=10,increment=1,width=10)
        self.SpinPhoto.grid(row=4,column=1)
        self.SpinPhoto.set(1)
        
        self.TitleEntryMass= tk.Label(self.window,text="Masse totale (kg)",bg="#EEEEEE",width=20)
        self.TitleEntryMass.grid(row=5,column=0)
        self.SpinMass = ttk.Spinbox(self.window,from_=1,to=100,increment=1,width=10)
        self.SpinMass.grid(row=5,column=1)
        self.SpinMass.set(15)

        self.TitleEntryOrigin= tk.Label(self.window,text="Origine",bg="#EEEEEE",width=20)
        self.TitleEntryOrigin.grid(row=6,column=0)
        self.ComboOrigin = ttk.Combobox(self.window,values=listePays, width = 15)
        self.ComboOrigin.grid(row=6,column=1)
        self.ComboOrigin.current(0)
        
        #----------------------------------------------------------------------
        #déclaration des widget hypothèse
        self.TitleHYPO = tk.Label(self.window,text="Hypothèses :",bg="#FFFFFF",width=40)
        self.TitleHYPO.grid(row=7,column=0,columnspan=2,padx=10,pady=10)

        self.hyp_poids = tk.IntVar()
        self.CheckPoids = ttk.Checkbutton(self.window,text="Le plus léger",variable=self.hyp_poids,width=30)
        self.CheckPoids.grid(row=8,column=0,columnspan=2)
        self.CheckPoids.config(state=tk.NORMAL)
         
        self.hyp_conso = tk.IntVar()
        self.CheckConso = ttk.Checkbutton(self.window,text="Le moins consomateur",variable=self.hyp_conso,width=30)
        self.CheckConso.grid(row=9,column=0,columnspan=2)
        self.CheckConso.config(state=tk.NORMAL)

        self.hyp_cout = tk.IntVar()
        self.CheckCout = ttk.Checkbutton(self.window,text="Le moins cher",variable=self.hyp_cout,width=30)
        self.CheckCout.grid(row=10,column=0,columnspan=2)
        self.CheckCout.config(state=tk.NORMAL)
        
        #----------------------------------------------------------------------
        #déclaration des widget liste besoin
        self.TitleBESOIN = tk.Label(self.window,text="Liste des besoins et caractéristiques :",bg="#FFFFFF",width=40)
        self.TitleBESOIN.grid(row=0,column=2,columnspan=2,padx=10,pady=10)
        self.ListeBesoin = tk.Listbox(self.window,width=45)
        self.ListeBesoin.insert(1,"En cours de dev")  
        self.ListeBesoin.grid(row=1,column=2,rowspan=11,columnspan=2)  

        #----------------------------------------------------------------------
        #déclaration des widget liste composant
        self.TitleCOMP = tk.Label(self.window,text="Liste des composants :",bg="#FFFFFF",width=40)
        self.TitleCOMP.grid(row=0,column=4,columnspan=2,padx=10,pady=10)
        self.ListeCOMP = tk.Listbox(self.window,width=45)
        self.ListeCOMP.insert(1,"En cours de dev")  
        self.ListeCOMP.grid(row=1,column=4,rowspan=11,columnspan=2)  
        
        
        #bouton run
        self.TitleRUN = tk.Label(self.window,text="Programme :",bg="#FFFFFF",width=40)
        self.TitleRUN.grid(row=11,column=0,columnspan=2,padx=10,pady=10)
        self.BoutonValide = ttk.Button(self.window,text="Valider les données",command=get_inputs,width=30)
        self.BoutonValide.grid(row=12,column=0,rowspan=2,columnspan=2)
        self.BoutonRun = ttk.Button(self.window,text="Run",command=afficher_resultat,width=30)
        self.BoutonRun.grid(row=14,column=0,rowspan=2,columnspan=2)
        self.BoutonClear = ttk.Button(self.window,text="Clear",command=clear_listbox,width=30)
        self.BoutonClear.grid(row=16,column=0,rowspan=2,columnspan=2)

        self.window.mainloop()