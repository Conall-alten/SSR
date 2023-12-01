
import math as m
import matplotlib.pyplot as plt
import numpy as np

plt.close('all')

#Ce code est la V2 du simulateur de maintien à poste, chacune des 3 versions réalise une tâche différente;
#La V1 est le fondement des versions suivantes, celle-ci calculle les paramètres orbitaux lors d'une manoeuvre consistant à remonter 
#l'altitude du satellite.
#La V2 pousse le concept en faisant des manoeuvres jusqu'à épuisement du carburant et trace les paramètres orbitaux
#La V3 est la version finale, qui réalise les calculs pour un ensemble de données en input dans un fichier excel, et renvoie les
#durées de vie dans un autre fichier "Résultats Simu maintien"
#Compte tenu de la lourdeur des calculs réalisés, cette dernière version a été créée pour lancer beaucoup de simulations en une fois.


#Constantes

R_T=6378000              #Rayon Terrestre (m)
mu_T=398600000000000     #Paramètre gravitationel standard terretre (m^3/s²)
J2=1.08E-3


#Paramètres de la simulation

Ias=2                #Indice d'activité solaire (1,2,3 = faible, moyenne, forte)
Z_critique = 240000  #Altitude de l'orbite avant manoeuvre(m)
Z_cible= 260000      #Altitude cible (en fin de manoeuvre) (m)


#Paramètres satellite 

P=2             #Poussée (N) >0.0051 sinon maintien impossible(cas d'activité solaire forte)
ISP=100           #Impulsion spécifique du moteur (s)
Msat=40           #Masse du satellite (kg)
S=0.2          #Surface de référence du satellite (m²)
Cx=4           #Coefficient de trainée
M_ergol=2          #Masse de carburant alloué (kg)

#Paramètres orbitaux initiaux
Z=Z_critique

a=(R_T+Z)               #demi-grand axe (m)
e=1E-15                 #excentricité de l'orbite (pour une orbite circulaire, indiquer 1E-15)
i=50                    #inclinaison (deg)
RAAN=0                  #Right Ascension of Ascending Node / Ascension droite du noeud ascendant (deg)
omega=0                 #argument du périgée (deg)
M=0                     #anomalie moyenne
theta=0                 #anomalie vraie
n=m.sqrt(mu_T/a**3)     #mouvement moyen
V=m.sqrt(mu_T/a)        #vitesse orbitale (m/s)
masse=Msat


r_a=R_T+Z               #apogée
r_p=R_T+Z               #périgée   (pour l'instant égaux à l'altitude car orbite circulaire)

#Initiation temps
t=0



#Initiation des vecteurs pour le tracé
DEMI_GRAND_AXE=[]
EXCENTRICITE=[]
INCLINAISON=[]
ASCENSION_DROITE=[]
ARGUMENT_PERIGEE=[]
ANOMALIE_MOYENNE=[]
TEMPS=[]
ALTITUDE=[]
ANOMALIE_EXCENTRIQUE=[]
MASSE=[]
MASSE_VOLUMIQUE=[]
THETA=[]
TEST=[]
APOGEE=[]
PERIGEE=[]
POUSSEE=[]
rayon=[]


def rho(x):             #Fonctions densité de l'atmosphère, dépendantes de l'activité solaire, tirées du fichier "Caractérisation détaillée atmosphère" à trouver dans Idéation -> Architecture Satellite -> Dimensionnement Sat  /!\ unités /!\
    if Ias==1:          #valable entre 100 et 1000 km d'altitude
        return 3789532215*(x/1000)**-8.322103382        # en kg/m^3
    if Ias==2:
        return 5887705.297*(x/1000)**-7.016396641
    if Ias==3:
        return 7462.4163143*(x/1000)**-5.66768425

F=P

#passage en radiants

i=i*m.pi/180
M=M*m.pi/180


#Equation de Gauss: avec poussée et deux perturbations : la trainée atmosphérique et le J2

#Définition de la fonction qui réalise les calculs et incrémentation des paramètres orbitaux

def gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F):
    n=m.sqrt(mu_T/(a**3))
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
    for k in range(5):                          #on réalise 5 itérations pour faire converger
        E=M-e*(E*m.cos(E)-m.sin(E))/(1-e*m.cos(E))
        
    theta=2*m.atan((m.sqrt((1+e)/1-e))*m.tan(E/2))
    
    Z=a*(1-e*m.cos(E))-R_T
    V=m.sqrt(mu_T/a)
    
    r_p=a*(1-e)
    r_a=a*(1+e)
    
    
    return r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E

