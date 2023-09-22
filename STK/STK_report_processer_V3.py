# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:47:44 2023

@author: DECLINE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

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

N = 1 # Nombre de constellations (entre 1 et 2)

#%%
#E: orbit : List of Strings : Type of Orbit (RCO or SSO)
#   inc : List of Integers : Inclination of the orbits
#   alt : List of Integers : Altitude of the orbits
#   res : List of Integers : Worst resolution off-nadir
#   Nplan : List of Integers : Number of plan per constellation
#   Nsat : List of Integers : Number of satellites per plan
#   add : List of Strings : Additional argument


def nom(orbit, inc, alt, res, Nplan, Nsat, add):
    
    if len(orbit)==1:
        
        if add[0] == None:
            name = "\\"+orbit[0]+"_"+str(Nsat[0])+"x"+str(Nplan[0])+"_"+str(inc[0])+"_"+str(alt[0])+"_"+str(res[0])
        else:
            name = "\\"+orbit[0]+"_"+str(Nsat[0])+"x"+str(Nplan[0])+"_"+str(inc[0])+"_"+str(alt[0])+"_"+str(res[0])+"_"+add[0]
  
    return name, inc, alt, res


def param(N):
    if N==1:
        
        orbit = []
        Nsat = np.zeros((N,1))
        Nplan = np.zeros((N,1))
        inc = np.zeros((N,1))
        alt = np.zeros((N,1))
        res = np.zeros((N,1))
        add = np.zeros((N,1))
        
        for i in range(N):
            
            orbit.append("RCO")
            Nsat[i] = 2
            Nplan[i] = 4
            inc[i] = 50
            alt[i] = 260
            res[i] = 1.6
            add[i] = None
            
        name = nom(orbit, inc, alt, res, Nplan, Nsat, add)
    
    elif N==2:
        
        orbit = np.zeros((N,1))
        Nsat = np.zeros((N,1))
        Nplan = np.zeros((N,1))
        inc = np.zeros((N,1))
        alt = np.zeros((N,1))
        res = np.zeros((N,1))
        add = np.zeros((N,1))
        
        orbit1 = "RCO"
        Nsat1 = 2
        Nplan1 = 4
        inc1 = 50
        alt1 = 260
        res1 = 1.6
        add1 = None
        
        orbit2 = "RCO"
        Nsat2 = 2
        Nplan2 = 4
        inc2 = 50
        alt2 = 260
        res2 = 1.6
        add2 = "Luhansk"
        
        r = [res1, res2]
        a = [alt1, alt2]
        p = [Nplan1, Nplan2]
        i = [inc1, inc2]
        d = [add1, add2]
        o = [orbit1, orbit2]
        s = [Nsat1, Nsat2]
        
        for j in range(N):
            
            orbit[j] = o[j]
            Nsat[j] = s[j]
            Nplan[j] = p[j]
            inc[j] = i[j]
            alt[j] = a[j]
            res[j] = r[j]
            add[j] = d[j]
            
        const1 = nom(orbit1, inc1, alt1, res1, Nplan1, Nsat1, add1)
        const2 = nom(orbit2, inc2, alt2, res2, Nplan2, Nsat2, add2)
        const = const1+const2
    
    return const, inc, alt, res


const, inc, alt, res = param(1)

#C:\Users\DECLINE\Desktop\logiciels\python\stk\conflict_rostov\FoM_points\resolution

def lecture():
    folder1 = "\\conflict_rostov"
    folder2 = "\\FoM_points"
    folder3 = "\\resolution"
    path = r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+folder2+folder3+nom(N)+".csv"
    try:
        db = pd.read_csv(path, delimiter=",")
    except:
        db = pd.read_csv(path, delimiter=";")
    return db, path
        
