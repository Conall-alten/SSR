# -*- coding: utf-8 -*-
"""
Created on Mon Jul 3 14:06:41 2023

@author: DECLINE
"""

import numpy as np
import matplotlib.pyplot as plt


plt.close("all")


#%% Affiche les listes ########################################################

#plt.close('all')

# Paramètres initiaux

res_NADIR = 0.825 # résolution au sol de la caméra (exemple 1 mètre = cahier
                  # des charges SSR)

#altitudes = [150, 180, 190, 196, 200, 250, 260, 300, 400, 500] # test de 
# plusieurs altitudes du satellite

altitudes = [100, 180, 200, 220, 240, 250, 260, 300, 500, 800] # altitude
altitudes = [100, 200, 300, 500, 800] # altitude
# Résolution off-nadir désirée 
res_sol1 = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5]
res_sol2 = [1.6, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
#res_sol = [4, 4.5, 5.0, 10]

R = 6378         # rayon de la Terre (km)

g_ND = 0         # booléen utilisé pour l'affichage de la distance ND en 
                 # fonction de l'angle
g_OD = 0         # booléen utilisé pour l'affichage de la distance OD en
                 # fonction de l'angle
g_reso = 1       # booléen utilisé pour l'affichage de la résolution au sol en
                 # fonction de l'angle
                 
cr = -1 # compteur
mu = 398600
v = np.sqrt(mu/(R+altitudes[0]))
ch = -1
        
deg = 4 # Degré des polynômes d'interpolation
N = len(altitudes)
M1 = np.zeros((N, deg+1))
power_list = []

for h in range(N):
    res_list = []
    ang_list = []
    ch+=1
    for r in res_sol1:
        
        res_list.append(r)
        cr += 1

        d_theta = res_NADIR/altitudes[h] # résolution angulaire au nadir en 
                                         # radians
        D_THETA = np.rad2deg(d_theta)    # résolution angulaire au nadir en degrés
        
        theta = np.deg2rad(np.arange(1, 90, D_THETA)) # discrétisation du champ
                                                    # de vue (theta) en radians
                                              
        THETA = np.rad2deg(theta) # discrétisation du champ de vue (theta) en 
                                  # degrés
        
        OD_simple = altitudes[h]/np.cos(theta) # calcul approximatif de la 
        # distance OD (sans prise en compte de la courbure de la Terre)
        
        ND_simple = altitudes[h]*np.tan(theta) # calcul approximatif de la 
        # distance ND (sans prise en compte de la courbure de la Terre)
    
        # coefficients du polynôme de degré 2 et calcul du déterminant delta
        a = 1+1/np.tan(theta)**2
        b = -2*(R+altitudes[h])/np.tan(theta)
        c = altitudes[h]*(altitudes[h]+2*R)
        delta = b**2-4*a*c

        xDp = (-b+np.sqrt(delta))/(2*a) # racine du polynôme à rejeter
        xDm = (-b-np.sqrt(delta))/(2*a)
    
        xD = xDm                 # coordonnée x du point au sol D
        yD = np.sqrt(R**2-xD**2) # coordonnée y du point au sol D
    
        OD = np.sqrt(xD**2+(R+altitudes[h]-yD)**2) # distance capteur - cible
        ND = np.sqrt((R-yD)**2+xD**2)              # distance nadir - cible
    
        res_THETA = (np.diff(xD)**2+np.diff(yD)**2)**0.5 # résolution au sol
                                                         # en mètres
                                                            
        res_THETA_theorique = res_NADIR/np.cos(theta)**2  # équation qui ne
        # prend pas en compte la courbure de la Terre
 
        if g_ND:
            plt.figure(1)
            plt.plot(THETA, ND, label="altitude h={0} km".format(
                altitudes[h]))
            clr = plt.gca().get_children()[2*cr].get_color()
            plt.plot(THETA, ND_simple, linestyle='dotted', color=clr)
            plt.show()
            
        elif g_OD:
            plt.figure(1)
            plt.plot(THETA, OD, label=r"altitude h={0} km".format(
                altitudes[h]))
            clr = plt.gca().get_children()[2*cr].get_color()
            plt.plot(THETA, OD_simple, linestyle='dotted', color=clr)
            plt.show()
            
        elif g_reso:
            plt.figure(1)
            if r == res_sol1[0]:
                plt.plot(THETA[:-1], res_THETA, 
                         label="altitude h={0} km".format(altitudes[h]))
            else:
                plt.plot(THETA[:-1], res_THETA)
            #plt.plot(THETA[:-1], res_THETA_theorique[:-1], 
                     #label="Résolution théorique")
            plt.grid()
            plt.xlabel(r"Angle de $visée$ (deg)")
            plt.ylabel("distance (km)")
            plt.title(r"distance capteur-cible (km) en fonction de l'angle de $visée$ (deg)")
            plt.legend()
            plt.show()
            
        e = 0.001
        i = 0
        while i<len(res_THETA) and r-res_THETA[i]>e:
            i = i+1
        print(res_THETA)
        ang_list.append((THETA[i-1]+THETA[i])/2)
        
        plt.figure(2)
        if r==res_sol1[0]:
            plt.plot(res_list, ang_list, label=str(altitudes[h])+"km")
        else:
            plt.plot(res_list, ang_list)
            
        plt.title(r"Interpolations entre 1 et 1.6 m")
        plt.xlabel(r"Résolution limite (m)")
        plt.ylabel(r"Angle de $visée$ (deg)")
        plt.grid()
        plt.legend()
        plt.show()
        
    mymodel = np.poly1d(np.polyfit(res_list, ang_list, deg))
    myline = np.linspace(res_list[0], res_list[-1], 100)

    for i in range(deg+1): # 4 degrés plus la constante
        
        M1[ch][i]=mymodel[i]
    plt.plot(myline, mymodel(myline), linestyle=':')
    
plt.figure(3)
equation_list1 = []
for i in range(len(M1)):
    for j in range(len(M1[0])):
        equation_list1.append(M1[i])

# Coefficient des polynômes pour chaque degré en fonction de l'altitude
plt.plot(M1, altitudes)

plt.xlabel("Coefficient")
plt.ylabel("Altitude (km)")

    
premier_elt_list = []
list_alt = []
for i in range(deg+1):
    premier_elt_list.append(M1[0][i])
    list_alt.append(altitudes[0])
    plt.scatter(premier_elt_list, list_alt, label="x^"+str(i))
plt.legend()
plt.show()

###############################################################################


#Tout pareil, on prend juste l'autre moitié de la liste res_sol2

cr = -1 # compteur
ch = -1
M2 = np.zeros((N, deg+1))
power_list = []

for h in range(len(altitudes)):
    res_list = []
    ang_list = []
    ch+=1
    for r in res_sol2:
        
        res_list.append(r)
        cr += 1

        d_theta = res_NADIR/altitudes[h] # résolution angulaire au nadir en 
                                         # radians
        D_THETA = np.rad2deg(d_theta)    # résolution angulaire au nadir en degrés
        
        theta = np.deg2rad(np.arange(1, 90, D_THETA)) # discrétisation du champ de vue 
                                            # (theta) en radians
                                              
        THETA = np.rad2deg(theta)           # discrétisation du champ de vue
                                            # (theta) en degrés
        
        OD_simple = altitudes[h]/np.cos(theta) # calcul approximatif de la 
        # distance OD (sans prise en compte de la courbure de la Terre)
        
        ND_simple = altitudes[h]*np.tan(theta) # calcul approximatif de la 
        # distance ND (sans prise en compte de la courbure de la Terre)
    
        # coefficients du polynôme de degré 2 et calcul du déterminant delta
        a = 1+1/np.tan(theta)**2
        b = -2*(R+altitudes[h])/np.tan(theta)
        c = altitudes[h]*(altitudes[h]+2*R)
        delta = b**2-4*a*c

        xDp = (-b+np.sqrt(delta))/(2*a) # racine du polynôme à rejeter
        xDm = (-b-np.sqrt(delta))/(2*a)
    
        xD = xDm                 # coordonnée x du point au sol D
        yD = np.sqrt(R**2-xD**2) # coordonnée y du point au sol D
    
        OD = np.sqrt(xD**2+(R+altitudes[h]-yD)**2) # distance capteur - cible
        ND = np.sqrt((R-yD)**2+xD**2)              # distance nadir - cible
    
        res_THETA = (np.diff(xD)**2+np.diff(yD)**2)**0.5  # résolution au sol
                                                          # en mètres
                                                  
        res_THETA_theorique = res_NADIR/np.cos(theta)**2  # équation qui ne
                                 # prend pas en compte la courbure de la Terre
 
        if g_ND:
            plt.figure(4)
            plt.plot(THETA, ND, label="altitude h={0} km".format(
                altitudes[h]))
            clr = plt.gca().get_children()[2*cr].get_color()
            plt.plot(THETA, ND_simple, linestyle='dotted', color=clr)
            plt.show()
            
        elif g_OD:
            plt.figure(4)
            plt.plot(THETA, OD, label=r"altitude h={0} km".format(
                altitudes[h]))
            clr = plt.gca().get_children()[2*cr].get_color()
            plt.plot(THETA, OD_simple, linestyle='dotted', color=clr)
            plt.show()
            
        elif g_reso:
            plt.figure(4)
            if r == res_sol2[0]:
                plt.plot(THETA[:-1], res_THETA, 
                         label="altitude h={0} km".format(altitudes[h]))
            else:
                plt.plot(THETA[:-1], res_THETA)
            #plt.plot(THETA[:-1], res_THETA_theorique[:-1], 
                     #label="Résolution théorique")
            plt.grid()
            plt.xlabel(r"Angle de $visée$ (deg)")
            plt.ylabel("distance (km)")
            plt.title(r"distance capteur-cible (km) en fonction de l'angle de $visée$ (deg)")
            plt.legend()
            plt.show()
            
        e = 0.01
        i = 0
        while r-res_THETA[i]>e:
            i=i+1
        #print(i, r, round(res_THETA[i],3))
        ang_list.append((THETA[i-1]+THETA[i])/2)
        print(ang_list[0], altitudes[h])
        plt.figure(5)
        if r==res_sol2[0]:
            plt.plot(res_list, ang_list, label=str(altitudes[h])+"km")
        else:
            plt.plot(res_list, ang_list)
            
        plt.title(r"Interpolations entre 1 et 1.6 m")
        plt.xlabel(r"Résolution limite (m)")
        plt.ylabel(r"Angle de $visée$ (deg)")
        plt.grid()
        plt.legend()
        
        if r==res_sol2[0]:
            power_list.append(2)
        
        
    mymodel = np.poly1d(np.polyfit(res_list, ang_list, deg))
    myline = np.linspace(res_list[0], res_list[-1], 100)

    for i in range(len(mymodel)+1): # 4 degrés plus la constante
        
        M2[ch][i]=mymodel[i]
    plt.plot(myline, mymodel(myline), linestyle=':')
    plt.show()
plt.figure(6)
equation_list2 = []
for i in range(len(M2)):
    for j in range(len(M2[0])):
        equation_list2.append(M2[i])

plt.plot(M2, altitudes)

plt.xlabel("Coefficient")
plt.ylabel("Altitude (km)")
    
premier_elt_list = []
list_alt = []
for i in range(deg+1):
    premier_elt_list.append(M2[0][i])
    list_alt.append(altitudes[0])
    plt.scatter(premier_elt_list, list_alt, label="x^"+str(i))
plt.legend()
plt.show()