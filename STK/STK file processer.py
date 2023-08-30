# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:47:44 2023

@author: DECLINE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Ce programme traite différents types de rapports STK. Ceux-ci doivent être au
# préalable stockés dans des dossiers portant un nom bien défini décrivant
# les paramètres de la simulation.

# Ferme toutes les fenêtres
plt.close('all')

# Cibles ponctuelles (lon, lat) en décimales
Donetsk = [37.805, 48.00277]
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


def indice_max(liste):
    maxi = liste[0]
    for i in range(len(liste)):
        if liste[i]>=maxi:
            maxi=liste[i]
            ind_max=i
    return ind_max

def indice_min(liste):
    mini = liste[0]
    for i in range(len(liste)):
        if liste[i]<=mini:
            mini=liste[i]
            ind_min=i
    return ind_min

# Calcule la moyenne des éléments non nuls d'une liste
def moy_non_null(liste):
    new_revisit_times = []
    minutes = []
    n = 0
    for m in liste:
        n += m
        if m!=0: # Si un temps de revisite est nul, cela veut dire que la zone
                 # sélectionnée est trop grande et donc que le satellite ne
                 # la couvre pas entièrement. Ces zones aveugles font baisser
                 # la moyenne de revisite sur la zone souhaitée.
            new_revisit_times.append(m)
            minutes.append(round(m/60,1))
            
    avg = n/(len(new_revisit_times)*60) # moyenne de revisite sur la 
                                        # période donnée
    
    return avg, minutes, new_revisit_times

# Paramètres de la constellation 1

orbit1 = "\RCO" # Type d'orbite (RCO, SSO)
#orbit = "\SSO"
sat1 = 2 # Nombre de satellites par plan (~2)
plan1 = 4 # Nombre de plans (~4 - ~12)
inc1 = "50" # Inclinaison des orbites (47 - 51, couplées 48_50, 47_49_50, ou
               # 90 si SSO)
alt1 = 260 # Altitude (150 - 500 km)
res1 = 3.0 # Résolution au nadir (1 - ~5 m) (1.0 et non 1 pour que les 
             # fichiers apparaissent dans l'ordre alphabétique (ex : 
             # RCO_2x4_50_260_1.5, RCO_2x4_50_260_1, RCO_2x4_50_260_2.5)). Il 
             # faut donc écrire 1.0, 2.0 ou 3.0 au lieu de 1, 2 et 3.

add = "_Luhansk" # Informations supplémentaires (cibles ponctuelles notamment)
add = ""

# Paramètres de la constellation 2

orbit2 = "+SSO" # SSO toujours en deuxième position
orbit2 = "\\SSO" # Si SSO est seule
sat2 = 2 # Nombre de satellites par plan
plan2 = 15 # Nombre de plans
inc2 = "50" # Inclinaison des orbites
inc2 = "90"
alt2 = 300 # Altitude (150 - 500 km)
res2 = 1.6

# Nom du fichier csv enregistré depuis STK
# Privilégier le format orbite_satxplan_inclinaison_altitude_resolution pour 
# sauvegarder les fichiers -> RCO_2x4_50_260_1.4

