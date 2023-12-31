# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 10:53:45 2023

@author: msige
"""

"""A partir des parametres keplerien de l'orbite et des coordonnes de la station sol,
Calculer le temps de vue du satellite avec la station sol afin d'en déduire un 
débit de communication raisonnable.

Amélioration :
    fonction Changement de repère (geocentrique en terrestre local GS)
    Plot Ground track plus précis
    path fichier dans GUI
"""

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import image
import skyfield.api as sf
import tkinter as tk


def interface_graph():
    """Fonction permettant l'ouverture d'une fenetre graphique pour 
    faciliter le paramétrage de la simulation (orbite, durée, station sol)"""
    # window parameter
    fenetre = tk.Tk()
    fenetre.title("Find A title")
    fenetre.geometry("600x180")

    # texts
    tk.Label(fenetre, text="Simulation Parameters", relief='sunken', bg='orange').grid(row=0, column=1)
    tk.Label(fenetre, text="Année").grid(row=2, column=0)
    tk.Label(fenetre, text="Mois").grid(row=3, column=0)
    tk.Label(fenetre, text="Jour").grid(row=4, column=0)
    tk.Label(fenetre, text="Heure").grid(row=5, column=0)
    tk.Label(fenetre, text="Minute de début").grid(row=6, column=0)
    tk.Label(fenetre, text="Durée de la simulation (en min)").grid(row=7, column=0)
    tk.Label(fenetre, text="Pas de la simulation").grid(row=8, column=0)

    tk.Label(fenetre, text="Orbit Parameters", relief='sunken', bg='yellow').grid(row=0, column=3)
    tk.Label(fenetre, text="Inclinaison").grid(row=2, column=2)
    tk.Label(fenetre, text="Ascension droite").grid(row=3, column=2)
    tk.Label(fenetre, text="Excentricité").grid(row=4, column=2)
    tk.Label(fenetre, text="Argument du périgé").grid(row=5, column=2)
    tk.Label(fenetre, text="Anomalie moyenne").grid(row=6, column=2)
    tk.Label(fenetre, text="Altitude (en km)").grid(row=7, column=2)
    tk.Label(fenetre, text="Nombre de Satellites").grid(row=8, column=2)

    # parameters saving
    s1 = tk.IntVar(value=2023)        # annee
    s2 = tk.IntVar(value=11)          # mois
    s3 = tk.IntVar(value=7)           # jour
    s4 = tk.IntVar(value=12)          # heure
    s5 = tk.IntVar(value=00)          # minute
    s6 = tk.IntVar(value=180)         # durée
    s7 = tk.DoubleVar(value=0.1)     # pas 
      
    s8 = tk.DoubleVar(value=50)     # inclinaison
    s9 = tk.DoubleVar(value=180)   # ascension droite
    s10 = tk.IntVar(value=0)          # excentricité
    s11 = tk.DoubleVar(value=0)  # argument du périgée
    s12 = tk.DoubleVar(value=0.5)  # anomalie moyenne
    s13 = tk.DoubleVar(value=250.0)   # altitude
    s14 = tk.IntVar(value=3)       # nombre de satellites

    # parameters windows
    e1 = tk.Entry(textvariable=s1, justify='center')
    e2 = tk.Entry(textvariable=s2, justify='center')
    e3 = tk.Entry(textvariable=s3, justify='center')
    e4 = tk.Entry(textvariable=s4, justify='center')
    e5 = tk.Entry(textvariable=s5, justify='center')
    e6 = tk.Entry(textvariable=s6, justify='center')
    e7 = tk.Entry(textvariable=s7, justify='center')
    e8 = tk.Entry(textvariable=s8, justify='center')
    e9 = tk.Entry(textvariable=s9, justify='center')
    e10 = tk.Entry(textvariable=s10, justify='center')
    e11 = tk.Entry(textvariable=s11, justify='center')
    e12 = tk.Entry(textvariable=s12, justify='center')
    e13 = tk.Entry(textvariable=s13, justify='center')
    e14 = tk.Entry(textvariable=s14, justify='center')
    
    # parameters position
    e1.grid(row=2, column=1)
    e2.grid(row=3, column=1)
    e3.grid(row=4, column=1) 
    e4.grid(row=5, column=1)
    e5.grid(row=6, column=1)
    e6.grid(row=7, column=1)
    e7.grid(row=8, column=1)
      
    e8.grid(row=2, column=3)
    e9.grid(row=3, column=3)
    e10.grid(row=4, column=3)
    e11.grid(row=5, column=3)
    e12.grid(row=6, column=3)
    e13.grid(row=7, column=3)
    e14.grid(row=8, column=3)

    # quit button
    btn = tk.Button(fenetre, text ="Okay", relief='sunken', bg='lightblue', command = fenetre.destroy)
    btn.grid(row=8, column=6)

    # run the app
    fenetre.mainloop()
    
    return s1.get(), s2.get(), s3.get(), s4.get(), s5.get(), s6.get(), s7.get(), s8.get(), s9.get(), s10.get(), s11.get(), s12.get(), s13.get(), s14.get()


def liste_GS():
    all_GS = {'Toulouse': (43.428889,1.497778), 'Papeete': (-17.511,-149.435), 'IleAmsterdam': (-37.493,77.337), 'Noumea': (-22.2758,166.458), 'Kiev': (50.45, 30.523611), 'Kourou': (5.25144, -52.8047), 'Redu': (50.001889, 5.146656), 'SantaMaria': (36.99725, -25.135722), 'Kiruna': (67.857128, 20.964325), 'Rapa': (-27.583333, -144.333333)}
    return all_GS


def array_gs(all_gs):
    array_gs = np.array([*all_gs.values()])
    lat_gs = []
    lon_gs = []
    for i in range(len(array_gs)):
        lat_gs.append(array_gs[i][0])
        lon_gs.append(array_gs[i][1])
    lat_gs = np.array(lat_gs)
    lon_gs = np.array(lon_gs)
    
    return lat_gs, lon_gs

    
def array_ssp(all_ssp):
    lat_ssp = []
    lon_ssp = []
    for i in range(len(all_ssp)):
        lat_ssp.append(all_ssp[i][0])
        lon_ssp.append(all_ssp[i][1])
    lat_ssp = np.array(lat_ssp)
    lon_ssp = np.array(lon_ssp)
    
    return lat_ssp, lon_ssp
    
    
def create_epoch(annee, mois, jour, heure, minute, lenght, step):
    """Fonction permettant la création d'une date et de la conertir au format
    compatible pour la TLE
    Crée aussi une liste de dates permettant la simulation sur une période"""
    # Créez un objet datetime avec les valeurs fournies par l'utilisateur
    date = datetime(annee, mois, jour, heure, minute)

    # Calcul du jour dans l'année avec une fraction de jour
    day_of_year = date.timetuple().tm_yday
    fraction_of_day = (date.hour * 3600 + date.minute * 60) / 86400

    # Créez la date au format TLE en combinant les deux derniers chiffres de l'année et le jour avec fraction de jour
    tle_date = f"{annee % 100:02d}{day_of_year + fraction_of_day:.8f}"

    ts = sf.load.timescale()
    minutes = np.arange(minute, minute+lenght, step)
    times = ts.utc(annee, mois, jour, heure, minutes)

    return times, tle_date


def mean_motion(h):
    """
    Cette fonction calcule le mouvement moyen, en rad/jour, 
    en fonction de l'altitude du satellite, en km'
    """
    Re = 6378  # Earth radius
    mu = 398600
    a = h + Re
    return np.round(np.sqrt(mu/(a**3))*3600*24/(2*np.pi),14)
    

def create_orbit(h, i, j, k, l, m, sat_i, num):
    """Fonction permettant de convertir au format TLE et d'intégrer dans la
    deuxième ligne de la TLE les paramètres donnés par l'utilisateur"""
    n = mean_motion(m)
    i_i = i + 360/num*sat_i
    end_tle_2 = f"{h:08.4f} {i_i:08.4f} {j:07d} {k:08.4f} {l:08.4f} {n:.14f}"
    return end_tle_2


