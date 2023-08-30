# -*- coding: utf-8 -*-
"""
Created on Wed May 10 01:58:09 2023

@author: DECLINE
"""

from turtle import *

#%% for txt files

num = 0
files = ['Villes_Ukraine','Luhansk_city','Swath_260_2.5_1_long','ConflictRostov','France','Launch','Outremer','UkraineEast','Bryansk','Kursk','Belgorod','RostovDon','crimea','zaporizhia','kherson','donetsk','luhansk','conflict','ukraine'] 
with open(files[num]+'.txt', "r+") as file:
    data = file.read()
    
    data = data.replace(",","")
    #data = data.replace("\n"," ")
    # for i in data:
    #    if i.isnumeric()==False and i!=" " and i!=".":
    #        data = data.replace(i,"")
    
    print(data)
    
with open(files[num]+'.at', "w") as file:
    file.write(str(data))

#%% Squares and rectangles areas
"""
eps = 0.1 # eps = 1 => square
L = 100 #km (parallèles)
l = L*eps #km (méridiens)

screen = Screen()
speed('fastest')
bgcolor('black')

thickness = 2
width(thickness)
color("red")
left(180)
forward(L*5)
left(180)
forward(L*10)
left(90)
forward(l*10)
left(90)
forward(L*10)
left(90)
forward(l*10)

screen.update()
ts = getscreen()
done()
"""

"""
# manually, for a list
l = [44.374752, 33.75,
44.508008, 33.596191,
44.484514, 33.859863,
44.515837, 34.112549,
44.601888, 33.585205,
44.601888, 33.914795,
44.601888, 34.277344,
44.796985, 33.640137,
44.812564, 33.991699,
44.812564, 34.398193,
44.84371, 34.672852,
44.812564, 34.980469,
44.84371, 35.090332,
44.968126, 33.651123,
44.968126, 33.903809,
44.983659, 34.222412,
44.991424, 34.628906,
44.991424, 34.969482,
44.991424, 35.2771,
44.991424, 35.892334,
45.043734, 36.276855,
45.074755, 33.651123,
45.074755, 33.95874,
45.074755, 34.28833,
45.074755, 34.661865,
45.082508, 35.090332,
45.136747, 35.650635,
45.206407, 36.112061,
45.206407, 36.386719,
45.360901, 36.364746,
45.345471, 36.156006,
45.330036, 35.881348,
45.314597, 35.123291,
45.314597, 34.903564,
45.314597, 34.606934,
45.275981, 34.343262,
45.275981, 34.134521,
45.252799, 33.804932,
45.237339, 33.62915,
45.237339, 33.354492,
45.384206, 33.013916,
45.376494, 32.860107,
45.368781, 32.640381,
45.415041, 33.519287,
45.415041, 33.892822,
45.415041, 34.255371,
45.438157, 34.628906,
45.438157, 35.024414,
45.584337, 34.958496,
45.576653, 34.628906,
45.561281, 34.28833,
45.561281, 34.112549,
45.561281, 33.936768,
45.561281, 33.728027,
45.561281, 33.552246,
45.553594, 33.299561,
45.553594, 33.134766,
45.553594, 32.947998,
45.644706, 33.013916,
45.630633, 33.33252,
45.645985, 33.771973,
45.645985, 34.233398,
45.669006, 34.639893,
45.829888, 34.541016,
45.829888, 34.40918,
45.829888, 34.200439,
45.829888, 34.002686,
45.829888, 33.826904,
45.829888, 33.62915,
45.966332, 33.662109,
46.043677, 33.936768,
46.013186, 34.101563,
45.952154, 34.277344,
46.127439, 33.728027]

lat = []
long = []

for i in range(len(l)):
    if i==0 or i%2==0:
        lat.append(l[i])
    else:
        long.append(l[i])
        
num_points = int(len(l)/2)

with open("crimea.txt", "w") as file:
    for i in range(0, num_points):
        file.write(str(lat[i])+" "+str(long[i])+"\n")


with open("crimea.at", "w") as file:
    for i in range(0, num_points):
        file.write(str(lat[i])+" "+str(long[i])+"\n")
"""
