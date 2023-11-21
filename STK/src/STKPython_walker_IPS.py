# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:56:21 2023

@author: Benjamin
"""
import numpy as np
import matplotlib.pyplot as plt # type: ignore
import os
import win32com.client
#import comtypes

# Start a new instance of STK
uiApplication = win32com.client.Dispatch('STK11.Application')
uiApplication.Visible = True

# Start new instance of STK
#from comtypes.client import CreateObject
#uiApplication = CreateObject('STK11.Application')
#uiApplication.Visible = True

# Get our IAgStkObjectRoot interface
root = uiApplication.Personality2

# Create a new scenario from 1 Nov 2023 to 8 Nov 2023
scenario = root.NewScenario('SSR')
# scenario.StartTime = '1 Nov 2023 10:30:00.000'
# scenario.StopTime = '8 Nov 2023 10:30:00.000'
root.Currentscenario.SetTimePeriod("1 Nov 2023 10:30:00.000", "8 Nov 2023 10:30:00.000")
root.ExecuteCommand('Animate * Reset');

# Create a satellite
satellite = root.CurrentScenario.Children.New(18, 'MySatellite')  # 18 represents STK object type for Satellite

# IAgSatellite satellite: Satellite object
keplerian = satellite.Propagator.InitialState.Representation.ConvertTo(1) # eOrbitStateClassical, Use the Classical Element interface
keplerian.SizeShapeType = 0  # eSizeShapeAltitude, Changes from Ecc/Inc to Perigee/Apogee Altitude
keplerian.LocationType = 5 # eLocationTrueAnomaly, Makes sure True Anomaly is being used
keplerian.Orientation.AscNodeType = 0 # eAscNodeLAN, Use LAN instead of RAAN for data entry

# Assign the perigee and apogee altitude values:
keplerian.SizeShape.PerigeeAltitude = 300      # km
keplerian.SizeShape.ApogeeAltitude = 300       # km

# Assign the other desired orbital parameters:
keplerian.Orientation.Inclination = 98         # deg
keplerian.Orientation.ArgOfPerigee = 0        # deg
keplerian.Orientation.AscNode.Value = 0       # deg
keplerian.Location.Value = 0                 # deg

# Apply the changes made to the satellite's state and propagate:
satellite.Propagator.InitialState.Representation.Assign(keplerian)
satellite.Propagator.Propagate()

# Create a sensor attached to the satellite
sensor = satellite.Children.New(20, 'sensor')  # 17 represents STK object type for Sensor
# IAgSensor sensor: Sensor object
# Change pattern and set
sensor.CommonTasks.SetPatternSimpleConic(48, 1) #48 = Demi angle fourni par res to angle

walker_constellation = root.ExecuteCommand('Walker  */Satellite/MySatellite  Type  Delta  NumPlanes  12  NumSatsPerPlane  2  InterPlanePhaseIncrement 1 ColorByPlane Yes ConstellationName walker_system SetUniqueNames Yes')

#toulouse
facility_tou = root.CurrentScenario.Children.New(8, 'Toulouse'); # ('eFacility', 'typeyourname')
facility_tou.Position.AssignGeodetic(43.428889,1.497778,0);  # absign LAT and LON
sensor = facility_tou.Children.New(20, 'ToulouseGS'); # adding a sensor ('eSensor', 'typeyourname') and attaching it to the facility
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293); # sensor proprieties (FOV, angular resolution)
sensor.Graphics.FillVisible = True;
sensor.Graphics.PercentTranslucency = 90;

#Papeete
facility_pap = root.CurrentScenario.Children.New(8, 'Papeete');
facility_pap.Position.AssignGeodetic(-17.511,-149.435,0);
sensor = facility_pap.Children.New(20, 'GPapeeteGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Ile Amsterdam 
facility_ile = root.CurrentScenario.Children.New(8, 'IleAmsterdam');
facility_ile.Position.AssignGeodetic(-37.493,77.337,0);
sensor = facility_ile.Children.New(20, 'IleAmsterdamGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Noumea
 
facility_nou = root.CurrentScenario.Children.New(8, 'Noumea');
facility_nou.Position.AssignGeodetic(-22.2758,166.458,0);
sensor = facility_nou.Children.New(20, 'NoumeaGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Kiev
 
facility_kie = root.CurrentScenario.Children.New(8, 'Kiev');
facility_kie.Position.AssignGeodetic(50.45, 30.523611,0);
sensor = facility_kie.Children.New(20, 'KievGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Kourou
 
facility_kou = root.CurrentScenario.Children.New(8, 'Kourou');
facility_kou.Position.AssignGeodetic(5.25144, -52.8047,0);
sensor = facility_kou.Children.New(20, 'KourouGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Redu
 
facility_red = root.CurrentScenario.Children.New(8, 'Redu');
facility_red.Position.AssignGeodetic(50.001889, 5.146656,0);
sensor = facility_red.Children.New(20, 'ReduGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Santa Maria
 
facility_sm = root.CurrentScenario.Children.New(8, 'SantaMaria');
facility_sm.Position.AssignGeodetic(36.99725, -25.135722,0);
sensor = facility_sm.Children.New(20, 'SantaMariaGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Kiruna
 
facility_kir = root.CurrentScenario.Children.New(8, 'Kiruna');
facility_kir.Position.AssignGeodetic(67.857128, 20.964325,0);
sensor = facility_kir.Children.New(20, 'KirunaGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

# Rapa
 
facility_rap = root.CurrentScenario.Children.New(8, 'Rapa');
facility_rap.Position.AssignGeodetic(-27.583333, -144.333333,0);
sensor = facility_rap.Children.New(20, 'RapaGS');
sensor.CommonTasks.SetPatternSimpleConic(30,0.17453293);
sensor.Graphics.FillVisible = False;
#sensor.Graphics.PercentTranslucency = 90;

#Change DateFormat dimension to epoch seconds to make the data easier to handle in
#Python
# root.UnitPreferences.Item('DateFormat').SetCurrentUnit('EpSec')
# #Get the current scenario
# scenario = root.CurrentScenario
# #Set up the access object
# access = satellite.GetAccessToObject(facility_tou)
# access.ComputeAccess()
# #Get the Access AER Data Provider
# accessDP = access.DataProviders.Item('Access Data').Exec(scenario.StartTime, scenario.StopTime)

# accessStartTimes = accessDP.DataSets.GetDataSetByName('Start Time').GetValues
# accessStopTimes = accessDP.DataSets.GetDataSetByName('Stop Time').GetValues

constellation = root.CurrentScenario.Children.New(6,'MyConstellation') # eConstellation

constellation.Objects.AddObject(sensor);

#constellation.Objects.Add('*/MySatellite011/sensor1')

areaTarget = root.CurrentScenario.Children.New(2, 'ConflictZone') # eAreaTarget
#location2 = root.CurrentScenario.Children.New('AreaTarget', 'ConflictZone');

areaTarget.AreaTypeData.RemoveAll()

boundary = [[46.362200, 31.025391],[46.384925, 31.234131],[46.157251, 31.322021]]
 
 
areaTarget.CommonTasks.SetAreaTypePattern(boundary);

#customRegion = root.GetObjectFromPath('AreaTarget/ConflictZone');

covDef = root.CurrentScenario.Children.New(7,'CovDef');


advanced = covDef.Advanced;
advanced.AutoRecompute = False;

covDef.Grid.BoundsType = 0;
covGrid = covDef.Grid;
bounds = covGrid.Bounds;
bounds.AreaTargets.Add('AreaTarget/ConflictZone');
Res = covGrid.Resolution;
Res.LatLon = 0.5;
covDef.AssetList.Add('Constellation/MyConstellation');

fom = covDef.Children.New(25,'RevisitTime');
fom.SetDefinitionType(10);
fom.Definition.SetComputeType(1) # eMaximum
#fom.Definition.Satisfaction.EnableSatisfaction = True;
#access = satellite.GetAccessToObject(facility_tou);
covDef.ComputeAccesses();

# fomDataProvider = fom.DataProviders.GetDataPrvFixedFromPath("Value by Grid Point")
# fomResults = fomDataProvider.Exec()

# avgTime = fomResults.DataSets.GetDataSetByName("FOM value (sec)").GetValues()[0]

# print("the fom is {a:4.2f} min.".format(a=avgTime))



#report_create = root.ExecuteCommand('ReportCreate */Analysis/FigureOfMerit/CoverageDefinition/CovDef/RevisitTime Type Export Style "Value By Grid Point" File "C:\result_test.csv"');

# Generate a coverage report
# Assuming you have a coverage object named 'MyCoverage'
coverage_object = root.GetObjectFromPath('CoverageDefinition/CovDef')  # Make sure to replace 'MyCoverage' with your coverage name


