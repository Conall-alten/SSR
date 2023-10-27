# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:46:01 2023

@author: DECLINE
"""

import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

# Paramètres initiaux

res_NADIR = 0.825 # Résolution au sol de la caméra (exemple 1 mètre = cahier
                  # des charges SSR)

altitudes = [100, 180, 200, 220, 240, 250, 260, 300, 500, 800] # altitude
altitudes = np.linspace(100, 500, 10)
altitudes = [100]
# Une couleur par altitude (plots)
# colors = ['b', 'r', 'g', 'k', 'orange', 'm', 'pink', 'grey', 'gold', 'cyan'] 
    
# Résolution off-nadir désirée 

res_sol1 = np.linspace(0.9, 1.6, 6)
res_sol2 = np.linspace(1.6, 5, 5)
res_sol3 = np.linspace(5, 10, 3)
res_sol_tot = [res_sol1, res_sol2, res_sol3]

res_sol1 = [6.189]
res_sol_tot = [res_sol1]

R = 6378         # Rayon de la Terre (km)

g_ND = 0         # Booléen utilisé pour l'affichage de la distance ND en 
                 # fonction de l'angle
g_OD = 0         # Booléen utilisé pour l'affichage de la distance OD en
                 # fonction de l'angle
g_reso = 1       # Booléen utilisé pour l'affichage de la résolution au sol en
                 # fonction de l'angle

N = len(altitudes)
deg = 4 # Degré des polynômes d'interpolation
M = np.zeros((N, deg+1))

# Fonction permettant d'obtenir les coefficients des polynômes d'interpolation
# des courbes résolution vs angle de visée pour chaque altitude
# Il faut spécifier le degré des polynômes, les listes des angles et des 
# résolutions pour créer le modèle d'interpolation, et l'altitude pour le label

def get_coeff(deg, res_sol_tot, altitudes, ang_list, h):

    plt.plot(res_list, ang_list, label=str(round(altitudes[h],1))+"km")#, c=colors[h])
    plt.title(r"Interpolations entre "+str(res_sol_tot[0][0])+" et "+str(
        res_sol_tot[-1][-1])+" m")
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

# Pour chaque résolution, on fait varier l'altitude

for rt in range(len(res_sol_tot)):
    for h in range(N):
        res_list = []
        ang_list = []
        d_theta = res_NADIR/altitudes[h] # Résolution angulaire au nadir en 
                                         # radians
        D_THETA = np.rad2deg(d_theta) # Résolution angulaire au nadir en degrés
        
        theta = np.deg2rad(np.arange(1, 90, D_THETA)) # Discrétisation du champ
                                                      # de vue en radians
                                              
        THETA = np.rad2deg(theta) # Discrétisation du champ de vue en degrés
        
        OD_simple = altitudes[h]/np.cos(theta) # Calcul approximatif de la 
        # distance OD (sans prise en compte de la courbure de la Terre)
        ND_simple = altitudes[h]*np.tan(theta) # Calcul approximatif de la 
        # distance ND (sans prise en compte de la courbure de la Terre)
    
        # Coefficients du polynôme de degré 2 et calcul du déterminant delta
        a = 1+1/np.tan(theta)**2
        b = -2*(R+altitudes[h])/np.tan(theta)
        c = altitudes[h]*(altitudes[h]+2*R)
        delta = b**2-4*a*c
    
        xDp = (-b+np.sqrt(delta))/(2*a) # Racine du polynôme à rejeter
        xDm = (-b-np.sqrt(delta))/(2*a)
    
        xD = xDm                 # Coordonnée x du point au sol D
        yD = np.sqrt(R**2-xD**2) # Coordonnée y du point au sol D
    
        OD = np.sqrt(xD**2+(R+altitudes[h]-yD)**2) # Distance capteur - cible
        ND = np.sqrt((R-yD)**2+xD**2)              # Distance nadir - cible
    
        res_THETA = (np.diff(xD)**2+np.diff(yD)**2)**0.5 # Résolution au sol
                                                         # en mètres
                                                            
        res_THETA_theorique = res_NADIR/np.cos(theta)**2  # équation qui ne
        # prend pas en compte la courbure de la Terre
         
        if g_ND:
            plt.figure(1)
            plt.plot(THETA, ND, label="altitude h={0} km".format(
                altitudes[h]))
            plt.plot(THETA, ND_simple, linestyle='dotted')#, c=colors[h])
            plt.show()
            
        elif g_OD:
            plt.figure(1)
            plt.plot(THETA, OD, label=r"altitude h={0} km".format(
                altitudes[h]))
            plt.plot(THETA, OD_simple, linestyle='dotted')#, c=colors[h])
            plt.show()
            
        elif g_reso:
            plt.figure(1)
            if rt==0:
                plt.plot(THETA[:-1], res_THETA, 
                      label="altitude h={0:9.1f} km".format(altitudes[h]))#,c=colors[h])
                plt.legend()
            else:
                plt.plot(THETA[:-1], res_THETA, 
                      label="altitude h={0:9.1f} km".format(altitudes[h]))#c=colors[h])
            # plt.plot(THETA[:-1], res_THETA_theorique[:-1], 
            #       label="Résolution théorique", c=colors[h])
            
            plt.title(
                "Résolution au sol (m) en fonction de l'angle de $visée$ (deg)")
            plt.xlabel("Angle de $visée$ (deg)")
            plt.ylabel("distance (km)")
            plt.grid()
            plt.show()
            
        # Toutes les résolutions par altitude
        
        for r in res_sol_tot[rt]:  
            res_list.append(r)
            e = 0.001
            i = 0
            while r-res_THETA[i]>e:
                i = i+1
            ang_list.append((THETA[i-1]+THETA[i])/2)
        
        plt.figure(2)
        if rt==0:
            mymodel, myline, M = get_coeff(deg, res_sol_tot, altitudes, 
                                            ang_list, h)
            plt.legend() # On affiche la légende une seule fois
        else:
            mymodel, myline, M = get_coeff(deg, res_sol_tot, altitudes, 
                                            ang_list, h)
        plt.plot(myline, mymodel(myline), linestyle=':')#, c=colors[h])
        
    plt.figure(2*rt+3)
    # print("Déterminant=",np.linalg.det(M))
    # Coefficient des polynômes pour chaque degré en fonction de l'altitude
    plt.plot(M, altitudes)
    plt.title(str(res_sol_tot[rt][0])+" m to "+str(res_sol_tot[rt][-1])+" m")
    plt.xlabel("Coefficients")
    plt.ylabel("Altitude (km)")
    
    premier_elt_list = []
    list_alt = []
    for i in range(deg+1):
        premier_elt_list.append(M[0][i])
        list_alt.append(altitudes[0])
        plt.scatter(premier_elt_list, list_alt, label="x^"+str(i))
    plt.legend()
    plt.show()
    
    plt.figure(2*(rt+2)) # La prochaine figure après la liste des res
    prop = [] # Coefficient de proportionalité k
    for i in range(np.shape(M)[0]): # Pour toutes les lignes
        l = []
        for j in range(deg+1): # Pour toutes les colonnes
            k=M[i][0]/M[i][j]  # On prend la constante de chaque polynôme (premier 
                               # terme de chaque ligne) comme référence
            l.append(k)
        prop.append(l) # Liste des coefficients de proportionalité
    for i in range(len(prop)):
        plt.plot([i for i in range(deg+1)], prop[i], label="h ="+str(
            round(altitudes[i],1))+" km")
        plt.title(str(res_sol_tot[rt][0])+" m to "+str(
            res_sol_tot[rt][-1])+" m")
        plt.xlabel('Puissance de x')
        plt.ylabel('k = $C/x^n$')
        plt.legend()
        
print("Résultat en degrés :",ang_list)
print("Résolution entre", res_THETA[i-1], "et", res_THETA[i],
      "m pour un angle de", THETA[i-1], "-",THETA[i],
      "degrés, à l'altitude",altitudes[h])
print("Moyenne de", (res_THETA[i-1]+res_THETA[i])/2,"m à",
      (THETA[i-1]+THETA[i])/2,"°")