#fonction pour la mise en tableau des paramètres orbitaux, cela évite de réécrire la même chose à chaque boucle
def mise_en_tableau(A_,B_,C_,D_,E_,F_,G_,H_,I_,J_,K_,L_,M_,N_,O_,P_,a_,b_,c_,d_,e_,f_,g_,h_,i_,j_,k_,l_,m_,n_,o_,p_):
    A_.append(a_)
    B_.append(b_)
    C_.append(c_)
    D_.append(d_)
    E_.append(e_)
    F_.append(f_)
    G_.append(g_)
    H_.append(h_)
    I_.append(i_)
    J_.append(j_)
    K_.append(k_)
    L_.append(l_)
    M_.append(m_)
    N_.append(n_)
    O_.append(o_)
    P_.append(p_)
    return A_,B_,C_,D_,E_,F_,G_,H_,I_,J_,K_,L_,M_,N_,O_,P_

delta_T=0.1

#On réalise une première manoeuvre "manuellement" pour initier certains paramètres (notamment le temps de première poussée utilisé ensuite comme paramètre d'arrêt de la boucle)
masse=Msat
while r_a<R_T+Z_cible and Z>100000 and masse>Msat-M_ergol:          #On monte d'abord l'apogée jusqu'à l'altitude cible, on montera ensuite le périgée avec une deuxième manoeuvre
  
    r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
    #mise des valeurs dans les vecteurs pour le tracé
    
    # DEMI_GRAND_AXE.append(a/1000)       #on récupère les valeurs en km pour le plotting
    # EXCENTRICITE.append(e)
    # INCLINAISON.append(i)
    # ASCENSION_DROITE.append(RAAN*180/m.pi)
    # ARGUMENT_PERIGEE.append(omega*180/m.pi)
    # ANOMALIE_MOYENNE.append(M*180/m.pi)
    # TEMPS.append(t)
    # ALTITUDE.append(Z)
    # ANOMALIE_EXCENTRIQUE.append(E)
    # MASSE.append(masse)
    # MASSE_VOLUMIQUE.append(rho(Z))
    # THETA.append(theta*180/m.pi)
    # APOGEE.append((r_a-6378000)/1000)
    # PERIGEE.append((r_p-6378000)/1000)
    # POUSSEE.append(F)
    # rayon.append(Z+R_T)
    
    #la fonction ci-dessous fait ce qui précède
    DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
    t+=delta_T              #Incrémentation du temps
T_première_poussée=t


#Attente jusqu'à l'apogée de l'orbite de transfert
F=0

delta_T=1
n=m.sqrt(mu_T/(a**3))

while M<m.pi-n*T_première_poussée/2 and Z>100000 and masse>Msat-M_ergol:                #on attends d'être au périgée moins le temps de poussée de la première manoeuvre
         
        #les deux lignes ci-dessous font le coeur du code: l'incrémentation des paramètres via les équations de gauss,
        #et la mise en vecteur des valeurs pour le tracé
        #Elles seront donc répétées à chaque étape 
        r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
        DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
        t+=delta_T              #Incrémentation du temps
        
#Deuxième phase de poussée, à l'apogée


#On refait exactement la même manoeuvre que pour monter l'apogée, même poussée. Seulement, pour les moteurs à faible poussée (électriques typiquement), on a besoin d'une autre condition puisque les faibles pousséees ont fait monter l'apogée et le périgée en parrallèle
F=P
delta_T=0.1
t_=t
while t<t_+T_première_poussée and r_p<R_T+Z_cible:
    r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
    #mise des valeurs dans les vecteurs pour le tracé
    
    DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
    t+=delta_T          

    
#Par la suite, on répète ses 3 étapes en en rajoutant une autre en amont de celles-ci: la phase d'attente du passage au périgée pour commencer la manoeuvre


