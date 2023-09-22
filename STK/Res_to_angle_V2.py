# -*- coding: utf-8 -*-
"""
Created on Mon Jul 3 14:06:41 2023

@author: DECLINE
"""

import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

# Il faut scinder la liste des résolutions en deux pour interpoler proprement
res_sol1 = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
res_sol2 = [1.6, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
altitudes = [100, 180, 200, 220, 240, 250, 260, 300, 500, 800] # altitude

# Paramètres initiaux

res_NADIR = 0.825 # resolution au sol de la caméra (exemple 1 mètre = cahier
                  # des charges SSR)

k = np.pi / 180  # facteur de conversion degré/radian

R = 6378         # rayon de la Terre (km)

g_ND = 0         # booléen utilisé pour l'affichage de la distance ND en 
                 # fonction de l'angle
                 
g_OD = 0         # booléen utilisé pour l'affichage de la distance OD en
                 # fonction de l'angle
                 
g_reso = 1       # booléen utilisé pour l'affichage de la résolution au sol
                 # en fonction de l'angle
                 


def survol(alt):
    
    v = []
    mu = 398600
    
    for i in range(len(altitudes)):
        v.append(np.sqrt(mu/(R+altitudes[i])))
        d_theta = res_NADIR/altitudes[i] # resolution angulaire au NADIR en radians
        D_THETA = d_theta/k   # resolution angulaire au NADIR en degrés
        
        theta = np.arange(1, 90, D_THETA)*k # discrétisation du champ de
                                            # vue (theta) en radians
                                              
        THETA = theta/k                     # discrétisation du champ de
                                            # vue(theta) en degrés
                
        # print("2 x distance nadir - capteur = ", round(2*np.tan((np.pi/180*(THETA[i-1]+THETA[i])/2))*altitudes[0], 2),"km")
        # print("Time over target :", round(2*np.tan((np.pi/180*(THETA[i-1]+THETA[i])/2))*altitudes[0]/(v[i]+v[i-1])/2,2),"seconds")
    
    return THETA, theta, v, altitudes

THETA = survol(altitudes)[0]
theta = survol(altitudes)[1]
plt.figure(0)
plt.plot(survol(altitudes)[2], altitudes)      
plt.show()

deg = 4 # Degré des polynômes d'interpolation
N = len(altitudes)
M = np.zeros((N, deg+1))

def res_to_angle(res_sol):
    list1 = []
    alt = survol(altitudes)[3]
    cr = -1 # compteur résolution
    ch = -1 # compteur altitude
    power_list = []
    for h in range(len(alt)):
        ch += 1
        res_list = []
        ang_list = []
        
        for r in res_sol:
            print(r)
            cr += 1
            res_list.append(r)
            
            THETA = survol(altitudes)[0]
            theta = survol(altitudes)[1]
            
            OD_simple = alt[h]/np.cos(theta) # calcul approximatif de la 
            # distance OD (sans prise en compte de la courbure de la Terre)

            ND_simple = alt[h]*np.tan(theta) # calcul approximatif de la 
            # distance ND (sans prise en compte de la courbure de la Terre)
        
            # coefficients du polynôme de degré 2 et calcul du déterminant
            
            a = 1+1/np.tan(theta)**2
            b = -2*(R+alt[h])/np.tan(theta)
            c = alt[h]*(alt[h]+2*R)
            delta = b**2-4*a*c
    
            xDp = (-b+np.sqrt(delta))/(2*a) # racine du polynôme à rejeter
            xDm = (-b-np.sqrt(delta))/(2*a)
        
            xD = xDm                 # coordonnée x du point au sol D
            yD = np.sqrt(R**2-xD**2) # coordonnée y du point au sol D
        
            OD = np.sqrt(xD**2+(R+alt[h]-yD)**2) # distance capteur-cible
            ND = np.sqrt((R-yD)**2+xD**2)        # distance nadir-cible
        
            res_THETA = (np.diff(xD)**2+np.diff(yD)**2)**0.5 # résolution sol
                                                             # en mètres
                                                             
            res_THETA_theorique = res_NADIR/np.cos(theta)**2 # équation qui ne
            # prend pas en compte la courbure de la Terre
     
            if g_ND:
                plt.figure(1)
    
                plt.plot(THETA, ND, label="altitude h={0} km".format(
                    alt[h]))
                clr = plt.gca().get_children()[2*cr].get_color()
                plt.plot(THETA, ND_simple, linestyle='dotted', color=clr)
                plt.show()
                
            elif g_OD:
                plt.figure(1)
    
                plt.plot(THETA, OD, label=r"altitude h={0} km".format(
                    alt[h]))
                clr = plt.gca().get_children()[2*cr].get_color()
                plt.plot(THETA, OD_simple, linestyle='dotted', color=clr)
                plt.show()
                
            elif g_reso:
                plt.figure(1)
                if r == res_sol[0]:
                    plt.plot(THETA[:-1], res_THETA, 
                             label="altitude h={0} km".format(alt[h]))
                    #plt.plot(THETA[:-1], res_THETA_theorique[:-1], 
                         #label="Résolution théorique")
                else:
                    plt.plot(THETA[:-1], res_THETA)
                    #plt.plot(THETA[:-1], res_THETA_theorique[:-1])
                    
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
                
            ang_list.append((THETA[i-1]+THETA[i])/2)
            #print(ang_list[0], altitudes[h])
            plt.figure(2)
            if r==res_sol[0]:
                plt.plot(res_list, ang_list, label=str(alt[h])+"km")
            else:
                plt.plot(res_list, ang_list)
                
            plt.title(r"Interpolations entre "+str(res_sol[0])+" et "+str(res_sol[-1])+" m")
            plt.xlabel(r"Résolution limite (m)")
            plt.ylabel(r"Angle de $visée$ (deg)")
            plt.grid()
            plt.legend()
            plt.show()
            
            if r==res_sol[0]:
                power_list.append(ang_list[0])
            
        mymodel = np.poly1d(np.polyfit(res_list, ang_list, deg))
        myline = np.linspace(res_list[0], res_list[-1], 100)
    
        for j in range(len(mymodel)+1): # 4 degrés + la constante
            
            M[ch][j]=mymodel[j]
        plt.plot(myline, mymodel(myline), linestyle=':')
        plt.show()

    plt.figure(3)
    equation_list = []
    for k in range(len(M)):
        for j in range(len(M[0])):
            equation_list.append(M[k])
    
    plt.plot(M, alt)
    plt.title("Coefficents pour chaque degrés du polynôme")
    plt.xlabel("Coefficient")
    plt.ylabel("Altitude (km)")
    
    # On prend la premier élément de chaque liste pour légender chaque courbe
    premier_elt_list = []
    list_alt = []
    for l in range(deg+1): # Il y a deg+1 courbes
        premier_elt_list.append(M[0][l]) # Premier élément de la courbe
        list_alt.append(alt[0]) # On lui associe la première altitude (par ex)
        plt.scatter(premier_elt_list, list_alt, label="x^"+str(l))
    plt.legend()
    plt.show()
    return ang_list, list1
        
        
res_to_angle(res_sol2)