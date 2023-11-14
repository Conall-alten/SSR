# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 11:42:08 2023

@author: edecline
"""

import numpy as np
import matplotlib.pyplot as plt

plt.close('all')


k = 1.91
h = 198
mu = 398600
R = 6378
theta = 33.11 # deg
T = 2*np.pi*np.sqrt((h+R)**3/mu)/3600
D = 2*k*h*np.tan(theta*np.pi/180)
V = 2*np.pi*R/24
x = np.arange(1, 12, 0.01)
d = []
n = []

for i in x:
    d.append(V*T/i-D)
    n.append(0)

c = 0
for i in d:
    if i<0:
        c+=d.index(i)
        break

plt.figure(1, dpi = 200)
plt.title("Largeur d'une lacune de revisite")
plt.plot(x, d, label=round(x[c], 3))
plt.plot(x, n)
plt.xticks([i for i in range(1,13)])
plt.ylabel("Distance séparant deux fauchées consécutives (km)")
plt.xlabel("Nombre de satellites par plan")
plt.legend()
print(T)




#
#ca = 0
#cb = 0
#clist = []
#k = np.arange(1, 2, 0.01)
#
#for j in k:
#            
#    a = 5
#    b = 6
#
#    h = 198
#    mu = 398600
#    R = 6378
#    theta = 33.11 # deg
#    T = 2*np.pi*np.sqrt((h+R)**3/mu)/3600
#    D = 2*j*h*np.tan(theta*np.pi/180)
#    V = 2*np.pi*R/24
#    x = np.arange(1, 12, 0.01)
#    d = []
#    n = []
#    
#    for i in x:
#        d.append(V*T/i-D)
#        n.append(0)
#    
#    c = 0
#    for i in d:
#        if i<0:
#            clist.append(x[d.index(i)])
#            c+=d.index(i)
#            print(j)
#            break
#        
#    
#    for i in d:
#        if i<5:
#            ca+=d.index(i)
#            break
#        if i<=6:
#            cb+=d.index(i)
#            break
#        
#    print("[",x[ca],",",x[cb],"]")
