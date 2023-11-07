# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.process.stk_utils import * 
from sklearn.metrics import r2_score


def process_fom_point(path, const1, const2):
    
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
    
    name = str(const1)
    if const2 :
        name = name + "_" + str(const2)
    
    N = const1.nb_sat()
    if const2 :
        N = N + const2.nb_sat()

    # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time (UTCG)")
    db = pd.read_csv(path + "/" + name +".csv",skiprows=25+N,sep=",")
    revisit_times = []
    lat = []
    lon = []
    for i in range(0, len(db)):
        try:
            if db.iloc[i, 2]<20000:
                revisit_times.append(db.iloc[i, 2]) # 3e colonne : revisite
                lat.append(db.iloc[i, 0])
                lon.append(db.iloc[i, 1])
            
        except:
            break
    
    avg, minutes, revisit_times_non_null = moy_non_null(revisit_times)
    lat_reduite, revisit_times_moy = doublons_moyenne(lat, revisit_times_non_null)
    # On trouve les indices du max et du min
    ind_max = indice_max(revisit_times_non_null)
    ind_min = indice_min(revisit_times_non_null)

    mymodel = np.poly1d(np.polyfit(lat, minutes, 5))
    myline = np.linspace(lat[0], lat[-1], 100)
    print(r2_score(minutes, mymodel(lat)))
    
    
    # Affiche la revisite en fonction de la latitude, avec une interpolation.
    revisit_times_moy_sec = []
    for i in revisit_times_moy:
        revisit_times_moy_sec.append(i/60)
    fig1 = plt.figure()
    # Affiche la corrélation et l'équation
    plt.scatter(lat_reduite, revisit_times_moy_sec, s=10)
    plt.minorticks_on()
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", 
              alpha=0.2)
    
    # Corrélation et équation polynomiale
    
    plt.title(name +", avg = "+minsec(avg))
    plt.xlabel("Latitude (deg)")
    plt.ylabel("Revisit time (min)")
    fig1.savefig("/".join((path, name)) + ".png", dpi=300, pad_inches=0)
    
    # Affiche la zone cible et les latitudes remarquables.
    
    fig2 = plt.figure()
    plt.title("Best = "+minsec(minutes[ind_min])+", worst = " 
              +minsec(minutes[ind_max])+", avg = "+ minsec(avg))
    plt.minorticks_on()   
    plt.scatter(lon, lat, s=10)
    
    # Affiche les villes
    for t in targets :
        plt.scatter(t[0], t[1], c='k', s=50)
    
    # Affiche les latitudes de l'inclinaison orbitale, de la pire et de la 
    # meilleure revisite.
    plt.axhline(y=int(const1.inc), c='k', label='inclination', linewidth=4, linestyle="--")
    plt.axhline(y=lat[ind_max], c='r', label='maximum', linewidth=4)
    plt.axhline(y=lat[ind_min], c='g', label='minimum', linewidth=4)
    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-",
              alpha = 0.2)
    plt.xlabel("Longitude (deg)")
    plt.ylabel("Latitude (deg)")
    plt.legend()
    fig2.savefig("/".join((path, "map", name + "_map.png")), dpi=300,
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
    
    
    
    ############################# Résolution #################################
    
    try:
        alt = [100, 180, 260, 300, 400, 500, 800]
        deg = 5
        M = np.zeros((len(alt), deg+1))
        #alt = [100]
        # Résolution au nadir (compose le nom de fichiers existants)
        #res = [0.85, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
        res1 = [0.85, 1.0, 1.5, 2.0]
        res2 = [2.5, 3.0, 3.5, 4.0, 5.0, 6.0]
        res3 = [6.0, 8.0, 10.0]
        res = [res1, res2, res3]
        colors = ['b', 'r', 'g', 'k', 'orange', 'm', 'pink'] # Une couleur par altitude
        fig3 = plt.figure(dpi=200)
        c = -1
        for a in alt:
            c+=1
            res_list = []
            lat_diff_min = []
            lat_diff_max = []  
            for r1 in res:
                for r2 in r1:
                    res_list.append(r2)
                    
                    name_res = const1.name_with_res(r2)

                    N = const1.nb_sat()
   
                    # Le délimiteur peut être , ou ; (changer si KeyError)
                    db = pd.read_csv(path + "/" + name_res + ".csv", 
                                      skiprows=25+N, delimiter=",") # 25 correspond au
                    # format du rapport STK
                    
                    revisit_times = np.zeros(len(db))
                    lat = np.zeros(len(db))
                    lon = np.zeros(len(db))
                    for i in range(0, len(db)):
                        try:
                            revisit_times[i] = db.iloc[i, 2]
                            lat[i] = db.iloc[i, 0]
                            lon[i] = db.iloc[i, 1]
                        except:
                            break
                        
                    revisit_times_non_null = []
                    minutes = []
            
                    n = 0
                    for m in revisit_times:
                        n += m
                        if m!=0:
                            revisit_times_non_null.append(m)
                            minutes.append(m/60)
                                        
                    avg = n/(len(revisit_times_non_null)*60) # moyenne de revisite sur la 
                    # période donnée
                    #print(str(int(avg))+" min "+str(round(60*(avg-int(avg)), 0))+" s")
            
                    id_max = indice_max(revisit_times_non_null)
                    id_min = indice_min(revisit_times_non_null)
                            
                    lat_diff_min.append(abs(float(const1.inc)-lat[id_min]))
                    lat_diff_max.append(abs(float(const1.inc)-lat[id_max]))
                    print(const1.inc)
                    print(lat[id_max])
                    print(abs(float(const1.inc)-lat[id_max]))
                    
                    
                    mymodel = np.poly1d(np.polyfit(res_list, lat_diff_min, deg))
                    myline = np.linspace(res_list[0], res_list[-1], 100)
                # On est sorti de l'indentation sinon l'interpolation
                # sera à chaque fois refaite à partir du premier point.
            for m in range(len(mymodel)+1):

                print("coeff",str(m),"=", mymodel[m], ", cc2 =", c)
                M[c][m]=mymodel[m]
                print("r2",r2_score(lat_diff_min, mymodel(res_list)))
                
            # Changer le nom des fichiers cible (la liste res) et l'altitude    
            plt.plot(res_list, lat_diff_max, marker="o", 
                       label="Inc - worst at "+str(a)+"km", c=colors[c], 
                       linestyle='--')
            plt.title("Difference in latitude at "+str(const1.inc)+"°")
            plt.xlabel("Resolution (m)")
            plt.ylabel("Latitude (deg)")
            # plt.xlim(0)
        plt.legend()
        plt.minorticks_on()
        plt.grid(True, which="major", color="k", linestyle="-")
        plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
        fig3.savefig(path+"/loi/"+str(const1.inc)+"_loi.png", 
                      dpi=300, pad_inches=0)
        fig4=plt.figure()
        # Coefficient des polynômes pour chaque degré en fonction de l'altitude
        plt.plot(M, alt) 
        fig4.savefig("/".join((path, "coefficients", name_res))+"_coeff.png", 
                      dpi=300, pad_inches=0)
    except:
        print("Pas d'autres fichiers similaires")
    
    
    ################################ IPS #####################################
    
    try:
    
        IPS = [i for i in range(const1.nplan)] # IPS (compose le nom de fichiers existants)
    
        colors = ['b', 'r', 'g', 'k', 'orange', 'm', 'pink', 'c', 'gold', 'yellowgreen', 'navy', 'darkturquoise'] # Une couleur par IPS
        fig3 = plt.figure(dpi=200)
        c = -1
        ips_list = []
        for ips in IPS:
            c+=1
            ips_list.append(ips)
            name = const1.name_with_ips(ips)
            N = const1.nb_sat()
            
            db = pd.read_csv(path + "/" + name + ".csv", 
                              skiprows=25+N, delimiter=",") # 25 correspond au
            # format du rapport STK
            revisit_times = np.zeros(len(db))
            lat = np.zeros(len(db))
            lon = np.zeros(len(db))
            for i in range(0, len(db)):
                try:
                    revisit_times[i] = db.iloc[i, 2]
                    lat[i] = db.iloc[i, 0]
                    lon[i] = db.iloc[i, 1]
                except:
                    break
    
            avg, minutes, new_revisit_times = moy_non_null(revisit_times)                
        
            plt.plot(ips_list[ips], avg, marker="o", 
                       label="IPS="+str(ips), c=colors[c], 
                       linestyle='--')
        plt.title("Revisite en fonction de l'IPS à "+str(const1.nplan)+" plans")
        plt.xlabel("IPS")
        plt.ylabel("Revisite (min)")
        # plt.xlim(0)
        plt.legend()
        plt.minorticks_on()
        plt.grid(True, which="major", color="k", linestyle="-")
        plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
        fig3.savefig(path + "/IPS/" + const1.name_with_ips("ips") + ".png", 
                          dpi=300, pad_inches=0)
    except:
        print("Pas d'autres fichiers similaires")
