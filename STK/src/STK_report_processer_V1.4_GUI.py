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
import argparse

from src.constellation import Constellation
from src.process.stk_process_access_sensors import process_access_sensors
from src.process.stk_process_fom_point import process_fom_point
from src.process.stk_process_region import process_region
from src.process.stk_process_access_ground import process_access_ground
import test_GUI_esteban as GUI

path_user = os.path.dirname(__file__)+'/../'
# Ferme toutes les fenêtres
plt.close('all')

[1.0, 1.2, 1.4, 1.6, 2.0, 2.5, 3.0, 3.5, 4.0]

def report_process(path, report_type, const1, const2, res = [], access_type = None) : 

    #%% Type de rapport : Access AreaTarget to Satellite-Sensor or Chain
    if report_type=="access_sensors":
        process_access_sensors(path, const1, const2 = const2, res = res)
        
    #%% Ici on s'intéresse aux rapports "Value By Grid Point", càd en tout point 
    # de coordonnées (lat, long)
    elif report_type=="FoM_points": # Loi des RCO
        process_fom_point(path, const1, const2 = const2)

    #%% Ici on s'intéresse aux reports "Stats By Region"
    elif report_type=="region":
        process_region(path, const1, const2 = const2, res = res)

    #%% Bases au sol
    elif report_type == "access_ground":
        process_access_ground(path, const1, access_type)

def generate_const(param_list) :
    if len(param_list)>6 :
        add1 = param_list[6]
    else :
        add1 = ""
    const = Constellation(
        param_list[0],
        int(param_list[1].split("x")[0]),
        int(param_list[1].split("x")[1]),
        param_list[2],
        int(param_list[3]),
        float(param_list[5]),
        int(param_list[4]),
        add1
    )

    return const

def no_gui(args) : 
    in_path = args.input_file.replace("\\", "/").split("/")
    filename = in_path[-1]
    report_type = in_path[-2]
    target_type = in_path[-3]
    path_start = "/".join(in_path[:-3])
    consts = [x.split("_") for x in filename[:-4].split("+")]

    const1 = generate_const(consts[0])

    const2 = None
    if len(consts)-1 :
        const1 = generate_const(consts[1])
    
    if args.absolute_path :
        path = "/".join(in_path)
    else : 
        path = "/".join((os.path.dirname(__file__), path_start, target_type, report_type))
    
    report_process(path, report_type, const1, const2,
                   res = [float(x) for x in args.res],
                   access_type = args.access_type)


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs='?', default="", help = 'The file containing the values.')
    parser.add_argument("-G", "--GUI", action = 'store_true', help = 'Start the GUI instead of looking from input from the terminal')
    parser.add_argument("-a", "--absolute_path", action = 'store_true', help = 'Indicate path is absolue instead of relative.')
    parser.add_argument("-r", "--res", default=[],  nargs='+', help = 'A list of resolution, separated by a comma without space')
    parser.add_argument("-t", "--access_type", default=None, nargs='?', const = None, choices=['link', 'duration', None], 
                                               help = 'The type of access monitored to the at file.')
    
    args = parser.parse_args(sys.argv[1:])
    
    if args.input_file: 
        no_gui(args)
    elif args.GUI:
        GUI.Report_GUI(report_process)
    else :
        print("Either a path to a file or -G is requiered to run the analysis")
    