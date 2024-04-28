import pandas as pd
import datetime
import math
import random

# Ruta a la lista de estaciones
ruta_stn="./datos_post/Estaciones.csv"
#Ruta a los datos de estaciones
ruta_data="./datos_post/"




#punto ignicion
#y_i= -37.39694
y_i= float(input("Ingrese la latitud en cordenadas geograficas (ejm: -36.0): "))
#x_i= -72.42389
x_i= float(input("Ingrese la longitud en cordenadas geograficas (ejm: -72.0): "))
count= int(input("Ingrese el numero de escenario que desea: "))
T= int(input("Cuantas horas debe durar casa escenario? "))

dn=3


"""
funciones
"""
def distancia(fila,y_i,x_i):
    if y_i==fila["lat"] and x_i== fila["lon"]:
        dis=0
    else:
        dis=math.sqrt((fila["lat"]-y_i)**2+(fila["lon"]-x_i)**2)
    return dis

def meteo_to_c2f(alfa):
    if alfa>=0 and alfa<180:
        theta=alfa+180
    elif alfa>=180 and alfa<=360:
        theta=alfa-180
    else:
        theta=math.nan
    return theta


#abrir archivos
list_stn=pd.read_csv(ruta_stn)
#calcula distancia al punto de ignicion
list_stn["Distancia"]=list_stn.apply(distancia,args=(y_i,x_i), axis=1) #calculo distancia
#Selecciona por distancia
aux=list_stn.sort_values(by=["Distancia"]).head(dn)
estaciones=aux["nombre"].tolist()


meteo=[]
for i in range(len(estaciones)):
    station=estaciones[i]+".csv"
    data=pd.read_csv(ruta_data+station, sep=',')#, index_col=0, parse_dates=True)
    meteo.append(data)


for i in range(count):
    j=random.randint(0,dn-1)
    n = len(meteo[j]["TMP [Cº]"]) - T
    m = random.randint(0, n)

    alpha = []
    for x in meteo[j]["WD [º]"].iloc[m:m + T].tolist():
        alpha.append(meteo_to_c2f(i))



    weather = pd.DataFrame()
    weather["Scenario"] = ["DMC "+str(i+1)] * T
    weather["datetime"] = meteo[j]["datetime"].iloc[m:m + T].tolist()
    weather["WS"] = meteo[j]["WS [km/h]"].iloc[m:m + T].tolist()
    weather["WD"] = alpha
    weather["TM"] = meteo[j]["TMP [Cº]"].iloc[m:m + T].tolist()
    weather["RH"] = meteo[j]["RH [%]"].iloc[m:m + T].tolist()

    # print(weather)
    weather.to_csv("weather"+str(i+1)+".csv", index=False)

