# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.process.stk_utils import *

def process_access_sensors(path, const1, const2, res):

    name = str(const1)
    if const2 :
        name = name + "+" + str(const2)

    # Résolution au nadir (compose le nom de fichiers existants)
    
    avg_list = []
    res_list = []
    for r in res:
        
        name_res = const1.name_with_res(r)
        if const2 :
            name_res = name_res + "+" + const2.name_with_res(r)
        print(name_res)
        
        # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time 
        # (UTCG)" par exemple)
        try :
            db = pd.read_csv(path + '/' + name_res + ".csv", delimiter = ",")
            db_sorted = db.sort_values(by=("Start Time (UTCG)"))
            index = np.arange(0, len(db_sorted))
            db_sorted.insert(0, "index", index)
            revisit_times = np.zeros(len(db_sorted))
            
            for i in range(0, len(db_sorted)-1):
                try:
                    revisit_times[i] = pd.to_datetime(
                        db_sorted.iloc[i+1, 2]).timestamp() - pd.to_datetime(
                            db_sorted.iloc[i, 3]).timestamp()
                except:
                    break
            avg, minutes, revisit_times_non_null = moy_non_null(revisit_times)

            fig1 = plt.figure()
            plt.minorticks_on()    
            plt.grid(True, which="major", color="k", linestyle="-")
            plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
            plt.title("Revisit time, avg = "+minsec(avg))
            plt.xlabel("Number of revisits")
            plt.ylabel("Revisit time (min)")
            plt.scatter(np.linspace(0, len(revisit_times_non_null), len(revisit_times_non_null)),
                        minutes, s=10)
            fig1.savefig(path + '/' + name_res + ".png",
                            dpi=300, bbox_inches='tight')
        
            print(minsec(avg))
            print(r)
            res_list.append(r)
            avg_list.append(avg)
        except FileNotFoundError as e :
            print(e)
        
    # Moyenne des revisites en fonction de la pire résolution atteignable.
    fig2 = plt.figure()
    plt.plot(res_list, avg_list, marker="o")
    plt.minorticks_on()    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    plt.title("Revisit time")
    plt.xlabel("Ground resolution at the cone\'s limit (m)")
    plt.ylabel("Revisit time (min)")
    fig2.savefig(path + "/" + name + "_res_moy.png", 
                    dpi=300, pad_inches=0)