name1 = orbit1+"_"+str(sat1)+"x"+str(plan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(res1)+add
name2 = orbit2+"_"+str(sat2)+"x"+str(plan2)+"_"+str(inc2)+"_"+str(alt2)+"_"+str(res2)
name2 = ""
name = name1 + name2

# Chemin d'accès au fichier
# Ajuster le nombre de \ (\\ -> \) peut se révéler nécessaire si le fichier 
# csv a transité sur Teams

# Type de cible considérée
folder1 = "\\conflict_rostov"
#folder1 = "\\hemisphere"
#folder1 = "\\points"
#folder1 = "\\secondary"
#folder1 = "\\shapes"

# Type de rapport à importer
folder2 = "\\FoM_points"
#folder2 = "\\region"
#folder2 = "\\access_sensors"
#folder2 = "\\access_ground"

# Paramètre à faire varier
folder3 = "\\plan"
folder3 = "\\resolution"
#folder3 = "\\inclination"
#folder3 = "\\link"
#folder3 = "\\duration"
#folder3 = ""

#%% Type de rapport : Access AreaTarget to Satellite-Sensor

if folder2=="\\access_sensors":
    
    # Traitement du fichier csv
    
    # Le délimiteur peut être , ou ; si le fichier csv a transité sur Teams 
    # (changer si KeyError: "Start Time (UTCG)")
    # db est un DataFrame (sorte de tableau)
    db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1
                     +folder2+folder3+name+".csv",delimiter=",")
    #db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1
    #                 +folder2+folder3+name+".csv",delimiter=";")
    
    # Les accès sont donnés pour chaque satellite, il faut donc les classer 
    # de façon chronologique indépendamment du satellite
    # Le fichier est trié selon la colonne Start Time
    db_sorted = db.sort_values(by = ("Start Time (UTCG)"))
    
    # Création d'une nouvelle colonne permettant d'indexer correctement les
    # nouvelles lignes classées (les anciens indices sont dans le désordre)
    index = np.arange(0, len(db_sorted))
    db_sorted.insert(0, "index", index)
    
    # Les temps de revisite seront stockés dans cette liste
    revisit_times = np.zeros(len(db_sorted))

    for i in range(0, len(db_sorted)-1):
        try:
            
            # Le temps de revisite correspond à la période entre la sortie de 
            # la zone et l'entrée suivante. On soustrait donc les dates 
            # d'entrée aux dates de sorties.
            # La première valeur de Start et la dernière de Stop sont 
            # inutilisables, d'où len(db_sorted)-1
            # db_sorted.iloc[i+1, 2] = valeur du (i+1)ème élément de la 2e 
            # colonne du tableau
            revisit_times[i] = pd.to_datetime(
                db_sorted.iloc[i+1, 2]).timestamp()-pd.to_datetime(
                    db_sorted.iloc[i, 3]).timestamp()
            
        except:
            
            # Le break est essentiel car à la fin du tableau, la fonction 
            # to_datetime n'a plus de sens
            break

    # Moyenne
    new_revisit_times = []
    minutes = []
    m = 0
    for i in revisit_times:
        m += i
        if i!=0: # Si un temps de revisite est nul, cela veut dire que la zone
                 # sélectionnée est trop grande et donc que le satellite ne
                 # la couvre pas entièrement. Ces zones aveugles font baisser
                 # la moyenne de revisite sur la zone souhaitée.
            new_revisit_times.append(i)
            minutes.append(i/60) # Minutes sont plus lisibles que les secondes
    avg = m/(len(revisit_times)*60) # Moyenne de revisite sur la période donnée
    #print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")

    # Durée de chaque revisite et moyenne
    fig1 = plt.figure()
    plt.minorticks_on()    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    plt.title("Revisit time, 1 week, avg = "+str(int(avg))+" min "+str(
        round(60*(avg-int(avg)), 0))+" s")
    plt.xlabel("Number of revisits")
    plt.ylabel("Revisit time (min)")
    plt.scatter(np.linspace(0, len(new_revisit_times), len(new_revisit_times)),
                minutes, s=10)
    fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                 folder2+folder3+name+".png", dpi=300, bbox_inches='tight')

    # La même chose en faisant varier la résolution.
    
    avg_list = []
    res_list = []
    lat_diff = []
    
    # Résolution au nadir (compose le nom de fichiers existants)
    res = [1.0, 1.2, 1.4, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0] 
    
    for r in res:
        
        name1 = orbit1+"_"+str(sat1)+"x"+str(plan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(r)+add
        
        print(name1)
        
        # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time 
        # (UTCG)" par exemple)
        db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
                         folder1+folder2+folder3+name1+".csv", delimiter = ",")
        #db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
                         #folder1+folder2+name+".csv", delimiter=";")
        
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
        avg, minutes, new_revisit_times = moy_non_null(revisit_times)
       
        print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")
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
    
    
#%% Ici on s'intéresse aux rapports "Value By Grid Point", càd en tout point 
# (lat, long)