# # Type de cible considérée
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
    db, path = lecture()
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

    new_revisit_times = []
    minutes = []
    m = 0
    for i in revisit_times:
        m += i
        if i!=0:
            new_revisit_times.append(i) # Secondes
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
    fig1.savefig(path.replace(".csv",".png"), dpi=300, bbox_inches='tight')


    # La même chose en faisant varier la résolution.

    avg_list = []
    res_list = []
    lat_diff = []
    
    # Résolution au nadir (compose le nom de fichiers existants)
    res = [1.0, 1.2, 1.4, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0] 
    
    for r in res:
        
        nom(N)
        
        # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time 
        # (UTCG)" par exemple)
        db = lecture()
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
        
        new_revisit_times = []
        minutes = []
        m = 0
        for i in revisit_times:
            m += i
            if i!=0:
                new_revisit_times.append(i)
                minutes.append(i/60)
        avg = m/(len(revisit_times)*60) # moyenne de revisite sur la période 
        # donnée
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
    plt.title("Revisit time, i = "+str(inc)+"°, h = "+str(alt)+"km")
    plt.xlabel("Ground resolution at the cone\'s limit")
    plt.ylabel("Revisit time (min)")
    
    
# #%% Ici on s'intéresse aux rapports "Value By Grid Point", càd en tout point 
# # (lat, long)

# elif folder2=="\\FoM_points": # Loi des RCO
    
#     N = sat1*plan1+sat2*plan2
#     # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time (UTCG)")
#     db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
#                      folder2+folder3+name1+name2+".csv",skiprows=25+N,sep=",")
#     #db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
#                      #folder2+name+".csv",delimiter=";")

#     #db_sorted = db.sort_values(by = ("Latitude (deg)"))

#     revisit_times = np.zeros(len(db))
#     lat = []
#     long = []
#     for i in range(0, len(db)):
#         try:
#             if db.iloc[i, 2]<20000:
#                 revisit_times[i] = db.iloc[i, 2]
#                 lat.append(db.iloc[i, 0])
#                 long.append(db.iloc[i, 1])
            
#         except:
#             break
        
#     new_revisit_times = []
#     minutes = []

#     n = 0
#     for m in revisit_times:
#         n += m
#         if m!=0:
#             new_revisit_times.append(m)
#             minutes.append(m/60)
                        
#     avg = n/(len(new_revisit_times)*60) # moyenne de revisite sur la période 
#     # donnée
#     #print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")
    
#     maxi=new_revisit_times[0]
#     indice_max=0
#     mini=new_revisit_times[0]
#     indice_min=0
#     for i in range(len(new_revisit_times)):
#         if new_revisit_times[i]>=maxi:
#             maxi=new_revisit_times[i]
#             indice_max=i
#         if new_revisit_times[i]<=mini:
#             mini=new_revisit_times[i]
#             indice_min=i
    
#     mymodel = np.poly1d(np.polyfit(lat, minutes, 5))
#     myline = np.linspace(lat[0], lat[-1], 100)
#     print(r2_score(minutes, mymodel(lat)))
    
    
#     # Affiche la revisite en fonction de la latitude, avec une interpolation.
    
#     fig1 = plt.figure()
#     #plt.plot(myline, mymodel(myline))
#     plt.scatter(lat, minutes, s=10)  
#     #plt.text(12, 60, mymodel)
#     #plt.text(12, 55, '{:.5f}'.format(r2_score(minutes, mymodel(lat))))
#     plt.minorticks_on()    
#     plt.grid(True, which="major", color="k", linestyle="-")
#     plt.grid(True, which="minor", color="grey", linestyle="-", 
#              alpha=0.2)
#     #plt.title("Revisit time, 1 week, avg = "+str(int(avg))+" min "+str(
#     #    round(60*(avg-int(avg)), 0))+" s\n"+str(mymodel)+", R = "+str(
#     #        "{:.5f}".format(r2_score(minutes, mymodel(lat)))))
#     plt.title("Revisit time, 1 week, avg = "+str(int(avg))+" min "+str(
#         round(60*(avg-int(avg)), 0))+" s")
#     plt.xlabel("Latitude (deg)")
#     plt.ylabel("Revisit time (min)")
#     fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
#                  folder2+folder3+name1+name2+".png", dpi=300, pad_inches=0)
   
    
#     # Affiche la zone cible et les latitudes remarquables.
    
#     fig2 = plt.figure()
#     plt.title("Map, avg = "+str(int(avg))+" min "+str(
#         round(60*(avg-int(avg)), 0))+" s")
    
#     plt.minorticks_on()   
#     plt.scatter(long, lat, s=30)
    
