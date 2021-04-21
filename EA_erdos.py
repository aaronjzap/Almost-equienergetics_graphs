import time
import numpy as np
import networkx as nx
import math
import random
import matplotlib.pyplot as plt
import copy
from scipy import linalg as LA
import sympy
from mpmath import mp
from Crossover import*
from comunes import*

from operaciones_matrices import*
mp.dps = 200



def Generar_poblacion(total,nodos):
    poblacion=[]
    probabilidades=np.linspace(0.5,1,total)
    valores_propios=[]
    for p in probabilidades:
        ws=nx.erdos_renyi_graph(nodos,p)
        m=Crear_matriz(ws, nodos)
        poblacion.append(m)  
    return poblacion
    
    


def Erdos(tam_poblacion, nodos, funciones, generaciones, operador_cruza, operador_mutacion, coef_cruza, coef_mutacion, EPS):
   
    P_t = Generar_poblacion(tam_poblacion,nodos)
    Energias, valores_propios =Evaluar(P_t, funciones)
    P, Energias,valores_propios, minimo = EA_erdos(P_t, Energias,valores_propios, tam_poblacion, nodos, funciones, generaciones, operador_cruza, operador_mutacion, coef_cruza,coef_mutacion, EPS)
    return  P, Energias,valores_propios, minimo
   
  




def EA_erdos(P_t, Energias, valores_propios, tam_poblacion, nodos,funciones, max_generaciones,operador_cruza, operador_mutacion, coef_cruza,coef_mutacion, EPS):
    
    L_P=Convert2list(P_t) 
    lon=len(L_P[0]) 
    parejas=Seleccion_padres(Energias,len(Energias)) 
    g=0
    minimo=[]
    while g< max_generaciones:
        print(g,"------")
        L_Q=Cruza(L_P,parejas, operador_cruza,coef_cruza,lon)
        L_Q=Mutacion(L_Q, operador_mutacion,lon, coef_mutacion)
        L=L_P+L_Q
        Q_t=Convert2Matrix(L_Q, nodos)
        M=P_t+Q_t
        Energias_Q, valores_propios_Q=Evaluar(Q_t,funciones)
        Energias=Energias+Energias_Q
        valores_propios= valores_propios+valores_propios_Q
        indices,valor = Seleccion_survivor(Energias, M,valores_propios, nodos, len(Energias), tam_poblacion, EPS)
        P_t, L_P, Energias,valores_propios = Separar(indices, M, Energias, L, valores_propios)
        parejas=Seleccion_padres(Energias,len(Energias)) 
        minimo.append(valor)
        g+=1
    return  P_t, Energias, valores_propios, minimo

