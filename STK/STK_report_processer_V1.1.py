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

# Indice du maximum d'une liste
def indice_max(liste):
    maxi = liste[0]
    for i in range(len(liste)):
        if liste[i]>=maxi:
            maxi=liste[i]
            ind_max=i
    return ind_max

# Indice du minimum d'une liste
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

# Convertit 24.768 en '24 min 46 s'
def minsec(minutes):
    return str(int(minutes))+" min "+str(int(round(60*(minutes-int(minutes)), 0)))+" s"
    
# Donne les coefficients des polynômes d'interpolation des courbes lat vs res
# pour chaque altitude, et les range dans une matrice (ligne N = altitude N)
def get_coeff(deg, res_sol_tot, altitudes, ang_list, h):

    plt.plot(res_list, ang_list, label=str(altitudes[h])+"km")#, c=colors[h])
    plt.title(r"Interpolations entre "+str(res_sol_tot[0][0])+" et "+str(res_sol_tot[-1][-1])+" m")
    plt.xlabel(r"Résolution limite (m)")
    plt.ylabel(r"Angle de $visée$ (deg)")
    plt.grid()
    plt.show()
    
    mymodel = np.poly1d(np.polyfit(res_list, ang_list, deg))
    myline = np.linspace(res_list[0], res_list[-1], 100)

    for i in range(deg+1): # 4 degrés plus la constante
        M[h][i]=mymodel[i] # Matrice des coefficients polynomiaux par altitude
                           # Constante, puis x, puis x²...

    return mymodel, myline, M


def doublons_moyenne(liste1, liste2):
    # liste1 : liste de nombres avec des doublons
    # liste2 : liste correspondante de même taille
    
    # Créez deux listes résultantes
    liste1_reduite = [] # Liste réduite sans doublons
    liste2_moy = [] # Liste contenant les "moyennes des doublons"

    # Listes auxiliaires pour stocker les sommes et les occurrences
    sommes = [0]*len(liste1)
    occurrences = [0]*len(liste1)

    for i in range(len(liste1)):
        n1 = liste1[i]
        n2 = liste2[i]

        # Si le nombre n'est pas déjà dans la liste_reduite, on l'y met
        if n1 not in liste1_reduite:
            liste1_reduite.append(n1)
        
        # Indice de ce nombre dans la liste_reduite
        index = liste1_reduite.index(n1)

        # Mettez à jour la somme et l'occurrence
        sommes[index]+=n2
        occurrences[index]+=1

    # Calculez les moyennes en utilisant les sommes et les occurrences
    for i in range(len(liste1_reduite)):
        moy = sommes[i]/occurrences[i]
        liste2_moy.append(moy)
        
    return liste1_reduite, liste2_moy    
    
#%% Paramétrage

# Paramètres de la constellation 1

orbit1 = "\RCO" # Type d'orbite (RCO, SSO, CITROUILLE)
#orbit1 = "\CITROUILLE"
#orbit1 = "\SSO"
sat1 = 2 # Nombre de satellites par plan (~2)
plan1 = 4 # Nombre de plans (~4 - ~12)
inc1 = "50" # Inclinaison des orbites (47, 51..., couplées 48_50, 47_49_50, ou
               # 0 si SSO) ou latitude du point focal pour une constellation 
               # citrouille
alt1 = 100 # Altitude (150 - 500 km)
res1 = 0.85   # Les fichiers apparaissent dans l'ordre alphabétique (ex : 
             # RCO_2x4_50_260_1.5, RCO_2x4_50_260_1, RCO_2x4_50_260_2.5)). Il 
             # faut donc écrire 1.0, 2.0 ou 3.0 au lieu de 1, 2 et 3 pour avoir
             # 1.0 avant 1.5

add = "_Luhansk" # Informations supplémentaires (cibles ponctuelles ou origine
                 # des satellites notamment)
add = "_KSZ"
add = "_FromFrance"
add = ""
#add = "_ChainBaseObject"

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
folder1 = "\\target_primary"
#folder1 = "\\hemisphere"
#folder1 = "\\files_points"
#folder1 = "\\target_secondary"
#folder1 = "\\general_shapes"

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
#folder3 = "IP_Spacing"

