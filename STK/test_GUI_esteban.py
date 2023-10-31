# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:39:58 2023

@author: cpelleray2
"""

import tkinter as tk
from tkinter import ttk

class Interface:
    
    def __init__(self):
        

        def const_simple():
            self.FRAME_const_simple.grid_forget()
            self.FRAME_const_hybride.grid_forget()
            self.FRAME_const_simple.grid(row=2,column=5,rowspan=8,columnspan=2)
            self.FRAME_const_hybride.grid_forget()
            self.var_1 = 1

        def const_hybride():
            self.FRAME_const_simple.grid_forget()
            self.FRAME_const_hybride.grid_forget()
            self.FRAME_const_simple.grid(row=2,column=5,rowspan=8,columnspan=2)
            self.FRAME_const_hybride.grid(row=2,column=7,rowspan=8,columnspan=2)
            self.var_1 = 2
        
        def get_inputs():
            #------------------------------------------------------------------
            #stokage const1
            self.type_orb=self.COMB_orb.get()
            self.sat=self.SPIN_sat.get()
            self.plan=self.SPIN_plan.get()
            self.alt=self.SPIN_alt.get()
            #cas particulier SSO pour l'inclinaison
            if self.type_orb=="\SSO":
                self.inc=0
            else:
                self.inc=self.SPIN_inc.get()
            self.res=self.SPIN_res.get()
            self.ips=self.SPIN_ips.get()
            self.name1 = self.type_orb+"_"+str(self.sat)+"x"+str(self.plan)+"_"+str(self.inc)+"_"+str(self.alt)+"_"+str(self.ips)+"_"+str(self.res)
                
            #------------------------------------------------------------------
            #stockage const2
            self.type_orb2=self.COMB_orb2.get()
            #cas partilculier si const simple ou hybride
            self.alt2=self.SPIN_alt2.get()
            self.res2=self.SPIN_res2.get()
            self.ips2=self.SPIN_ips2.get()
            #cas particulier SSO pour l'inclinaison
            if self.type_orb2=="+SSO":
                self.inc2=0
            else:
                self.inc2=self.SPIN_inc.get()
            if self.var_1 == 1:
                self.sat2=0
                self.plan2=0
                self.name2=""
            else:
                self.sat2=self.SPIN_sat2.get()
                self.plan2=self.SPIN_plan2.get()
                self.name2 = self.type_orb2+"_"+str(self.sat2)+"x"+str(self.plan2)+"_"+str(self.inc2)+"_"+str(self.alt2)+"_"+str(self.ips2)+"_"+str(self.res2)
                
            self.name = self.name1+self.name2
            #------------------------------------------------------------------
            #chemin des fichiers
            self.path = self.ENTRY_path.get()
            self.folder1 = self.COMB_f1.get()
            self.folder2 = self.COMB_f2.get()
            self.folder3 = ""
            self.chemin = self.folder1+self.folder2
            #self.window.destroy()
            return
        
        def verif():
            get_inputs()
            self.TextVERIF1bis.config(text=self.name)
            self.TextVERIF0bis.config(text=self.chemin)
            try:
                open(self.path+self.folder1+self.folder2+self.name+".csv")
            except FileNotFoundError:
                self.TextVERIF2bis.config(text="Inexistant  ಠ╭╮ಠ")
                self.BoutonRun.grid_forget()
            else:
                self.TextVERIF2bis.config(text="Existe! ( ͡° ͜ʖ ͡°)")
                self.BoutonRun.grid(row=10,column=0,columnspan=2)
                
        def combo_bind(event):
            verif()
                


        self.window = tk.Tk()
        self.window.geometry('1400x400')
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
        #bouton run
        self.TitleRUN = tk.Label(self.window,text="Programme :",bg="#FFFFFF",width=60)
        self.TitleRUN.grid(row=5,column=0,columnspan=2)
        self.TextVERIF0 = tk.Label(self.window,text="Chemin :",bg="#EEEEEE",width=15)
        self.TextVERIF0.grid(row=6,column=0)
        self.TextVERIF0bis = tk.Label(self.window,text="Pas encore de chemin",bg="#FFFFFF",width=40)
        self.TextVERIF0bis.grid(row=6,column=1)
        self.TextVERIF1 = tk.Label(self.window,text="Fichier :",bg="#EEEEEE",width=15)
        self.TextVERIF1.grid(row=7,column=0)
        self.TextVERIF1bis = tk.Label(self.window,text="Pas encore de fichier",bg="#FFFFFF",width=40)
        self.TextVERIF1bis.grid(row=7,column=1)
        self.TextVERIF2 = tk.Label(self.window,text="Vérif :",bg="#EEEEEE",width=15)
        self.TextVERIF2.grid(row=8,column=0)
        self.TextVERIF2bis = tk.Label(self.window,text="RAS dans le secteur",bg="#FFFFFF",width=25)
        self.TextVERIF2bis.grid(row=8,column=1)
        
#------------------------------------------------------------------------------
        #chemin d'entrée
        self.TITRE_path= tk.Label(self.window,text="Chemin de la base données",bg="#FFFFFF",width=60)
        self.TITRE_path.grid(row=0,column=0,columnspan=4)
        self.TITRE_path_exemple= tk.Label(self.window,text=r"Exemple: C:\Users\folder_x\folder_y",bg="#EEEEEE",width=50)
        self.TITRE_path_exemple.grid(row=1,column=0,columnspan=4)
        self.ENTRY_path = tk.Entry(self.window,width=50)
        self.ENTRY_path.grid(row=2,column=0,columnspan=4)
        self.ENTRY_path.insert(0,r"C:\Users\cpelleray2\Documents\GitHub\SSR\STK")
            

            
        liste_Type = [r"\RCO",r"\SSO",r"\CITROUILLE"]
        liste_Type2 = ["+RCO","+SSO","+CITROUILLE"]
        #frame const simple
        self.FRAME_const_simple = tk.Frame(self.window)
        self.FRAME_const_simple.grid(row=2,column=5,rowspan=8,columnspan=2)
        
        self.TITRE_Frame_const_simple = tk.Label(self.FRAME_const_simple,text="Constellation principale")
        self.TITRE_Frame_const_simple.grid(row=0,column=0,columnspan=2)
        
        self.TITRE_orb= tk.Label(self.FRAME_const_simple,text="Type d'orbite",bg="#EEEEEE",width=20)
        self.TITRE_orb.grid(row=1,column=0)
        self.COMB_orb = ttk.Combobox(self.FRAME_const_simple,values=liste_Type,width = 10)
        self.COMB_orb.grid(row=1,column=1)
        self.COMB_orb.current(0)
        self.COMB_orb.bind('<<ComboboxSelected>>',combo_bind)
    
        self.TITRE_plan= tk.Label(self.FRAME_const_simple,text="Nb plan",bg="#EEEEEE",width=20)
        self.TITRE_plan.grid(row=3,column=0)
        self.SPIN_plan = ttk.Spinbox(self.FRAME_const_simple,from_=1,to=100,increment=1,width=10,command=verif)
        self.SPIN_plan.grid(row=3,column=1)
        self.SPIN_plan.set(4)
        
        self.TITRE_sat= tk.Label(self.FRAME_const_simple,text="Nb sat/plan",bg="#EEEEEE",width=20)
        self.TITRE_sat.grid(row=2,column=0)
        self.SPIN_sat = ttk.Spinbox(self.FRAME_const_simple,from_=1,to=100,increment=1,width=10,command=verif)
        self.SPIN_sat.grid(row=2,column=1)
        self.SPIN_sat.set(2)
        
        self.TITRE_alt= tk.Label(self.FRAME_const_simple,text="Altitude (km)",bg="#EEEEEE",width=20)
        self.TITRE_alt.grid(row=5,column=0)
        self.SPIN_alt = ttk.Spinbox(self.FRAME_const_simple,from_=100,to=800,increment=10,width=10,command=verif)
        self.SPIN_alt.grid(row=5,column=1)
        self.SPIN_alt.set(260)
        
        self.TITRE_inc= tk.Label(self.FRAME_const_simple,text="Inclinaison (deg)",bg="#EEEEEE",width=20)
        self.TITRE_inc.grid(row=4,column=0)
        self.SPIN_inc = ttk.Spinbox(self.FRAME_const_simple,from_=0,to=120,increment=1,width=10,command=verif)
        self.SPIN_inc.grid(row=4,column=1)
        self.SPIN_inc.set(50)
        
        self.TITRE_ips= tk.Label(self.FRAME_const_simple,text="IPS",bg="#EEEEEE",width=20)
        self.TITRE_ips.grid(row=6,column=0)
        self.SPIN_ips = ttk.Spinbox(self.FRAME_const_simple,from_=0,to=3000,increment=1,width=10,command=verif)
        self.SPIN_ips.grid(row=6,column=1)
        self.SPIN_ips.set(0)
        
        self.TITRE_res= tk.Label(self.FRAME_const_simple,text="Résolution (m)",bg="#EEEEEE",width=20)
        self.TITRE_res.grid(row=7,column=0)
        self.SPIN_res = ttk.Spinbox(self.FRAME_const_simple,from_=0,to=30,increment=0.1,width=10,command=verif)
        self.SPIN_res.grid(row=7,column=1)
        self.SPIN_res.set(1.0)

        
        #♣frame const secondaire
        self.FRAME_const_hybride = tk.Frame(self.window)
        self.TITRE_Frame_const_hybride = tk.Label(self.FRAME_const_hybride,text="Constellation secondaire")
        self.TITRE_Frame_const_hybride.grid(row=0,column=0,columnspan=2)
        
        self.TITRE_orb2= tk.Label(self.FRAME_const_hybride,text="Type d'orbite",bg="#EEEEEE",width=20)
        self.TITRE_orb2.grid(row=1,column=0)
        self.COMB_orb2 = ttk.Combobox(self.FRAME_const_hybride,values=liste_Type2, width = 10)
        self.COMB_orb2.grid(row=1,column=1)
        self.COMB_orb2.current(0)
        self.COMB_orb2.bind('<<ComboboxSelected>>',combo_bind)
        
        self.TITRE_plan2= tk.Label(self.FRAME_const_hybride,text="Nb plan",bg="#EEEEEE",width=20)
        self.TITRE_plan2.grid(row=3,column=0)
        self.SPIN_plan2 = ttk.Spinbox(self.FRAME_const_hybride,from_=1,to=100,increment=1,width=10,command=verif)
        self.SPIN_plan2.grid(row=3,column=1)
        self.SPIN_plan2.set(4)
        
        self.TITRE_sat2= tk.Label(self.FRAME_const_hybride,text="Nb sat/plan",bg="#EEEEEE",width=20)
        self.TITRE_sat2.grid(row=2,column=0)
        self.SPIN_sat2 = ttk.Spinbox(self.FRAME_const_hybride,from_=1,to=100,increment=1,width=10,command=verif)
        self.SPIN_sat2.grid(row=2,column=1)
        self.SPIN_sat2.set(2)
        
        self.TITRE_alt2= tk.Label(self.FRAME_const_hybride,text="Altitude (km)",bg="#EEEEEE",width=20)
        self.TITRE_alt2.grid(row=5,column=0)
        self.SPIN_alt2 = ttk.Spinbox(self.FRAME_const_hybride,from_=100,to=800,increment=10,width=10,command=verif)
        self.SPIN_alt2.grid(row=5,column=1)
        self.SPIN_alt2.set(260)
        
        self.TITRE_inc2= tk.Label(self.FRAME_const_hybride,text="Inclinaison (deg)",bg="#EEEEEE",width=20)
        self.TITRE_inc2.grid(row=4,column=0)
        self.SPIN_inc2 = ttk.Spinbox(self.FRAME_const_hybride,from_=0,to=120,increment=1,width=10,command=verif)
        self.SPIN_inc2.grid(row=4,column=1)
        self.SPIN_inc2.set(50)
        
        self.TITRE_ips2= tk.Label(self.FRAME_const_hybride,text="IPS",bg="#EEEEEE",width=20)
        self.TITRE_ips2.grid(row=6,column=0)
        self.SPIN_ips2 = ttk.Spinbox(self.FRAME_const_hybride,from_=0,to=3000,increment=1,width=10,command=verif)
        self.SPIN_ips2.grid(row=6,column=1)
        self.SPIN_ips2.set(0)
        
        self.TITRE_res2= tk.Label(self.FRAME_const_hybride,text="Résolution (m)",bg="#EEEEEE",width=20)
        self.TITRE_res2.grid(row=7,column=0)
        self.SPIN_res2 = ttk.Spinbox(self.FRAME_const_hybride,from_=0,to=30,increment=0.1,width=10,command=verif)
        self.SPIN_res2.grid(row=7,column=1)
        self.SPIN_res2.set(1.0)  

        
        #type const
        self.var_1 = tk.IntVar()
        #self.var_1.set(1)
        self.TITRE_type = tk.Label(self.window,text="Type de constellation",bg="#FFFFFF",width=60)
        self.TITRE_type.grid(row=0,column=5,columnspan=2)
        self.R1 = ttk.Radiobutton(self.window,text="Constellation simple",variable=self.var_1,value=1,command=lambda:[const_simple(), verif()])
        self.R1.grid(row=1,column=5)
        self.R2 = ttk.Radiobutton(self.window,text="Constellation hybride",variable=self.var_1,value=2,command=lambda:[const_hybride(), verif()])
        self.R2.grid(row=1,column=6)
        
        
#-----------------------------------------------------------------------------
        
        liste_f1 = [r"\target_primary",r"\target_secondary",r"\global",r"\files_points",r"\general_shapes"]
        liste_f2 = [r"\access_sensors",r"\access_ground",r"\FoM_points",r"\region"]
        self.TITRE_f1 = tk.Label(self.window,text="Folder 1",width=20)
        self.TITRE_f1.grid(row=3,column=0)
        self.COMB_f1 = ttk.Combobox(self.window,values=liste_f1, width = 25)
        self.COMB_f1.grid(row=3,column=1)
        self.COMB_f1.current(0)
        self.COMB_f1.bind('<<ComboboxSelected>>',combo_bind)
        self.TITRE_f2 = tk.Label(self.window,text="Folder 2",width=20)
        self.TITRE_f2.grid(row=4,column=0)
        self.COMB_f2 = ttk.Combobox(self.window,values=liste_f2, width = 25)
        self.COMB_f2.grid(row=4,column=1)
        self.COMB_f2.current(0)
        self.COMB_f2.bind('<<ComboboxSelected>>',combo_bind)

        self.BoutonRun = ttk.Button(self.window,text="o(≧∀≦)o LANCEZ LES SCHEMAS !!! ^_~",command=self.window.destroy,width=35)
        #self.BoutonRun.grid(row=10,column=0,columnspan=2)

        #verif()

        self.window.mainloop()
    