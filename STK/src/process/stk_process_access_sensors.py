# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stk_utils import *

def process_access_sensors(path, name, Nsat1, Nplan1, inc1, alt1, IPS1, add1):

    avg, minutes, revisit_times_non_null = doing_thing(path, name, always_take = False)
    
    # Durée de chaque revisite et moyenne
    fig1 = plt.figure()
    plt.minorticks_on()    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    plt.title("Revisit time, avg = "+minsec(avg))
    plt.xlabel("Number of revisits")
    plt.ylabel("Revisit time (min)")
    plt.scatter(np.linspace(0, len(revisit_times_non_null), len(revisit_times_non_null)),
                minutes, s=10)
    fig1.savefig(path + '/' + name + ".png", dpi=300, bbox_inches='tight')

    # La même chose en faisant varier la résolution.
    
    avg_list = []
    res_list = []
    lat_diff = []
    
    # Résolution au nadir (compose le nom de fichiers existants)
    res = [1.0, 1.2, 1.4, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0] 
    
    for r in res:
        
        name1 = const1+"_"+str(Nsat1)+"x"+str(Nplan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(IPS1)+"_"+str(r)+add1
        print(name1)
        
        # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time 
        # (UTCG)" par exemple)
        db = pd.read_csv(path + '/' + name1 + ".csv", delimiter = ",")
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
       
        print(minsec(avg))
        print(r)
        res_list.append(r)
        avg_list.append(avg)
        
    # Moyenne des revisites en fonction de la pire résolution atteignable.
    fig2 = plt.figure()
    plt.plot(res_list, avg_list, marker="o")
    plt.minorticks_on()    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    plt.title("Revisit time, i = "+str(inc1)+"°, h = "+str(alt1)+"km")
    plt.xlabel("Ground resolution at the cone\'s limit")
    plt.ylabel("Revisit time (min)")