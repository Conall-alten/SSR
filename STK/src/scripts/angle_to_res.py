# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:36:52 2023

@author: Decline
"""

import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

# Paramètres initiaux

res_NADIR = 0.825    # resolution au sol de la caméra (exemple 1 mètre = cahier
                     # des charges SSR)
                     
angle = [66.5] # Angle maximum souhaité

R = 6378      # rayon de la Terre (km)

cc = -1 # compteur

altitudes = [100] # test d'une ou plusieurs altitudes du satellite
N = len(altitudes)
for h in range(N):
    res_list = []
    for ang in angle:
        cc += 1
        d_theta = res_NADIR/altitudes[h] # Résolution angulaire au nadir en 
                                         # radians
        D_THETA = np.rad2deg(d_theta) # Résolution angulaire au nadir en degrés
        
        theta = np.deg2rad(np.arange(1, ang+1, D_THETA)) # Discrétisation du champ
                                                         # de vue en radians
                                              
        THETA = np.rad2deg(theta) # Discrétisation du champ de vue en degrés
        
        OD_simple = altitudes[h]/np.cos(theta) # calcul approximatif de la distance OD (sans
                                    # prise en compte de la courbure de la Terre)
        ND_simple = altitudes[h]*np.tan(theta) # calcul approximatif de la distance ND (sans 
                                    # prise en compte de la courbure de la Terre)
    
        # coefficients du polynôme de degré 2 et calcul du déterminant delta
        a = 1+1/np.tan(theta)**2
        b = -2*(R+h)/np.tan(theta)
        c = altitudes[h]*(altitudes[h]+2*R)
        delta = b**2-4*a*c
    
        xDp = (-b+np.sqrt(delta))/(2*a) # racine du polynôme à rejeter
        xDm = (-b-np.sqrt(delta))/(2*a)
    
        xD = xDm                   # coordonnée x du point au sol D
        yD = np.sqrt(R**2 - xD**2) # coordonnée y du point au sol D
    
        res_THETA = (np.diff(xD)**2+np.diff(yD)**2)**0.5  # résolution au sol en 
                                                          # mètres
        res_THETA_theorique = res_NADIR/np.cos(theta)**2  # équation qui ne 
        # prend pas en compte la courbure de la Terre
    
        if ang==angle[0]:
            plt.plot(THETA[:-1], res_THETA, label=r"altitude h={0} km".format(altitudes[h]))
        else:
            plt.plot(THETA[:-1], res_THETA)
        plt.grid()
        plt.xlabel(r"Angle de $visée$ (deg)")
        plt.ylabel("distance (km)")
        plt.title(r"distance capteur-cible (km) en fonction de l'angle de "
                    "$visée$ (deg)")
        plt.legend()
        plt.show()
        
        e = 0.01
        i = 0
        while ang - THETA[i] > e :
            i = i + 1
            # print("Résolutions :", res_THETA[i], "et angles de", THETA[i],
            # "degrés")
        res_list.append((res_THETA[i-1]+res_THETA[i])/2)
    
        print("Résolution entre", res_THETA[i-1], "et", res_THETA[i],
              "m pour un angle de", THETA[i-1], "-",THETA[i],
              "degrés, à l'altitude",altitudes[h])
        print("Moyenne de", (res_THETA[i-1]+res_THETA[i])/2,"m à",
              (THETA[i-1]+THETA[i])/2,"°")
    