#     # Affiche les villes
#     plt.scatter(Donetsk[0], Donetsk[1], c='k', s=100)
#     plt.scatter(Kherson[0], Kherson[1], c='k', s=100)
#     plt.scatter(Luhansk[0], Luhansk[1], c='k', s=100)
#     plt.scatter(Zaporizhzhia[0], Zaporizhzhia[1], c = 'k', s = 100)
#     plt.scatter(Sevastopol[0], Sevastopol[1], c = 'k', s = 100)
    
#     # Affiche les latitudes de l'inclinaison orbitale, de la pire et de la 
#     # meilleure revisite.
#     plt.axhline(y=50, c='k', label='inclination')
#     plt.axhline(y=lat[indice_max], c='r', label='maximum')
#     plt.axhline(y=lat[indice_min], c='g', label='minimum')
    
#     plt.grid(True, which="major", color="k", linestyle="-")
#     plt.grid(True, which="minor", color="grey", linestyle="-",
#              alpha = 0.2)
#     plt.xlabel("Longitude (deg)")
#     plt.ylabel("Latitude (deg)")
#     plt.legend()
#     fig2.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
#                  folder2+"\map"+name1+name2+"_map.png", dpi=300,
#                  pad_inches=0)
    
  
#     # Règle des RCO
    
#     # Plot la différence entre la latitude de revisite minimale et
#     # l'inclinaison orbitale
    
    
#     # La "convergence" a lieu car la partie la moins revisitée de la cible,
#     # relativement à toutes les autres parties de la cible, change brusqement :
#     # on passe du point le plus éloigné de l'inclinaison orbitale, à angle 
#     # faible, donc le plus méridional, au point le plus septentrional. La
#     # convergence semble logarithmique : on converge à 1.75 m pour 500 km, 
#     # 3.5 m pour 300 km, et à 5 m pour 260 km. Que se passe-t-il à 100 km 
#     # d'altitude ? Etant donné que l'angle du cône est limité à 180°, 
#     # peut-être qu'à une latitude donnée, il n'y a plus convergence du tout 
#     # (trop bas pour que l'agrandissement du cône ne permette plus d'observer 
#     # la point le plus méridional plus souvent que le plus spetentrional.
#     # Trouver la formule générale de la règle des RCO.
#     # La "bosse" observée sur lat=f(res) pour 500 km est intrigante. Pourquoi ?
#     # Question : Y a-t-il une inversion de la tendance quand on s'approche
#     # d'une résolution de 0 m ? Et pourquoi ? Faire 3.5, 5.0, 10, 0.5, 0.1, 
#     # pour alt = 100, 180, 260, 300, 500 et 800.
#     # Sauvegarder les profils rev=f(lat).
    
#     alt = [100, 180, 260, 300, 500]
#     deg = 6
#     N = len(alt)
#     M = np.zeros((N, deg+1))
#     #alt = [100]
#     # Résolution au nadir (compose le nom de fichiers existants)
#     #res = [0.85, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
#     res = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0]
#     color = ['b', 'r', 'g', 'k', 'orange'] # Une couleur par altitude
#     fig3 = plt.figure()
#     c = -1
#     for a in alt:
#         c+=1
#         res_list = []
#         lat_diff_min = []
#         lat_diff_max = []
        
#         for r in res:
            
#             res_list.append(r)
            
#             name1 = orbit1+"_"+str(sat1)+"x"+str(plan1)+"_"+inc1+"_"+str(a)+"_"+str(r)
#             print(name1)
#             N = sat1*plan1
#             # Le délimiteur peut être , ou ; (changer si KeyError)
#             db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
#                              folder1+folder2+folder3+name1+name2+".csv", 
#                              skiprows=25+N, delimiter=",") # 25 correspond au
#             # format du rapport STK
            
#             #db_sorted = db.sort_values(by = ("Latitude (deg)"))
    
            
#             revisit_times = np.zeros(len(db))
#             lat = np.zeros(len(db))
#             long = np.zeros(len(db))
#             for i in range(0, len(db)):
#                 try:
#                     revisit_times[i] = db.iloc[i, 2]
#                     lat[i] = db.iloc[i, 0]
#                     long[i] = db.iloc[i, 1]
#                 except:
#                     break
                
#             new_revisit_times = []
#             minutes = []
    
#             n = 0
#             for m in revisit_times:
#                 n += m
#                 if m!=0:
#                     new_revisit_times.append(m)
#                     minutes.append(m/60)
                                