def ground_track(tle_line1, tle_line2, dates):
    """
    Cette fonction cree le satellite à partir des informations de la TLE 
    (two lines elements) et renvoie sa position projeté sur Terre (lat, lon)
    ainsi que sa hauteur
    """
    sat = sf.EarthSatellite(tle_line1, tle_line2)
    geocentric = sat.at(dates)
    subsat = geocentric.subpoint()

    lat = subsat.latitude.degrees
    lon = subsat.longitude.degrees
    elev = subsat.elevation.km

    return lat, lon, elev


def size_seen(h):
    """
    Cette fonction calcule l'horizon du point de vue du satellite en fonction 
    de sa distance a la Terre (altitude)
    Elle renvoie en degrée la distance maximale visible depuis 
    la longitude ou latitude du point sous le satllite sur Terre
    """
    Re = 6378  # Earth radius
    lam = np.arccos(Re/(Re+h))
    return lam*180/np.pi


def is_seen(SSP, lat_gr, lon_gr, hori=10):
    """
    Cette fonction renvoie une liste contenant les moments ou la station au 
    sol est dans le champs de vue du satellite ainsi que l'angle entre le 
    zénith local et le satellite
    le paramètre hori permet de définir un angle minimal au dessus de l'horizon
    pour considerer le satellite comme visible (10° par exemple)
    """
    Re = 6378
    # Conversion en coordonées cartesienne (origine centre Terre)
    x_GS = np.cos(lat_gr*np.pi/180)*np.cos(lon_gr*np.pi/180)*Re
    y_GS = np.cos(lat_gr*np.pi/180)*np.sin(lon_gr*np.pi/180)*Re
    z_GS = np.sin(lat_gr*np.pi/180)*Re
    
    x = np.cos(SSP[0]*np.pi/180)*np.cos(SSP[1]*np.pi/180)*(Re+SSP[2])
    y = np.cos(SSP[0]*np.pi/180)*np.sin(SSP[1]*np.pi/180)*(Re+SSP[2])
    z = np.sin(SSP[0]*np.pi/180)*(Re+SSP[2])
    
    # vecteurs normalisés
    v_GS_sat = [x-x_GS, y-y_GS, z-z_GS]/(np.sqrt((x-x_GS)**2+(y-y_GS)**2+(z-z_GS)**2))
    u = np.sqrt(x_GS**2 + y_GS**2 + z_GS**2)  #norme
    v_GS_zenith = [x_GS/u, y_GS/u, z_GS/u]
    
    # angle entre les vecteurs (elevation)
    cos_th = v_GS_sat[0]*v_GS_zenith[0] + v_GS_sat[1]*v_GS_zenith[1] + v_GS_sat[2]*v_GS_zenith[2]
    th = np.arccos(cos_th)
    
    # angle entre les vecteurs projeté sur le plan local (azimuth)
    v_GS_sat_loc = [SSP[0]-lat_gr, SSP[1]-lon_gr]
    n = np.sqrt(v_GS_sat_loc[0]**2 + v_GS_sat_loc[1]**2)  #norme
    v_origin_lon = [-1, 0]  # droit vers l'equateur
    v_origin_lat = [0, 1]  # droit vers l'est
    cos_alp = (v_GS_sat_loc[0]*v_origin_lon[0] + v_GS_sat_loc[1]*v_origin_lon[1])/n
    sign = v_GS_sat_loc[0]*v_origin_lat[0] + v_GS_sat_loc[1]*v_origin_lat[1]
    alp = np.arccos(cos_alp)

    tempo=[]
    elev=[]
    azim=[]
    
    for i in range(len(th)):
        if th[i]*180/np.pi < (90-hori) :
            tempo.append(i)
            elev.append(90-th[i]*180/np.pi)
            if sign[i] > 0 :
                azim.append(alp[i]*180/np.pi)
            else:
                azim.append(360-alp[i]*180/np.pi)
            
    groupes = zip(tempo, azim, elev)

    # Création d'une liste à trois dimensions
    liste_3d = [list(groupe) for groupe in groupes]
      
    return liste_3d
    