elif folder2=="\\FoM_points": # Loi des RCO
    
    N = sat1*plan1+sat2*plan2
    # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time (UTCG)")
    db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                     folder2+folder3+name1+name2+".csv",skiprows=25+N,sep=",")
    #db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                     #folder2+name+".csv",delimiter=";")

    #db_sorted = db.sort_values(by = ("Latitude (deg)"))

    
    revisit_times = np.zeros(len(db))
    lat = []
    long = []
    for i in range(0, len(db)):
        try:
            if db.iloc[i, 2]<20000: # Les très grandes valeurs correspondent
                                    # à une revisite inexistante (typiquement
                                    # au niveau du pôle Nord).
                
                lat.append(db.iloc[i, 0])        # 1e colonne : latitude
                long.append(db.iloc[i, 1])       # 2e colonne : longitude
                revisit_times[i] = db.iloc[i, 2] # 3e colonne : revisite
                
        except:
            break
        
    # Moyenne

    avg, minutes, new_revisit_times = moy_non_null(revisit_times)
    ind_max = indice_max(new_revisit_times)
    ind_min = indice_min(new_revisit_times)

    mymodel = np.poly1d(np.polyfit(lat, minutes, 5))
    myline = np.linspace(lat[0], lat[-1], 100)
    print(r2_score(minutes, mymodel(lat)))
    ############################## travaux


    # Affiche la revisite en fonction de la latitude, avec une interpolation.
    
    fig1 = plt.figure()
    #plt.plot(myline, mymodel(myline))
    plt.scatter(lat, minutes, s=10)  
    #plt.text(12, 60, mymodel)
    #plt.text(12, 55, '{:.5f}'.format(r2_score(minutes, mymodel(lat))))
    plt.minorticks_on()
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", 
             alpha=0.2)
    #plt.title("Revisit time, 1 week, avg = "+str(int(avg))+" min "+str(
    #    round(60*(avg-int(avg)), 0))+" s\n"+str(mymodel)+", R = "+str(
    #        "{:.5f}".format(r2_score(minutes, mymodel(lat)))))
    plt.title("Revisit time, 1 week, avg = "+str(int(avg))+" min "+str(
        round(60*(avg-int(avg)), 0))+" s")
    plt.xlabel("Latitude (deg)")
    plt.ylabel("Revisit time (min)")
    fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                 folder2+folder3+name1+name2+".png", dpi=300, pad_inches=0)
   
    
    # Affiche la zone cible et les latitudes remarquables.
    
    fig2 = plt.figure()
    plt.title("Map, avg = "+str(int(avg))+" min "+str(
        round(60*(avg-int(avg)), 0))+" s")
    
    plt.minorticks_on()   
    plt.scatter(long, lat, s=30)
    
    # Affiche les villes
    plt.scatter(Donetsk[0], Donetsk[1], c='k', s=100)
    plt.scatter(Kherson[0], Kherson[1], c='k', s=100)
    plt.scatter(Luhansk[0], Luhansk[1], c='k', s=100)
    plt.scatter(Zaporizhzhia[0], Zaporizhzhia[1], c = 'k', s = 100)
    plt.scatter(Sevastopol[0], Sevastopol[1], c = 'k', s = 100)
    
    # Affiche les latitudes de l'inclinaison orbitale, de la pire et de la 
    # meilleure revisite.
    plt.axhline(y=50, c='k', label='inclination')
    plt.axhline(y=lat[ind_max], c='r', label='maximum')
    plt.axhline(y=lat[ind_min], c='g', label='minimum')
    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-",
             alpha = 0.2)
    plt.xlabel("Longitude (deg)")
    plt.ylabel("Latitude (deg)")
    plt.legend()
    fig2.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                 folder2+"\map"+name1+name2+"_map.png", dpi=300,
                 pad_inches=0)
    
  

    # Règle des RCO
    
    # Plot la différence entre la latitude de revisite minimale et
    # l'inclinaison orbitale
    
    
    # La "convergence" a lieu car la partie la moins revisitée de la cible,
    # relativement à toutes les autres parties de la cible, change brusqement :
    # on passe du point le plus éloigné de l'inclinaison orbitale, à angle 
    # faible, donc le plus méridional, au point le plus septentrional. La
    # convergence semble logarithmique : on converge à 1.75 m pour 500 km, 
    # 3.5 m pour 300 km, et à 5 m pour 260 km. Que se passe-t-il à 100 km 
    # d'altitude ? Etant donné que l'angle du cône est limité à 180°, 
    # peut-être qu'à une latitude donnée, il n'y a plus convergence du tout 
    # (trop bas pour que l'agrandissement du cône ne permette plus d'observer 
    # la point le plus méridional plus souvent que le plus spetentrional.
    # Trouver la formule générale de la règle des RCO.
    # La "bosse" observée sur lat=f(res) pour 500 km est intrigante. Pourquoi ?
    # Question : Y a-t-il une inversion de la tendance quand on s'approche
    # d'une résolution de 0 m ? Et pourquoi ? Faire 3.5, 5.0, 10, 0.5, 0.1, 
    # pour alt = 100, 180, 260, 300, 500 et 800.
    # Sauvegarder les profils rev=f(lat).
    
    alt = [100, 180, 260, 300,400,  500]
    deg = 4
    N = len(alt)
    M = np.zeros((N, deg+1))
    #alt = [100]
    # Résolution au nadir (compose le nom de fichiers existants)
    #res = [0.85, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     
    # La liste de toutes les résolutions est scindée pour que numpy puisse
    # correctement interpoler chaque morceau de la courbe totale.
    
    res1 = [0.85, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    res2 = [5.0, 6.0, 8.0, 10.0]
    res = [res1, res2]
    #res = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0]
    color = ['b', 'r', 'g', 'k', 'orange', 'm'] # Une couleur par altitude
    fig3 = plt.figure()
    c = -1
    for a in alt: # Pour chaque altitude
        c+=1
        
        for r1 in res: # Pour chaque segment de la liste des résolutions
            res_list = []
            diff_lat_min = []
            diff_lat_max = []
            for r2 in r1: # Pour chaque résolution dans le segment
                
                res_list.append(r2)
                
                name1 = orbit1+"_"+str(sat1)+"x"+str(plan1)+"_"+inc1+"_"+str(a)+"_"+str(r2)
                print(name1)
                N = sat1*plan1
                # Le délimiteur peut être , ou ; (changer si KeyError)
                db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
                                 folder1+folder2+folder3+name1+name2+".csv", 
                                 skiprows=25+N, delimiter=",") # 25 correspond au
                # format du rapport STK
                
                #db_sorted = db.sort_values(by = ("Latitude (deg)"))
        
                
                revisit_times = np.zeros(len(db))
                lat = np.zeros(len(db))
                long = np.zeros(len(db))
                for i in range(0, len(db)):
                    try:
                        revisit_times[i] = db.iloc[i, 2]
                        lat[i] = db.iloc[i, 0]
                        long[i] = db.iloc[i, 1]
                    except:
                        break
                    
                avg, minutes, new_revisit_times = moy_non_null(revisit_times)
                
                #print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")
                
                # On trouve les indices du max et du min
                ind_max = indice_max(new_revisit_times)
                ind_min = indice_min(new_revisit_times)
                        
                # Position du maximum et du minimum de revisite
                # Ces latitudes - l'inclinaison donne une différence en degrés
                # Cette différence doit être connue avec précision afin de lancer
                # une constellation sur une cible avec le plus de précision.
                
                diff_lat_min.append(abs(int(inc1)-lat[ind_min]))
                diff_lat_max.append(abs(int(inc1)-lat[ind_max]))
                print(inc1)
                print(lat[ind_max])
                print(abs(int(inc1)-lat[ind_max]))
                
                # Interpolation des courbes lat vs res
                mymodel = np.poly1d(np.polyfit(res_list, diff_lat_min, deg))
                myline = np.linspace(res_list[0], res_list[-1], 100)
                for m in range(deg+1): # 4 degrés plus la constante
    
                    print(mymodel[m], "cc2 =", c, ", m =", m)
                    M[c][m]=mymodel[m]
                    print("r2",r2_score(diff_lat_min, mymodel(res_list)))
                plt.plot(myline, mymodel(myline), linestyle=':')
                
            # Changer le nom des fichiers cible (la liste res) et l'altitude    
            # De plus, il faut que len(color) = len(altitudes)
            
            if r1==res[0]:
                
                plt.plot(res_list, diff_lat_min, marker="o", 
                         label="Inc - best at "+str(a)+"km", c=color[c]) 
            else:
                plt.plot(res_list, diff_lat_min, marker="o", c=color[c]) 
            
            
            # plt.plot(res_list, diff_lat_max, marker="o", 
            #           label="Inc - worst at "+str(a)+"km", c=color[c], 
            #           linestyle=':')
            plt.title("Difference in latitude at "+str(inc1)+"°")
    plt.xlabel("Resolution")
    plt.ylabel("Latitude (deg)")
    plt.xlim(0)
    plt.legend()
    plt.minorticks_on()
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    fig3.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"
                 +folder1+folder2+"\loi\\"+str(inc1)+"_loi.png", 
                 dpi=300, pad_inches=0)
    
    fig4=plt.figure()
    # Coefficient des polynômes pour chaque degré en fonction de l'altitude
    plt.plot(M, alt) 
    