#             avg = n/(len(new_revisit_times)*60) # moyenne de revisite sur la 
#             # période donnée
#             #print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")
    
#             maxi = new_revisit_times[0]
#             indice_max = 0
#             mini = new_revisit_times[0]
#             indice_min = 0
#             for i in range(len(new_revisit_times)):
#                 if new_revisit_times[i]>=maxi:
#                     maxi = new_revisit_times[i]
#                     indice_max = i
#                 if new_revisit_times[i]<=mini:
#                     mini = new_revisit_times[i]
#                     indice_min = i
                    
#             lat_diff_min.append(abs(int(inc1)-lat[indice_min]))
#             lat_diff_max.append(abs(int(inc1)-lat[indice_max]))
#             print(inc1)
#             print(lat[indice_max])
#             print(abs(int(inc1)-lat[indice_max]))
            
            
#             mymodel = np.poly1d(np.polyfit(res_list, lat_diff_min, deg))
#             myline = np.linspace(res_list[0], res_list[-1], 100)
#             for m in range(len(mymodel)+1):

#                 print(mymodel[m], "cc2 =", c, ", m =", m)
#                 M[c][m]=mymodel[m]
#                 print("r2",r2_score(lat_diff_min, mymodel(res_list)))
#             plt.plot(myline, mymodel(myline), linestyle=':')
            
#         # Changer le nom des fichiers cible (la liste res) et l'altitude    
        
#         plt.plot(res_list, lat_diff_min, marker="o", 
#                  label="Inc - best at "+str(a)+"km", c=color[c])
#         plt.plot(res_list, lat_diff_max, marker="o", 
#                  label="Inc - worst at "+str(a)+"km", c=color[c], 
#                  linestyle=':')
#         plt.title("Difference in latitude at "+str(inc1)+"°")
#         plt.xlabel("Resolution")
#         plt.ylabel("Latitude (deg)")
#         plt.xlim(0)
#     plt.legend()
#     plt.minorticks_on()
#     plt.grid(True, which="major", color="k", linestyle="-")
#     plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
#     fig3.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"
#                  +folder1+folder2+"\loi\\"+str(inc1)+"_loi.png", 
#                  dpi=300, pad_inches=0)

        

# #%% Ici on s'intéresse aux reports "Stats By Region"

# elif folder2=="\\region":
    
#     res = [2.0, 3.0, 4.0]
#     res_list = []
    
#     for r in res:
        
#         res_list.append(r)
#         name1 = orbit1+"_"+str(sat1)+"x"+str(plan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(r)
#         # Traitement du fichier csv
#         N = sat1*plan1
#         # Le délimiteur peut être , ou ; si le fichier csv a transité sur Teams
#         # (changer si KeyError: "Start Time (UTCG)")
#         # db est un DataFrame (sorte de tableau)
#         db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
#                          folder1+folder2+folder3+name1+".csv", skiprows=24+N, 
#                          delimiter=",")

#         db_sorted = db.sort_values(by=("Region Name"))
#         # Les temps de revisite seront stockés dans cette liste
#         revisit_times = np.zeros(len(db_sorted))
#         cities = []
#         for i in range(0, len(db_sorted)):
#             # db_sorted.iloc[i, 2] = valeur du ième élément de la 2e colonne
#             # du tableau
#             revisit_times[i] = db_sorted.iloc[i, 4]
#             cities.append(db_sorted.iloc[i, 0])
            
#         lat = []
#         long = []
#         for i in targets:
#             lat.append(i[1])
#             long.append(i[0])
#         db_sorted.insert(0, "lat", lat)
#         db_sorted.insert(1, "long", long)
        
#         #
#         minutes = []
#         m = 0
#         for i in revisit_times:
#             m+=i
#             minutes.append(round(i/60,1))
#         avg = m/(len(revisit_times)*60)
        
#         fig1 = plt.figure()
#         plt.minorticks_on()
#         plt.title("Revisit time, avg = "+str(int(avg))+" min "+str(round(
#             60*(avg-int(avg)), 0))+" s")
#         plt.xlabel("Longitude (deg)")
#         plt.ylabel("Latitude (deg)")
        
#         for i in range(len(db)):
              
