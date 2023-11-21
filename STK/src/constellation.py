# -*- coding: utf-8 -*-
"""
Created on _

@author: S-GADIOUX
"""

class Constellation :

    def __init__(self, name, nsat, nplan, inc, alt, res, ips, added):
        self.name = name
        self.nsat = nsat # Nombre de satellites par plan
        self.nplan = nplan # Nombre de plans
        self.inc = inc # Inclinaison des orbites (0° par convention pour une SSO)
        self.alt = alt # Altitude (km)
        self.res = res   # Les fichiers apparaissent dans l'ordre alphabétique (ex : 
                    # RCO_2x4_50_260_0_1.5, RCO_2x4_50_260_0_1, RCO_2x4_50_260_0_2.5)). Il 
                    # faut donc écrire 1.0, 2.0 ou 3.0 au lieu de 1, 2 et 3 pour avoir
                    # 1.0 avant 1.5
        self.ips = ips
        # Informations supplémentaires (cibles ponctuelles ou origine des satellites notamment)
        self.added = added
    
    def __str__(self):
        if not self.name :
            return ""
        return "_".join((
            self.name,
            str(self.nsat)+"x"+str(self.nplan),
            str(self.inc),
            str(self.alt),
            str(self.ips),
            str(self.res),
            self.added
            )).strip("_")

    def name_with_res(self, res) :
        if not self.name :
            return ""
        return "_".join((
            self.name,
            str(self.nsat)+"x"+str(self.nplan),
            str(self.inc),
            str(self.alt),
            str(self.ips),
            str(res),
            self.added
            )).strip("_")
    
    def name_with_ips(self, ips) :
        if not self.name :
            return ""
        return "_".join((
            self.name,
            str(self.nsat)+"x"+str(self.nplan),
            str(self.inc),
            str(self.alt),
            str(ips),
            str(self.res),
            self.added
            )).strip("_")
    
    def nb_sat(self):
        return self.nsat*self.nplan
