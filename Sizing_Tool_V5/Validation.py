# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:06:36 2023

@author: cdepaor
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%%
import Spacecraft_Sizing_Tool as SST
#%%IMPORT SMAD Validation Case
val_cas = pd.read_csv(r"Val_case_2_SMAD.csv")
#%% function to format the data
def val_formater(budget):
    budget_array = budget 
    val_array = pd.DataFrame([[budget_array[0,0], float(budget_array[0,1]) + float(budget_array[4,1])], #Communications + OBDH
                          [budget_array[1,0], float(budget_array[1,1])], #payload
                          [budget_array[2,0], float(budget_array[2,1])], #propulsion
                          [budget_array[5,0], float(budget_array[5,1])], #Power
                          [budget_array[6,0], float(budget_array[6,1]) + float(budget_array[4,1])], #AOCS + GNC
                          [budget_array[7,0], float(budget_array[7,1])], #Thermal
                          [budget_array[8,0], float(budget_array[8,1])]]) #Structure
    
    return val_array


#%% parses the mass_budget output by the Space_craft_sizing tool and puts it 
    #beside the SMAD validation data
def val_comparitor(alt, res, fauche, ddv, ppo):
    mass_budget, power_budget = SST.mass_estimator(alt, res, fauche, ddv, ppo)
    mass_array = np.array(list(mass_budget.items()))
    val_array = val_formater(mass_array)
    val_array.ix[:,1] = 100*val_array.ix[:,1]/sum(val_array.ix[:,1])
    side_by_side = pd.DataFrame([val_cas.ix[:,1]*100, val_array.ix[:,1], val_cas.ix[:,2]*100,val_array.ix[:,1] - val_cas.ix[:,1]*100]).T
    side_by_side = side_by_side.rename(columns = {"avgs":"SMAD", 1:"Outil", 2:"standard deviation", "Unnamed 0":"delta"})
    side_by_side = side_by_side.rename(index = {0:"Communication", 
                                                1:"Payload", 
                                                2:"Propulsion",
                                                3:"Power",
                                                4:"AOCS",
                                                5:"Thermal",
                                                6:"Structure",})
    return side_by_side, mass_array
#%%
def val_explorer(POI, length):
    deltas = np.zeros([7, length])
    raw_values = np.zeros([7, length])
    k=0
    for i in np.linspace(POI-POI/10, POI+POI/10, length):
        val_matrix, mass_budget = val_comparitor(i, res, fauche, ddv, ppo)
        deltas[:, k] = (val_matrix["delta"].values)/val_matrix["stddev"].values
        raw_values[:, k] = val_formater(mass_budget).ix[:, 1]
        k=k+1
    return deltas, raw_values
#%%
def val_explorer1(POI, length):
    raw_values = np.zeros([10, length])
    k=0
    for i in np.linspace(POI-POI/10, POI+POI/10, length):
        mass_budget, power_budget = SST.mass_estimator(i, res, fauche, ddv, ppo)
        raw_values[:, k] = list(mass_budget.values())
        k=k+1
        print(k)
    return raw_values
#%%
alt = 250000 # altitude [m]
res = 1 #resolution au sol [m]
fauche = 6000 # fauche [m]
ddv = 180 # dure de vie [days]
ppo= 5 # pictures per orbit [#]


##%%
#aa, bb = val_comparitor(alt, res, fauche, ddv, ppo)
#shpa = val_formater(bb)
#%%
POI = alt
#errors, raw_values = val_explorer(POI, 100)
#%%
alt_variation = raw_values
#%%
x = np.linspace(POI-POI/5, POI+POI/5, 100)
plt.figure()
plt.plot(x, errors[0,:], label = "Communications")
plt.plot(x, errors[1,:], label = "Payload")
plt.plot(x, errors[2,:], label = "Propulsion")
plt.plot(x, errors[3,:], label = "Power")
plt.plot(x, errors[4,:], label = "AOCS")
plt.plot(x, errors[5,:], label = "Thermal")
plt.plot(x, errors[6,:], label = "Structure")
plt.title("Sizing differences normalized with respect to std dev")
plt.xlabel("photos per orbit")
plt.ylabel("standard deviation")
plt.axhline(1, color = "g", linestyle ="--", linewidth = 1)
plt.axhline(-1, color = "g", linestyle ="--", linewidth = 1)
plt.axhline(2, color = "y", linestyle ="--", linewidth = 1)
plt.axhline(-2, color = "y", linestyle ="--", linewidth = 1)
plt.axhline(3, color = "r", linestyle ="--", linewidth = 1)
plt.axhline(-3, color = "r", linestyle ="--", linewidth = 1)
plt.legend()
    
#%% Raw Value plotter
plt.figure()
plt.plot(x, raw_values[0,:], label = "Communications + OBDH")
plt.plot(x, raw_values[1,:], label = "payload")
plt.plot(x, raw_values[2,:], label = "propulsion")
plt.plot(x, raw_values[3,:], label = "power")
plt.plot(x, raw_values[4,:], label = "AOCS + GNC")
plt.plot(x, raw_values[5,:], label = "Thermal")
plt.plot(x, raw_values[6,:], label = "Structure")
plt.legend()

#%% Raw value unformatted plotter
#plt.figure()
x = np.linspace(POI-POI/10, POI+POI/10, 10)
#%%
AA = val_explorer1(POI, 10)
#%%
plt.figure()    
plt.plot(x, AA[0,:], label = "AOCS")
plt.plot(x, AA[1,:], label = "Camera")
plt.plot(x, AA[2,:], label = "Communications")
plt.plot(x, AA[3,:], label = "GNC")
plt.plot(x, AA[4,:], label = "OBDH")
plt.plot(x, AA[5,:], label = "Power")
plt.plot(x, AA[6,:], label = "Propulsion")
plt.plot(x, AA[7,:], label = "Structure")
plt.plot(x, AA[8,:], label = "ThermaL")
#plt.plot(x, AA[9,:], label = "TOTAL")
plt.legend()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    