# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:08:22 2023

@author: gblavet
"""
#Ce code est la V3 du simulateur de maintien à poste, chacune des 3 versions réalise une tâche différente;
#La V1 est le fondement des versions suivantes, celle-ci calculle les paramètres orbitaux lors d'une manoeuvre consistant à remonter 
#l'altitude du satellite.
#La V2 pousse le concept en faisant des manoeuvres jusqu'à épuisement du carburant et trace les paramètres orbitaux
#La V3 est la version finale, qui réalise les calculs pour un ensemble de données en input dans un fichier excel, et renvoie les
#durées de vie dans un autre fichier "Résultats Simu maintien
#Compte tenu de la lourdeur des calculs réalisés, cette dernière version a été créée pour lancer beaucoup de simulations en une fois.

#Pour l'utilisation vous aurez besoin de changer le fichier d'entrée ligne 242 en indiquant le path de votre fichier excel sous le format:
#           A         |         B          |    C     |  D   |   E      |      F        |       G               |       H
# 1    Masse sat (kg) |	Masse ergol (kg)   | ISP (s)  |	 Cx  | Sref (m²)|  Altitude(km) | Plage_altitude(km)    |   Poussée (N)
# 2         x         |         X          |    X     |   X  |   X      |      X        |       X               |       X
# 3         x         |         X          |    X     |   X  |   X      |      X        |       X               |       X
# 4       ...

#Changer également l'utilisateur du lien ligne 260 pour que le fichier de résultat soit disponible sur votre bureau
#Plage_altitude décrit l'intervalle d'altitude acceptable [Altitutde-plage;Altitude+plage]
#Le satellite effectuera une manoeuvre en arrivant en bas de la plage pour remonter en haut de la plage.

#Ce sont les seuls paramètres ayant un impact sur la durée de vie



import math as m
import pandas as pd #module servant à communiquer avec Excel

#La fonction Simu_maintien est la fonction main de ce code

def Simu_maintien(Msat,ISP,M_ergol,S,Cx,Altitude,Plage_altitude,Poussée=0.1)   :
    
    #Fonctions densité de l'atmosphère, dépendantes de l'activité solaire,
    #nécessaire au calcul à chaque pas de temps, c'est pourquoi on a besoin de la recalculer en permanence selon l'altitude du satellite
    #tirées du fichier "Caractérisation détaillée atmosphère" à trouver dans Idéation -> Architecture Satellite -> Dimensionnement Sat  /!\ unités /!\
    def rho(x):             # entrée en km
        if Ias==1:          #valable entre 100 et 1000 km d'altitude
            return 3789532215*(x/1000)**-8.322103382        # en kg/m^3
        if Ias==2:
            return 5887705.297*(x/1000)**-7.016396641
        if Ias==3:
            return 7462.4163143*(x/1000)**-5.66768425
    #Constantes

    R_T=6378000              #Rayon Terrestre (m)
    mu_T=398600000000000     #Paramètre gravitationel standard terretre (m^3/s²)
    J2=1.08E-3               #Première harmonique du potentiel terrestre (terme prépondérant des perturbations liées au potentiel terrestre)

    Altitude*=1000          #Passage de km à m
    Plage_altitude*=1000
    #Paramètres de la simulation

    Ias=2                #Indice d'activité solaire (1,2,3 = faible, moyenne, forte) Pour 2024, on est en cas d'activité moyenne (2)
    Z_critique = Altitude-Plage_altitude  #Altitude de l'orbite avant manoeuvre(m)
    Z_cible= Altitude+Plage_altitude      #Altitude cible (en fin de manoeuvre) (m)
    #Ces deux précédents termes définissent la plage d'altitude acceptable pour le satellite

    #Paramètres satellite 
    #Ce simulateur ayant été créé pour répondre à une manoeuvre non impulsionelle, il est spécifiquement adapté aux petites poussées
    P=Poussée             #Poussée (N) >0.0051 sinon maintien impossible(cas d'activité solaire forte)

    #Paramètres orbitaux initiaux
    Z=Z_critique             #On commence la simulation par une manoeuvre suite au maintien à poste

    a=(R_T+Z)               #demi-grand axe (m)
    e=1E-15                 #excentricité de l'orbite (pour une orbite circulaire, indiquer 1E-15)
    i=50                    #inclinaison (deg)
    RAAN=0                  #Right Ascension of Ascending Node / Ascension droite du noeud ascendant (deg)
    omega=0                 #argument du périgée (deg)
    M=0                     #anomalie moyenne
    theta=0                 #anomalie vraie
    n=m.sqrt(mu_T/a**2/a)     #mouvement moyen      # mu/a3 mais on fait mu/a2/a car a3 génère un integer overflow (>2^63)
    V=m.sqrt(mu_T/a)        #vitesse orbitale (m/s)
    masse=Msat              #Initiation de la variable masse, qui servira pour les itérations


    r_a=R_T+Z               #apogée
    r_p=R_T+Z               #périgée   (pour l'instant égaux à l'altitude car orbite circulaire)

    #Initiation temps
    t=0
    

    #passage en radiants

    i=i*m.pi/180
    M=M*m.pi/180

    #Fonction qui fait le coeur du code; le calcul des variations des paramètres orbitaux et leur incrémentation
    #Selon les équations de Gauss de perturbations du mouvement orbital
    def gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F):
        
        
        
        n=m.sqrt(mu_T/a**2/a)
        delta_a=(2/(n**2*a)*V*F/masse
                 -(rho(Z)*S*Cx/masse*V**3/(n**2*a)))*delta_T
        
        delta_e=((2*F/masse/V-(rho(Z)*S*Cx/masse*V))*(e+m.cos(theta)))*delta_T
        
        delta_i=0
        
        delta_RAAN=-3/2*J2*(R_T/a)**2*n*m.cos(i )/((1-e**2)**2)*delta_T
        
        delta_omega=((2*m.sin(theta)/(V*e)*F/masse
                      -(rho(Z)*S*Cx/masse*V*m.sin(theta))/e)
                     +3/4*J2*(R_T/a)**2*n*(5*m.cos(i)**2-1)/(1-e**2)**2)*delta_T
        
        delta_M=(n-m.sqrt(1-e**2)/(e*V)*(2*m.sin(theta)*(1+e*m.cos(theta)+e**2)/(1+e*m.cos(theta)))*F/masse
            +rho(Z)*S*Cx/masse*V*m.sin(theta)/e*(1+e**2/(1+e*m.cos(theta))*m.sqrt(1-e**2))
            + 3/4*n**2*J2*(R_T/a)**2*(3*m.cos(i )**2-1)/(1+e**2)**(3/2))*delta_T
        
        delta_masse=-F*delta_T/9.80665/ISP
        
        #incrémentation des paramètres gaussiens et masse   
        a+=delta_a
        e=abs(e+delta_e)
        i+=delta_i
        RAAN+=delta_RAAN
        omega+=delta_omega
        M=(M+delta_M)%(2*m.pi)
        
        masse+=delta_masse
        
        #calcul de l'anomalie excentrique pour obtenir les variations de theta et Z (position sur l'orbite et altitude)    
        
        E=M-e*(M*m.cos(M)-m.sin(M))/(1-e*m.cos(M))
        for k in range(5):                          #on réalise 5 itérations pour faire converger la valeur de E
            E=M-e*(E*m.cos(E)-m.sin(E))/(1-e*m.cos(E))
            
        theta=2*m.atan((m.sqrt((1+e)/1-e))*m.tan(E/2))  #Calcul du nouveau théta
        
        Z=a*(1-e*m.cos(E))-R_T  #Calcul du nouveau Z
        
        
        V=m.sqrt(mu_T/a)    #Vitesse orbitale
        
        r_p=a*(1-e)     #nouvelles altitudes périgée et apogée
        r_a=a*(1+e)
        
        
        return r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E
    #Activation moteurs
    F=P
    delta_T=0.1 #Initiation du pas de temps pour la phase de poussée

    #On réalise une première manoeuvre "manuellement" pour initier certains paramètres (notamment le temps de première poussée utilisé ensuite comme paramètre d'arrêt de la boucle)
    masse=Msat
    while r_a<R_T+Z_cible and Z>100000 and masse>Msat-M_ergol:          #On monte d'abord l'apogée jusqu'à l'altitude cible, on montera ensuite le périgée avec une deuxième manoeuvre
      
        r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
        t+=delta_T              #Incrémentation du temps
    T_première_poussée=t


    #Attente jusqu'à l'apogée de l'orbite de transfert
    F=0         #extinction moteurs

    delta_T=1
    n=m.sqrt(mu_T/(a**3))

    while M<m.pi-n*T_première_poussée/2 and Z>100000:                
             #On cherche à réaliser une poussée au périgée, mais comme la durée de poussée est longue,
             #il faut commencer avant d'y être et faire en sorte que l'on pousse autant avant l'apogée qu'après.
             #La seconde condition porte sur l'altitude, c'est sur cette partie que le satellite peut retomber trop bas si la 
             #poussée est insuffisante, ainsi on vérifie pour éviter des erreurs(altitude négative par exemple)
            
            r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
            #On appelle la fonction Gauss définie précédemment pour incrémenter les paramètres à chaque pas de temps
            t+=delta_T              #Incrémentation du temps
            


    F=P
    delta_T=0.1
    t_=t
    #Une fois l'apogée atteint, on pousse pour remonter le périgée
    while t<t_+T_première_poussée and r_p<R_T+Z_cible and Z>100000:
        r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
        t+=delta_T          

    #Fin de la première boucle d'initiation des paramètres
    #On va maintenant lancer une boucle qui fonctionne tant que le satellite n'est pas retombé et tant qu'il a du carburant
    #A chaque instant, on vérifie l'altitude, si en dessous de l'altitude critique, on initie une manoeuvre
    #On attends ensuite de retomber à cette altitude critique et ainsi de suite tant qu'il y a du carburant    

    durée_de_vie=t
    while Z>100000:
       if r_p<Z_critique+R_T:
          
           n=m.sqrt(mu_T/(a**3))          
           while M<m.pi-n*T_première_poussée/2 and masse>Msat-M_ergol: 
                
                     delta_T=1      
                     F=0
                     
                     r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)                  
                     t+=delta_T
                     n=m.sqrt(mu_T/(a**3))
                     
           T_première_poussée=0          
           while r_a<(R_T+Z_cible) and masse>Msat-M_ergol:          
                   F=P
                   delta_T=0.1      
                   
                   r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
                   t+=delta_T
                   T_première_poussée+=delta_T
                
           
           n=m.sqrt(mu_T/(a**3))          
           while M<m.pi-n*T_première_poussée/2 and masse>Msat-M_ergol:
                
                     delta_T=1      

                     F=0
                    
                     r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)                  
                     t+=delta_T         
                     n=m.sqrt(mu_T/(a**3))
                     t_=t

           while   t<t_+T_première_poussée and r_p<R_T+Z_cible and masse>Msat-M_ergol:
               
                      delta_T=0.001   
                      F=P
                      
                      r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
                      t+=delta_T   
           
          
       #Propagation naturelle de l'orbite une fois le carburant épuisé
       F=0
       delta_T=1
       r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
       t+=delta_T    
       if Z>Z_critique:         #Tant que le simulateur tourne, on actualise la durée de vie si le satellite est dans la bonne plage d'altitude pour fonctionner correctement
           durée_de_vie=t
    return durée_de_vie/86400 


#%% Cette section sert à communiquer avec Excel pour deux choses, récupérer les données d'entrées et renvoyer les résultats

df=pd.read_excel("../input/Imput simu maintien.xlsx")      #Récupération des données d'entrée
for i in range(len(df)):
    #Pour chaque ligne du tableau d'entrée, on récupère les paramètres
    Msat=df.iat[i,0]
    M_ergol=df.iat[i,1]
    ISP=df.iat[i,2]
    Cx=df.iat[i,3]
    Sref=df.iat[i,4]
    Altitude=df.iat[i,5]
    Plage_altitude=df.iat[i,6]
    Poussée=df.iat[i,7]
    #On appelle la fonction de simulation de maintien à poste, qui renvoie la durée de vie
    D_vie=Simu_maintien(Msat, ISP, M_ergol, Sref, Cx,Altitude,Plage_altitude,Poussée)
    #On met la valeur dans le tableur
    df.iat[i,8]=D_vie
    print("cas n°",i," sur ",len(df)," terminé")
#On renvoie un fichier excel différent qui contient un tableur avec les paramètres d'entrée et les résultats
df.to_excel("../output/Résultats simu maintien.xlsx","Résultats",index=False)   #Export des résultats