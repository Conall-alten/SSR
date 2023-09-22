# -*- coding: utf-8 -*-
"""
Created on Mon Jul 3 14:06:41 2023

@author: DECLINE
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


plt.close("all")

"""
# Paramètres initiaux
res_NADIR = 0.825    # resolution au sol de la caméra (exemple 1 mètre = cahier des charges SSR)
#altitudes = [150, 180, 190, 196, 200, 250, 260, 300, 400, 500]     # test de plusieurs altitudes du satellite
altitudes = [250]     # altitude de WorldView-3 (697km) sinon altitude test

# Ce qu'on veut
res_sol = 1.6

k = np.pi / 180  # facteur de conversion degré/radian
R = 6378       # rayon de la Terre (km)
g_ND = 0      # booléen utilisé pour l'affichage de la distance ND en fonction de l'angle
g_OD = 0      # booléen utilisé pour l'affichage de la distance OD en fonction de l'angle
g_reso = 1    # booléen utilisé pour l'affichage de la résolution au sol en fonction de l'angle
cc = -1 # compteur
mu = 398600
v = np.sqrt(mu/(R+altitudes[0]))


for h in altitudes:

    cc += 1

    d_theta = res_NADIR / h       # resolution angulaire au NADIR en radians
    D_THETA = d_theta / k         # resolution angulaire au NADIR en degres
    
    theta = np.arange(1, 70, D_THETA) * k   # discrétisation du champ de vue (theta) en radians
    THETA = theta / k                       # discrétisation du champ de vue (theta) en degres
    
    OD_simple = h/np.cos(theta) # calcul approximatif de la distance OD (sans prise en compte de la courbure de la Terre)
    ND_simple = h*np.tan(theta) # calcul approximatif de la distance ND (sans prise en compte de la courbure de la Terre)

    # coefficients du polynôme de degré 2 et calcul du déterminant delta
    a = 1 + 1/np.tan(theta)**2
    b = -2*(R + h)/np.tan(theta)
    c = h*(h+2*R)
    delta = b**2 - 4*a*c

    xDp = (-b+np.sqrt(delta))/(2*a) # racine du polynôme à rejeter
    xDm = (-b-np.sqrt(delta))/(2*a)

    xD = xDm                   # coordonnée x du point au sol D
    yD = np.sqrt(R**2 - xD**2) # coordonnée y du point au sol D

    OD = np.sqrt(xD**2 + (R+h-yD)**2)     # distance capteur - cible
    ND = np.sqrt((R - yD)**2 + xD ** 2)   # distance Nadir - cible

    res_THETA = (np.diff(xD)**2 + np.diff(yD)**2)**0.5  # résolution au sol en mètres
    res_THETA_theorique = res_NADIR / np.cos(theta)**2  # equation qui ne prend pas en compte la courbure de la Terre

    if g_ND:
        plt.plot(THETA, ND, label=r"altitude h={0} km".format(h))
        clr = plt.gca().get_children()[2*cc].get_color()
        #plt.plot(THETA, ND_simple, linestyle='dotted', color=clr, label="calcul simple")
        plt.plot(THETA, ND_simple, linestyle='dotted', color=clr)

    if g_OD:
        plt.plot(THETA, OD, label=r"altitude h={0} km".format(h))
        clr = plt.gca().get_children()[2 * cc].get_color()
        #plt.plot(THETA, OD_simple, linestyle='dotted', color=clr, label="calcul simple")
        plt.plot(THETA, OD_simple, linestyle='dotted', color=clr)

    if g_reso:
        plt.plot(THETA[:-1], res_THETA, label=r"altitude h={0} km".format(h))
        plt.plot(THETA[:-1], res_THETA_theorique[:-1], label="Résolution théorique")
        plt.grid()
        plt.xlabel(r"Angle de $visée$ (deg)")
        plt.ylabel("distance (km)")
        plt.title(r"distance capteur-cible (km) en fonction de l'angle de $visée$ (deg)")
        plt.legend()
        plt.show()
    
    e = 0.001
    i = 0
    while res_sol - res_THETA[i] > e :
        i = i + 1
    
        #print("Résolutions :", res_THETA[i], "et angles de", THETA[i],"degrés")

    print("Résolution entre", res_THETA[i-1], "et", res_THETA[i], "m pour un angle de", THETA[i-1], "-",THETA[i],"degrés, à l'altitude",h)
    print("Moyenne de", (res_THETA[i-1]+res_THETA[i])/2,"m à",(THETA[i-1]+THETA[i])/2,"°")
    print("2 x distance Nadir - capteur = ", 2*np.tan((np.pi/180*(THETA[i-1]+THETA[i])/2))*altitudes[0],"km")
    print("Time over target :", round(2*np.tan((np.pi/180*(THETA[i-1]+THETA[i])/2))*altitudes[0]/v,1),"seconds")