durée_de_vie=t
while Z>100000:
   if r_p<Z_critique+R_T:
      
       n=m.sqrt(mu_T/(a**3))          
       while M<m.pi-n*T_première_poussée/2 and masse>Msat-M_ergol: #on attends d'être presque au périgée pour commencer la première maoneuvre visant à remonter l'apogée
            
                 delta_T=1      #pas de temps plus grand que pour les phases de poussées (besoin de précision moindre sur la propagation naturelle de l'orbite)
                 F=0
                 
                 r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)                  
                 DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
                 
                 t+=delta_T
                 n=m.sqrt(mu_T/(a**3))
                 
       T_première_poussée=0          
       while r_a<(R_T+Z_cible) and masse>Msat-M_ergol:          #On monte d'abord l'apogée jusqu'à l'altitude cible, on montera ensuite le périgée avec une deuxième manoeuvre
               F=P
               delta_T=0.1      #changement du pas de temps pour les phases propulsées car besoin de précision
               
               r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
               DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
    
               t+=delta_T
               T_première_poussée+=delta_T
            
       
       n=m.sqrt(mu_T/(a**3))          
       while M<m.pi-n*T_première_poussée/2 and masse>Msat-M_ergol:
            
                 delta_T=1      #pas de temps plus grand que pour les phases de poussées (besoin de précision moindre sur la propagation naturelle de l'orbite)

                 F=0
                
                 r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)                  
                 DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
                 
                 t+=delta_T         
                 n=m.sqrt(mu_T/(a**3))
                 t_=t

       while  t<t_+T_première_poussée and r_p<R_T+Z_cible and masse>Msat-M_ergol:
           
                  delta_T=0.001   #pas de temps plus précis pour phases propulsées
                  F=P
                  
                  r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
                  DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
                  
                  t+=delta_T   
       
      
   #Propagation naturelle de l'orbite une fois le carburant épuisé
   F=0
   delta_T=1
   r_a,r_p, a,e,i,RAAN,omega,M,masse,Z,V,theta,t,E=gauss(delta_T,a,e,i,RAAN,omega,M,masse,Z,V,theta,t,F)
   DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon=mise_en_tableau(DEMI_GRAND_AXE,EXCENTRICITE,INCLINAISON,ASCENSION_DROITE,ARGUMENT_PERIGEE,ANOMALIE_MOYENNE,TEMPS,ALTITUDE,ANOMALIE_EXCENTRIQUE,MASSE,MASSE_VOLUMIQUE,THETA,APOGEE,PERIGEE,POUSSEE,rayon,a/100,e,i,RAAN*180/m.pi,omega*180/m.pi,M*180/m.pi,t,Z,E,masse,rho(Z),theta*180/m.pi,(r_a-6378000)/1000,(r_p-6378000)/1000,F,Z+R_T)
   
   t+=delta_T    
   if Z>Z_critique:
       durée_de_vie=t
   
print(" durée de vie à poste:",int(durée_de_vie),"s \n soit ", durée_de_vie/86400," jours")
print(" temps avant retombée:",int(t/864)/100, " jours")
#%%         TRACE DES RESULTATS
ANGLE_ABSOLU=[]
for i in range(len(THETA)):
    ANGLE_ABSOLU.append(THETA[i]+ARGUMENT_PERIGEE[i])
    
plt.close("all")    


figure, axis = plt.subplots(3,4)
figure.suptitle("Paramètres lors de la manoeuvre en fonction du temps (s)")
manager = plt.get_current_fig_manager()
manager.window.showMaximized()

axis[0,0].plot(TEMPS,DEMI_GRAND_AXE)
axis[0,0].set_title('Demi-grand axe')
axis[0,0].set_ylabel("Demi-grand axe (km)")
axis[0,0].grid('on')

axis[0,1].plot(TEMPS,EXCENTRICITE)
axis[0,1].set_title('excentricité')
axis[0,1].set_ylabel("excentricité")
axis[0,1].grid('on')

axis[0,2].plot(TEMPS,ARGUMENT_PERIGEE)
axis[0,2].set_title('argument du périgée')
axis[0,2].set_ylabel("argument du périgée (deg)")
axis[0,2].grid('on')

axis[0,3].plot(TEMPS,ANGLE_ABSOLU)
axis[0,3].set_title('Angle Absolu')
axis[0,3].set_ylabel("Angle absolu")
axis[0,3].grid('on')

axis[1,0].plot(TEMPS,ANOMALIE_MOYENNE)
axis[1,0].set_title('Anomalie moyenne')
axis[1,0].set_ylabel("Anomalie moyenne (deg)")
axis[1,0].grid('on')