def decouper_liste_en_sous_listes(liste):
    """Dans le cas ou la satellite est visible a des moments différents, cette
    fonction permet de séparer ces moments"""
    sous_listes = []
    sous_liste = [liste[0]]

    for i in range(1, len(liste)):
        if liste[i][0] == liste[i - 1][0] + 1:
            sous_liste.append(liste[i])
        else:
            sous_listes.append(sous_liste)
            sous_liste = [liste[i]]

    sous_listes.append(sous_liste)
    return sous_listes


def time_seen(group, dates):
    """Fonction qui calcule la durée de visibilité du satellite et précise 
    entre quelles dates"""
    print("La station est visible entre", dates[group[0][0]], "et",  dates[group[-1][0]])
    dt = datetime.strptime(dates[group[-1][0]], "%Y-%m-%d %H:%M:%S TT")-datetime.strptime(dates[group[0][0]], "%Y-%m-%d %H:%M:%S TT")
    print("Soit pendant :", dt.seconds, "s")
    
    return dates[group[0][0]], dates[group[-1][0]], dt.seconds
 

def speed_rotation(positions1, positions2, temps):
    """Fonction pour calculer la vitesse de rotation de l'antenne à partir 
    de son orientation en fonction du temps"""
    positions1 = np.array(positions1)
    positions2 = np.array(positions2)
    temps = np.array(temps)

    # Calculer les différences finies centrées pour obtenir la dérivée
    derivee1 = np.gradient(positions1, temps)
    derivee2 = np.gradient(positions2, temps)

    # Tracer les résultats
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(temps, derivee1, marker='.', linestyle='-', color='green')
    ax1.set_ylabel('Rotation zenith local (°/s)')
    
    ax2.plot(temps, derivee2, marker='.', linestyle='-', color='royalblue')
    ax2.set_xlabel('seconds')
    ax2.set_ylabel('Elevation (°/s)')
    plt.title('Vitesses de rotation de l\'antenne sol')
    plt.tight_layout()
    plt.show()


