# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.process.stk_utils import *

def process_region(path, const1, const2, res):

    res_list = []

    # Cibles ponctuelles (lon, lat) en décimales
    Donetsk = [37.805, 48.003]
    Kherson = [32.611, 46.634]
    Luhansk = [39.303, 48.567]
    RostovDon = [39.7, 47.24]
    Sevastopol = [33.5225, 44.605]
    Zaporizhzhia = [35.1175, 47.85]

    # Ordre alphabétique !!!
    targets = [Donetsk, 
            Kherson, 
            Luhansk, 
            RostovDon, 
            Sevastopol, 
            Zaporizhzhia]
    
    for r in res:
        
        res_list.append(r)
        name = const1.name_with_res(r)
        # Traitement du fichier csv
        N = const1.nb_sat()
        # Le délimiteur peut être , ou ; si le fichier csv a transité sur Teams
        # (changer si KeyError: "Start Time (UTCG)")
        # db est un DataFrame (sorte de tableau)
        try :
            db = pd.read_csv(path + "/" + name + ".csv", skiprows=24+N, delimiter=",")

            db_sorted = db.sort_values(by=("Region Name"))
            # Les temps de revisite seront stockés dans cette liste
            revisit_times = np.zeros(len(db_sorted))
            cities = []
            for i in range(0, len(db_sorted)):
                # db_sorted.iloc[i, 2] = valeur du ième élément de la 2e colonne
                # du tableau
                revisit_times[i] = db_sorted.iloc[i, 4]
                cities.append(db_sorted.iloc[i, 0])
                
            lat = []
            lon = []
            for i in targets:
                lat.append(i[1])
                lon.append(i[0])
            db_sorted.insert(0, "lat", lat)
            db_sorted.insert(1, "lon", lon)
            

            avg, minutes, revisit_times_non_null = moy_non_null(revisit_times)
            fig1 = plt.figure()
            plt.minorticks_on()
            plt.title("Revisit time, avg = "+minsec(avg))
            plt.xlabel("Longitude (deg)")
            plt.ylabel("Latitude (deg)")
            
            for i in range(len(db)):
                plt.grid(True, which="major", color="k", linestyle="-")
                plt.grid(True, which="minor", color="grey", linestyle="-",
                        alpha = 0.2)
                plt.scatter(db_sorted.iloc[i, 1], db_sorted.iloc[i, 0], s = 50, 
                            label = str(cities[i]).replace("_city","")+", "+str(
                                minutes[i])+" min")
                plt.legend()
            
            fig1.savefig(path + "/" + name + ".png", dpi=300,
                        bbox_inches='tight')
        
        except FileNotFoundError as e :
            print(const1.name_with_res(r), "does not exist")