#%% Type de rapport : Access AreaTarget to Satellite-Sensor or Chain

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
        
            
            # Le temps de revisite correspond à la période entre la sortie de 
            # la zone et l'entrée suivante. On soustrait donc les dates 
            # d'entrée aux dates de sorties.
            # La première valeur de Start et la dernière de Stop sont 
            # inutilisables, d'où len(db_sorted)-1
            # db_sorted.iloc[i+1, 2] = valeur du (i+1)ème élément de la 2e 
            # colonne du tableau
        if len(db_sorted.iloc[0, 1])>1:
            try:
                revisit_times[i] = pd.to_datetime(
                    db_sorted.iloc[i+1, 1]).timestamp()-pd.to_datetime(
                        db_sorted.iloc[i, 2]).timestamp()
            except:
                 
                # Le break est essentiel car à la fin du tableau, la fonction 
                # to_datetime n'a plus de sens
                break
        else: # Un fichier Chain contient une colonne de plus contenant des 
              # indices, il faut donc augmenter les indices de 1. On
              # différencie un rapport chain d'un rapport access "manuel" en 
              # comptant la longueur de la 2e colonne (si 1, on a un indice,
              # sinon on a une date du type 1 Aug 2023 10:15:31.325)
            try:
                revisit_times[i] = pd.to_datetime(
                    db_sorted.iloc[i+1, 2]).timestamp()-pd.to_datetime(
                        db_sorted.iloc[i, 3]).timestamp()
            except:
                
                # Le break est essentiel car à la fin du tableau, la fonction 
                # to_datetime n'a plus de sens
                break
    # Moyenne
    avg, minutes, new_revisit_times = moy_non_null(revisit_times)
    
    # Durée de chaque revisite et moyenne
    fig1 = plt.figure()
    plt.minorticks_on()    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    plt.title("Revisit time, 1 week, avg = "+minsec(avg))
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
    
    
#%% Ici on s'intéresse aux rapports "Value By Grid Point", càd en tout point 
# de coordonnées (lat, long)

