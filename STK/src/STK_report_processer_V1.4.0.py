# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 17:12:47 2023

@author: DECLINE
"""

import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..',)
sys.path.append(mymodule_dir)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

from src.constellation import Constellation
from src.process.stk_process_access_sensors import process_access_sensors
from src.process.stk_process_fom_point import process_fom_point
from src.process.stk_process_region import process_region
from src.process.stk_process_access_ground import process_access_ground

path_user = os.path.dirname(__file__)+'/../'
# Ferme toutes les fenêtres
plt.close('all')

#%% Paramétrage

# Paramètres de la constellation 1
const1 = Constellation(
    name = "RCO",
    nsat = 2,
    nplan = 4,
    inc = "50",
    alt = 260,
    res = 2.0,
    ips = 0,
    added = ""
)

const2 = Constellation(
    name = None,
    nsat = 2,
    nplan = 15,
    inc = "90",
    alt = 300,
    res = 1.6,
    ips = 0,
    added = ""
)

# Type de cible considérée
folder1 = "target_primary"
# folder1 = "global"
# folder1 = "files_points"
# folder1 = "target_secondary"
# folder1 = "general_shapes"

# Type de rapport à importer
# folder2 = "FoM_points"
folder2 = "region"
# folder2 = "access_sensors"
# folder2 = "access_ground"

folder3 = ""

path = "/".join((path_user, folder1, folder2))
print("END INIT")

#%% Type de rapport : Access AreaTarget to Satellite-Sensor or Chain
if folder2=="access_sensors":
    process_access_sensors(path, const1, const2 = None, res = [1.0, 1.2, 1.4, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0])
    
#%% Ici on s'intéresse aux rapports "Value By Grid Point", càd en tout point 
# de coordonnées (lat, long)
elif folder2=="FoM_points": # Loi des RCO
    process_fom_point(path, const1, const2 = None)

#%% Ici on s'intéresse aux reports "Stats By Region"
elif folder2=="region":
    process_region(path, const1, const2 = None, res = [1.0, 1.2, 1.4, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0])

#%% Bases au sol
elif folder2 == "access_ground":
    process_access_ground(path, name, folder3)