#             plt.grid(True, which="major", color="k", linestyle="-")
#             plt.grid(True, which="minor", color="grey", linestyle="-",
#                      alpha=0.2)
#             plt.scatter(db_sorted.iloc[i, 1], db_sorted.iloc[i, 0], s = 50, 
#                         label = str(cities[i]).replace("_city","")+", "+str(
#                             minutes[i])+" min")
#             plt.legend()
#         fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
#                      folder2+folder3+name+".png", dpi=300,
#                      bbox_inches='tight')

# #%% Bases au sol

# elif folder2 == "\\access_ground":
    
#     #%% Link budget
    
#     antenna_type = "dish"
#     diameter = [0.5, 3, 6]
    
#     for d in diameter:
        
#         name = "\\"+str(antenna_type)+"_"+str(d)
        
#         if folder3 == "\\link":
                
#             col_names = ["Time (UTCG)", "EIRP (dBW)", "Rcvd. Frequency (GHz)",
#                          "Rcvd. Iso. Power (dBW)", "Flux Density (dBW/m^2)", 
#                          "g/T (dB/K)", "C/No (dB*Hz)", "Bandwidth (kHz)", 
#                          "C/N (dB)", "Eb/No (dB)", "Bit Error Rate"]
            
#             # Traitement du fichier csv
            
#             # Le délimiteur peut être , ou ; si le fichier csv a transité sur 
#             # Teams (changer si KeyError: "Start Time (UTCG)")
#             # db est un DataFrame (sorte de tableau)
#             db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
#                              folder1+folder2+folder3+name+".csv", 
#                              delimiter=",", names=col_names)
#             db_sorted = db.sort_values(by=("Time (UTCG)"))
            
#             Time = []
#             EIRP = []
#             RF = []
#             RIP = []
#             FD = []
#             g_T = []
#             C_No = []
#             BW = []
#             C_N = []
#             Eb_No = []
#             BER = [] # Bit error rate
#             data = [Time, EIRP, RF, RIP, FD, g_T, C_No, BW, C_N, Eb_No, BER]
            
#             for i in range(len(data)):
#                 for j in range(len(db_sorted)-1):
#                     if i==0:
#                         try:
#                             data[i].append(pd.to_datetime(
#                                 db_sorted.iloc[j, i]).timestamp())
#                         except:
#                             break
                        
#                     else:
#                         try:
#                             data[i].append(float(db_sorted.iloc[j, i]))
#                         except:
#                             break
                        
    
#             for k in range(len(data)-1):
                
#                 plt.figure(k+1)
#                 plt.plot(Time, data[k+1], label="diameter = "+str(d)+" m")
#                 plt.title("Parabolic dish antenna")
#                 plt.xlabel("Time (s)")
#                 plt.ylabel(col_names[k+1])         
#                 plt.legend()
#                 plt.show()
                
#     #%% Access duration
    
#         elif folder3 == "\\duration":
        
#             antenna_type = "parabola"
#             diameter = [0.5, 6]
#             for d in diameter:
                
#                 name = "\\"+str(antenna_type)+str(d)
    
#                 # Traitement du fichier csv
                
#                 # Le délimiteur peut être , ou ; si le fichier csv a transité sur
#                 # Teams (changer si KeyError: "Start Time (UTCG)")
#                 # db est un DataFrame (sorte de tableau)
#                 db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
#                                  folder1+folder2+folder3+name+".csv", 
#                                  delimiter=",")
#                 duration = np.zeros(len(db))
#                 minutes = np.zeros(len(db))
#                 index = np.arange(0, len(db))
#                 for i in range(0, len(db)):
#                     duration[i] = db.iloc[i, 3]
#                     minutes[i] = db.iloc[i, 3]/60
                    
#                 a = 0
#                 for i in duration:
#                     a += i
#                 avg = a/(len(duration)*60) # moyenne de revisite sur la 
#                 # période donnée
#                 print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")
    
#             fig1 = plt.figure()
#             plt.plot(index, minutes, marker = "o")
#             plt.minorticks_on()    
#             plt.grid(True, which="major", color="k", linestyle="-")
#             plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
#             plt.title("Access duration")
#             plt.xlabel("Number of accesses")
#             plt.ylabel("Duration (min)")