#%% Ici on s'intéresse aux reports "Stats By Region"

elif folder2=="\\region":
    
    res = [2.0, 3.0, 4.0]
    res_list = []
    
    for r in res:
        
        res_list.append(r)
        name1 = orbit1+"_"+str(sat1)+"x"+str(plan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(r)
        # Traitement du fichier csv
        N = sat1*plan1
        # Le délimiteur peut être , ou ; si le fichier csv a transité sur Teams
        # (changer si KeyError: "Start Time (UTCG)")
        # db est un DataFrame (sorte de tableau)
        db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
                         folder1+folder2+folder3+name1+".csv", skiprows=24+N, 
                         delimiter=",")

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
        

        avg, minutes, new_revisit_times = moy_non_null(revisit_times)
        fig1 = plt.figure()
        plt.minorticks_on()
        plt.title("Revisit time, avg = "+str(int(avg))+" min "+str(round(
            60*(avg-int(avg)), 0))+" s")
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
        fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                     folder2+folder3+name+".png", dpi=300,
                     bbox_inches='tight')

#%% Bases au sol

elif folder2 == "\\access_ground":
    
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
            db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
                             folder1+folder2+folder3+name+".csv", 
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
            Eb_No = []
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
                db = pd.read_csv(
                    r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1
                    +folder2+folder3+name+".csv", delimiter=",")
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
                print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")
                
            fig1 = plt.figure()
            plt.plot(index, minutes, marker = "o")
            plt.minorticks_on()    
            plt.grid(True, which="major", color="k", linestyle="-")
            plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
            plt.title("Access duration")
            plt.xlabel("Number of accesses")
            plt.ylabel("Duration (min)")