def antenna_rotation(liste, pas):
    """Convertie les indices en secondes et trace la position de l'antenne pour
    un bon suivi du satellite"""
    for group in liste:
        indice, azimuth, hauteur = zip(*group)
        indice_s = (np.array(indice) - indice[0])*pas*60
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(indice_s, azimuth, marker='.', linestyle='-', color='green')
        ax1.set_ylabel('Rotation zenith local (°)')
        
        ax2.plot(indice_s, hauteur, marker='.', linestyle='-', color='royalblue')
        ax2.set_xlabel('seconds')
        ax2.set_ylabel('Elevation (°)')
        
        plt.title('Positions de l\'antenne sol')
        plt.tight_layout()
        plt.show()
        
        speed_rotation(azimuth, hauteur, indice_s)
        
 
def plot_ground_track(all_SSP, all_gs):
    """Trace la position du satellite sur Terre ainsi que la station sol"""

    lat_gs, lon_gs = array_gs(all_gs)
    SSP_0, SSP_1 = array_ssp(all_SSP)
    
    fig, ax = plt.subplots()
    img = image.imread('planisphere-4000.jpg')  #x=4000, y=2000 pixels
    couleurs = plt.cm.plasma(np.linspace(0, 1, len(SSP_0)))
    
    new_lat = (-100/9)*SSP_0 + 1000
    new_lon = (200/18)*SSP_1 + 2000
    new_lat_gs = (-100/9)*lat_gs + 1000
    new_lon_gs = (200/18)*lon_gs + 2000
    
    for i in range(len(SSP_0)):
        ax.scatter(new_lon[i], new_lat[i], marker='.', color=couleurs[i])
    ax.scatter(new_lon_gs, new_lat_gs, marker='*', color='red')
    plt.imshow(img)
    plt.show()
    

def find_cle(dic, valeur_recherchee):
    for cle, valeur in dic.items():
        if valeur == valeur_recherchee:
            cle_trouvee = cle
            return cle_trouvee
   
      
def main():
    
    a, b, c, d, e, f, g, h, i, j, k, l, m, n = interface_graph()
    
    file_path = "result_inc"+str(h)+"deg_"+str(n)+"sat_"+str(f)+"min_"+str(m)+"km"+".csv"     
    fichier = open(file_path, "w")
    fichier.write('N° Sat,Name Station,T Begin,T End, Period (s)' + '\n')
    
    all_gs = liste_GS()
    all_SSP = []
    times, epoch = create_epoch(a, b, c, d, e, f, g)
    
    for sat_i in range(n):  # n satellites dans la constellation
        print('*********************************************************\n')
        print("Satellite n°", (sat_i+1))
    
        tle_1 = "1 00001U 98067A   " + epoch + "  .00021906  00000+0  28403-3 0  8652" 
        tle_2 = "2 00001 " + create_orbit(h, i, j, k, l, m, sat_i, n)

        SSP = ground_track(tle_1, tle_2, times)
        all_SSP.append(SSP)
    
        lats_ground_stations, lons_ground_stations = array_gs(all_gs)
        for k in range(len(lats_ground_stations)):
            name_gs = find_cle(all_gs, (lats_ground_stations[k], lons_ground_stations[k]))
            moments = is_seen(SSP, lats_ground_stations[k], lons_ground_stations[k])
        
            if moments==[]:
                print("La station", name_gs, "n'est jamais visible \n")
            
            else :
                print("Concernant la station", name_gs, ":")
                sub_listes = decouper_liste_en_sous_listes(moments)
                for group in sub_listes:
                    t0, t1, dt = time_seen(group, times.tt_strftime())
                    fichier.write(str(sat_i+1) +','+ name_gs +','+ t0 +','+ t1 +','+ str(dt) + '\n')
                    
                antenna_rotation(sub_listes, g)
                print('\n\n-------------------------------------------------------------\n')
                
    fichier.close()            
    plot_ground_track(all_SSP, all_gs)        

if __name__ == "__main__":
    main()