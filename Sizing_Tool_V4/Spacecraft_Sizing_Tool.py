# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 09:41:45 2023

@author: cdepaor
"""

import numpy as np
import pandas as pd
import math as m
import matplotlib.pyplot as plt
import warnings
import scipy.optimize as sc
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

#%% Importing Databases
cameras = pd.read_csv("cameras.csv")
e_thrusters = pd.read_csv("Electric_Thrusters.csv", encoding= 'unicode_escape')
he_thrusters = pd.read_csv("Hall_Effect_Thrusters.csv")
RW = pd.read_csv("Reaction_Wheels.csv")
ST = pd.read_csv("Star_Trackers.csv")
CPUs = pd.read_csv("OBDH.csv")
db_GNC = pd.read_csv("GNC_modules.csv", encoding = 'unicode_escape')
Transmitters = pd.read_csv("Transmitters.csv")
Gyroscopes = pd.read_csv("Gyroscopes.csv")
dbSS = pd.read_csv("Sunsensors.csv")

#%% Plotting functions

## Log plotting ##
def logplot(x, y, xlabel, ylabel, title): #just like SMAD fidure 13.5
    fig, ax = plt.subplots()
    ax.loglog(x, y)
    ax.set_xticks([10E-1, 10E0, 10E1, 10E2, 10E3, 10E4, 10E5, 10E6, 10E7, 10E8, 10E9, 10E10])
    ax.set_xlim([10**(0), 10**(10)])
    ax.set_ylim([10**(-2), 10**(5)])
    ax.grid(True, which = "both", axis="both")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid()
    
### plotting one line ###
def plot(x, y, xlabel, ylabel, handle, title): 
    plt.figure()
    plt.plot(x, y, label = handle)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

### plotting 2 lines ###    
def plot2(x, y1, y2, xlabel, ylabel, handle1, handle2, title):
    plt.figure()
    plt.plot(x, y1, label = handle1)
    plt.plot(x, y2, label = handle2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    
#%% Regression functions
def linear_reg(x, y, intercept):
    curve = np.polyfit(x, y, 1)
    m = curve[0]
    if intercept == 0: 
        c = intercept
    else:
        c = curve[1]
    def y_out(x_in, m):
        return x_in*m + c
#    print(curve)
    adj = m/100
    ers = []
    R2s = []
    ms = []
    for i in range(0, 30):
        m_adj = (m*0.85)+adj*i
        ms.append(m_adj)
        k=0
        Errors2 = 0
        sos = 0
        for i in x:
            Errors2 = Errors2 + (y_out(i, m_adj) - y[k])**2
            sos = sos + (y_out(i, m_adj) - np.mean(y))**2
            R2 = 1 - Errors2/sos
            k=k+1
        ers.append(Errors2)
        R2s.append(R2)
    q = np.argmin(ers)
    R_squared = max(R2s)
    m_q = (m*0.85)+adj*q
    
    
    return m_q, c, R_squared # returns the slope of the line, the y-intercept and the R2
#%%
def polynomial_reg(x, y, intercept):
    curve = np.polyfit(x, y, 2)
    m = curve[0]
    if intercept == 0: 
        c = intercept
    else:
        c = curve[1]
    def y_out(x_in, m):
        return x_in*m + c
    
    adj = m/100
    ers = []
    R2s = []
    ms = []
    for i in range(0, 30):
        m_adj = (m*0.85)+adj*i
        ms.append(m_adj)
        k=0
        Errors2 = 0
        sos = 0
        for i in x:
            Errors2 = Errors2 + (y_out(i, m_adj) - y[k])**2
            sos = sos + (y_out(i, m_adj) - np.mean(y))**2
            R2 = 1 - Errors2/sos
            k=k+1
        ers.append(Errors2)
        R2s.append(R2)
    q = np.argmin(ers)
    R_squared = max(R2s)
    m_q = (m*0.85)+adj*q
    
    
    return m_q, c, R_squared # returns the coefficient of  x2 ,the y-intercept, and the R2

#%% polynomial_reg test
#x = np.array(cameras["mass (kg)"])
#y = np.array(cameras["alt/gsd"])
#coeffs = np.polyfit(y, x, 2)
#x_gven = np.linspace(0,max(y), 15)
#y_pred = (x_gven**2)*coeffs[0]+x_gven*coeffs[1]+coeffs[2]
#plt.figure()
#plt.scatter(y, x)
#plt.plot(x_gven, y_pred)
#

#%%
def exp_reg(x, y):
    var = 0
    x_pred = np.linspace(0,800000, len(y))
    var = np.linspace(2E-6,8E-6, 30)
    ers = []
    R2s = []
    def y_out(x_in, var):
        return 1.5*np.e**(var*x_in)
    for i in var:
        k=0
        Errors2=0
        sos = 0
#        print("bla")
        for j in x_pred:
            Errors2 = Errors2 + (y_out(j, i) - y[k])**2
            sos = sos + (y_out(j, i) - np.mean(y))**2
            R2 = 1 - Errors2/sos
            k=k+1
        ers.append(Errors2)
        R2s.append(R2)
    q = np.argmin(ers)
#    print(R2s)
    le_bon_R2 = max(R2s)
    le_bon_var = var[q]
    guess = 4E-6
#    plt.figure()
#    plt.xlim(0, 800000)
#    plt.ylim(0, 50)
#    plt.plot(x_pred, y_out(x_pred, guess), label = "{0}".format(le_bon_R2))
#    plt.scatter(x, y)
#    plt.legend()
    
    return le_bon_var, le_bon_R2
#    return q
    
#%% scipyfit
def func(x, A, B):
        y = A*x**2+B*x
        return y
    
def scifit(X, Y):
    parameters, covariance = sc.curve_fit(func, X, Y)
    return parameters, covariance

#%% half power beamwidth
def HPBW(gain):
    return 70/gain
#%%
AA = []
gains = range(1,100)
for i in gains:
    AA.append(HPBW(i))

#%%
def Rho(alt):
    return 1000*(5887.705297*alt**(-7.016396641)) #grace a Charles BST SSR V01
    

molars = {
        "Xenon": 0.13125, # molar masses of different fuels
        "Krypton": 0.083798}
#%%
def m_camera(alt, res):
    coeff, intercept, R2 = polynomial_reg(cameras["alt/gsd"], cameras["mass (kg)"], 0)
    m_camera = (1/2.314)*coeff*(alt/res)**2
    return np.round(m_camera, 3)
#%%
m_camera(250000, 1)
#%%
def p_camera(alt, res):
    k=0
    candidates_m = []
    candidates_p = []
    for i in cameras["alt/gsd"]:
        if i >= 250000:
            candidates_m.append(cameras["mass (kg)"][k])
            candidates_p.append(cameras["power (W)"][k])
        k=k+1
    
    return np.round(candidates_p[np.argmin(candidates_m)], 3)
#%%
p_camera(250000, 1)
#%%    
def m_propulsion(alt, lifetime):
    Isp = 3241
    fuel = "Xenon"
    V = 7550
    S = 0.1*0.1
    Cd = 1.08
    rho = Rho(alt/1000)
    drag = 0.5*rho*V**2*S*Cd
    
    coeff1 = 1378.6251095743646
    coeff2 = 1.507462522088801
    m_thruster = coeff1*drag + coeff2
        
    m_prop = drag/(9.81*Isp)*(lifetime*24*60*60)
    R_spec = 8.314/molars[fuel]
    T = 293 #Kelvin
    P = 100E+5 #Pa
    prop_volume = m_prop*R_spec*T/P
    outer_volume = prop_volume*1.3221
    m_tanks = 0.0063*(P/1E5)*(prop_volume*1000)

    estimate = m_thruster + m_tanks
    return np.round(estimate, 3)

#%% 
m_propulsion(250000, 180)
#%%    
def p_propulsion(alt, lifetime):
    x_var = e_thrusters["thrust (N)"]
    y_var = e_thrusters["power (W)"]
    ms, c, R2s = linear_reg(x_var, y_var, 1)
    
    V = 7550
    S = 0.1*0.1
    Cd = 1.08
    rho = Rho(alt/1000)
    drag = 0.5*rho*V**2*S*Cd
    thrust_req = drag
    p_req = thrust_req*ms+c
    
    return np.round(p_req, 3)

#%%
p_propulsion(250000, 180)      
#%%
def m_GNC():
    m_GNC = np.min(db_GNC["mass (kg)"])
    return np.round(m_GNC, 3)
#%%
#m_GNC()
    
#%%
def p_GNC():
    return np.round(db_GNC["power (W)"][np.argmin(db_GNC["mass (kg)"])], 3)
#%%
#p_GNC()
#%%
def m_OBDH(res, fauche, pictures_per_orbit):
    photo_size = (fauche/res)*(fauche/res)*24
    dataload_per_orbit = pictures_per_orbit*photo_size/1E9 #Gigabits
    sumass=0
    count = 0
    k=0
    for i in CPUs["storage (GB)"]:
        if i > dataload_per_orbit/8:
            sumass = sumass + CPUs.iloc[k, 1]
            count = count+1
        k=k+1
        
    avg_mass = sumass/count
    return np.round(avg_mass, 3)

#%%
#m_OBDH(1, 6000, 5) 
#%%
def p_OBDH(res, fauche):
    slope, intercept, R = linear_reg(CPUs["mass (kg)"][:-1], CPUs["power (W)"][:-1], 1) #finding sizing rule
    mass_OBDH = m_OBDH(1, 6000, 5)
    
    p_OBDH = mass_OBDH*slope + intercept
    return np.round(p_OBDH, 3)
#%%
#p_OBDH(1, 6000)
#%%
def p_comms(alt, res, fauche, pictures_per_orbit):
#    alt = alt/1000
    photo_size = (fauche/res)*(fauche/res)*24 # 24 bits/pixel
    ROIM_data = pictures_per_orbit*photo_size #assuming 24-bit imagery

    ### ALternative parametric method using a Link budget equation
    EbNo = 12.6 #[dB] typical minimum signal to noise ratio.
    L_l = 0 #line loss [dB]
    L_a = 0 #atmospheric loss [dB], ~0 of we use S-band
    freq = 2.17E9 #S-band goes from 2-4GHz
    c = 299458792 #speed of light [m/s]
    lam = c/freq #wavelength [m]
    d=np.sqrt((6371000+alt)**2 - 6371000**2) #distance to reciever [m]
    L_s = 10*np.log10((lam/(4*np.pi*d))**2)
    G_t = 19.35 #transmitter gain [dB] independant variable
    eta = 0.55 #reciever efficiency (typical)
    r = 2#antenna radius
    A = np.pi*r**2 # reciever area (effective)
    G_r = 10*np.log10((4*np.pi*eta*A)/lam**2) #reciever gain [dB]
    k = 10*np.log10(1.380E-23) #Boltzmann constant [J/K]
    T_s = 10*np.log10(135) #link noise temperature [K] 100k seems to be a typical value but need calculation
    R = 10*np.log10(ROIM_data) #datarate [dBMbits/s]
    p_req_dBW = EbNo - L_l - L_a - L_s - G_t - G_r + k + T_s + R #[dBW]
    equation = {"line loss           [dB]     ":np.round(L_l, 2),
                "atmo loss           [dB]     ":np.round(L_a, 2),
                "freespace loss      [dB]     ":np.round(L_s, 2),
                "transmitter gain    [dB]     ":np.round(G_t, 2),
                "reciever gain       [dB]     ":np.round(G_r, 2),
                "Botlzmann constant  [dB(J/K)]":np.round(k, 2),
                "Noise temperature   [dBK]    ":np.round(T_s, 2),
                "datarate            [dB(bps)]":np.round(R, 2)}
    
    p_req = 10**(p_req_dBW/10)
    return np.round(p_req, 3)
#%%
#p_comms(250000, 1, 6000, 5)
#%%
def m_comms(alt, res, fauche, pictures_per_orbit):
    k=0
    candidates = []
    p_req = p_comms(alt, res, fauche, pictures_per_orbit)
    
    for i in Transmitters["power"]:
        if i >= p_req:
            candidates.append(Transmitters["mass"][k])
        k=k+1
        
    return np.round(min(candidates), 3) # pick the minimum transmitter which meets the reqs

#%%
#m_comms(250000, 1, 6000, 5)  
#%% 
def m_thermal(total_mass, total_power):
    
    m_thermal_prime = 0.00832*total_power #from the SMAD
    return np.round(m_thermal_prime, 3)


#%%
#m_thermal(18, 191)
#%%
def m_AOCS(alt, res, total_mass, fauche):
    stability_req = 0.2*np.arctan((0.5*fauche)/(alt))*3600
    dbST = pd.read_csv("Star_Trackers.csv")
    k=0
    j = 1
    mass = 0
    for i in dbST["arcsec"]:
        if i < stability_req:
            mass = mass + dbST.iloc[k, 3]            
            j=j+1
        k=k+1    
    avgmass = mass/j
    
    m_ST = avgmass
    m_SS = np.mean(dbSS["mass (kg)"]) #all sunsensors very small and the same weight
    m_Gyro = min(Gyroscopes["mass (kg)"]) #no particular ARW requirement known, so we take the min
    
    ### Sizing Reaction Wheels sizing case: antenna pointing speed.
    x = np.linspace(-1000000, +1000000, 100)
    V = np.sqrt(3.986E5/(6371+alt/1000))
    slew_rate_for_antenna_pointing = (V/(alt/1000+((x**2)/alt/1000)))*180/(np.pi) # from geometry derivitive of arctan(alt/x)
    req_slew_rate = max(slew_rate_for_antenna_pointing)
    req_ang_acc = req_slew_rate/2
    
    I = (1/12)*total_mass*0.6**2## moment of inertia for a long rod of uniform density
    T_req = I*(req_ang_acc/180)*np.pi
    p_req = 125.63*T_req + 1.0205 #from Reaction Wheels.xlsx
    m_RW = p_req*0.1868 #from Reaction Wheels.xlsx

    
    Sensors_mass = m_ST + m_SS + m_Gyro + m_RW
    return np.round(Sensors_mass, 3)
#%%
m_AOCS(250000,1,18,6000)

#%% Structure
def m_str(total_mass):
    
    m_str = 0.217*total_mass #from the SMAD
    return np.round(m_str, 3)
    
#%%    
m_str(20)
#%%
def p_AOCS(alt, res, total_mass, fauche):
    stability_req = 0.2*np.arctan((0.5*fauche)/(alt))*3600 # pointing acc of camera
    k=0
    j = 1
    power = 0
    for i in ST["arcsec"]:
        if i < stability_req:
            power = power + ST.iloc[k, 4]            
            j=j+1
        k=k+1    
    avgpower = power/j
    p_ST = avgpower
    
    p_SS = 0 # sunsensors can be passive. photocell outputs current for light
    
    p_Gyro = Gyroscopes["power (W)"][np.argmin(Gyroscopes["mass (kg)"])]
    
    x = np.linspace(-1000000, +1000000, 100) # ground-track range from ground station
    V = np.sqrt(3.986E5/(6371+alt/1000)) #flight speed of s/c
    slew_rate_for_antenna_pointing = (V/(alt/1000+((x**2)/alt/1000)))*180/(np.pi) # from geometry derivitive of arctan(alt/x)
    req_slew_rate = max(slew_rate_for_antenna_pointing)
    req_ang_acc = req_slew_rate/2
    I = (1/12)*total_mass*0.6**2## moment of inertia for a long rod of uniform density
    T_req = I*(req_ang_acc/180)*np.pi
    p_RW = 125.63*T_req + 1.0205 #from Reaction Wheels.xlsx

    p_AOCS = p_ST + p_SS + p_Gyro + p_RW
    return np.round(p_AOCS, 3)
#%%
p_AOCS(250000, 1, 20, 6000)
#%%
def m_power(alt, total_power, return_mp):
    v_req = 28
    p_req = total_power
#    print("p_req is of type:", type(p_req), p_req)
    ###############Mainsail##################
    cell_size = 30.15 #cm2
    cell_mass = 0.00268 #kg
    cell_fill_factor = 0.8 
    cell_voltage = 2.32 #V
    cell_ampage = 0.473 #A
    
    c_series = m.ceil(v_req/cell_voltage)
    c_parallel = m.ceil((p_req/v_req)/cell_ampage)
    total_cells = c_parallel*c_series 
    mainsail_mass = total_cells*cell_mass
    mainsail_area = total_cells*cell_size/cell_fill_factor
    ##############Battery##################
    eclipse_time = 2*np.arcsin(6371/(alt/1000+6371))*np.sqrt(((alt/1000+6371)**3)/3.98610E5)/60/60
    orbital_period = 2*np.pi*np.sqrt(((alt/1000+6371)**3)/3.98610E5)/60/60
    energy_req = p_req*eclipse_time
    
    bcell_mass = 1.13 #kg
    bcell_volume = 0.551 #U
    bcell_voltage = 4 #V
    bcell_ampage = 45 #Ah
    discharge_limit = 0.8
    
    bc_series = m.ceil(v_req/bcell_voltage)
    bc_parallel = m.ceil((p_req/v_req)/bcell_ampage)
    charge_req = (energy_req/v_req)/0.8 #Ah
    
    total_cells = bc_parallel*bc_series
    battery_mass = total_cells*bcell_mass
#    print(battery_mass)
#    print(charge_req)
    battery_volume = total_cells*bcell_volume
    ####################chargesail#####################
    charge_time = orbital_period - eclipse_time
    charging_voltage = 28
    charge_current = charge_req/charge_time #Amps
    charging_power = charge_current*charging_voltage
    
    cc_series = m.ceil(charging_voltage/cell_voltage)
    cc_parallel = m.ceil((charge_current/cell_ampage))
    total_charge_cells = cc_parallel*cc_series
    chargesail_mass = total_charge_cells*cell_mass
    chargesail_area = total_charge_cells*cell_size/cell_fill_factor

    p_mass = mainsail_mass + battery_mass + chargesail_mass
    
    if return_mp == 0:
        return np.round(p_mass, 3)
    elif return_mp == 1:
        return np.round(charging_power, 3)
    
    
#%%
m_power(250000,191, 1)
#%% Iterative mass section
def iterator(alt, res, fauche, lifetime, pictures_per_orbit, mass_guess_factor):
    ## Bottom up sizing ##
    mass_comms = m_comms(alt, res, fauche, pictures_per_orbit)
    mass_camera = m_camera(alt, res)
    mass_propulsion = m_propulsion(alt, lifetime)
    mass_GNC = m_GNC()
    mass_OBDH = m_OBDH(res, fauche, pictures_per_orbit) 
    ## Guessing the total mass ##
    partial_mass = mass_comms + mass_camera + mass_propulsion + mass_GNC + mass_OBDH    
    guess_mass = partial_mass/mass_guess_factor
    
    ## top down sizing EXCEPT power ##
    
    mass_AOCS = m_AOCS(alt,res,guess_mass,fauche)
    mass_structure = m_str(guess_mass)

    ## power sizing ##
    power_comms = p_comms(alt, res, fauche, pictures_per_orbit)
    power_camera = p_camera(alt, res)
    power_propulsion = p_propulsion(alt, lifetime)   
    power_GNC = p_GNC()
    power_OBDH = p_OBDH(res, fauche)
    power_AOCS = p_AOCS(alt, res, guess_mass, fauche)
    power_thermal = 0
    power_structure = 0
    
    ## sizing mass of the power ss ##
    partial_power = power_comms + power_camera + power_propulsion + power_GNC + power_AOCS + power_OBDH + power_thermal + power_structure
    charging_power = m_power(alt, partial_power, 1)
    mass_power = m_power(alt,partial_power, 0)
    
    total_power = partial_power + charging_power # this is the total peak power the panels are providing
    mass_thermal = m_thermal(guess_mass, total_power) # mass of thermal system is sized using power
    
    total_mass = np.round(mass_structure + mass_comms + mass_camera + 
                          mass_propulsion + mass_GNC + mass_OBDH + 
                          mass_power + mass_AOCS + mass_thermal, 3)
    m_error = total_mass - guess_mass
    
    
    mass_breakdown = {"Communications[kg]" :mass_comms,
                      "Camera        [kg]" :mass_camera,
                      "Propulsion    [kg]" :mass_propulsion,
                      "GNC           [kg]" :mass_GNC,
                      "OBDH          [kg]" :mass_OBDH,
                      "Power         [kg]" :mass_power,
                      "AOCS          [kg]" :mass_AOCS,
                      "Thermal       [kg]" :mass_thermal, 
                      "Structure     [kg]" :mass_structure,
                      "total         [kg]" :total_mass}
    
    
    power_breakdown = {"Communications[W]" :power_comms,
                      "Camera        [W]" :power_camera,
                      "Propulsion    [W]" :power_propulsion,
                      "GNC           [W]" :power_GNC,
                      "OBDH          [W]" :power_OBDH,
                      "Power         [W]" :charging_power,
                      "AOCS          [W]" :power_AOCS,
                      "Thermal       [W]" :power_thermal, 
                      "Structure     [W]" :power_structure,
                      "total         [W]" :total_power}
    
   
    
    return np.round(guess_mass, 3), np.round(total_mass, 3), np.round(m_error, 3), mass_breakdown, np.round(total_power, 3), np.round(charging_power, 3), power_breakdown
#%%
iterator(250000, 1, 6000, 180, 5, 0.49)

#%%
def mass_estimator(alt, res, fauche, lifetime, pictures_per_orbit):
    mass_guess_factors = np.linspace(0.2, 0.95, 50)

    guess_masses = np.zeros(50)
    total_masses = np.zeros(50)
    m_errors = np.zeros(50)
    
    k=0    
    for i in mass_guess_factors: 
        guess_masses[k], total_masses[k], m_errors[k], m_budget, total_power, p_charging, p_budget = iterator(alt, res, fauche, lifetime, pictures_per_orbit, i)
        if  -1 < m_errors[k] < 1:
            the_good_m_budget = m_budget
            the_good_p_budget = p_budget
        k=k+1


    return the_good_m_budget, the_good_p_budget

    
#%%
mass_budget, power_budget = mass_estimator(250000, 1, 6000, 180, 5) #(alt, res, fauche, durée de vie, photos per orbit)





