elif folder2=="\\FoM_points": # Loi des RCO
    
    N = sat1*plan1+sat2*plan2
    # Le délimiteur peut être , ou ; (changer si KeyError: "Start Time (UTCG)")
    db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                     folder2+folder3+name1+name2+".csv",skiprows=25+N,sep=",")
    # Le nombre 25 correspond au nombre de ligne qu'il faut sauter pour ce type
    # de rapport, lequel dépend du nombre de satellites

    #db_sorted = db.sort_values(by = ("Latitude (deg)"))

    revisit_times = []
    lat = []
    long = []
    for i in range(0, len(db)):
        try:
            if db.iloc[i, 2]<20000: # Les très grandes valeurs correspondent
                                    # à une revisite inexistante (typiquement
                                    # au niveau du pôle Nord). Celle-ci font
                                    # chuter la moyenne sur les régions utiles
                
                lat.append(db.iloc[i, 0])      # 1e colonne : latitude
                long.append(db.iloc[i, 1])     # 2e colonne : longitude
                revisit_times.append(db.iloc[i, 2]) # 3e colonne : revisite
        except:
            break
    
    # La simulation STK ne peut pas se faire sur une durée trop longue
    # (typiquement plus de 2 semaines) pour des raisons de temps de calcul.
    # Ainsi, il existe une variation des valeurs pour chaque latitude parce
    # que les satellites n'ont pas tourné assez longtemps autour de la Terre.
    # On retrouve donc plusieurs valeurs pour chaque latitude, et le nombre de
    # valeurs différentes dépend des latitudes. Il est donc impossible 
    # d'obtenir une moyenne de revisite exacte en faisant la moyenne de toutes
    # les valeurs dont on dispose puisque certaines correspondent à la même
    # latitude.
    
    lat_reduite, revisit_times_moy = doublons_moyenne(lat, revisit_times)
    
    # Moyenne
    avg, minutes, new_revisit_times = moy_non_null(revisit_times_moy)
    
    ind_max = indice_max(new_revisit_times)
    ind_min = indice_min(new_revisit_times)
    #mymodel, myline, M = get_coeff(deg, lat, altitudes, minutes, h)
    mymodel = np.poly1d(np.polyfit(lat_reduite, minutes, 5))
    myline = np.linspace(lat[0], lat[-1], 100)
    print(r2_score(minutes, mymodel(lat_reduite)))


    # # Affiche la revisite en fonction de la latitude, avec une interpolation.
    
    # fig1 = plt.figure()
    # # Affiche la corrélation et l'équation
    # # plt.plot(myline, mymodel(myline))
    # # plt.text(12, 60, mymodel)
    # # plt.text(12, 55, '{:.5f}'.format(r2_score(minutes, mymodel(lat))))
    # plt.scatter(lat_reduite, revisit_times_moy, s=10)  
    # plt.minorticks_on()
    # plt.grid(True, which="major", color="k", linestyle="-")
    # plt.grid(True, which="minor", color="grey", linestyle="-", 
    #          alpha=0.2)
    
    # # Corrélation et équation polynomiale
    # # plt.title("Revisit time, 1 week, avg = "+minsec(avg)+" s\n"+str(mymodel)+", R = "+str(
    # #         "{:.5f}".format(r2_score(minutes, mymodel(lat)))))
    
    # plt.title(name1.replace('\\', '')+", avg = "+minsec(avg))
    # plt.xlabel("Latitude (deg)")
    # plt.ylabel("Revisit time (min)")
    # fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
    #              folder2+folder3+name1+name2+".png", dpi=300, pad_inches=0)
   
    
    # # Affiche la zone cible et les latitudes remarquables.
    
    # fig2 = plt.figure()
    # plt.title("Best = "+minsec(minutes[ind_min])+", worst = " 
    #           +minsec(minutes[ind_max])+", avg = "+ minsec(avg))
    
    # plt.minorticks_on()   
    # plt.scatter(long, lat, s=10)
    
    # # Affiche les villes
    # # plt.scatter(Donetsk[0], Donetsk[1], c='k', s=50)
    # # plt.scatter(Kherson[0], Kherson[1], c='k', s=50)
    # # plt.scatter(Luhansk[0], Luhansk[1], c='k', s=50)
    # # plt.scatter(Zaporizhzhia[0], Zaporizhzhia[1], c = 'k', s = 50)
    # # plt.scatter(Sevastopol[0], Sevastopol[1], c = 'k', s = 50)
    
    # # Affiche les latitudes de l'inclinaison orbitale, de la pire et de la 
    # # meilleure revisite.
    # plt.axhline(y=int(inc1), c='k', label='inclination', linewidth=4, linestyle="--")
    # plt.axhline(y=lat[ind_max], c='r', label='maximum', linewidth=4)
    # plt.axhline(y=lat[ind_min], c='g', label='minimum', linewidth=4)
    
    # plt.grid(True, which="major", color="k", linestyle="-")
    # plt.grid(True, which="minor", color="grey", linestyle="-",
    #          alpha = 0.2)
    # plt.xlabel("Longitude (deg)")
    # plt.ylabel("Latitude (deg)")
    # plt.legend()
    # fig2.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
    #              folder2+"\map"+name1+name2+"_map.png", dpi=300,
    #              pad_inches=0)
    

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
    
    alt = [100, 180, 260, 300, 400, 500, 800]
    deg = 4
    N = len(alt)
    M = np.zeros((N, deg+1))
    #alt = [100]
    # Résolution au nadir (compose le nom de fichiers existants)
    #res = [0.85, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     
    # La liste de toutes les résolutions est scindée pour que numpy puisse
    # correctement interpoler chaque morceau de la courbe totale.
    
    res1 = [0.85, 1.0, 1.5, 2.0, 2.5, 3.0]
    res2 = [3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0]
    res = [res1, res2]
    #res = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0]
    color = ['b', 'r', 'g', 'k', 'orange', 'm', 'pink'] # Une couleur par altitude
    c = -1
    fig3 = plt.figure()
    for a in alt: # Pour chaque altitude
        c+=1
        for r1 in res: # Pour chaque segment de la liste des résolutions
            res_list = []
            diff_lat_min = []
            diff_lat_max = []
            for r2 in r1: # Pour chaque résolution dans le segment
                plt.close('all')
                res_list.append(r2)
                
                name1 = orbit1+"_"+str(sat1)+"x"+str(plan1)+"_"+inc1+"_"+str(a)+"_"+str(r2)
                print(name1)
                N = sat1*plan1 # Nombre total de satellites permettant de sauter
                # certaines lignes du rapport
                # Le délimiteur peut être , ou ; (changer si KeyError)
                db = pd.read_csv(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+
                                  folder1+folder2+folder3+name1+name2+".csv", 
                                  skiprows=25+N, delimiter=",") # 25 correspond au
                # format du rapport STK, dépendant du nombre total de satellites
                #db_sorted = db.sort_values(by = ("Latitude (deg)")) # Si besoin
                
                revisit_times = np.zeros(len(db))
                lat = np.zeros(len(db))
                long = np.zeros(len(db))
                for i in range(0, len(db)):
                    try:
                        lat[i] = db.iloc[i, 0]
                        long[i] = db.iloc[i, 1]
                        revisit_times[i] = db.iloc[i, 2]
                    except:
                        break
                
                avg, minutes, new_revisit_times = moy_non_null(revisit_times)
                
                #print(minsec(avg))
                
                # On trouve les indices du max et du min
                ind_max = indice_max(new_revisit_times)
                ind_min = indice_min(new_revisit_times)
                        
                # Position du maximum et du minimum de revisite
                # Ces latitudes moins l'inclinaison donnent une différence en 
                # degrés. Cette différence doit être connue avec précision 
                # afin de lancer une constellation sur une cible avec la plus 
                # grande précision.
                
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
                plt.plot(myline, mymodel(myline), linestyle=':', c=color[c])
                
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
    fig4.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"
                  +folder1+folder2+"\coefficients"+name1+name2+"_coeff.png", 
                  dpi=300, pad_inches=0)
    # mymodel = np.poly1d(np.polyfit(lat_reduite, minutes, 5))
    # myline = np.linspace(lat[0], lat[-1], 100)
    # print(r2_score(minutes, mymodel(lat_reduite)))


    ############################################################################
    
    add = np.arange(0,plan1)

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
        fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                     folder2+folder3+name+".png", dpi=300,
                     bbox_inches='tight')

