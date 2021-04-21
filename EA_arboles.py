import time
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import copy
from Crossover import*
from comunes import*

from operaciones_matrices import*
from collections import Counter
from itertools import chain

def nuevo_trees(sequence):
    n = len(sequence) + 2
    degree = Counter(chain(sequence, range(n)))
    T = nx.empty_graph(n)
    M = np.zeros((n,n))
    not_orphaned = set()
    index = u = next(k for k in range(n) if degree[k] == 1)
    nodos= set([])
    for v in sequence:
        T.add_edge(u, v)
        not_orphaned.add(u)
        M[u][v]=1
        M[v][u]=1
        degree[v] -= 1
        if v < index and degree[v] == 1:
            u = v
        else:
            index = u = next(k for k in range(index + 1, n) if degree[k] == 1)
    # At this point, there must be exactly two orphaned nodes; join them.
    orphans = set(T) - not_orphaned
    u, v = orphans
    M[u][v]=1
    M[v][u]=1
    return M



def Generar_poblacion_arboles(total,n, seed=None):
    poblacion, S=[], []
    for i in range(total):
        sequence = [random.choice(range(n)) for i in range(n-2)]
        S.append(sequence)
        arbol=nx.from_prufer_sequence(sequence)
        m=Grafo2matriz(arbol, n)
        poblacion.append(m)
        
       
    return poblacion, S
    
    





def Arboles(tam_poblacion, nodos, funciones, generaciones, operador_cruza, operador_mutacion, coef_cruza, coef_mutacion, EPS):
   
    P_t, S = Generar_poblacion_arboles(tam_poblacion,nodos)
    Energias, valores_propios =Evaluar(P_t, funciones)
    P, Energias,valores_propios, minimo = EA_arboles(P_t, Energias,valores_propios, S, tam_poblacion, nodos, funciones, generaciones, operador_cruza, operador_mutacion, coef_cruza,coef_mutacion, EPS)
    return  P, Energias,valores_propios, minimo
   
  







def EA_arboles(P_t, Energias, valores_propios, S, tam_poblacion, nodos,funciones, max_generaciones,operador_cruza, operador_mutacion, coef_cruza,coef_mutacion, EPS):
    
    g=0
    L_P=S 
    lon=len(L_P[0]) 
    minimo =[]
    parejas=Seleccion_padres(Energias,len(Energias)) 
    while g< max_generaciones:
        print(g)
        L_Q=Cruza(L_P,parejas, operador_cruza,coef_cruza,lon)
        L_Q=Mutacion(L_Q, operador_mutacion,lon, coef_mutacion)
    
        L=L_P+L_Q
        
        Q_t= [nuevo_trees(sequence) for sequence in L_Q]
        M=P_t+Q_t
     
        Energias_Q, valores_propios_Q = Evaluar(Q_t,funciones)
        Energias=Energias+Energias_Q
        valores_propios= valores_propios+valores_propios_Q
        indices,valor = Seleccion_survivor(Energias, M,valores_propios, nodos, len(Energias), tam_poblacion, "Tree", EPS)
        P_t, L_P, Energias,valores_propios = Separar(indices, M, Energias, L, valores_propios)
        parejas=Seleccion_padres(Energias,len(Energias)) 

        minimo.append(valor)
        g+=1
    return  P_t, Energias, valores_propios, minimo








   
