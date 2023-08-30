# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:36:52 2023

@author: Quentin
"""

import numpy as np
import matplotlib.pyplot as plt

k = np.pi / 180  # facteur de conversion degré/radian
res_NADIR = 0.825    # resolution au sol de la caméra (exemple 1 mètre = cahier
                     # des charges SSR)
angle = np.linspace(0, 70, 20)
#res_NADIR = 1.24 # 1.24m = résolution WorldView-3
R = 6378      # rayon de la Terre (km)

g_ND = 0      # booléen utilisé pour l'affichage de la distance ND e fonction 
              # de l'angle
g_OD = 0      # booléen utilisé pour l'affichage de la distance OD en fonction 
              # de l'angle
g_reso = 1    # booléen utilisé pour l'affichage de la résolution au sol en 
              # fonction de l'angle

cc = -1 # compteur

altitudes = [150, 180, 190, 196, 200, 250, 260, 300, 400, 500, 800] # test de 
# plusieurs altitudes du satellite

#altitudes = [160]     # altitude de WorldView-3 (697km) sinon altitude test

for h in altitudes:
    res_list = []
    for ang in angle:
        
        cc += 1
    
        d_theta = res_NADIR / h       # resolution angulaire au NADIR en radians
        D_THETA = d_theta / k         # resolution angulaire au NADIR en degres
        
        theta = np.arange(1, 70, D_THETA) * k   # discrétisation du champ de vue 
                                                # (theta) en radians
        THETA = theta / k                       # discrétisation du champ de vue 
                                                # (theta) en degres
        
        OD_simple = h/np.cos(theta) # calcul approximatif de la distance OD (sans
                                    # prise en compte de la courbure de la Terre)
        ND_simple = h*np.tan(theta) # calcul approximatif de la distance ND (sans 
                                    # prise en compte de la courbure de la Terre)
    
        # coefficients du polynôme de degré 2 et calcul du déterminant delta
        a = 1+1/np.tan(theta)**2
        b = -2*(R+h)/np.tan(theta)
        c = h*(h+2*R)
        delta = b**2-4*a*c
    
        xDp = (-b+np.sqrt(delta))/(2*a) # racine du polynôme à rejeter
        xDm = (-b-np.sqrt(delta))/(2*a)
    
        xD = xDm                   # coordonnée x du point au sol D
        yD = np.sqrt(R**2 - xD**2) # coordonnée y du point au sol D
    
        OD = np.sqrt(xD**2+(R+h-yD)**2)     # distance capteur - cible
        ND = np.sqrt((R-yD)**2+xD**2)   # distance Nadir - cible
    
        res_THETA = (np.diff(xD)**2+np.diff(yD)**2)**0.5  # résolution au sol en 
                                                          # mètres
        res_THETA_theorique = res_NADIR/np.cos(theta)**2  # equation qui ne 
        # prend pas en compte la courbure de la Terre
    
        if g_ND:
            plt.plot(THETA, ND, label=r"altitude h={0} km".format(h))
            clr = plt.gca().get_children()[2*cc].get_color()
            #plt.plot(THETA, ND_simple, linestyle='dotted', color=clr, 
            #label="calcul simple")
            plt.plot(THETA, ND_simple, linestyle='dotted', color=clr)
    
        if g_OD:
            plt.plot(THETA, OD, label=r"altitude h={0} km".format(h))
            clr = plt.gca().get_children()[2 * cc].get_color()
            #plt.plot(THETA, OD_simple, linestyle='dotted', color=clr, label=
            #"calcul simple")
            plt.plot(THETA, OD_simple, linestyle='dotted', color=clr)
    
        if g_reso:
            plt.plot(THETA[:-1], res_THETA, label=r"altitude h={0} km".format(h))
            plt.grid()
            plt.xlabel(r"Angle de $visée$ (deg)")
            plt.ylabel("distance (km)")
            plt.title(r"distance capteur-cible (km) en fonction de l'angle de "
                      "$visée$ (deg)")
            plt.legend()
            plt.show()
        
        e = 0.001    
        i = 0
        while ang - THETA[i] > e :
            i = i + 1
            #print("Résolutions :", res_THETA[i], "et angles de", THETA[i],
            #"degrés")
        res_list.append((res_THETA[i-1]+res_THETA[i])/2)
    
        print("Résolution entre", res_THETA[i-1], "et", res_THETA[i],
              "m pour un angle de", THETA[i-1], "-",THETA[i],
              "degrés, à l'altitude",h)
        print("Moyenne de", (res_THETA[i-1]+res_THETA[i])/2,"m à",
              (THETA[i-1]+THETA[i])/2,"°")
        


# affichages
# if g_OD:
#     plt.grid()
#     plt.axhline(500, linewidth=3, color="black", linestyle="dashed")
#     plt.xlabel(r"Angle de $visée$ (deg)")
#     plt.ylabel("distance (km)")
#     plt.title(r"distance capteur-cible (km) en fonction de l'angle de $visée$
     #(deg)")
#     plt.legend()
#     plt.show()

# if g_ND:
#     plt.grid()
#     plt.xlabel(r"Angle de $visée$ (deg)")
#     plt.ylabel("distance (km)")
#     plt.title(r"distance SSP-cible (km) en fonction de l'angle de $visée$ 
#(deg)")
#     plt.legend()
#     plt.show()

# if g_reso:
#     plt.plot(THETA, res_THETA_theorique, color="black")
#     plt.xlabel(r"Angle de $visée$ (deg)")
#     plt.ylabel("taille du pixel (m)")
#     plt.title(r"résolution au sol (m) en fonction de l'angle de $visée$ 
#(deg)")
#     plt.grid()
#     plt.legend()
#     plt.show()