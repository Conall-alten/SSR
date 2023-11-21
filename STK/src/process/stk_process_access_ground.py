# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.process.stk_utils import *

def process_access_ground(path, const1, access_type):

    # Traitement du fichier csv

    avg, minutes, revisit_times_non_null = doing_thing(path, str(const1), always_take = True)
    
    # Durée de chaque revisite et moyenne
    fig1 = plt.figure()
    plt.minorticks_on()
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    plt.title("Revisit time, 1 week, avg = "+minsec(avg))
    plt.xlabel("Number of revisits")
    plt.ylabel("Revisit time (min)")
    plt.scatter(np.linspace(0, len(revisit_times_non_null), len(revisit_times_non_null)),
                minutes, s=10)
    fig1.savefig(path + "/" + name + ".png", dpi=300, bbox_inches='tight')
        
    #%% Link budget
    
    antenna_type = "dish"
    diameter = [0.5, 3, 6]
    
    for d in diameter:
        
        name = "\\"+str(antenna_type)+"_"+str(d)
        
        if access_type == "link":
                
            col_names = ["Time (UTCG)", "EIRP (dBW)", "Rcvd. Frequency (GHz)",
                         "Rcvd. Iso. Power (dBW)", "Flux Density (dBW/m^2)", 
                         "g/T (dB/K)", "C/No (dB*Hz)", "Bandwidth (kHz)", 
                         "C/N (dB)", "Eb/No (dB)", "Bit Error Rate"]
            
            # Traitement du fichier csv
            
            # Le délimiteur peut être , ou ; si le fichier csv a transité sur 
            # Teams (changer si KeyError: "Start Time (UTCG)")
            # db est un DataFrame (sorte de tableau)
            db = pd.read_csv(path + "/" + name + "_" + access_type + ".csv", 
                             delimiter=",", names=col_names)
            db_sorted = db.sort_values(by=("Time (UTCG)"))
            
            Time = []
            EIRP = []
            RF = []
            RIP = []
            FD = []
            g_T = []
            C_No = []
            BW = []
            C_N = []
            Eb_No = [] # Must be >1e-12???
            BER = [] # Bit error rate
            data = [Time, EIRP, RF, RIP, FD, g_T, C_No, BW, C_N, Eb_No, BER]
            
            for i in range(len(data)):
                for j in range(len(db_sorted)-1):
                    if i==0:
                        try:
                            data[i].append(pd.to_datetime(
                                db_sorted.iloc[j, i]).timestamp())
                        except:
                            break
                        
                    else:
                        try:
                            data[i].append(float(db_sorted.iloc[j, i]))
                        except:
                            break
                        
    
            for k in range(len(data)-1):
                
                plt.figure(k+1)
                plt.plot(Time, data[k+1], label="diameter = "+str(d)+" m")
                plt.title("Parabolic dish antenna")
                plt.xlabel("Time (s)")
                plt.ylabel(col_names[k+1])         
                plt.legend()
                plt.show()
                
        #%% Access duration
    
        elif access_type == "duration":

        
            antenna_type = "parabola"
            diameter = [0.5, 6]
            for d in diameter:
                
                name = "\\"+str(antenna_type)+str(d)
    
                # Traitement du fichier csv
                
                # Le délimiteur peut être , ou ; si le fichier csv a transité 
                # sur Teams (changer si KeyError: "...")
                # db est un DataFrame (sorte de tableau)
                db = pd.read_csv(path+access_type+name+".csv", delimiter=",")
                duration = np.zeros(len(db))
                minutes = np.zeros(len(db))
                index = np.arange(0, len(db))
                for i in range(0, len(db)):
                    duration[i] = db.iloc[i, 3]
                    minutes[i] = db.iloc[i, 3]/60
                    
                a = 0
                for i in duration:
                    a += i
                avg = a/(len(duration)*60) # moyenne de revisite sur la 
                # période donnée
                print(minsec(avg))
                
            fig1 = plt.figure()
            plt.plot(index, minutes, marker = "o")
            plt.minorticks_on()    
            plt.grid(True, which="major", color="k", linestyle="-")
            plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
            plt.title("Access duration")
            plt.xlabel("Number of accesses")
            plt.ylabel("Duration (min)")
