# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 10:55:17 2023

@author: cdepaor
"""
import numpy as np
import matplotlib.pyplot as plt
#%%
alt = 250000

solar_flux = 1370
reflection = 0.3
earth_albedo = solar_flux*reflection*(((6371000/(6371000+alt)))**2)
earth_IR = (solar_flux*(1-reflection)/4)*(((6371000/(6371000+alt)))**2)

#    a = 0.2
#    e = 0.8
T_space = 4 #around LEO
T_max = 313
#    alpha_epsilon = a/e
sigma  = 5.670374419E-8
#    alpha_epsilon = (2*sigma/solar_flux)(T_max**4-T_space**4)

##### energy arriving on each face in the worst case scenario ####
e_nadir = earth_IR + earth_albedo
e_anti_nadir = solar_flux
e_forward = (earth_IR + earth_albedo)*0.5451688  
# avg value of ((cos(theta)/(Re+h))**2)*(sin(theta)) 
# Where theta is the view angle to the surface of the earth
e_backward = (earth_IR + earth_albedo)*0.5451688  
e_left = (earth_IR + earth_albedo)*0.5451688
e_right = (earth_IR + earth_albedo)*0.5451688

### Required material properties of each face ###
ae_nadir = (2*sigma/e_nadir)*(T_max**4-T_space**4)
ae_anti_nadir = (2*sigma/e_anti_nadir)*(T_max**4-T_space**4)
ae_forward = (2*sigma/e_forward)*(T_max**4-T_space**4)
ae_backward = (2*sigma/e_backward)*(T_max**4-T_space**4)
ae_left = (2*sigma/e_left)*(T_max**4-T_space**4)
ae_right = (2*sigma/e_right)*(T_max**4-T_space**4)

results1 = {"ae_nadir      " :np.round(ae_nadir, 3) ,
           "ae_anti_nadir " :np.round(ae_anti_nadir, 3),
           "ae_forward    " :np.round(ae_forward, 3) ,
           "ae_backward   " :np.round(ae_backward, 3) ,
           "ae_left       " :np.round(ae_left, 3),
           "ae_right      " :np.round(ae_right, 3),}

plt.figure()
#plt.figure
x = np.linspace(0,1,10)
plt.plot(x, x*ae_nadir, label = "nadir")
plt.plot(x, x*ae_anti_nadir, label = "anti-nadir")
plt.plot(x, x*ae_forward, label = "forward")
plt.plot(x, x*ae_backward, label = "backward")
plt.plot(x, x*ae_left, label = "left")
plt.plot(x, x*ae_right, label = "right")
plt.scatter(0.95, 0.9, label = "Black Paint")
plt.scatter(0.75, 0.15, label = "SSM")
plt.scatter(0.8, 0.2, label = "White Paint")
plt.scatter(0.75, 0.52, label = "MLI")
plt.scatter(0.15, 0.05, label = "Polished Aluminium")
plt.scatter(0.3, 0.31, label = "Brilliant Aluminium")
plt.scatter(0.95, 0.9, label = "Solar Cell")

plt.legend(loc='upper left',bbox_to_anchor=(1.05, 1))
plt.xlim(0,1)
plt.ylim(0,1)
plt.title("required thermal properties")
plt.xlabel("epsilon")
plt.ylabel("alpha")
plt.tight_layout()



results2 = {"e_nadir      " :np.round(e_nadir, 3) ,
           "e_anti_nadir " :np.round(e_anti_nadir, 3),
           "e_forward    " :np.round(e_forward, 3) ,
           "e_backward   " :np.round(e_backward, 3) ,
           "e_left       " :np.round(e_left, 3),
           "e_right      " :np.round(e_right, 3),}

results1
#t_max = (T_space + alpha_epsilon*0.5*(solar_flux/sigma))**0.25