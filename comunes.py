import time
import numpy as np
import networkx as nx
import math
import random
import copy
from Crossover import*
from operaciones_matrices import*
from collections import Counter
from itertools import chain



def Evaluar(P_t,F):
    aptitud, valores_propios=[],[]
    for p in P_t:
        e,x=F(p) 
        aptitud.append(e)
        valores_propios.append(x)
    return aptitud,valores_propios
  
    
     
    
        
def Cruza(P_t,parejas ,operador_cruza,coef_cruza, n):
    hijos=[]
    for par in parejas:
        X=P_t[int(par[0])].copy()
        Y=P_t[int(par[1])].copy()
        if random.random()<coef_cruza:
            hijos+=list(operador_cruza(X,Y, n))            
        else:
            lista=[X, Y]
            hijos+=lista
    return hijos
    
    
    
def Mutacion(poblacion,operador_mutacion,n, coef):
    nueva_poblacion=[operador_mutacion(individuo, n, coef) for individuo in poblacion]
    return nueva_poblacion
 


def Energia(matriz):    
    x = np.linalg.eigvals(matriz)
    e=np.sum(np.abs(x))
    x.sort()
    return e,x







   
  
def Separar(indices, M, Energias, L, grados):
    P_t= [M[i] for i in indices]
    L_P= [L[i] for i in indices]
    Energias= [Energias[i] for i in indices]
    g= [grados[i] for i in indices]
    return P_t, L_P, Energias , g

   
   

   
   

   

def Isomorfia_rapida( pares, vectores_propios):
    validos=[]
    sobras= []
    for conjunto, vectores in zip(pares, vectores_propios):
        sub_validos=[]
        tam=len(conjunto)
        for i in range(tam-1):
            indicador=True
            x = vectores[i]
            for j in range(i+1,tam):
                y = vectores[j]
                x.sort()
                y.sort()
                dif=sum(abs(x-y))
                if dif<0.000001:
                    
                    indicador=False
                    continue
                
            if indicador:
                sub_validos.append(conjunto[i])
        if sub_validos!=[]:
            sub_validos.append(conjunto[-1])
            validos.append(sub_validos)
        else: 
            sobras.append(conjunto[-1])
    return validos, sobras
                
                
                
       
def Conexidad(indices, Matrices, sobras,n):
    validos=[]
    for conjunto, matrices in zip(indices, Matrices):
        sub_validos=[]
        for i in range(len(conjunto)):
            H=Crear_grafica(Obtener_aristas(matrices[i],n))
            m= nx.number_connected_components(H)
            if m==1:
                sub_validos.append(conjunto[i])
                
        tam= len(sub_validos)
        if tam>1:  
            validos.append(sub_validos)
        elif tam == 1:
            validos.extend(sub_validos)
            
    return validos, sobras
                
        
   

            
            
def Secuencias(Aux, EPS):
    indices=[]
    ant=Aux[0][1]
    aux_in=[ant]
    for act,sig in zip(Aux, Aux[1:]):
        diff= sig[0]-act[0]
        if diff<EPS:
            if act[1]==ant:
                aux_in.append(sig[1])
            else:
                aux_in=[act[1], sig[1]]
            ant=sig[1]
        else:
            indices.append(aux_in)
    return indices



         
def Conex(sobras, SM, n):
    new=[]
    for index, M in zip(sobras, SM):
        H=Crear_grafica(Obtener_aristas(M,n))
        m= nx.number_connected_components(H)
        if m==1:
           new.append(index)
    return new




    
def Rapida(Energias, pares, eigen_vectores, P,n, modo, EPS = 1.0e-8):
    index=[i for ind in pares for i in ind]
    index=list(set(index))
    Ene= [Energias[i] for i in index]
    Aux=list(zip( Ene, index))
    Aux.sort()
    indices= Secuencias(Aux, EPS)
    
    vectores_propios=[]
    for conjunto in indices:
        ve = [eigen_vectores[i]  for i in conjunto]
        vectores_propios.append(ve)
    
    validos, sobras= Isomorfia_rapida(indices, vectores_propios)
    if modo !="Tree":
        Matrices=[]
        for val in validos:
            sub= [P[v] for v in val]
            Matrices.append(sub)
            
        SM=[]
        for v in sobras:
            SM.append(P[v])
        sobras= Conex(sobras, SM, n) 
        validos, sobras = Conexidad(validos, Matrices, sobras, n)
        
    return validos, sobras






   








def Calcular_distancias(Energias, tam_poblacion):
    aux=[(e, int(i)) for  i,e in enumerate(Energias)]
    aux.sort()    
    distancias=[(abs(aux[i+1][0]-aux[i][0]),[aux[i+1][1],aux[i][1]]) for i in range(tam_poblacion-1) ]    
    distancias.sort()
    return distancias
    
def Posibles_almost(distancias, tam_poblacion, EPS):
    j=0
    pares=[]
    while j< tam_poblacion-1 and distancias[j][0] <EPS :
          par=distancias[j][1]
          pares.append(par)
          j+=1
    return pares, j
          


   
def Seleccion_survivor(Energias,P,Eigen,n, tam_poblacion, mitad, modo, EPS = 1.0e-8):    
    validos, sobras, distancias,j = Almost(Energias, tam_poblacion, Eigen, P, n, modo, EPS)
    uno_uno=[v for val in validos for v in val]
    indices = set(uno_uno)|set(sobras) 
    
    if j<tam_poblacion-1:
        v=len(uno_uno)
        print(distancias[j][0], len(uno_uno))   
        while len(indices)<mitad and j<tam_poblacion-2:
            indices = indices| set(distancias[j][1])
            j+=1
        indices=list(indices)
        return indices, v
    else:
        return indices[:tam_poblacion], tam_poblacion
    
      


def Almost( Energias, tam_poblacion, Eigen, P,n, modo, EPS):
    distancias= Calcular_distancias(Energias, tam_poblacion)
    indices, ind=[],[]
    pares, j= Posibles_almost(distancias, tam_poblacion, EPS)
    uno_uno=[]
    if pares!=[]:
        validos, sobras= Rapida(Energias, pares, Eigen, P,n, modo,  EPS)
        return validos, sobras, distancias, j
    else: 
        return [], [], distancias, j
     



def Seleccion_padres(Energias,tam_poblacion):
    mitad=int(tam_poblacion/2)
    validos=list(range(0,tam_poblacion))
    muestras= random.sample(validos, mitad)
    parejas=[]
    for m in muestras:
        [i,j]= random.sample(validos, 2)
        if abs(Energias[i]-Energias[m])<abs(Energias[m]-Energias[j]):
            parejas.append([m,i])
        else:
            parejas.append([m,j])
            
    return parejas



