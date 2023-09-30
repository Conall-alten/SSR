import numpy as np
print("-----------------------------------------")
print("Partie 0 du code : Le choix des hypothèses, des spécificités et définition de labase de donnée")
print("-----------------------------------------")
print(" ")

hypothese_poids = 1 # 1=prit en compte ou 0 = inactif
hypothese_conso = 1 # 1 ou 0
hypothese_cout = 0 # 1 ou 0


req_origine = "europe" #europe / france / osef
req_pousse = 20 #en Newton
req_ISP = 290 #en s

europe = ["France","Allemagne","Belgique","Italie","Espagne"]

entete = ["nom","poids(kg)","consomation(W)","cout(€)","origine(pays)","ISP(s)","poussée(N)"]
m1 = ["OmeletteFromage",0.7,2,4000,"France",250,20]
m2 = ["Jaeger1000",0.8,5,5000,"Allemagne",320,22]
m3 = ["Gun&Engine",2,3,3500,"USA",350,50]
m4 = ["Cocorico_Max",0.6,1.5,3500,"France",300,15]
m5 = ["FriteSat",0.5,0.5,3500,"Belgique",300,19]
m6 = ["BierePousseur",1.2,2.3,7000,"Belgique",291,30]
m7 = ["BigBurger",1.4,6,5000,"USA",300,30]
m8 = ["Fraternité_7",1.4,3,5000,"France",300,30]
mot = [m1,m2,m3,m4,m5,m6,m7,m8]

print("Liste initiale, avec",len(mot),"moteurs:")
print(" ")
for x1 in range(len(mot)):
    print(mot[x1])
print(" ")

print("-----------------------------------------")
print("Partie 1 du code : Le tri initial")
print("-----------------------------------------")
print(" ")
#la partie 1 s'occupe de gérer les paramètres spécifiques aux composants.
#c'est ici qu'on exclue ce qui n'est pas compatible avec le CDC (Cahier des Charges)
l1 = len(mot)
x=0
while x < l1:
    #première boucle pour retirer les cas hors scope
    try:
        if mot[x][6]<req_pousse:
            #ici on regarde la poussée, si c'est trop bas on retire la ligne
            #et on reprend à la ligne 0
            del mot[x]
            x=0
        elif mot[x][5]<req_ISP:
            #ici on regarde l'ISP, si c'est trop bas on retire la ligne
            #et on reprend à la ligne 0
            del mot[x]
            x=0
        elif req_origine == "europe":
            #ici on regarde l'origine, si pas en europe on retire la ligne
            #et on reprend à la ligne 0
            #sinon on avance
            if mot[x][4] not in europe:
                del mot[x]
                x=0
            else:
                x+=1
        elif req_origine == "france":
            #ici on regarde l'origine, si pas en france on retire la ligne
            #et on reprend à la ligne 0
            #sinon on avance
            if mot[x][4] != "France":
                del mot[x]
                x=0
            else:
                x+=1
        else:
            #cas osef pour les necessités
            x+=1         
    except:
        break
    if len(mot)==0:
        print("Pas de moteur disponible sous ces conditions")

#maintenant la liste "moteur" n'a que les élements compatible avec le CDC
#il s'agit de la liste candidat
print("Liste après tri, il reste",len(mot),"moteurs en compétition:")
print(" ")
for x1 in range(len(mot)):
    print(mot[x1])
print(" ")
#%%
print("-----------------------------------------")
print("Partie 2 du code : La comparaison")
print("-----------------------------------------")
print(" ")
#la partie 2 s'occupe de géré prendre de compte les hypothèses de choix.
#c'est ici qu'on choisi lequel est le meilleur
poids = [0]*len(mot)
cout = [0]*len(mot)
isp = [0]*len(mot)
poussee = [0]*len(mot)
conso = [0]*len(mot)

for x in range(len(mot)):
    poids[x]=mot[x][1]
    conso[x]=mot[x][2]
    cout[x]=mot[x][3]
    isp[x]=mot[x][5]
    poussee[x]=mot[x][6]

#ici on normalise par le max de la série candidat pour que tou soi comparable
Poids = np.array(poids)
Poids = Poids/max(Poids)
Conso = np.array(conso)
Conso = Conso/max(Conso)
Cout = np.array(cout)
Cout = Cout/max(Cout)
ISP = np.array(isp)
ISP = ISP/max(ISP)
Poussee = np.array(poussee)
Poussee = Poussee/max(Poussee)

#ici on prend en compte les hypothèses
#le cas particulier où tt les hypothèses sont nulles,
#alors on cherche le plus proche possible des caractéristiques spécifiques
#ici pour un moteur ISP et Poussée
if hypothese_poids==0 and hypothese_conso==0 and hypothese_cout==0:
    score = ISP+Poussee
else:
    score = hypothese_poids*Poids + hypothese_conso*Conso + hypothese_cout*Cout

score_min = min(score)
index_min = [i for i, x in enumerate(score) if x==score_min]

resultat = [0]*len(index_min)
for x in range(len(index_min)):
    resultat[x]=mot[index_min[x]]
    
print("Voici le(s) meillieur(s) moteur(s):")
print(" ")
for x1 in range(len(resultat)):
    print(resultat[x1])
print(" ")