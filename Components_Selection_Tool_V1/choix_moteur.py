# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 10:25:57 2023

@author: cpelleray2
"""

import numpy as np
import pandas as pd

def normalisation(a):
    a_max = np.nanmax(a)
    a_min = np.nanmin(a)
    a_norm = a.copy()
    for x in range(len(a)):
        a_norm[x] = (a[x]-a_min)/(a_max-a_min)
    return a_norm

def CHOIX_MOTEUR(hy1,hy2,hy3,req_O,req_POUSSEE,req_ISP):
    MOTEUR = pd.read_excel("MOTEUR.xlsx")

    hypothese_poids = hy1 # 1=prit en compte ou 0 = inactif
    hypothese_conso = hy2 # 1 ou 0
    hypothese_cout = hy3 # 1 ou 0

    req_origine = req_O #europe / france / osef
    req_pousse = req_POUSSEE #en Newton
    req_ISP = req_ISP #en s
    
    Europe = ["Allemagne","Autriche","Belgique","France","Italie","Espagne","Finlande","Luxembourg","Norvège","Suède"]
    OTAN = ["Allemagne","France","Etats-Unis"]
    #------------------------------------------------------------------------------
    #la partie 1 s'occupe de gérer les paramètres spécifiques aux composants.

    #boucle de l'origine
    if req_origine == "Par Défault":
        #par défaut, si on s'en fou de l'origine on prend tt le monde
        MOTEUR = MOTEUR
    elif req_origine == "Europe":
        #ici on prend que ce qui est dans l'europe
        MOTEUR = MOTEUR[MOTEUR['Origine (Pays)'].isin(Europe)]
    elif req_origine == "OTAN":
        #ici on prend que ce qui est dans l'OTAN
        MOTEUR = MOTEUR[MOTEUR['Origine (Pays)'].isin(OTAN)]
    else:
        #dans les autres cas c'est qu'on regarde que le pays
        MOTEUR.drop(MOTEUR[MOTEUR['Origine (Pays)'] != req_origine].index, inplace = True)
        
    #c'est ici qu'on exclue ce qui n'est pas compatible avec le CDC (Cahier des Charges)
    MOTEUR.drop(MOTEUR[MOTEUR['ISP (s)'] <= req_ISP].index, inplace = True)
    MOTEUR.drop(MOTEUR[MOTEUR['Poussée (N)'] <= req_pousse].index, inplace = True)
    
    #ici on retire les "NaN" pour ceux qu'on veux comparer
    if hypothese_poids==1:
        MOTEUR = MOTEUR.dropna(subset=['Poids (kg)'])
    if hypothese_conso==1:
        MOTEUR = MOTEUR.dropna(subset=['Conso (W)'])
    if hypothese_cout==1:
        MOTEUR = MOTEUR.dropna(subset=['Cout (€)'])
    
    #maintenant la liste "MOTEUR" n'a que les élements compatible avec le CDC
    #il s'agit de la liste candidat
    
    #------------------------------------------------------------------------------
    #la partie 2 s'occupe de géré prendre de compte les hypothèses de choix.
    #c'est ici qu'on choisi lequel est le meilleur
    
    if len(MOTEUR)>0:
    #ci-dessous on récupère toutes les colonnes sous forme vectoriel
    #au passage on normalise entre 0 et 1 (fonction custom)
    #aussi on remplace "NaN" par un chiffre très gros
        Poids = np.nan_to_num( normalisation(MOTEUR['Poids (kg)'].to_numpy()), nan=2e64)
        Conso = np.nan_to_num( normalisation(MOTEUR['Conso (W)'].to_numpy()), nan=2e64)
        Cout = np.nan_to_num( normalisation(MOTEUR['Cout (€)'].to_numpy()), nan=2e64)
        ISP = np.nan_to_num( normalisation(MOTEUR['ISP (s)'].to_numpy()), nan=2e64)
        Poussee = np.nan_to_num( normalisation(MOTEUR['Poussée (N)'].to_numpy()), nan=2e64)
        
        #ici on prend en compte les hypothèses
        if hypothese_poids==0 and hypothese_conso==0 and hypothese_cout==0:
            #Cas par défaut sans hypothèse, on cherche au plus proche du CDC
            #ici pour un moteur: ISP et Poussée
            score = ISP+Poussee
        else:
            #Autre cas, on prend le reste en compte :
            #Si on prend pas en compte un paramètre, on le multiplie par 0
            score = Poids*hypothese_poids + Conso*hypothese_conso + Cout*hypothese_cout
        
        #Ici on prend en compte si il y a plusieurs candidats
        score_min = min(score)
        index_min = [i for i, x in enumerate(score) if x==score_min]
        
        return MOTEUR.iloc[index_min[0],0]
    else:
        return "Pas de moteur dans ces conditions"

BIMILA = CHOIX_MOTEUR(0, 0, 0, "Etats-Unis", 0.001, 100)