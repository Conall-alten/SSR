# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:03:34 2023

@author: msige
"""

# This code compute the link budget the same way as LinkBudget_V2 does but 
# with a user interface that allow to put antenna's parameters

import tkinter as tk
import LinkBudget_V2 as LBV2


def interface_graph():
    
    # window parameter
    fenetre = tk.Tk()
    fenetre.title("Link Budget")
    fenetre.iconbitmap("../inputs/asset/626rocket_100672.ico")
    fenetre.geometry("550x180")

    # texts
    tk.Label(fenetre, text="Emitter Parameters", relief='sunken', bg='orange').grid(row=0, column=1)
    tk.Label(fenetre, text="Diameter emitter (m)").grid(row=2, column=0)
    tk.Label(fenetre, text="Power emitter (W)").grid(row=3, column=0)
    tk.Label(fenetre, text="Gain emitter (dB)").grid(row=4, column=0)
    tk.Label(fenetre, text="Altitude emitter (m)").grid(row=5, column=0)
    tk.Label(fenetre, text="Latitude emitter (m)").grid(row=6, column=0)
    tk.Label(fenetre, text="Longitude emitter (m)").grid(row=7, column=0)
    tk.Label(fenetre, text="Frequency (Hz)").grid(row=8, column=0)

    tk.Label(fenetre, text="Receiver Parameters", relief='sunken', bg='yellow').grid(row=0, column=3)
    tk.Label(fenetre, text="Diameter receiver (m)").grid(row=2, column=2)
    tk.Label(fenetre, text="Receiver Bandwidth (Hz)").grid(row=3, column=2)
    tk.Label(fenetre, text="Altitude receiver (m)").grid(row=5, column=2)
    tk.Label(fenetre, text="Latitude receiver (m)").grid(row=6, column=2)
    tk.Label(fenetre, text="Longitude receiver (m)").grid(row=7, column=2)

    # parameters saving
    s1 = tk.DoubleVar()  # Diameter emitter
    s2 = tk.DoubleVar()  # Power emitter
    s3 = tk.DoubleVar()  # Gain emitter
    s4 = tk.DoubleVar()  # Diameter receiver
    s5 = tk.DoubleVar(value=300000)  # Altitude emitter
    s6 = tk.DoubleVar(value=43)  # Latitude emitter
    s7 = tk.DoubleVar(value=1)  # Longitude emitter
    s12 = tk.DoubleVar(value=2.2*10** 9)  # Frequency
    
    s8 = tk.DoubleVar(value=200)  # Altitude receiver
    s9 = tk.DoubleVar(value=44)  # Latitude receiver
    s10 = tk.DoubleVar(value=2)  # Longitude receiver
    s11 = tk.DoubleVar(value=100)  # Receiver Bandwidth

    # parameters windows
    e1 = tk.Entry(textvariable=s1, justify='center')
    e2 = tk.Entry(textvariable=s2, justify='center')
    e3 = tk.Entry(textvariable=s3, justify='center')
    e4 = tk.Entry(textvariable=s4, justify='center')
    e5 = tk.Entry(textvariable=s5, justify='center')
    e6 = tk.Entry(textvariable=s6, justify='center')
    e7 = tk.Entry(textvariable=s7, justify='center')
    e8 = tk.Entry(textvariable=s8, justify='center')
    e9 = tk.Entry(textvariable=s9, justify='center')
    e10 = tk.Entry(textvariable=s10, justify='center')
    e11 = tk.Entry(textvariable=s11, justify='center')
    e12 = tk.Entry(textvariable=s12, justify='center')
    
    # parameters position
    e1.grid(row=2, column=1)
    e2.grid(row=3, column=1)
    e3.grid(row=4, column=1)    
    e5.grid(row=5, column=1)
    e6.grid(row=6, column=1)
    e7.grid(row=7, column=1)
    e12.grid(row=8, column=1)
    
    e4.grid(row=2, column=3)
    e8.grid(row=5, column=3)
    e9.grid(row=6, column=3)
    e10.grid(row=7, column=3)
    e11.grid(row=3, column=3)

    # quit button
    btn = tk.Button(fenetre, text ="Okay", relief='sunken', bg='lightblue', command = fenetre.destroy)
    btn.grid(row=8, column=4)

    # run the app
    fenetre.mainloop()
    
    return s1.get(), s2.get(), s3.get(), s4.get(), s5.get(), s6.get(), s7.get(), s8.get(), s9.get(), s10.get(), s11.get(), s12.get()

d_e, p_e, g_e, d_r, h_e, lat_e, lon_e, h_r, lat_r, lon_r, Bandwidth, freq  = interface_graph()

res = LBV2.compute_margin(p_e, d_e, d_r, g_e, h_e, lat_e, lon_e, h_r, lat_r, lon_r, Bandwidth, freq)

print("The link budget margin is", res, "dB\n")