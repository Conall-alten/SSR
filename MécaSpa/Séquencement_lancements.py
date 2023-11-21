# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:15:19 2023

@author: -gblavet
"""
import pandas as pd
import math as m
import copy
path_bases=r"C:\Users\gblavet\Desktop\V3-Créneau_Tir_Automatique.xlsx"

# Definition des fonctions trigo en degrés pour utilisations plus faciles

def cosd(x):
    return m.cos(x*m.pi/180)
def sind(x):
    return m.sin(x*m.pi/180)
def acosd(x):
    return 180/m.pi*m.acos(x)
def asind(x):
    return 180/m.pi*m.asin(x)


class base:
    def __init__(self,nom,lat,lon,azimut_min,azimut_max,militaire):
        """
        Initie un élément de la classe 'base' 
        ----------
        nom : string
            nom de la base de lancement 
            
        lat : int
            latitude de la base
            
        lon : int
            longitude de la base
            
        azimut_min : int
            azimut de tir minimal possible (en degrés) (défini par rapport au nord, en sens horraire)
            
        azimut_max : int
            azimut de tir maximal possible (idem)
            
        militaire : bool
            base militaire = True, base civile = False
        """
        
        base.name=nom
        base.lat=lat
        base.lon=lon
        base.az_min=azimut_min
        base.az_max=azimut_max
        base.lanc_nord=False
        base.lanc_sud=False
        base.militaire=militaire
        base.azimut_tir=0
        
    def __repr__(self):
        return f"Base {self.name}"
    def __str__(self):
        return f"Base {self.name}"
    
    def get_info(self):
        print(" nom: ", self.name, "\n latitude,longitude: ",self.lat,", ", self.lon,"\n azimut min et max: ",self.az_min," , ",self.az_max)

class constellation:
    class plan():
        
        def __init__(self,numero,raan):
            
            r=raan
            n=numero          
            
            constellation.plan.raan=r
            constellation.plan.num=n
            constellation.plan.launched=False
        def __repr_(self):
            return f"Plan {constellation.plan.num} de la constellation {constellation.nom} "
        def __str__(self):
            return f"Plan {constellation.plan.num} de la constellation {constellation.nom} "
    
    def __init__(self,nom,nb_plans,nb_sat_par_plan,inclinaison):
        """
        définit une constellation de satellite 
        ------------
        nom : string
            nom de la constellation entre guillemet
        nb_plans : int
            nombre de plans de la constellation
        nb_sat_par_plan : int
            nombre de satellites sur chaque plan de la constellation
        inclinaison: int 
            inclinaison des plans de la constellation
        -------------
        Renvoie un élément de la classe constellation
        """
        
        constellation.name=nom
        constellation.nb_plans=nb_plans
        constellation.nb_sat_par_plan=nb_sat_par_plan
        constellation.inc=inclinaison
        constellation.ecart=360/nb_plans
        constellation.plans=[]
        
        
        for i in range(nb_plans):
            if i==0:
                
                p=copy.deepcopy(constellation.plan(0,0))
                p.num=0
                p.raan=0
                constellation.plans.append(p)
            else:
                pl=copy.deepcopy(constellation.plan(i,360*i/nb_plans))
                pl.num=i
                pl.raan=360*i/nb_plans
                constellation.plans.append(pl)
    
    def __repr__(self):
        return f"Constellation {self.name} : {self.nb_sat_par_plan}x{self.nb_plans} plans à {self.inc}° d'inclinaison"
    def __str__(self):
        return f"Constellation {self.name} : {self.nb_sat_par_plan}x{self.nb_plans} plans à {self.inc}° d'inclinaison"
    
df_bases=pd.read_excel(path_bases,sheet_name="Bases de tir")

def recup_bases(df):
    """
    

    récupère un tableau de bases de lancements avec différents paramètres et transforme chaque base du tableau en objet:base
    
    ----------
    df : pandas.data_frame
        Tableau des bases de lancements disponibles
    
    -------
    Renvoie une liste de bases
    """

    liste=[]
    for i in range(len(df)):

        b=base(df.iat[i,0],df.iat[i,6],df.iat[i,5],df.iat[i,8],df.iat[i,9],False)
        b.name,b.lat,b.lon,b.az_min,b.az_max,b.militaire=df.iat[i,0],df.iat[i,6],df.iat[i,5],df.iat[i,8],df.iat[i,9],False
        liste.append(b)
        
    return liste    
        
def dans_intervalle(az_min,az_max,angle):          
    """
    

    Parameters
    ----------
    az_min : int
        azimut minimal de la base étudiée
    az_max : int
        azimut maximal de la base étudiée
    angle : int
        azimut de tir nécessaire pour le lancement

    Returns
    -------
    bool
        possible de réaliser le lancement à l'angle donné en entrée: True ou False

    """
    
    if az_min<=az_max:
        if az_min<=angle<=az_max:
            return True
        else: 
            return False
    if az_min>az_max:
        if -180<=angle<=az_max or az_min<=angle<=180:
            return True
        else:
            return False
        
def tri_bases(liste,inclinaison):   
    """
    Fait le tri des bases capables de réaliser un lancement sur une orbite à l'inclinaison donnée

    Parameters
    ----------
    liste : list(base)
        liste de bases de lancements
    inclinaison : int
        inclinaison de l'orbite cible
        
    Returns
    -------
    list
        Renvoie une liste triée sans les bases ne pouvant pas réaliser le tir à l'inclinaison donnée
        (car leur latitude est supérieure à l'inclinasion en valeur absolue)
        
    """
                                    
    liste_triée=[]
    for i in range(len(liste)):
        
        b=liste[i]
        if abs(b.lat)<inclinaison:
            azimut_tir=asind(cosd(inclinaison)/cosd(b.lat))
            # print(b)
            # print(b.az_min)
            # print(b.az_max)
            # print("az_tir=",azimut_tir)
            if dans_intervalle(b.az_min,b.az_max,azimut_tir):
                b.lanc_nord=True            
                                
            if dans_intervalle(b.az_min,b.az_max,180-azimut_tir):
                b.lanc_sud=True
                
            # print("lancement nord =",b.lanc_nord,"lancement sud =",b.lanc_sud)         
            if b.lanc_nord or b.lanc_sud:
                liste_triée.append(b)
        
            
    return liste_triée                  

def raan_base(base,const):
    """
    

    Parameters
    ----------
    base : element of class 'base'
        the base you want to find the distance to
    const : element of class 'constellation'
        studied constellation

    Raises
    ------
    Exception
        si éléments en entrés pas de la bonne classe

    Returns
    -------
    raan : int
        longitude du noeud ascendant des plans au moment du lancement

    """
    if base.__class__.__name__!='base':
        raise Exception("l'objet n'est pas une base")
    if const.__class__.__name__!="constellation":
        raise Exception("Ceci n'est pas un objet de la classe constellation")
        
    Az=asind(cosd(const.inc)/cosd(base.lat))
    
    if base.lanc_sud==True:
        Az_s=m.pi-Az
        
    RAAN_Az=acosd(cosd(Az)/sind(const.inc))
    
    if base.lat>0: #Pour des raisons géométriques, l'ascension droite est positive si latitude négative et inversement
        RAAN_Az*=-1
        
    raan=RAAN_Az+base.lon
    
    if base.lanc_sud:
       raan_sud=RAAN_Az-Az_s
       return raan,raan_sud
   
    return raan


def ecart(const,base):
    """
    

    Parameters
    ----------
    const : constellation (classe)
        constellation étudiée
    base : base (classe)
        base de lancement pour laquelle on veut calculer l'écart au plan

    Returns
    -------
    m : int
        écart min entre les plans et la base
    j : int
        numéro du plan le plus proche de la base pour lancement nord
    k : int
        numéro du plan le plus proche de la base pour lancement sud
    """

    L_num=[]
    L_dif_raan=[]
    j=0
    k=0


    if type(raan_base(base,const))==tuple:
        
        raan_cible,raan_cible_sud=raan_base(base,const)
        if base.lanc_nord==True:

            for i in range(const.nb_plans):
                if const.plans[i].launched==False:
                    
                        L_num.append(const.plans[i].num)
                        L_dif_raan.append((const.plans[i].raan-raan_cible)%360)
                        

                        if (const.plans[i].raan-raan_cible)<L_dif_raan[j-1]:
                            j=i

        if base.lanc_sud==True:

            for i in range(const.nb_plans):
                
                if const.plans[i].launched==False:
                    
                        L_num.append(const.plans[i].num)
                        L_dif_raan.append((const.plans[i].raan-raan_cible_sud)%360)

                        if (const.plans[i].raan-raan_cible_sud)<L_dif_raan[k-1]:
                            k=i

        m=min(L_dif_raan)   #on renvoie la distance min aux plans
        
    else:
        raan_cible=raan_base(base,const)
        if base.lanc_nord==True:

            for i in range(const.nb_plans):
                if const.plans[i].launched==False:
                    
                        L_num.append(const.plans[i].num)
                        L_dif_raan.append((const.plans[i].raan-raan_cible)%360)

                        if (const.plans[i].raan-raan_cible)%360<L_dif_raan[j-1]:
                            j=i

        m=min(L_dif_raan)
    # print(base,"\nécart en raan", m, "\n")

    
    if L_dif_raan[j]==m:    #et le numéro du plan associé, selon si le lancement s'effectue vers le nord ou sud
        return m,j
    return m,k


def raan_to_temps(raan):
    """
    

    Parameters
    ----------
    raan : int
        écart de longitude (ou raan) en degrés

    Returns
    -------
    int
        renvoie le nb de secondes correspondant à la rotation de la terre de {raan} degrés

    """
    omega_Terre=4.178075e-3 #deg/s
    return raan/omega_Terre

def decalage_plans(const,raan):
    """
    

    Parameters
    ----------
    const : constellation
        constellation que l'on souhaite décaler
    raan : int
        ascension droite de laquelle on veut décaler la constellation

    Returns
    -------
    const : constellation
        la constellation décalée du raan souhaitée

    """
    for i in range(len(const.plans)):
        const.plans[i].raan+=raan
    
    return const

def lancement(base,const,num=0):
    """
    

    Parameters
    ----------
    base : base
        Base depuis laquelle est fait le lancement
    const : constellation
        constellation dont on lance un plan
    num: int
        numéro du plan a lancé, si 0, on calcule le plochain plan lançable
    Returns
    -------
    const : constellation
        constellation avec un plan de lancé
    tps : int
        temps écoulé pour le lancement depuis le dernier lancement

    """
    if num==0:
        
        e,num=ecart(const,base)
    e,num=ecart(const,base)   # si un numéro de plan est spécifié, on l'utilise, sinon on calcule le premier plan a arrivé sur une base
    const_=decalage_plans(const, e)
    const_.plans[num].launched=True
    tps=raan_to_temps(e)
    return const_,tps

def planning_lancement(df_bases,const,nb_bases):

    bases_=recup_bases(df_bases)
    t=0
    bases=tri_bases(bases_, const.inc)
    statut_plans=[]
    const1=const
    for i in range(const.nb_plans):
        statut_plans.append(const.plans[i].launched)
    bases_utilisees=[]
    j=0
    
    while False in statut_plans and j<const1.nb_plans:
        ecarts=[]
        num_pl=[]
        indices=[]
        for i in range(len(bases)):
            if (bases[i] in bases_utilisees) or ((bases[i] not in bases_utilisees) and len(bases_utilisees)<nb_bases):
                # print(i)
                
                dist,num=ecart(const1,bases[i])
                ecarts.append(dist)
                num_pl.append(num)
                indices.append(i)
        d=min(ecarts)
        # print(indices)
        ind=indices[ecarts.index(d)]
        if bases[ind] not in bases_utilisees:
            
            bases_utilisees.append(bases[ind])
        n=num_pl[ecarts.index(d)]
        const1,tps=lancement(bases[ind],const1,n)
        # print(bases[ind])

        # print(bases_utilisees)
        t+=tps
        # print(t)
        # print("bases utilisées:",bases_utilisees)
        j+=1
        print(f"lancement {j} de la {bases[ind]} à t= {int(t/3600)}h {int((t%3600)/60)}min")
            