# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 10:42:42 2023

@author: cpelleray2
"""

import tkinter as tk
from tkinter import ttk

import choix_moteur as ch_m

class outile(tk.Tk):
    
    def __init__(self,*args,**kwargs):
        
        tk.Tk.__init__(self,*args,**kwargs)
        
        page_base=tk.Frame(self)
        page_base.pack(side="top",fill="both",expand=True)
        page_base.grid_rowconfigure(0, weight=1)
        page_base.grid_columnconfigure(0, weight=1)
        
        self.frames={}
        
        for F in (Page_1,Estimator,Selector):
            frame=F(page_base,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
            
        self.show_frame(Page_1)
        
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()
        
class Page_1(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        label=ttk.Label(self,text="page 1")
        label.grid(row=0,column=0)
        
        button1=ttk.Button(self,text="page 1",
        command = lambda : controller.show_frame(Page_1))
        button1.grid(row=1,column=0)
        
        button2=ttk.Button(self,text="estimator",
        command = lambda : controller.show_frame(Estimator))
        button2.grid(row=1,column=1)
        
        button3=ttk.Button(self,text="selector",
        command = lambda : controller.show_frame(Selector))
        button3.grid(row=1,column=2)
        
class Estimator(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=ttk.Label(self,text="estimator")
        label.grid(row=0,column=0)
        
        button1=ttk.Button(self,text="page 1",
        command = lambda : controller.show_frame(Page_1))
        button1.grid(row=1,column=0)
        
        button2=ttk.Button(self,text="estimator",
        command = lambda : controller.show_frame(Estimator))
        button2.grid(row=1,column=1)
        
        button3=ttk.Button(self,text="selector",
        command = lambda : controller.show_frame(Selector))
        button3.grid(row=1,column=2)
        
        label2=ttk.Label(self,text="choisi ton estimation")
        label2.grid(row=2,column=2)
        
        self.ISP=1000
        
class Selector(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=ttk.Label(self,text="selector")
        label.grid(row=0,column=0)
        
        button1=ttk.Button(self,text="page 1",
        command = lambda : controller.show_frame(Page_1))
        button1.grid(row=1,column=0)
        
        button2=ttk.Button(self,text="estimator",
        command = lambda : controller.show_frame(Estimator))
        button2.grid(row=1,column=1)
        
        button3=ttk.Button(self,text="selector",
        command = lambda : controller.show_frame(Selector))
        button3.grid(row=1,column=2)
        
        listePays=["Par Défault","Europe","France", "Allemagne","Italie","Israel","Suède","Afrique du Sud","Etats-Unis"]
        
        def get_inputs():
            #input de la partie Cahier des Charges$            
            
            self.altitude = float(SpinAlt.get())
            self.resolution = float(SpinRes.get())
            self.vie = float(SpinVie.get())
            self.photo = float(SpinPhoto.get())
            self.masse = float(SpinMass.get())
            self.origine = ComboOrigin.get()
            
            self.hy1 = hyp_poids.get()
            self.hy2 = hyp_conso.get()
            self.hy3 = hyp_cout.get()
            #self.ISP = 100
            self.POUSSEE = 0.1
            self.ISP = Estimator.ISP
            print("ready")
            return
        
        def afficher_resultat():
            ListeCOMP.insert(0,ch_m.CHOIX_MOTEUR(self.hy1, self.hy2, self.hy3, self.origine, self.POUSSEE, self.ISP))
        
        def clear_listbox():
            ListeBesoin.delete(0,tk.END)
            ListeCOMP.delete(0,tk.END)

        #déclaration des widget cahier des charges
        TitleCDC = tk.Label(self,text="Cahier des Charges :",bg="#FFFFFF",width=40)
        TitleCDC.grid(row=2,column=0,columnspan=2,padx=10,pady=10)

        TitleEntryAlt= tk.Label(self,text="Altitude (km)",bg="#EEEEEE",width=20)
        TitleEntryAlt.grid(row=3,column=0)
        SpinAlt = ttk.Spinbox(self,from_=200,to=1000,increment=5,width=10)
        SpinAlt.grid(row=3,column=1)
        SpinAlt.set(400)
         
        TitleEntryRes= tk.Label(self,text="Résolution (m)",bg="#EEEEEE",width=20)
        TitleEntryRes.grid(row=4,column=0)
        SpinRes = ttk.Spinbox(self,from_=0.1,to=100,increment=0.1,width=10)
        SpinRes.grid(row=4,column=1)
        SpinRes.set(1)

        TitleEntryVie= tk.Label(self,text="Durée Vie (mois)",bg="#EEEEEE",width=20)
        TitleEntryVie.grid(row=5,column=0)
        SpinVie = ttk.Spinbox(self,from_=0,to=50,increment=1,width=10)
        SpinVie.grid(row=5,column=1)
        SpinVie.set(6)

        TitleEntryPhoto= tk.Label(self,text="Photo/orbite (nb)",bg="#EEEEEE",width=20)
        TitleEntryPhoto.grid(row=6,column=0)
        SpinPhoto = ttk.Spinbox(self,from_=1,to=10,increment=1,width=10)
        SpinPhoto.grid(row=6,column=1)
        SpinPhoto.set(1)
        
        TitleEntryMass= tk.Label(self,text="Masse totale (kg)",bg="#EEEEEE",width=20)
        TitleEntryMass.grid(row=7,column=0)
        SpinMass = ttk.Spinbox(self,from_=1,to=100,increment=1,width=10)
        SpinMass.grid(row=7,column=1)
        SpinMass.set(15)

        TitleEntryOrigin= tk.Label(self,text="Origine",bg="#EEEEEE",width=20)
        TitleEntryOrigin.grid(row=8,column=0)
        ComboOrigin = ttk.Combobox(self,values=listePays, width = 15)
        ComboOrigin.grid(row=8,column=1)
        ComboOrigin.current(0)
        
        #----------------------------------------------------------------------
        #déclaration des widget hypothèse
        TitleHYPO = tk.Label(self,text="Hypothèses :",bg="#FFFFFF",width=40)
        TitleHYPO.grid(row=9,column=0,columnspan=2,padx=10,pady=10)

        hyp_poids = tk.IntVar()
        CheckPoids = ttk.Checkbutton(self,text="Le plus léger",variable=hyp_poids,width=30)
        CheckPoids.grid(row=10,column=0,columnspan=2)
        CheckPoids.config(state=tk.NORMAL)
         
        hyp_conso = tk.IntVar()
        CheckConso = ttk.Checkbutton(self,text="Le moins consomateur",variable=hyp_conso,width=30)
        CheckConso.grid(row=11,column=0,columnspan=2)
        CheckConso.config(state=tk.NORMAL)

        hyp_cout = tk.IntVar()
        CheckCout = ttk.Checkbutton(self,text="Le moins cher",variable=hyp_cout,width=30)
        CheckCout.grid(row=12,column=0,columnspan=2)
        CheckCout.config(state=tk.NORMAL)
        
        #----------------------------------------------------------------------
        #déclaration des widget liste besoin
        TitleBESOIN = tk.Label(self,text="Liste des besoins et caractéristiques :",bg="#FFFFFF",width=40)
        TitleBESOIN.grid(row=2,column=2,columnspan=2,padx=10,pady=10)
        ListeBesoin = tk.Listbox(self,width=45)
        ListeBesoin.insert(1,"En cours de dev")  
        ListeBesoin.grid(row=3,column=2,rowspan=11,columnspan=2)  

        #----------------------------------------------------------------------
        #déclaration des widget liste composant
        TitleCOMP = tk.Label(self,text="Liste des composants :",bg="#FFFFFF",width=40)
        TitleCOMP.grid(row=2,column=4,columnspan=2,padx=10,pady=10)
        ListeCOMP = tk.Listbox(self,width=45)
        ListeCOMP.insert(1,"En cours de dev")  
        ListeCOMP.grid(row=3,column=4,rowspan=11,columnspan=2)  
        
        
        #bouton run
        TitleRUN = tk.Label(self,text="Programme :",bg="#FFFFFF",width=40)
        TitleRUN.grid(row=13,column=0,columnspan=2,padx=10,pady=10)
        BoutonValide = ttk.Button(self,text="Valider les données",command=get_inputs,width=30)
        BoutonValide.grid(row=14,column=0,rowspan=2,columnspan=2)
        BoutonRun = ttk.Button(self,text="Run",command=afficher_resultat,width=30)
        BoutonRun.grid(row=16,column=0,rowspan=2,columnspan=2)
        BoutonClear = ttk.Button(self,text="Clear",command=clear_listbox,width=30)
        BoutonClear.grid(row=18,column=0,rowspan=2,columnspan=2)
        
app = outile()
app.mainloop()
        
        
        
        