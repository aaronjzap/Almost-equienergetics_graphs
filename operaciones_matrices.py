import random
import numpy as np
import networkx as nx




def Grafo2matriz(ws,n):
    matriz=np.zeros((n,n))
    edges=ws.edges()
    for e in edges:
        matriz[e[0]][e[1]]=1
        matriz[e[1]][e[0]]=1
    return matriz





def Crear_matriz(ws, n):
    matriz=np.zeros((n,n))
    edges=ws.edges()
    for e in edges:
        matriz[e[0]][e[1]]=1
        matriz[e[1]][e[0]]=1
    return matriz



def Obtener_aristas(matriz, n):
    Aristas=[]
    for i in range(n):
        for j in range(i+1,n):
            if matriz[i][j]!=0:
                Aristas.append((i,j))
    return Aristas

    

def Crear_grafica(graph):
    G=nx.Graph()
    nodos=set([n1 for n1,n2 in graph]+[n2 for n1,n2 in graph])
    for nodo in nodos:
        G.add_node(nodo)
      
    for edge in graph:
            G.add_edge(edge[0],edge[1])
    edges=G.edges()
    return G





def Convert2list(P_t):
    L=[ reordenar(p) for p in P_t]
    return L

def Convert2Matrix(P_t, n):
    matriz=[ Lista2Matriz(p, n) for p in P_t]
    return matriz
    
def reordenar(matriz):
    elementos=[l for i, lista in enumerate(matriz) for l in lista[int(i+1):]]
    return elementos

    
def Lista2Matriz(lista, n):
    matriz=np.zeros((n,n))
    inicio=0
    fin=n-1

    for  i in range(n):
        matriz[i, i+1:n]=lista[inicio: fin]
        matriz[ i+1:n, i]=lista[inicio: fin]
        inicio=fin
        fin+=n-i-2
    return matriz


