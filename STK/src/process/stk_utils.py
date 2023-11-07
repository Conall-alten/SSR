# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def indice_max(liste):
    """Indice du maximum d'une liste
    """
    return liste.index(max(liste))


def indice_min(liste):
    """Indice du minimum d'une liste
    """
    return liste.index(min(liste))


def moy_non_null(liste):
    """Calcule la moyenne des éléments non nuls d'une liste.

    Args :
        liste (list): liste de réels en secondes.

    Returns:
        avg : moyennes des éléments non nuls de liste.
        minutes : liste mais en minutes.
        new_revisit_times : liste mais sans les éléments nuls.

    """
    new_revisit_times = [] # Secondes
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


def minsec(minutes):
    """
    Args :
        minutes (float): nombre réel en minutes (par exemple 24.768).

    Returns:
        min_sec (str): string de la forme '24 min 46 s'
    """
    min_sec = str(int(minutes))+" min "+str(int(round(60*(minutes-int(minutes)), 0)))+" s"
    return min_sec
    

def get_coeff(deg, res_sol_tot, altitudes, ang_list, h):
    """
    Donne les coefficients des polynômes d'interpolation des courbes lat vs res
    pour chaque altitude, et les range dans une matrice (ligne N = altitude N)

    Parameters
    ----------
    deg : integer
        Degré du polynôme d'interpolation.
    res_sol_tot : list
        Liste des sous-listes de résolutions.
    altitudes : list
        Liste des altitudes.
    ang_list : TYPE
        DESCRIPTION.
    h : TYPE
        DESCRIPTION.

    Returns
    -------
    mymodel : TYPE
        DESCRIPTION.
    myline : TYPE
        DESCRIPTION.
    M : TYPE
        DESCRIPTION.

    """

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


def doing_thing(path, name, always_take = False):
    # Traitement du fichier csv
    
    # Le délimiteur peut être , ou ; si le fichier csv a transité sur Teams 
    # (changer si KeyError: "Start Time (UTCG)")
    # db est un DataFrame (sorte de tableau)
    
    # Les accès sont donnés pour chaque satellite, il faut donc les classer 
    # de façon chronologique indépendamment du satellite
    # Le fichier est trié selon la colonne Start Time
    
    # Création d'une nouvelle colonne permettant d'indexer correctement les
    # nouvelles lignes classées (les anciens indices sont dans le désordre)
    
    # Les temps de revisite seront stockés dans cette liste
    
    db = pd.read_csv(path + '/' + name + ".csv", delimiter=",")
    db_sorted = db.sort_values(by = ("Start Time (UTCG)"))
    index = np.arange(0, len(db_sorted))
    db_sorted.insert(0, "index", index)
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
                val = pd.to_datetime(
                    db_sorted.iloc[i+1, 1]).timestamp()-pd.to_datetime(
                        db_sorted.iloc[i, 2]).timestamp()
                if abs(val)<20000 or always_take :
                    revisit_times[i] = val
            except:
                # Le break est essentiel car à la fin du tableau, la fonction 
                # to_datetime n'a plus de sens
                break
            
            
        else: 
            # Un fichier Chain contient une colonne de plus contenant des 
            # indices, il faut donc augmenter les indices de 1. On
            # différencie un rapport chain d'un rapport access "manuel" en 
            # comptant la longueur de la 2e colonne (si 1, on a un indice,
            # sinon on a une date du type 1 Aug 2023 10:15:31.325)
            try:
                val = pd.to_datetime(
                    db_sorted.iloc[i+1, 2]).timestamp()-pd.to_datetime(
                        db_sorted.iloc[i, 3]).timestamp()
                if abs(val)<20000 or always_take :
                    revisit_times[i] = valeur
            except:
                # Le break est essentiel car à la fin du tableau, la fonction 
                # to_datetime n'a plus de sens
                break
    # Moyenne
    return moy_non_null(revisit_times)
