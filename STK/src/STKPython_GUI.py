# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:56:21 2023

@author: Benjamin


The goal of this program is to autonomize the use of STK for creation of satellite constellations (adding sensors, adding ground stations) 
and calculating for example the maximum revisit time of a target area, this will greatly accelerate simulations.
This will allow a new consultant or any person on the project to quickly be able to launch simulations without intimate knowledge of the workings of STK.

-When launching this program, a GUI will appear to enter different parameters (altitude, inclination, etc.)
-By default the parameters will be filled (this is to accelerate when testing if new code is working properly).
-To add more zones of interest (currently only ConflictRostov and ConflictZone) a new .csv file need to be created with its coordinates.
-They will also need to be added as options to the dropdown menu. 
-To launch this program, STK needs to be installed, and the (currently) 2 CSV files associated to the area targets need to be present.
-These .csv files should be saved in your current directory where you're working from.
-This will also be the same directory where the .csv file with the results will be saved.
 

Future improvements:
-combine with STK processor program. This will allow us to enter the parameters, get the results AND the analysis (graphs) all in one.
-add more options for results (currently it is exporting a csv that would correspond to "value by grid point" (Lat, Long, FOM) from the report manager, but more can be addded.
-Create a new dropdown menu to select the analysis (example: -value by grid point, -value by latitude, -...)  and minimum/average/maximum revisit time instead of only maximum. 
-Save 2D and 3D image: done
-Save 2D and 3D video: done
-Add option to save image/video and add a timer for animation: done

"""
import numpy as np
import matplotlib.pyplot as plt 
import os
import win32com.client
import comtypes
from comtypes.client import CreateObject
import csv
import pandas as pd
import tkinter as tk
import time
import re
from datetime import datetime, timedelta

from tkinter import ttk
#code below indented to tkinter since we want it to launch AFTER the user clicks 'launch'

def launch_stk():
    altitude = int(altitude_entry.get())
    altitude = int(altitude) if altitude else 300
    inclination = int(inclination_entry.get())
    inclination = int(inclination) if inclination else 50
    Number_of_planes = int(planes_entry.get())
    Number_of_planes = int(Number_of_planes) if Number_of_planes else 12
    Sat_per_plane = int(sat_per_plane_entry.get())
    Sat_per_plane = int(Sat_per_plane) if Sat_per_plane else 2
    IPS = int(ips_entry.get())
    IPS = int(IPS) if IPS else 0
    resolution = float(resolution_entry.get())
    resolution = float(resolution) if resolution else 0.5
    selected_target = target_var.get()
    selected_result = result_var.get()
    start_date_str = start_date_entry.get()
    start_date_str = str(start_date_str) if start_date_str else "1 Nov 2023"
    start_time_str = start_time_entry.get()
    start_time_str = str(start_time_str) if start_time_str else "10:00:00.000"
    end_date_str = end_date_entry.get()
    end_date_str = str(end_date_str) if end_date_str else "8 Nov 2023"
    end_time_str = end_time_entry.get()
    end_time_str = str(end_time_str) if end_time_str else "10:00:00.000"
    save2D = save2D_var.get()
    save3D = save3D_var.get()
    timer = int(timer_entry.get())
    width = float(width_entry.get())
    coord = float(coord_entry.get())
    
    # Start a new instance of STK
    uiApplication = win32com.client.Dispatch('STK11.Application')
    #uiApplication = CreateObject("STK11.Application")
    uiApplication.Visible = True
    uiApplication.UserControl = True
    
    # Start new instance of STK
    #from comtypes.client import CreateObject
    #uiApplication = CreateObject('STK11.Application')
    #uiApplication.Visible = True
    
    # Get our IAgStkObjectRoot interface
    root = uiApplication.Personality2
        
    from comtypes.gen import STKUtil
    from comtypes.gen import STKObjects
        
    # Create a new scenario from 1 Nov 2023 to 8 Nov 2023
    scenario = root.NewScenario('SSR')
    # scenario.StartTime = '1 Nov 2023 10:30:00.000'
    # scenario.StopTime = '8 Nov 2023 10:30:00.000'
    #scenario2 = scenario.QueryInterface(STKObjects.IAgSenario)
    #scenario2.SetTimePeriod("1 Nov 2023 10:30:00.000", "8 Nov 2023 10:30:00.000")
    #root.Currentscenario.SetTimePeriod("1 Nov 2023 10:30:00.000", "8 Nov 2023 10:30:00.000")
    root.Currentscenario.SetTimePeriod(f'{start_date_str} {start_time_str}', f'{end_date_str} {end_time_str}')
    root.ExecuteCommand('Animate * Reset');
    root.Rewind()
    
    # altitude = 300
    # inclination = 98
    # Number_of_planes = 12 #make sure to also change in walker command !!
    # Sat_per_plane = 2     #make sure to also change in walker command !!
    orbit_type = 'RCO'    #or SSO
    # IPS = 1               #inter plane spacing  , make sure to also change in walker command !!
    # resolution = 0.5      #resolution of coverage definition
    
    if inclination == 98:
        orbit_type = 'SSO'
    
    # Create a satellite
    satellite = root.CurrentScenario.Children.New(18, 'MySatellite')  # 18 represents STK object type for Satellite
    
    satellite.SetPropagatorType(2)
    # IAgSatellite satellite: Satellite object
    keplerian = satellite.Propagator.InitialState.Representation.ConvertTo(1) # eOrbitStateClassical, Use the Classical Element interface
    #SGP4 = satellite.Propagator.InitialState.Representation.ConvertTo(1)
    
    # satellite.SetPropagatorType(4) # ePropagatorSGP4
    # propagator = satellite.Propagator
    # propagator.UseScenarioAnalysisTime
    # #propagator.CommonTasks.AddSegsFromOnlineSource('25544') # International Space Station
    # #propagator.AutoUpdateEnabled = True
    
    
    keplerian.SizeShapeType = 0  # eSizeShapeAltitude, Changes from Ecc/Inc to Perigee/Apogee Altitude
    keplerian.LocationType = 5 # eLocationTrueAnomaly, Makes sure True Anomaly is being used
    keplerian.Orientation.AscNodeType = 0 # eAscNodeLAN, Use LAN instead of RAAN for data entry
    
    # Assign the perigee and apogee altitude values:
    keplerian.SizeShape.PerigeeAltitude = altitude      # km
    keplerian.SizeShape.ApogeeAltitude = altitude       # km
    
    # Assign the other desired orbital parameters:
    keplerian.Orientation.Inclination = inclination        # deg
    keplerian.Orientation.ArgOfPerigee = 0        # deg
    keplerian.Orientation.AscNode.Value = 0       # deg
    keplerian.Location.Value = 0                 # deg
    
    
    # Apply the changes made to the satellite's state and propagate:
    satellite.Propagator.InitialState.Representation.Assign(keplerian)
    #satellite.Propagator.InitialState.Representation.Assign(SGP4)
    
    satellite.Propagator.Propagate()
    
    
    
    
    
    # Create a sensor attached to the satellite
    sensor = satellite.Children.New(20, 'sensor')  # 20 represents STK object type for Sensor
    
    transmitter = satellite.Children.New(24, 'MyTransmitter') # eTransmitter
    # IAgSensor sensor: Sensor object
    # Change pattern and set
    sensor.CommonTasks.SetPatternSimpleConic(48,1) #for rectangular with 45° swath: .SetPatternRectangular(45,45)
    
    walker_constellation = root.ExecuteCommand(f'Walker  */Satellite/MySatellite  Type  Delta  NumPlanes  {str(Number_of_planes)}  NumSatsPerPlane  {str(Sat_per_plane)}  InterPlanePhaseIncrement {str(IPS)} ColorByPlane Yes ConstellationName walker_system SetUniqueNames Yes')
    
    
    
    
    print('Executing walker command')
    
    #EXPAND or COLLAPSE for all facility coordnates/parameters 
    #%%
    #toulouse
    facility_tou = root.CurrentScenario.Children.New(8, 'Toulouse'); # ('eFacility', 'typeyourname')
    facility_tou.Position.AssignGeodetic(43.428889,1.497778,0);  # absign LAT and LON
    sensor_tou = facility_tou.Children.New(20, 'ToulouseGS'); # adding a sensor ('eSensor', 'typeyourname') and attaching it to the facility
    sensor_tou.CommonTasks.SetPatternSimpleConic(30,0.17453293); # sensor proprieties (FOV, angular resolution)
    sensor_tou.Graphics.FillVisible = True;
    receiver_tou = facility_tou.Children.New(17, 'ToulouseReceiver') # eReceiver
    sensor_tou.Graphics.PercentTranslucency = 90;
    
    #Papeete
    facility_pap = root.CurrentScenario.Children.New(8, 'Papeete');
    facility_pap.Position.AssignGeodetic(-17.511,-149.435,0);
    sensor_pap = facility_pap.Children.New(20, 'GPapeeteGS');
    sensor_pap.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_pap.Graphics.FillVisible = False;
    receiver_pap = facility_pap.Children.New(17, 'PapeeteReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Ile Amsterdam 
    facility_ile = root.CurrentScenario.Children.New(8, 'IleAmsterdam');
    facility_ile.Position.AssignGeodetic(-37.493,77.337,0);
    sensor_ile = facility_ile.Children.New(20, 'IleAmsterdamGS');
    sensor_ile.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_ile.Graphics.FillVisible = False;
    receiver_ile = facility_ile.Children.New(17, 'IleAmsterdamReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Noumea
     
    facility_nou = root.CurrentScenario.Children.New(8, 'Noumea');
    facility_nou.Position.AssignGeodetic(-22.2758,166.458,0);
    sensor_nou = facility_nou.Children.New(20, 'NoumeaGS');
    sensor_nou.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_nou.Graphics.FillVisible = False;
    receiver_nou = facility_nou.Children.New(17, 'NoumeaReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Kiev
     
    facility_kie = root.CurrentScenario.Children.New(8, 'Kiev');
    facility_kie.Position.AssignGeodetic(50.45, 30.523611,0);
    sensor_kie = facility_kie.Children.New(20, 'KievGS');
    sensor_kie.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_kie.Graphics.FillVisible = False;
    receiver_kie = facility_kie.Children.New(17, 'KievReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Kourou
     
    facility_kou = root.CurrentScenario.Children.New(8, 'Kourou');
    facility_kou.Position.AssignGeodetic(5.25144, -52.8047,0);
    sensor_kou = facility_kou.Children.New(20, 'KourouGS');
    sensor_kou.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_kou.Graphics.FillVisible = False;
    receiver_kou = facility_kou.Children.New(17, 'KourouReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Redu
     
    facility_red = root.CurrentScenario.Children.New(8, 'Redu');
    facility_red.Position.AssignGeodetic(50.001889, 5.146656,0);
    sensor_red = facility_red.Children.New(20, 'ReduGS');
    sensor_red.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_red.Graphics.FillVisible = False;
    receiver_red = facility_red.Children.New(17, 'ReduReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Santa Maria
     
    facility_sm = root.CurrentScenario.Children.New(8, 'SantaMaria');
    facility_sm.Position.AssignGeodetic(36.99725, -25.135722,0);
    sensor_sm = facility_sm.Children.New(20, 'SantaMariaGS');
    sensor_sm.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_sm.Graphics.FillVisible = False;
    receiver_sm = facility_sm.Children.New(17, 'SantaMariaReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Kiruna
     
    facility_kir = root.CurrentScenario.Children.New(8, 'Kiruna');
    facility_kir.Position.AssignGeodetic(67.857128, 20.964325,0);
    sensor_kir = facility_kir.Children.New(20, 'KirunaGS');
    sensor_kir.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_kir.Graphics.FillVisible = False;
    receiver_kir = facility_kir.Children.New(17, 'KrunaReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    # Rapa
     
    facility_rap = root.CurrentScenario.Children.New(8, 'Rapa');
    facility_rap.Position.AssignGeodetic(-27.583333, -144.333333,0);
    sensor_rap = facility_rap.Children.New(20, 'RapaGS');
    sensor_rap.CommonTasks.SetPatternSimpleConic(30,0.17453293);
    sensor_rap.Graphics.FillVisible = False;
    receiver_rap = facility_rap.Children.New(17, 'RapaReceiver') # eReceiver
    #sensor.Graphics.PercentTranslucency = 90;
    
    print('Added ground stations')
    
    #%%
    
    constellation = root.CurrentScenario.Children.New(6,'MyConstellation') # eConstellation
    const_transmitter = root.CurrentScenario.Children.New(6,'Const_Transmitter')
    const_receiver = root.CurrentScenario.Children.New(6,'Const_Receiver')
    
    print('Adding sensors to constellation')
    
    
    const_receiver.Objects.AddObject(receiver_tou)
    const_receiver.Objects.AddObject(receiver_ile)
    const_receiver.Objects.AddObject(receiver_kie)
    const_receiver.Objects.AddObject(receiver_kir)
    const_receiver.Objects.AddObject(receiver_kou)
    const_receiver.Objects.AddObject(receiver_nou)
    const_receiver.Objects.AddObject(receiver_pap)
    const_receiver.Objects.AddObject(receiver_rap)
    const_receiver.Objects.AddObject(receiver_red)
    const_receiver.Objects.AddObject(receiver_sm)
    
    
    #Multiple Satellites/Sensors by default are named ex: Satellite011/Sensor1, Satellite012/Sensor2, Satellite021/Sensor3 ...
    #                                                  Plane number ^^Satellite in that plane number
    #Once you get to a higher number the naming becomes ex: Satellite101/Sensor10, Satellite102/Sensor11, Satellite111/Sensor12 ...
    #Because of that "0" in front of the number for the first case, if we want to add the names automatically to the constellation (containing the sensors)
    #A condition is written below to take that into account
    m = 1
    j = 1
    for i in range (1,Number_of_planes+1):
        if Number_of_planes < 10:
            k=1
            for k in range (1,Sat_per_plane+1):
                    sensor_name = f'Satellite/MySatellite{m}{k}/Sensor/sensor{j+k-1}' 
                    transmitter_name = f'Satellite/MySatellite{m}{k}/Transmitter/MyTransmitter{j+k-1}'
                    sensor = root.GetObjectFromPath(sensor_name)  
                    transmitter = root.GetObjectFromPath(transmitter_name)
                    constellation.Objects.AddObject(sensor)    
                    const_transmitter.Objects.AddObject(transmitter)
                    
            m += 1 
            j += Sat_per_plane
            
        if Number_of_planes > 9:
            if j < 9*Sat_per_plane:
                k=1
                for k in range (1,Sat_per_plane+1):
                        sensor_name = f'Satellite/MySatellite0{m}{k}/Sensor/sensor{j+k-1}'  
                        transmitter_name = f'Satellite/MySatellite0{m}{k}/Transmitter/MyTransmitter{j+k-1}'
                        sensor = root.GetObjectFromPath(sensor_name)   
                        transmitter = root.GetObjectFromPath(transmitter_name)
                        constellation.Objects.AddObject(sensor) 
                        const_transmitter.Objects.AddObject(transmitter)
                        
                m += 1 
                j += Sat_per_plane
            else:
                k=1
                for k in range (1,Sat_per_plane+1):
                        sensor_name = f'Satellite/MySatellite{m}{k}/Sensor/sensor{j+k-1}'  
                        transmitter_name = f'Satellite/MySatellite{m}{k}/Transmitter/MyTransmitter{j+k-1}'
                        sensor = root.GetObjectFromPath(sensor_name)   
                        transmitter = root.GetObjectFromPath(transmitter_name)
                        constellation.Objects.AddObject(sensor)
                        const_transmitter.Objects.AddObject(transmitter)
                        
                m += 1 
                j += Sat_per_plane
                
       
    print('Added sensors to constellation')
    
    print('Adding area targets')
    
    #CONFLICTROSTOV
    areaTarget = root.CurrentScenario.Children.New(2, 'ConflictRostov') # eAreaTarget
    areaTarget.AreaTypeData.RemoveAll()
    

    # Define the path to the CSV file
    file_path_conflictrostov = 'conflictrostov.csv'
    current_dir = os.getcwd()
    relative_path = os.path.join(current_dir, file_path_conflictrostov)
    conflictrostov_df = pd.read_csv(file_path_conflictrostov, sep=';')
    
    latitudes = conflictrostov_df['Latitude'].tolist()
    longitudes = conflictrostov_df['Longitude'].tolist()
    boundary = []
    
    for i in range(len(latitudes)):
        latitude = latitudes[i]
        longitude = longitudes[i]
        boundary.append([latitude, longitude])
    
    
    areaTarget.CommonTasks.SetAreaTypePattern(boundary);
    
    #CONFLICTZONE
    areaTarget2 = root.CurrentScenario.Children.New(2, 'ConflictZone') # eAreaTarget
    areaTarget2.AreaTypeData.RemoveAll()
    
    
    # Define the path to the CSV file
    file_path_conflictzone = 'conflictzone.csv'
    current_dir = os.getcwd()
    relative_path = os.path.join(current_dir, file_path_conflictzone)
    conflictzone_df = pd.read_csv(file_path_conflictzone, sep=';')
    
    latitudes = conflictzone_df['Latitude'].tolist()
    longitudes = conflictzone_df['Longitude'].tolist()
    boundary2 = []
    
    for i in range(len(latitudes)):
        latitude = latitudes[i]
        longitude = longitudes[i]
        boundary2.append([latitude, longitude])
    
    
     
    areaTarget2.CommonTasks.SetAreaTypePattern(boundary2);
    
    areaTarget3 = root.CurrentScenario.Children.New(2, 'Rectangular') # eAreaTarget
    areaTarget3.AreaTypeData.RemoveAll()
    
    boundary3 = [ 
    [coord-width/2,	coord-width/2],
    [coord-width/2,	coord+width/2],
    [coord+width/2,	coord+width/2],
    [coord+width/2,	coord-width/2]
    ]
    
    areaTarget3.CommonTasks.SetAreaTypePattern(boundary3);
    
    covDef = root.CurrentScenario.Children.New(7,'CovDef'); #7= coverage definition
        
    advanced = covDef.Advanced;
    advanced.AutoRecompute = False;
    
    covDef.Grid.BoundsType = 0;
    covGrid = covDef.Grid;
    bounds = covGrid.Bounds;
    bounds.AreaTargets.Add(f'AreaTarget/{str(selected_target)}'); #'AreaTarget/ConflictZone'
    Res = covGrid.Resolution;
    Res.LatLon = resolution;
    covDef.AssetList.Add('Constellation/MyConstellation');
    
    fom = covDef.Children.New(25,'RevisitTime');
    fom.SetDefinitionType(10);
    fom.Definition.SetComputeType(1) # eMaximum
    
    
   
    print('Computing access')
    covDef.ComputeAccesses();
    print('Computing access complete')
    
    #root.ExecuteCommand('Access */Facility/Toulouse/ToulouseReceiver */Satellite/MySatellite/MyTransmitter')
    receiver = root.GetObjectFromPath('Facility/Toulouse/Receiver/ToulouseReceiver')
    transmitter = root.GetObjectFromPath('Satellite/MySatellite/Transmitter/MyTransmitter')
    access = transmitter.GetAccessToObject(receiver) 
    
    chain = root.CurrentScenario.Children.New(4, 'Mychain')
    chain.ClearAccess()
    chain.Objects.Add('Satellite/MySatellite/Transmitter/MyTransmitter')
    chain.Objects.Add('Facility/Toulouse/Receiver/ToulouseReceiver')
    chain.AutoRecompute = False
    chain.EnableLightTimeDelay = False
    chain.TimeConvergence = 0.001
    chain.DataSaveMode = 2
    chain.SetTimePeriodType(2)
    chain.ComputeAccess()
    
    chain2 = root.CurrentScenario.Children.New(4, 'Chain_Tran_Receiv')
    chain2.ClearAccess()
    chain2.Objects.Add('Constellation/Const_Transmitter')
    chain2.Objects.Add('Constellation/Const_Receiver')
    chain2.AutoRecompute = False
    chain2.EnableLightTimeDelay = False
    chain2.TimeConvergence = 0.001
    chain2.DataSaveMode = 2
    chain2.SetTimePeriodType(2)
    chain2.ComputeAccess()
    
    
    coverage_object = root.GetObjectFromPath('CoverageDefinition/CovDef')  
        
    print('Executing dataprovider for Value by Grid point')
    
    #FoMDP = fom.DataProviders.Item('Value By Point')
    
    
    #chainDP = chain.DataProviders.Item('Link Information').Exec("1 Nov 2023 10:30:00.000", "8 Nov 2023 10:30:00.000",60)
    
    starttime = root.CurrentScenario.StartTime
    stoptime = root.CurrentScenario.StopTime
    currenttime = starttime
    time_step_seconds = 60
    current_datetime = datetime.strptime(starttime, '%d %b %Y %H:%M:%S.%f')
    stop_time = datetime.strptime(stoptime, '%d %b %Y %H:%M:%S.%f')
    #new_stoptime = stop_time - timedelta(hours=1) 
    
    all_EIRP_data = []
    all_ISO_data = []
    all_time_data = []
    all_name_data = []
    all_num_data = []
    
    match = re.search(r'(\.\d+)', currenttime)
    
    if match:
        milliseconds = match.group(1)
    else:
        milliseconds = ''
    
    current_datetime = datetime.strptime(currenttime, '%d %b %Y %H:%M:%S' + milliseconds)
    new_datetime = current_datetime 
    
    # Format the new datetime as a string
    new_time_str = new_datetime.strftime('%d %b %Y %H:%M:%S.%f')[:-3]
            
    while new_datetime <= stop_time:
        chainDP = chain.DataProviders.Item('Link Information').Exec(new_time_str, stoptime, time_step_seconds)
        chainEIRP = chainDP.DataSets.GetDataSetByName('EIRP1').GetValues()
        chainISO = chainDP.DataSets.GetDataSetByName('Rcvd. Iso. Power1').GetValues()
        chainTime = chainDP.DataSets.GetDataSetByName('Time').GetValues()
        chainName = chainDP.DataSets.GetDataSetByName('Link Name').GetValues()
        all_EIRP_data.extend(list(chainEIRP))
        all_ISO_data.extend(list(chainISO))
        all_time_data.extend(list(chainTime))
        all_name_data.extend(list(chainName))
    
        currenttime = all_time_data[-1]
        
        match = re.search(r'(\.\d+)', all_time_data[-1])

        if match:
            milliseconds = match.group(1)
        else:
            milliseconds = ''
        
        current_datetime = datetime.strptime(all_time_data[-1], '%d %b %Y %H:%M:%S' + milliseconds)
        new_datetime = current_datetime + timedelta(hours=1)
        
        # Format the new datetime as a string
        new_time_str = new_datetime.strftime('%d %b %Y %H:%M:%S.%f')[:-3]
        
        #to do whole csv file
        # if new_datetime > stop_time:
        #     match = re.search(r'(\.\d+)', starttime)
            
        #     if match:
        #         milliseconds = match.group(1)
        #     else:
        #         milliseconds = ''
            
        #     current_datetime = datetime.strptime(starttime, '%d %b %Y %H:%M:%S' + milliseconds)
        #     new_datetime = current_datetime 
            
        #     # Format the new datetime as a string
        #     new_time_str = new_datetime.strftime('%d %b %Y %H:%M:%S.%f')[:-3]
        
        
        
    #chainDP = chain.DataProviders.Item('Link Information').Exec((str(start_date_str + ' ' + start_time_str)), (str(end_date_str + ' ' + end_time_str)),60)   
    #chainISO = chainDP.DataSets.GetDataSetByName('Rcvd. Iso. Power1').GetValues()    
    # EIRP = list(chainEIRP)
    # ISO = list(chainISO)
    
    
    data = {
        'Time': all_time_data,
        'EIRP': all_EIRP_data,
        'Rcvd. Iso. Power': all_ISO_data,
        'Link Name': all_name_data
        }
    df = pd.DataFrame(data)
    
    print('Exported CSV file')
    
    file_path = f'LinkBudget_{orbit_type}_{str(Sat_per_plane)}x{str(Number_of_planes)}_{str(inclination)}_{str(altitude)}_{str(IPS)}_{str(resolution)}.csv'
    current_dir = os.getcwd()
    relative_path = os.path.join(current_dir, file_path)
    
    df.to_csv(relative_path, index=False, sep=',')
    
    
    
    #rptElements = ['Latitude','Longitude','FOM Value']
    
    FoMDP = fom.DataProviders.Item('Value By Point').Exec()
    FoMDPLat = FoMDP.DataSets.GetDataSetByName('Latitude').GetValues()
    FoMDPLon = FoMDP.DataSets.GetDataSetByName('Longitude').GetValues()
    FoMDPFOM = FoMDP.DataSets.GetDataSetByName('FOM Value').GetValues()
        
    lat = list(FoMDPLat)
    lon = list(FoMDPLon)
    FOM = list(FoMDPFOM)
    
    # Combine the lists into a single list of tuples
    if result_var.get() == 'Value by Grid Point':
        data = {
           'latitude': lat,
           'longitude': lon,
           'fom_sec': FOM
        }
        df = pd.DataFrame(data)
    
    print('Completed dataprovider')
        
    # Define the path to the CSV file
    file_path = f'{orbit_type}_{str(Sat_per_plane)}x{str(Number_of_planes)}_{str(inclination)}_{str(altitude)}_{str(IPS)}_{str(resolution)}.csv'
    current_dir = os.getcwd()
    relative_path = os.path.join(current_dir, file_path)
    
    
    
    df.to_csv(relative_path, index=False, sep=',')
    
    
    if save2D_var.get() == 'Yes':
        #Take a screenshot from initial state in 2D window
        root.ExecuteCommand(f'SoftVTR2D * Record On FileFormat TIF OutputDir "{current_dir}" Prefix 2D_{orbit_type}_{str(Sat_per_plane)}x{str(Number_of_planes)}_{str(inclination)}_{str(altitude)}_{str(IPS)}_{str(resolution)}')     
        root.ExecuteCommand('SoftVTR2D * SnapWindow')    
        root.ExecuteCommand('SoftVTR2D * Record Off')
        print("Saved 2D image")
    
    if save3D_var.get() == 'Yes':
        #Take a screenshot from initial state in 3D window
        root.ExecuteCommand(f'SoftVTR3D * Record On FileFormat TIF OutputDir "{current_dir}" Prefix 3D_{orbit_type}_{str(Sat_per_plane)}x{str(Number_of_planes)}_{str(inclination)}_{str(altitude)}_{str(IPS)}_{str(resolution)}')    
        root.ExecuteCommand('SoftVTR3D * SnapWindow')   
        root.ExecuteCommand('SoftVTR3D * Record Off')
        print("Saved 3D image")
    
    if save2D_var.get() == 'Yes':
        #Take a movie in 3D window, change sleep timer to set length of desired video
        root.ExecuteCommand(f'SoftVTR2D * Record On FileFormat AVI OutputDir "{current_dir}" Prefix 2D_{orbit_type}_{str(Sat_per_plane)}x{str(Number_of_planes)}_{str(inclination)}_{str(altitude)}_{str(IPS)}_{str(resolution)}')     
        root.ExecuteCommand('Animate * Start')  
        print("Starting 2D timer")
        time.sleep(timer)  
        print("Stopping 2D timer")
        root.ExecuteCommand('SoftVTR2D * Record Off')   
        root.ExecuteCommand('Animate * Pause')
        print("Saved 2D video")
    
    if save3D_var.get() == 'Yes':
        #Take a movie in 3D window, change sleep timer to set length of desired video
        root.ExecuteCommand(f'SoftVTR3D * Record On FileFormat AVI OutputDir "{current_dir}" Prefix 3D_{orbit_type}_{str(Sat_per_plane)}x{str(Number_of_planes)}_{str(inclination)}_{str(altitude)}_{str(IPS)}_{str(resolution)}')     
        root.ExecuteCommand('Animate * Start') 
        print("Starting 3D timer")
        time.sleep(timer)   
        print("Stopping 3D timer")
        root.ExecuteCommand('SoftVTR3D * Record Off')   
        root.ExecuteCommand('Animate * Pause')
        print("Saved 3D video")
#change name to have 2D and 3D at the end of the name
    #root.quit()
    
root = tk.Tk()
root.title("STK Launcher")

# Create labels and entry fields for user input
tk.Label(root, text="Altitude (km):").grid(row=0, column=0)
altitude_entry = ttk.Entry(root)
altitude_entry.grid(row=0, column=1, pady=(10,0))
altitude_entry.insert(0, "300")

tk.Label(root, text="Inclination (deg):").grid(row=1, column=0)
inclination_entry = ttk.Entry(root)
inclination_entry.grid(row=1, column=1, pady=(10,0))
inclination_entry.insert(0, "50")

tk.Label(root, text="Number of Planes:").grid(row=2, column=0)
planes_entry = ttk.Entry(root)
planes_entry.grid(row=2, column=1, pady=(10,0))
planes_entry.insert(0, "12")

tk.Label(root, text="Satellites per Plane:").grid(row=3, column=0)
sat_per_plane_entry = ttk.Entry(root)
sat_per_plane_entry.grid(row=3, column=1, pady=(10,0))
sat_per_plane_entry.insert(0, "2")

tk.Label(root, text="Inter-Plane Spacing:").grid(row=4, column=0)
ips_entry = ttk.Entry(root)
ips_entry.grid(row=4, column=1, pady=(10,0))
ips_entry.insert(0, "0")

tk.Label(root, text="Resolution:").grid(row=5, column=0)
resolution_entry = ttk.Entry(root)
resolution_entry.grid(row=5, column=1, pady=(10,0))
resolution_entry.insert(0, "0.5")


tk.Label(root, text="Start Date (D MMM YYYY):").grid(row=6, column=0)
start_date_entry = ttk.Entry(root)
start_date_entry.grid(row=6, column=1, pady=(10,0))
start_date_entry.insert(0, "1 Nov 2023")

tk.Label(root, text="Start Time (HH:MM:SS.000):").grid(row=7, column=0)
start_time_entry = ttk.Entry(root)
start_time_entry.grid(row=7, column=1, pady=(10,0))
start_time_entry.insert(0, "10:00:00.000")

# Add entry fields for end date and time
tk.Label(root, text="End Date (D MMM YYYY):").grid(row=8, column=0)
end_date_entry = ttk.Entry(root)
end_date_entry.grid(row=8, column=1, pady=(10,0))
end_date_entry.insert(0, "8 Nov 2023")

tk.Label(root, text="End Time (HH:MM:SS.000):").grid(row=9, column=0)
end_time_entry = ttk.Entry(root)
end_time_entry.grid(row=9, column=1, pady=(10,0))
end_time_entry.insert(0, "10:00:00.000")


# Add a drop-down menu for selecting targets
target_label = ttk.Label(root, text="Select Target:")
target_label.grid(row=10, column=0, pady=(10,0))

targets = ["ConflictRostov", "ConflictZone", "Rectangular"]  # Predefined targets
target_var = tk.StringVar(value=targets[0])  # Set default value to the first target
target_dropdown = ttk.Combobox(root, textvariable=target_var, values=targets)
target_dropdown.grid(row=10, column=1, pady=(10,0))

#Add a drop-down menu for selecting results
result_label = ttk.Label(root, text="Select results:")
result_label.grid(row=11, column=0, pady=(10,0))

results = ["Value by Grid Point"]  # Predefined targets
result_var = tk.StringVar(value=results[0])  # Set default value to the first target
result_dropdown = ttk.Combobox(root, textvariable=result_var, values=results)
result_dropdown.grid(row=11, column=1, pady=(10,0))

save2D_label = ttk.Label(root, text="Take 2D image and video:")
save2D_label.grid(row=0, column=3, pady=(10,0))
save2D = ["Yes", "No"]
save2D_var = tk.StringVar(value=save2D[1])
save2D_dropdown = ttk.Combobox(root, textvariable=save2D_var, values=save2D)
save2D_dropdown.grid(row=0, column=4, pady=(10,0))

save3D_label = ttk.Label(root, text="Take 3D image and video:")
save3D_label.grid(row=1, column=3, pady=(10,0))
save3D = ["Yes", "No"]
save3D_var = tk.StringVar(value=save3D[1])
save3D_dropdown = ttk.Combobox(root, textvariable=save3D_var, values=save3D)
save3D_dropdown.grid(row=1, column=4, pady=(10,0))


tk.Label(root, text="Timer for video (s):").grid(row=2, column=3)
timer_entry = ttk.Entry(root)
timer_entry.grid(row=2, column=4, pady=(10,0))
timer_entry.insert(0, "5")

tk.Label(root, text="Width/Length for rectangle:").grid(row=3, column=3)
width_entry = ttk.Entry(root)
width_entry.grid(row=3, column=4, pady=(10,0))
width_entry.insert(0, "5.0")

tk.Label(root, text="Coordinates for rectangle:").grid(row=4, column=3)
coord_entry = ttk.Entry(root)
coord_entry.grid(row=4, column=4, pady=(10,0))
coord_entry.insert(0, "0.0")

# Create a "Launch" button
launch_button = ttk.Button(root, text="Launch", command=launch_stk)
launch_button.grid(row=12, columnspan=8, pady=(10,0))

# Start the GUI main loop
root.mainloop()

#https://www.youtube.com/watch?v=L_LHzVYJsds&ab_channel=AnsysGovernmentIntiatives%28AGI%29 > source for dataproviders function



































