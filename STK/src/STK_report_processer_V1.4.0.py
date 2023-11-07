# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 17:12:47 2023

@author: DECLINE
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from process.stk_utils import *
from process.stk_process_access_sensor import process_access_sensors
from process.stk_process_process_fom_point import process_fom_point

# Ce programme traite différents types de rapports STK. Ceux-ci doivent être au
# préalable stockés dans des dossiers portant un nom bien défini décrivant
# les paramètres de la simulation.


path_user = os.path.dirname(__file__)+'/../'
# Ferme toutes les fenêtres
plt.close('all')

#%% Variables et fonctions utiles

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

#%% Paramétrage

# Paramètres de la constellation 1

const1 = "\RCO" # Type d'orbite (RCO, SSO, CITROUILLE)
#const1 = "\CITROUILLE"
const1 = "\SSO"
Nsat1 = 2 # Nombre de satellites par plan
Nplan1 = 12 # Nombre de plans
inc1 = "0" # Inclinaison des orbites (0° par convention pour une SSO)
alt1 = 250 # Altitude (km)
res1 = 2.0   # Les fichiers apparaissent dans l'ordre alphabétique (ex : 
             # RCO_2x4_50_260_0_1.5, RCO_2x4_50_260_0_1, RCO_2x4_50_260_0_2.5)). Il 
             # faut donc écrire 1.0, 2.0 ou 3.0 au lieu de 1, 2 et 3 pour avoir
             # 1.0 avant 1.5
IPS1 = 0

# Informations supplémentaires (cibles ponctuelles ou origine
                 # des satellites notamment)
add1 = "_FromFrance"
add1 = ""

# Paramètres de la constellation 2

const2 = "+SSO" # SSO toujours en deuxième position
const2 = "\\SSO" # Si SSO est seule
Nsat2 = 2 # Nombre de satellites par plan
Nplan2 = 15 # Nombre de plans
inc2 = "50" # Inclinaison des orbites
inc2 = "90"
alt2 = 300 # Altitude (150 - 500 km)
res2 = 1.6
IPS2 = 0
add2 = ""
# Nom du fichier csv enregistré depuis STK
# Privilégier le format orbite_satxplan_inclinaison_altitude_resolution pour 
# sauvegarder les fichiers -> RCO_2x4_50_260_1.4

name1 = const1+"_"+str(Nsat1)+"x"+str(Nplan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(IPS1)+"_"+str(res1)+add1
name2 = const2+"_"+str(Nsat2)+"x"+str(Nplan2)+"_"+str(inc2)+"_"+str(alt2)+"_"+str(IPS2)+"_"+str(res2)+add2
name2 = ""
name = name1 + name2

# Chemin d'accès au fichier
# Ajuster le nombre de \ (\\ -> \) peut se révéler nécessaire si le fichier 
# csv a transité sur Teams

# Type de cible considérée
folder1 = "target_primary"
folder1 = "global"
# folder1 = "files_points"
# folder1 = "target_secondary"
# folder1 = "general_shapes"

# Type de rapport à importer
folder2 = "FoM_points"
# folder2 = "region"
# folder2 = "access_sensors"
# folder2 = "access_ground"

folder3 = ""

path = "/".join(path_user, folder1, folder2)


#%% Type de rapport : Access AreaTarget to Satellite-Sensor or Chain

if folder2=="access_sensors":
    process_access_sensors(path, name, Nsat1, Nplan1, inc1, alt1, IPS1, add1)
    
#%% Ici on s'intéresse aux rapports "Value By Grid Point", càd en tout point 
# de coordonnées (lat, long)

elif folder2=="FoM_points": # Loi des RCO
    process_fom_point()

#%% Ici on s'intéresse aux reports "Stats By Region"

elif folder2=="region":
    
    res = [2.0, 3.0, 4.0]
    res_list = []
    
    for r in res:
        
        res_list.append(r)
        name1 = const1+"_"+str(Nsat1)+"x"+str(Nplan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(IPS1)+"_"+str(r)+add1
        # Traitement du fichier csv
        N = Nsat1*Nplan1
        # Le délimiteur peut être , ou ; si le fichier csv a transité sur Teams
        # (changer si KeyError: "Start Time (UTCG)")
        # db est un DataFrame (sorte de tableau)
        db = pd.read_csv(path + "/" + name1 + ".csv", skiprows=24+N, delimiter=",")

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
        long = []
        for i in targets:
            lat.append(i[1])
            long.append(i[0])
        db_sorted.insert(0, "lat", lat)
        db_sorted.insert(1, "long", long)
        

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

#%% Bases au sol

elif folder2 == "access_ground":
    
    # Traitement du fichier csv

    avg, minutes, revisit_times_non_null = doing_thing(path, name, always_take = True)
    
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
        
        if folder3 == "\\link":
                
            col_names = ["Time (UTCG)", "EIRP (dBW)", "Rcvd. Frequency (GHz)",
                         "Rcvd. Iso. Power (dBW)", "Flux Density (dBW/m^2)", 
                         "g/T (dB/K)", "C/No (dB*Hz)", "Bandwidth (kHz)", 
                         "C/N (dB)", "Eb/No (dB)", "Bit Error Rate"]
            
            # Traitement du fichier csv
            
            # Le délimiteur peut être , ou ; si le fichier csv a transité sur 
            # Teams (changer si KeyError: "Start Time (UTCG)")
            # db est un DataFrame (sorte de tableau)
            db = pd.read_csv(path+folder3+name+".csv", 
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
    
        elif folder3 == "\\duration":
        
            antenna_type = "parabola"
            diameter = [0.5, 6]
            for d in diameter:
                
                name = "\\"+str(antenna_type)+str(d)
    
                # Traitement du fichier csv
                
                # Le délimiteur peut être , ou ; si le fichier csv a transité 
                # sur Teams (changer si KeyError: "...")
                # db est un DataFrame (sorte de tableau)
                db = pd.read_csv(path+folder3+name+".csv", delimiter=",")
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