"""


#%% Affiche les listes #################################################

# Paramètres initiaux
res_NADIR = 0.825    # resolution au sol de la caméra (exemple 1 mètre = cahier des charges SSR)
#altitudes = [150, 180, 190, 196, 200, 250, 260, 300, 400, 500]     # test de plusieurs altitudes du satellite
altitudes = [100, 180, 200, 220, 240, 250, 260, 300, 400, 500, 800]     # altitude de WorldView-3 (697km) sinon altitude test
altitudes = [100]
# Ce qu'on veut
res_sol = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 10]
res_sol = [6.0]

k = np.pi / 180  # facteur de conversion degré/radian
R = 6378       # rayon de la Terre (km)
g_ND = 0      # booléen utilisé pour l'affichage de la distance ND en fonction de l'angle
g_OD = 0      # booléen utilisé pour l'affichage de la distance OD en fonction de l'angle
g_reso = 1    # booléen utilisé pour l'affichage de la résolution au sol en fonction de l'angle
cc = -1 # compteur
mu = 398600
v = np.sqrt(mu/(R+altitudes[0]))


for h in altitudes:
    res_list = []
    ang_list = []
    for r in res_sol:
        res_list.append(r)
        cc += 1
        d_theta = res_NADIR/h # resolution angulaire au NADIR en radians
        D_THETA = d_theta/k   # resolution angulaire au NADIR en degres
        
        theta = np.arange(1, 90, D_THETA)*k   # discrétisation du champ de vue (theta) en radians
        THETA = np.rad2deg(theta)                     # discrétisation du champ de vue (theta) en degres
        
        OD_simple = h/np.cos(theta) # calcul approximatif de la distance OD (sans prise en compte de la courbure de la Terre)
        ND_simple = h*np.tan(theta) # calcul approximatif de la distance ND (sans prise en compte de la courbure de la Terre)
        
        # coefficients du polynôme de degré 2 et calcul du déterminant delta
        a = 1+1/np.tan(theta)**2
        b = -2*(R+h)/np.tan(theta)
        c = h*(h+2*R)
        delta = b**2-4*a*c
        
        xDp = (-b+np.sqrt(delta))/(2*a) # racine du polynôme à rejeter
        xDm = (-b-np.sqrt(delta))/(2*a)
        
        xD = xDm                 # coordonnée x du point au sol D
        yD = np.sqrt(R**2-xD**2) # coordonnée y du point au sol D
        
        OD = np.sqrt(xD**2+(R+h-yD)**2)     # distance capteur - cible
        ND = np.sqrt((R-yD)**2+xD**2)   # distance Nadir - cible
    
        res_THETA = (np.diff(xD)**2+np.diff(yD)**2)**0.5  # résolution au sol en mètres
        res_THETA_theorique = res_NADIR/np.cos(theta)**2  # equation qui ne prend pas en compte la courbure de la Terre
        
        if g_ND:
            plt.figure(1)
            
            plt.plot(THETA, ND, label="altitude h={0} km".format(h))
            clr = plt.gca().get_children()[2*cc].get_color()
            #plt.plot(THETA, ND_simple, linestyle='dotted', color=clr, label="calcul simple")
            plt.plot(THETA, ND_simple, linestyle='dotted', color=clr)
            plt.show()
            
        elif g_OD:
            plt.figure(1)
            
            plt.plot(THETA, OD, label=r"altitude h={0} km".format(h))
            clr = plt.gca().get_children()[2 * cc].get_color()
            #plt.plot(THETA, OD_simple, linestyle='dotted', color=clr, label="calcul simple")
            plt.plot(THETA, OD_simple, linestyle='dotted', color=clr)
            plt.show()
            
        elif g_reso:
            plt.figure(1)
            if r == res_sol[0]:
                plt.plot(THETA[:-1], res_THETA, label="altitude h={0} km".format(h))
            else:
                plt.plot(THETA[:-1], res_THETA)
            #plt.plot(THETA[:-1], res_THETA_theorique[:-1], label="Résolution théorique")
            plt.grid()
            plt.xlabel(r"Angle de $visée$ (deg)")
            plt.ylabel("distance (km)")
            plt.title(r"distance capteur-cible (km) en fonction de l'angle de $visée$ (deg)")
            plt.legend()
            plt.show()
            
        e = 0.001
        i = 0
        while r - res_THETA[i] > e :
            i = i + 1
        
            #print("Résolutions :", res_THETA[i], "et angles de", THETA[i],"degrés")
    
        print(str(h),", ",str(r),", ",(round(res_THETA[i-1]+res_THETA[i])/2,4),"m à", round((THETA[i-1]+THETA[i])/2,1),"°")
        ang_list.append((THETA[i-1]+THETA[i])/2)
        
          
    plt.figure(2)
    plt.plot(res_list, ang_list, label=str(h)+"km")
    plt.xlabel(r"Pire résolution (m)")
    plt.ylabel(r"Angle de $visée$ (deg)")
    plt.grid()
    plt.legend()
    plt.show()
    

plt.figure(3)

# Pixels
if g_OD:
    plt.grid()
    plt.axhline(500, linewidth=3, color="black", linestyle="dashed")
    plt.xlabel(r"Angle de $visée$ (deg)")
    plt.ylabel("distance (km)")
    plt.title(r"distance capteur-cible (km) en fonction de l'angle de $visée$ (deg)")
    plt.legend()
    plt.show()

if g_ND:
    plt.grid()
    plt.xlabel(r"Angle de $visée$ (deg)")
    plt.ylabel("distance (km)")
    plt.title(r"distance SSP-cible (km) en fonction de l'angle de $visée$ (deg)")
    plt.legend()
    plt.show()

if g_reso:
    plt.plot(THETA, res_THETA_theorique, color="black")
    plt.xlabel(r"Angle de $visée$ (deg)")
    plt.ylabel("taille du pixel (m)")
    plt.title(r"résolution au sol (m) en fonction de l'angle de $visée$ (deg)")
    plt.grid()
    plt.legend()
    plt.yscale('log')
    plt.show()
