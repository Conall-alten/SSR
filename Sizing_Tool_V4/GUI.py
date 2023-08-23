# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:41:34 2023

@author: cdepaor
"""

import tkinter as tk
import Spacecraft_Sizing_Tool as SST

#%%

import tkinter as tk

def process_input():
    input_text = [input_boxes[i].get("1.0", "end-1c") for i in range(5)]
    alt = float(input_text[0])*1000
    res = float(input_text[1])
    fauche = float(input_text[2])
    ddv = float(input_text[3])
    ppo = float(input_text[4])

    # Perform some processing using the input_text variables
    mass_budget, power_budget = SST.mass_estimator(alt, res, fauche, ddv, ppo)
    mtotal = mass_budget["total         [kg]"]
    mAOCS = mass_budget["AOCS          [kg]"] 
    mpayload = mass_budget["Camera        [kg]"]
    mcomms = mass_budget["Communications[kg]"]
    mGNC = mass_budget["GNC           [kg]"]
    mOBDH = mass_budget["OBDH          [kg]"]
    mPower = mass_budget["Power         [kg]"]
    mPropulsion = mass_budget["Propulsion    [kg]"]
    mStructure = mass_budget["Structure     [kg]"]
    mThermal = mass_budget["Thermal       [kg]"]

    ptotal = power_budget["total         [W]"]
    pAOCS = power_budget["AOCS          [W]"] 
    ppayload = power_budget["Camera        [W]"]
    pcomms = power_budget["Communications[W]"]
    pGNC = power_budget["GNC           [W]"]
    pOBDH = power_budget["OBDH          [W]"]
    pPower = power_budget["Power         [W]"]
    pPropulsion = power_budget["Propulsion    [W]"]
    pStructure = power_budget["Structure     [W]"]
    pThermal = power_budget["Thermal       [W]"]

    output_text = [mtotal, mAOCS, mpayload, mcomms, mGNC, mOBDH, mPower, mPropulsion, mStructure, mThermal,
                   ptotal, pAOCS, ppayload, pcomms, pGNC, pOBDH, pPower, pPropulsion, pStructure, pThermal]

    for i in range(20):
        output_boxes[i].delete("1.0", "end")
        output_boxes[i].insert("1.0", output_text[i])

root = tk.Tk()
root.title("Advanced User Interface")

# Titles for input and output boxes
input_titles = ["Altitude [km]:", "resolution [m]:", "fauchée [m]:", "Durée de Vie [jours]:", "Pictures Per Orbit [#]:"]
output_titles = ["Total Mass [kg]","AOCS [kg]","payload [kg]","Comms [kg]","GNC [kg]","OBDH [kg]","Power [kg]","Propulsion [kg]","Structure [kg]","Thermal [kg]",
                 "Total Power [W]","AOCS [W]","payload [W]","Comms [W]","GNC [W]","OBDH [W]","Power [W]","Propulsion [W]","Structure [W]","Thermal [W]"]

# Input boxes
input_boxes = []
for i in range(5):
    
    tk.Label(root, text=input_titles[i]).grid(row=i, column=0, padx=5, pady=5)
    input_box = tk.Text(root, height=2, width=20)
    input_box.grid(row=i, column=1, columnspan=8, padx=5, pady=5, sticky="w")
    input_boxes.append(input_box)

# Button
process_button = tk.Button(root, text="Calculate", command=process_input)
process_button.grid(row=5, column=0, columnspan=10, padx=5, pady=10, sticky="n")

# Output boxes
output_boxes = []
for i in range(20):
    tk.Label(root, text=output_titles[i]).grid(row=6 + i // 10 * 2, column=i % 10 * 2, padx=5, pady=5)
    output_box = tk.Text(root, height=2, width=15)
    output_box.grid(row=7 + i // 10 * 2, column=i % 10 * 2, columnspan=2, padx=5, pady=5, sticky="w")
    output_boxes.append(output_box)

root.mainloop()


















