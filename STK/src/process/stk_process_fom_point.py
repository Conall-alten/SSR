# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stk_utils import *
from sklearn.metrics import r2_score


def process_fom_point(path, name1, name2, Nsat1, Nplan1, Nsat2, Nplan2, inc1, alt1, IPS1, r, add1):
    if name2=="":
        Nsat2=0
        Nplan2=0
    
    N = Nsat1*Nplan1+Nsat2*Nplan2
    # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time (UTCG)")
    db = pd.read_csv(path+folder3+name1+name2+".csv",skiprows=25+N,sep=",")
    revisit_times = []
    lat = []
    long = []
    for i in range(0, len(db)):
        try:
            if db.iloc[i, 2]<20000:
                revisit_times.append(db.iloc[i, 2]) # 3e colonne : revisite
                lat.append(db.iloc[i, 0])
                long.append(db.iloc[i, 1])
            
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
    # plt.plot(myline, mymodel(myline))
    # plt.text(12, 60, mymodel)
    # plt.text(12, 55, '{:.5f}'.format(r2_score(minutes, mymodel(lat))))
    plt.scatter(lat_reduite, revisit_times_moy_sec, s=10)
    plt.minorticks_on()
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", 
              alpha=0.2)
    
    # Corrélation et équation polynomiale
    # plt.title("Revisit time, 1 week, avg = "+minsec(avg)+" s\n"+str(mymodel)+", R = "+str(
    #         "{:.5f}".format(r2_score(minutes, mymodel(lat)))))
    
    plt.title(name1+", avg = "+minsec(avg))
    plt.xlabel("Latitude (deg)")
    plt.ylabel("Revisit time (min)")
    fig1.savefig("/"join(path, name1 + name2) + ".png", dpi=300, pad_inches=0)
    
    # Affiche la zone cible et les latitudes remarquables.
    
    fig2 = plt.figure()
    plt.title("Best = "+minsec(minutes[ind_min])+", worst = " 
              +minsec(minutes[ind_max])+", avg = "+ minsec(avg))
    plt.minorticks_on()   
    plt.scatter(long, lat, s=10)
    
    # Affiche les villes
    plt.scatter(Donetsk[0], Donetsk[1], c='k', s=50)
    plt.scatter(Kherson[0], Kherson[1], c='k', s=50)
    plt.scatter(Luhansk[0], Luhansk[1], c='k', s=50)
    plt.scatter(Zaporizhzhia[0], Zaporizhzhia[1], c = 'k', s = 50)
    plt.scatter(Sevastopol[0], Sevastopol[1], c = 'k', s = 50)
    
    # Affiche les latitudes de l'inclinaison orbitale, de la pire et de la 
    # meilleure revisite.
    plt.axhline(y=int(inc1), c='k', label='inclination', linewidth=4, linestyle="--")
    plt.axhline(y=lat[ind_max], c='r', label='maximum', linewidth=4)
    plt.axhline(y=lat[ind_min], c='g', label='minimum', linewidth=4)
    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-",
              alpha = 0.2)
    plt.xlabel("Longitude (deg)")
    plt.ylabel("Latitude (deg)")
    plt.legend()
    fig2.savefig("/".join(path, "map", name1 + name2 + "_map.png"), dpi=300,
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
        #alt = [100, 180, 260, 300, 400, 500, 800]
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
                    name1 = const1+"_"+str(Nsat1)+"x"+str(Nplan1)+"_"+str(inc1)+"_"+str(a)+"_"+str(IPS1)+"_"+str(r2)+add1
                    print(name1)
                    N = Nsat1*Nplan1
                    # Le délimiteur peut être , ou ; (changer si KeyError)
                    db = pd.read_csv(path+folder3+name1+name2+".csv", 
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
            
                    maxi = revisit_times_non_null[0]
                    indice_max = 0
                    mini = revisit_times_non_null[0]
                    indice_min = 0
                    for i in range(len(revisit_times_non_null)):
                        if revisit_times_non_null[i]>=maxi:
                            maxi = revisit_times_non_null[i]
                            indice_max = i
                        if revisit_times_non_null[i]<=mini:
                            mini = revisit_times_non_null[i]
                            indice_min = i
                            
                    lat_diff_min.append(abs(float(inc1)-lat[indice_min]))
                    lat_diff_max.append(abs(float(inc1)-lat[indice_max]))
                    print(inc1)
                    print(lat[indice_max])
                    print(abs(float(inc1)-lat[indice_max]))
                    
                    
                    mymodel = np.poly1d(np.polyfit(res_list, lat_diff_min, deg))
                    myline = np.linspace(res_list[0], res_list[-1], 100)
                # On est sorti de l'indentation sinon l'interpolation
                # sera à chaque fois refaite à partir du premier point.
            for m in range(len(mymodel)+1):

                print("coeff",str(m),"=", mymodel[m], ", cc2 =", c)
                M[c][m]=mymodel[m]
                print("r2",r2_score(lat_diff_min, mymodel(res_list)))
            #plt.plot(myline, mymodel(myline), linestyle=':', c=colors[c])
                
            # Changer le nom des fichiers cible (la liste res) et l'altitude    
            
            #plt.plot(res_list, lat_diff_min, marker="o", 
            #          label="Inc - best at "+str(a)+"km", c=colors[c])
            plt.plot(res_list, lat_diff_max, marker="o", 
                       label="Inc - worst at "+str(a)+"km", c=colors[c], 
                       linestyle='--')
            plt.title("Difference in latitude at "+str(inc1)+"°")
            plt.xlabel("Resolution (m)")
            plt.ylabel("Latitude (deg)")
            # plt.xlim(0)
        plt.legend()
        plt.minorticks_on()
        plt.grid(True, which="major", color="k", linestyle="-")
        plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
        fig3.savefig(path+folder3+"\loi\\"+str(inc1)+"_loi.png", 
                      dpi=300, pad_inches=0)
        fig4=plt.figure()
        # Coefficient des polynômes pour chaque degré en fonction de l'altitude
        plt.plot(M, alt) 
        fig4.savefig(path+folder3+"\coefficients"+name1+name2+"_coeff.png", 
                      dpi=300, pad_inches=0)
    except:
        print("Pas d'autres fichiers similaires")
    
    
    ################################ IPS #####################################
    
    try:
        
        const1 = "\SSO"
        Nsat1 = 2 # Nombre de satellites par plan
        Nplan1 = 12 # Nombre de plans
        inc1 = "0" # Inclinaison des orbites (0° par convention pour une SSO)
        alt1 = 250 # Altitude (km)
        res1 = 2.0
    
        IPS = [i for i in range(Nplan1)] # IPS (compose le nom de fichiers existants)
    
        colors = ['b', 'r', 'g', 'k', 'orange', 'm', 'pink', 'c', 'gold', 'yellowgreen', 'navy', 'darkturquoise'] # Une couleur par IPS
        fig3 = plt.figure(dpi=200)
        c = -1
        ips_list = []
        for ips in IPS:
            c+=1
            ips_list.append(ips)
            name1 = const1+"_"+str(Nsat1)+"x"+str(Nplan1)+"_"+str(inc1)+"_"+str(alt1)+"_"+str(ips)+"_"+str(res1)+add1
            name = name1+name2
            print(name)
            if name2=="":
                Nsat2 = 0
                Nplan2 = 0
            N = Nsat1*Nplan1+Nsat2*Nplan2
            
            db = pd.read_csv(path+folder3+name+".csv", 
                              skiprows=25+N, delimiter=",") # 25 correspond au
            # format du rapport STK
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
        
            plt.plot(ips_list[ips], avg, marker="o", 
                       label="IPS="+str(ips), c=colors[c], 
                       linestyle='--')
        plt.title("Revisite en fonction de l'IPS à "+str(Nplan1)+" plans")
        plt.xlabel("IPS")
        plt.ylabel("Revisite (min)")
        # plt.xlim(0)
        plt.legend()
        plt.minorticks_on()
        plt.grid(True, which="major", color="k", linestyle="-")
        plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
        fig3.savefig(path+"\IPS\\"+const1+"_"+str(Nsat1)+"x"+str(Nplan1)+"_"+str(inc1)+"_"+str(alt1)+"_ips_"+str(res1)+add1+".png", 
                          dpi=300, pad_inches=0)
    except:
        print("Pas d'autres fichiers similaires")