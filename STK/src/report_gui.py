# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:39:58 2023

@author: cpelleray2
"""

import tkinter as tk
from tkinter import ttk
from constellation import Constellation

class Report_GUI:

    def get_inputs(self):

            #cas particulier SSO pour l'inclinaison
            if self.frame_const_comp[0][1][1].get()=="SSO":
                self.frame_const_comp[0][4][1].set(0)

            self.name1 = "_".join((self.frame_const_comp[0][1][1].get(),
                                   self.frame_const_comp[0][2][1].get() + "x" + self.frame_const_comp[0][3][1].get(),
                                   self.frame_const_comp[0][4][1].get(),
                                   self.frame_const_comp[0][5][1].get(),
                                   self.frame_const_comp[0][6][1].get(),
                                   self.frame_const_comp[0][7][1].get()))
                
            if self.var_1.get() == 2 :
                if self.frame_const_comp[1][1][1].get()=="SSO":
                    self.frame_const_comp[1][4][1].set(0)

                self.name2 = "+" + "_".join((self.frame_const_comp[1][1][1].get(),
                                             self.frame_const_comp[1][2][1].get() + "x" + self.frame_const_comp[1][3][1].get(),
                                             self.frame_const_comp[1][4][1].get(),
                                             self.frame_const_comp[1][5][1].get(),
                                             self.frame_const_comp[1][6][1].get(),
                                             self.frame_const_comp[1][7][1].get()))
            else :
                self.name2 = ""
                
            self.name = self.name1 + self.name2
            #------------------------------------------------------------------
            #chemin des fichiers
            self.path = self.ENTRY_path.get()
            self.folder1 = self.COMB_f1.get()
            self.folder2 = self.COMB_f2.get()
            self.folder3 = ""
            self.chemin = "/".join((self.folder1, self.folder2))
            return


    def verif(self):
        self.get_inputs()
        self.TextVERIF1bis.config(text=self.name)
        self.TextVERIF0bis.config(text=self.chemin)
        try:
            open("/".join((self.path, self.folder1, self.folder2, self.name+".csv")))
        except FileNotFoundError:
            self.TextVERIF2bis.config(text="Inexistant  ಠ╭╮ಠ")
            self.BoutonRun.grid_forget()
            print("/".join((self.path, self.folder1, self.folder2, self.name+".csv")))
        else:
            self.TextVERIF2bis.config(text="Existe! ( ͡° ͜ʖ ͡°)")
            self.BoutonRun.grid(row=10,column=0,columnspan=2)


    def combo_bind(self, event):
        self.verif()


    def add_row(self, idx, row, name, from_, to, inc, def_val):
            self.frame_const_comp[idx].append([
                tk.Label(self.frame_cons[idx], text=name,bg="#EEEEEE",width=20),
                ttk.Spinbox(self.frame_cons[idx], from_=from_, to=to, increment=inc, width=10, command=self.verif)
            ])
            self.frame_const_comp[idx][-1][0].grid(row=row, column=0) 
            self.frame_const_comp[idx][-1][1].grid(row=row, column=1)
            self.frame_const_comp[idx][-1][1].set(def_val)


    def add_constellation(self, const_name, liste_Type):
    
        self.frame_cons.append(tk.Frame(self.window))
        self.frame_const_comp.append([])

        self.frame_const_comp[-1].append([
            tk.Label(self.frame_cons[-1], text=const_name),
        ])
        self.frame_const_comp[-1][-1][0].grid(row=0,column=0,columnspan=2)

        self.frame_const_comp[-1].append([
            tk.Label(self.frame_cons[-1], text="Type d'orbite",bg="#EEEEEE",width=20),
            ttk.Combobox(self.frame_cons[-1], values=liste_Type,width = 10)
        ])
        self.frame_const_comp[-1][-1][0].grid(row=1, column=0) 
        self.frame_const_comp[-1][-1][1].grid(row=1, column=1)
        self.frame_const_comp[-1][-1][1].current(0)
        self.frame_const_comp[-1][-1][1].bind('<<ComboboxSelected>>', self.combo_bind)
        
        self.add_row(-1, 2, "Nb sat/plan", 1, 100, 1, 2)
        self.add_row(-1, 3, "Nb plan", 1, 100, 1, 4)
        self.add_row(-1, 4, "Inclinaison (deg)", 0, 120, 1, 5)
        self.add_row(-1, 5, "Altitude (km)", 100, 800, 10, 260)
        self.add_row(-1, 6, "IPS", 0, 3000, 1, 0)
        self.add_row(-1, 7, "Résolution (m)", 0, 30, 0.1, 1.0)


    def const_simple(self):
            self.frame_cons[0].grid_forget()
            self.frame_cons[1].grid_forget()
            self.frame_cons[0].grid(row=2,column=5,rowspan=8,columnspan=2)
            self.frame_cons[1].grid_forget()


    def const_hybride(self):
        self.frame_cons[0].grid_forget()
        self.frame_cons[1].grid_forget()
        self.frame_cons[0].grid(row=2,column=5,rowspan=8,columnspan=2)
        self.frame_cons[1].grid(row=2,column=7,rowspan=8,columnspan=2)


    def run_exec_fun(self):
        const1 = Constellation(*[elem[1].get() for elem in self.frame_const_comp[0][1:]], "")
        if self.var_1.get() == 2 :
            const2 = Constellation(*[elem[1].get() for elem in self.frame_const_comp[1][1:]], "")
        else :
            const2 = None
        self.exec_fun(
            "/".join((self.ENTRY_path.get(), self.COMB_f1.get(), self.COMB_f2.get())),
            self.COMB_f2.get(),
            const1, const2,
            res = [self.frame_const_comp[0][-1][1].get()],
            access_type = None
        )
        print("DONE")

    def __init__(self, exec_fun):
        
        self.exec_fun = exec_fun
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        self.window.geometry('1400x400')
        self.window.configure(bg='#EEEEEE')
        self.window.title('Outile V1')

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
        
        
        #------------------------------------------------------------------------------
        #Creation du constellation manager

        self.frame_cons = []
        self.frame_const_comp = []
        self.add_constellation("Constellation principale", ["RCO", "SSO", "CITROUILLE"])
        self.add_constellation("Constellation secondaire", ["RCO", "SSO", "CITROUILLE"])

        self.var_1 = tk.IntVar()
        self.TITRE_type = tk.Label(self.window,text="Type de constellation",bg="#FFFFFF",width=60)
        self.TITRE_type.grid(row=0, column=5, columnspan=2)
        self.R1 = ttk.Radiobutton(self.window, text="Constellation simple", variable=self.var_1, value=1, command=lambda:[self.const_simple(), self.verif()])
        self.R1.grid(row=1,column=5)
        self.R2 = ttk.Radiobutton(self.window, text="Constellation hybride", variable=self.var_1, value=2, command=lambda:[self.const_hybride(), self.verif()])
        self.R2.grid(row=1,column=6)


        #-----------------------------------------------------------------------------
        
        liste_f1 = ["target_primary", "target_secondary", "global", "files_points", "general_shapes"]
        liste_f2 = ["access_sensors", "access_ground", "FoM_points", "region"]
        self.TITRE_f1 = tk.Label(self.window,text="Folder 1",width=20)
        self.TITRE_f1.grid(row=3,column=0)
        self.COMB_f1 = ttk.Combobox(self.window,values=liste_f1, width = 25)
        self.COMB_f1.grid(row=3,column=1)
        self.COMB_f1.current(0)
        self.COMB_f1.bind('<<ComboboxSelected>>', self.combo_bind)
        self.TITRE_f2 = tk.Label(self.window,text="Folder 2",width=20)
        self.TITRE_f2.grid(row=4,column=0)
        self.COMB_f2 = ttk.Combobox(self.window,values=liste_f2, width = 25)
        self.COMB_f2.grid(row=4,column=1)
        self.COMB_f2.current(0)
        self.COMB_f2.bind('<<ComboboxSelected>>', self.combo_bind)

        self.BoutonRun = ttk.Button(self.window, text="o(≧∀≦)o LANCEZ LES SCHEMAS !!! ^_~", command=self.run_exec_fun, width=35)

        self.window.mainloop()
    