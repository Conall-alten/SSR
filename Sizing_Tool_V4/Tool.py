# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:57:17 2023

@author: cdepaor
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math as m
#%%Databases
cameras = pd.read_csv("cameras.csv")
e_thrusters = pd.read_csv("Electric_Thrusters.csv", encoding= 'unicode_escape')
he_thrusters = pd.read_csv("Hall_Effect_Thrusters.csv")
RW = pd.read_csv("Reaction_Wheels.csv")
ST = pd.read_csv("Star_Trackers.csv")
CPUs = pd.read_csv("OBCs.csv")
#%% Atmospheres

Rho_alt = {
  150000: 2E-9, 
  200000: 5E-10,
  250000: 2E-10, 
  300000: 8E-11,
  350000: 4E-11,
  400000: 2E-11
}

#%% molar masses
molars = {
        "Xenon": 0.13125,
        "Krypton": 0.083798}
#%% pltting function
def plot(name, x, y, x_in, y_out, R2, xlabel, ylabel):
    plt.figure()
    plt.scatter(x, y, label = "data")
    plt.plot(x_in, y_out, color = "r", label = "model")
    plt.plot(0,0, color = "white", label = "R2 = {}".format(R2))
    plt.title(name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    
    

#%%
def cam_mass_rule(alt, res): #(meters, meters)
    x = cameras["alt/gsd"]
    y = cameras["mass (kg)"]
    deg = 2
    
    ###
    x_in = np.linspace(0, max(x), max(x)) #creating input array for predictor
    z = np.polyfit(x, y, deg)             #the regression algo. returns polynomial coeffs
    y_out = np.zeros(max(x))              #creating the output array for predictor
    j = z[0]/100                           #adjustement increment
    t=1
    p = 1
    c = 0
    Error2 = [1000000, 100000]            #init. of sum of residual error squared array
    while Error2[p] < Error2[p-1]:
        for i in range(0,max(x)):         #loop for adjusting the coefficient returned by polyfit
            adjust = t*j              
            coeff = (z[0]-adjust)         #adjusting the coefficient
            y_out[i] = coeff*x_in[i]**deg #The predictor
        k=0       
        er = 0
        for i in x-1:
            er = er + (y_out[i]- y[k])**2 #calculating sum of residuals squared
            k=k+1
        Error2.append(er)
        p=p+1
        c = c+1
        t = t+1
    
    sos = 0
    for i in x-1:
        sos = sos + (y_out[i] - np.mean(y))**2      #sum of the squares
    R2 = 1 - er/sos                  
    ###
    
    x1 = alt/res
    estimate =  coeff*x1**2
#    
    #plotting the adjusted curves
    plot("cam_mass_rule", x, y, x_in, y_out, np.round(R2, 2), "alt/GSD", "mass (kg)")
    return estimate, R2

def cam_power_rule(alt, res): #(meters, meters)
    
    x = cameras["alt/gsd"]
    y = cameras["power (W)"]
    deg = 1
    
    ###
    x_in = np.linspace(0, max(x), max(x)) #creating input array for predictor
    z = np.polyfit(x, y, deg)             #the regression algo. returns polynomial coeffs
    y_out = np.zeros(max(x))              #creating the output array for predictor
    
    j = z[0]/100                            #adjustement increment
    t=1
    p = 1
    c = 0
    Error2 = [1000000, 100000]            #init. of sum of residual error squared array
    while Error2[p] < Error2[p-1]:
        for i in range(0,max(x)):         #loop for adjusting the coefficient returned by polyfit
            adjust = t*j              
            coeff = (z[0]-adjust)         #adjusting the coefficient
            y_out[i] = coeff*x_in[i]**deg #The predictor
        k=0       
        er = 0
        for i in x-1:
            er = er + (y_out[i]- y[k])**2 #calculating sum of residuals squared
            k=k+1
        Error2.append(er)
        p=p+1
        c = c+1
        t = t+1
      
    sos = 0
    for i in x-1:
        sos = sos + (y_out[i] - np.mean(y))**2      #sum of the squares
    R2 = 1 - er/sos  
    ###
    
    x1 = alt/res
    estimate = coeff*x1
    plot("cam_power_rule", x, y, x_in, y_out, R2, "alt/GSD", "power (W)") #plotting the adjusted curves
    return estimate, R2

def e_thruster_mass_rule(alt): #(meters)
    V = 7550
    S = 0.1*0.1
    Cd = 1.08
    Rho = Rho_alt[alt]
    drag = 0.5*Rho*V**2*S*Cd
    
    x = e_thrusters["thrust (N)"]
    y = e_thrusters["mass (kg)"]
    deg=1
    ###
    
    x_in = x #creating input array for predictor
    z = np.polyfit(x, y, deg)             #the regression algo. returns polynomial coeffs
    y_out = np.zeros(len(x))              #creating the output array for predictor
   
    j = z[0]/100                            #adjustement increment
    t=1
    p = 1
    c = 0
    Error2 = [1000000, 100000]            #init. of sum of residual error squared array
    while Error2[p] < Error2[p-1]:
        for i in range(0,len(x)):         #loop for adjusting the coefficient returned by polyfit
            adjust = t*j              
            coeff = (z[0]-adjust)         #adjusting the coefficient
            y_out[i] = coeff*x_in[i]**deg #The predictor
        k=0       
        er = 0
        for i in range(0,len(x)):
            er = er + (y_out[i]- y[i])**2 #calculating sum of residuals squared
            k=k+1
        Error2.append(er)
        p=p+1
        c = c+1
        t = t+1
      #plotting the adjusted curves
    sos = 0
    for i in range(0,len(x)):
        sos = sos + (y_out[i] - np.mean(y))**2      #sum of the squares
    R2 = 1 - er/sos  
    plot("electric thruster mass rule", x, y, x_in, y_out, R2, "thrust", "mass")
    ####
    estimate = coeff*drag
    return estimate, R2
    
def prop_mass_rule(alt, lifetime, Isp, fuel): #(meters, days, seconds)
    V = 7550
    S = 0.1*0.1
    Cd = 1.08
    Rho = Rho_alt[alt]
    drag = 0.5*Rho*(V**2)*S*Cd
    m_dot = drag/(9.81*Isp) # from the thrust equation F = go*Isp*m_dot
    m_prop = m_dot*(lifetime*24*60*60)
    R_spec = 8.314/molars[fuel] #for ideal gas law
    T = 293 #Kelvin
    P = 100E+5 #Pa
    inner_volume = m_prop*R_spec*T/P #meters3
    outer_volume = inner_volume*1.3221 # citation needed
    tank_dry_mass = 0.0063*(P/1E5)*(inner_volume*1000) # source: Equipment Propulsion. R2 = 0.8688
    return m_prop, tank_dry_mass


def OBDH():
    mass = np.mean(CPUs["mass"]) #mean from satcatalog smallsats
    return mass
    
def power(alt, p_req, v_req):
    #mainsail siszing
    cell_size = 30.15
    cell_mass = 0.00268
    cell_fill_factor = 0.8
    cell_voltage = 2.32
    cell_ampage = 0.473
    
    c_series = m.ceil(28/2.32)
    c_parallel = (p_req/v_req)/cell_ampage
    total_cells = c_parallel*c_series 
    mainsail_mass = total_cells*cell_mass
    mainsail_area = total_cells*cell_size/0.8
    
    #battery sizing
    eclipse_time = np.arcsin(6371/(alt+6371))*np.sqrt(((alt+6371)**3)/3.98610E5)/60/60
    orbital_period = 2*np.pi*np.sqrt(((alt+6371)**3)/3.98610E5)/60/60
    energy_req = p_req*eclipse_time
    
    
    
#%% Calling
    
#cam_mass_rule(250000, 1)
#cam_power_rule(250000, 1)
#e_thruster_mass_rule(250000)
prop_mass_rule(250000, 180, np.mean(e_thrusters["isp (s)"]), "Xenon")