axis[1,1].plot(TEMPS,ALTITUDE)
axis[1,1].set_title('Altitude')
axis[1,1].set_ylabel("Altitude (m)")
axis[1,1].grid('on')


axis[1,2].plot(TEMPS,MASSE)
axis[1,2].set_title('Masse du satellite')
axis[1,2].set_ylabel("Masse satellite (kg)")
axis[1,2].grid('on')

axis[1,3].plot(TEMPS,APOGEE)
axis[1,3].set_title('Variation de l\'apogée')
axis[1,3].set_ylabel("Apogée (km)")
axis[1,3].grid('on')

axis[2,0].plot(TEMPS,THETA)
axis[2,0].set_title('anomalie vraie')
axis[2,0].set_ylabel("anomalie vraie(deg)")
axis[2,0].grid('on')

axis[2,1].plot(TEMPS,POUSSEE)
axis[2,1].set_title('Poussée en fonction du temps')
axis[2,1].set_ylabel("Poussée(N)")
axis[2,1].grid('on')

axis[2,3].plot(TEMPS,PERIGEE)
axis[2,3].set_title('Variation du périgée')
axis[2,3].set_ylabel("périgée (km)")
axis[2,3].grid('on')


axis[2,2].plot(TEMPS,APOGEE,label='Apogée')
axis[2,2].plot(TEMPS,PERIGEE,label='Périgée')
axis[2,2].legend(["Apogée","Périgée"])
axis[2,2].set_title('Variation de l\'apogée et du périgée')
axis[2,2].set_ylabel("Apogée / périgée (km)")
axis[2,2].grid('on')

                
#Tracé 3D de l'orbite au dessus de la Terre

#Transfert des coordonnées en cartésiennes
x=[]
y=[]
z=[]


#Transformation des données angulaire de degrées à radians, étape nécessaire pour les fonctions de numpy ci-dessous
def deg_to_rad(vect):       
    for i in range(len(vect)):
        vect[i]=vect[i]*m.pi/180
    return vect    

deg_to_rad(THETA)
deg_to_rad(ARGUMENT_PERIGEE)
deg_to_rad(ASCENSION_DROITE)

#Conversion des données orbitales en paramètres cartésiens par une matrice de rotation
matrice_de_rotation=[rayon*(np.cos(THETA)*(np.cos(ARGUMENT_PERIGEE)*np.cos(ASCENSION_DROITE)-np.sin(ARGUMENT_PERIGEE)*np.cos(INCLINAISON)*np.sin(ASCENSION_DROITE))-np.sin(THETA)*(np.sin(ARGUMENT_PERIGEE)*np.cos(ASCENSION_DROITE)+np.cos(ARGUMENT_PERIGEE)*np.cos(INCLINAISON)*np.sin(ASCENSION_DROITE))),
                      rayon*(np.cos(THETA)*(np.cos(ARGUMENT_PERIGEE)*np.sin(ASCENSION_DROITE)+np.sin(ARGUMENT_PERIGEE)*np.cos(INCLINAISON)*np.cos(ASCENSION_DROITE))+np.sin(THETA)*(np.cos(ARGUMENT_PERIGEE)*np.cos(INCLINAISON)*np.cos(ASCENSION_DROITE)-np.sin(ARGUMENT_PERIGEE)*np.sin(ASCENSION_DROITE))),
                      rayon*(np.cos(THETA)*(np.sin(ARGUMENT_PERIGEE)*np.sin(INCLINAISON))+np.sin(THETA)*(np.cos(ARGUMENT_PERIGEE)*np.sin(INCLINAISON)))]
x,y,z=matrice_de_rotation

fig=plt.figure()
ax=plt.axes(projection='3d')
ax.grid()
ax.plot3D(x,y,z,"m-", linewidth=1)
#définition des axes à 7000 km pour une meilleure vue
ax.axes.set_xlim3d(-7000000,7000000)
ax.axes.set_ylim3d(-7000000, 7000000)
ax.axes.set_zlim3d(-7000000,7000000)

#Tracé Terre 3D

u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
xt = R_T*np.cos(u) * np.sin(v)
yt = R_T*np.sin(u) * np.sin(v)
zt = R_T*np.cos(v)
ax.plot_surface(xt,yt,zt,shade=0,alpha=0.5)



