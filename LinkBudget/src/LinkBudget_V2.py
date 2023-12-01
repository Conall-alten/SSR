# This code have the aim to compute link budget for a given transmitting antenna (on the CubeSat)
# and a given receiving antenna (Ground station)


import numpy as np
import pandas as pd


# constants
c = 3*10** 8  # speed of light (m/s)
k = 1.38*10** -23  # Boltzmann constant (dB)

Treshold = 10  # Treshold (dB)
R0 = 6378000  # earth radius (m)
T_s = 400  # system noise (K) ! to be recompute after final choice of feeder !


def compute_free_space_loss(lat_e, lon_e, h_e, lat_r, lon_r, h_r, lam):
    cos_phi = np.cos(lat_r)*np.cos(lat_e)*np.cos(np.abs(lon_r-lon_e)) + np.sin(lat_r)*np.sin(lat_e)
    R = (h_e - h_r)*np.sqrt(1+2*R0/(h_e-h_r)*(1+R0/(h_e-h_r))*(1-cos_phi))
    L_fs = (4*np.pi*R/lam)**2  # free space loss

    return L_fs


def compute_gain(diam_rec, lam, eta=0.6):
    G_max = eta*(np.pi*diam_rec/lam)**2
    return G_max


def compute_link(P_e, G_e, G_r, FSL, B):
    # emiter
    EIRP_max = P_e*G_e  # (W)

    # receiver
    P_r = EIRP_max*G_r/FSL  # power received

    # finaly
    C_N0 = P_r/T_s/k
    C_N = C_N0/B

    # print
    #print("C/N0 =", 10*np.log10(C_N0), "dBHz")
    #print("C/N =", 10*np.log10(C_N), "dB")

    return 10*np.log10(C_N)

def compute_margin(P_e, D_e, D_r, G_e, h_e=300000, lat_e=43, lon_e=1, h_r=200, lat_r=44, lon_r=2, Bandwidth=100, freq=2.2*10** 9):
    lam = c/freq
    L_fs = compute_free_space_loss(lat_e, lon_e, h_e, lat_r, lon_r, h_r, lam)
    Gain_r = compute_gain(D_r, lam)
    l_b = compute_link(P_e, G_e, Gain_r, L_fs, Bandwidth)
    #print("margin = ", l_b - Treshold, "dB")
    return l_b - Treshold


def find_best(liste, fichier_e, fichier_r):
    best = np.max(liste)
    indice_best = np.argmax(liste)
    name_r = fichier_r['NOM'][indice_best//len(fichier_e)]
    name_e = fichier_e['Microstrip Antenna - CubeSat'][indice_best-(len(fichier_e)*(indice_best//len(fichier_e)))]
    
    print("\nBest choice is", name_r, "as ground antenna with", name_e, "on the CubeSat for a margin of", np.round(best, 3), "dB\n")


def main():
    res = []
    for i in range(len(excel_r)):
        D_r = excel_r['Diametre (m)'][i]
        for j in range (len(excel_e)):
            P_e = excel_e['Average Power (W)'][j]
            D_e = excel_e['Diametre'][j]
            G_e = excel_e['Gain'][j]
            res.append(compute_margin(P_e, D_e, D_r, G_e))
    
    print(res)
    find_best(res, excel_e, excel_r)


if __name__ == "__main__":
    excel_r = pd.read_excel("../inputs/ground_station/GroundStation.xlsx", usecols=['NOM', 'Diametre (m)']).dropna().reset_index()
    excel_e = pd.read_excel("../inputs/embeded_communication_equipement/Equipement Communication embarqué.xlsx", sheet_name='Microstrip Antenna', 
                            usecols=['Microstrip Antenna - CubeSat', 'Diametre', 'Gain', 'Average Power (W)']).dropna().reset_index()
    print(excel_r)
    print(excel_e)

    main()    