#%% Bases au sol

elif folder2 == "\\access_ground":
    
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
        
            
            # Le temps de revisite correspond à la période entre la sortie de 
            # la zone et l'entrée suivante. On soustrait donc les dates 
            # d'entrée aux dates de sorties.
            # La première valeur de Start et la dernière de Stop sont 
            # inutilisables, d'où len(db_sorted)-1
            # db_sorted.iloc[i+1, 2] = valeur du (i+1)ème élément de la 2e 
            # colonne du tableau
        if len(db_sorted.iloc[0, 1])>1:
            try:
                revisit_times[i] = pd.to_datetime(
                    db_sorted.iloc[i+1, 1]).timestamp()-pd.to_datetime(
                        db_sorted.iloc[i, 2]).timestamp()
            except:
                 
                # Le break est essentiel car à la fin du tableau, la fonction 
                # to_datetime n'a plus de sens
                break
        else: # Un fichier Chain contient une colonne de plus contenant des 
              # indices, il faut donc augmenter les indices de 1. On
              # différencie un rapport chain d'un rapport access "manuel" en 
              # comptant la longueur de la 2e colonne (si 1, on a un indice,
              # sinon on a une date du type 1 Aug 2023 10:15:31.325)
            try:
                revisit_times[i] = pd.to_datetime(
                    db_sorted.iloc[i+1, 2]).timestamp()-pd.to_datetime(
                        db_sorted.iloc[i, 3]).timestamp()
            except:
                
                # Le break est essentiel car à la fin du tableau, la fonction 
                # to_datetime n'a plus de sens
                break
    # Moyenne
    avg, minutes, new_revisit_times = moy_non_null(revisit_times)
    
    # Durée de chaque revisite et moyenne
    fig1 = plt.figure()
    plt.minorticks_on()    
    plt.grid(True, which="major", color="k", linestyle="-")
    plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
    plt.title("Revisit time, 1 week, avg = "+minsec(avg))
    plt.xlabel("Number of revisits")
    plt.ylabel("Revisit time (min)")
    plt.scatter(np.linspace(0, len(new_revisit_times), len(new_revisit_times)),
                minutes, s=10)
    fig1.savefig(r"C:\Users\DECLINE\Desktop\logiciels\python\stk"+folder1+
                 folder2+folder3+name+".png", dpi=300, bbox_inches='tight')
        
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
                print(minsec(avg))
                
            fig1 = plt.figure()
            plt.plot(index, minutes, marker = "o")
            plt.minorticks_on()    
            plt.grid(True, which="major", color="k", linestyle="-")
            plt.grid(True, which="minor", color="grey", linestyle="-", alpha=0.2)
            plt.title("Access duration")
            plt.xlabel("Number of accesses")
            plt.ylabel("Duration (min)")