
import tkinter as tk
from tkinter import ttk
import Spacecraft_Sizing_Tool as SST
import numpy as np

#%%  setting up GUI
def process_input():
    input_text = [input_boxes[i].get("1.0", "end-1c") for i in range(5)]
    alt = float(input_text[0]) * 1000
    res = float(input_text[1])
    fauche = float(input_text[2])
    ddv = float(input_text[3])
    ppo = float(input_text[4])

    # Perform mass sizing
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

    # Perform power sizing
    ptotal = np.round(power_budget["total         [W]"], 3)
    pAOCS = power_budget["AOCS          [W]"] 
    ppayload = power_budget["Camera        [W]"]
    pcomms = power_budget["Communications[W]"]
    pGNC = power_budget["GNC           [W]"]
    pOBDH = power_budget["OBDH          [W]"]
    pPower = power_budget["Power         [W]"]
    pPropulsion = power_budget["Propulsion    [W]"]
    pStructure = power_budget["Structure     [W]"]
    pThermal = power_budget["Thermal       [W]"]

    #output array
    output_text = [mtotal, mAOCS, mpayload, mcomms, mGNC, mOBDH, mPower, mPropulsion, mStructure, mThermal,
                   ptotal, pAOCS, ppayload, pcomms, pGNC, pOBDH, pPower, pPropulsion, pStructure, pThermal]

    #Putting the outputs to the boxes in the GUI
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
    row_index = i % 10 * 2
    col_index = i // 10 * 2 + 12
    tk.Label(root, text=output_titles[i]).grid(row=row_index, column=col_index, padx=5, pady=5, sticky= "W")
    output_box = tk.Text(root, height=2, width=15)
    output_box.grid(row=row_index + 1, column=col_index, columnspan=2, padx=5, pady=5, sticky= "W")
    output_boxes.append(output_box)

# Additional text labels in dark grey beside the input boxes
additional_text_1 = tk.Label(root, text="Baseline: [250] -  Range: [100, 1610]", fg="grey")
additional_text_2 = tk.Label(root, text="Baseline: [1] -    Range: [0.36, 1.65]", fg="grey")
additional_text_3 = tk.Label(root, text="Baseline: [6000] - Range: [1, 16700]", fg="grey")
additional_text_4 = tk.Label(root, text="Baseline: [180] -  Range: [0, 998,000]", fg="grey")
additional_text_5 = tk.Label(root, text="Baseline: [5] -    Range: [1, 38]", fg="grey")

additional_text_1.grid(row=0, column=7, padx=220, pady=5, sticky="w")
additional_text_2.grid(row=1, column=7, padx=220, pady=5, sticky="w")
additional_text_3.grid(row=2, column=7, padx=220, pady=5, sticky="w")
additional_text_4.grid(row=3, column=7, padx=220, pady=5, sticky="w")
additional_text_5.grid(row=4, column=7, padx=220, pady=5, sticky="w")

root.mainloop()
