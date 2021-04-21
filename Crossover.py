import numpy as np
import random
import copy
import math



#Cruza-------------------------------------------------------



def Cruza_punto(X,Y, n):
    pivote1=random.randint(1, n-2)
    H1=X[:pivote1] +Y[pivote1:]
    H2= Y[:pivote1] + X[pivote1:]
    return [H1, H2]
    
    
def Adaptation(X,Y,n):
    if random.random()<0.5:
        H=Cruza_Uniforme(X,Y, n)
    else:
        H=Doble_punto(X,Y,n)
    return H




def Cruza_Uniforme_random(X,Y,n,m=10):
    XX=X.copy()
    YY=Y.copy()
    indices=random.sample(range(0,n-1),coef)
    for i in indices:
        XX[i]=YY[i]
    indices=random.sample(range(0,n-1),coef)
    for i in indices:
        YY[i] = XX[i]
    return [XX, YY] 
    
    
    
    
    
    
def Uniform(X,Y,n):
    XX=X.copy()
    YY=Y.copy()
    for i in range(0,n,2):
        XX[i]=YY[i]
    for i in range(1,n,2):
        YY[i] = XX[i]
    return [XX, YY] 
    
    
    
    




def Doble_punto(X,Y, n):
    pivote1=random.randint(1, n-10)
    pivote2=random.randint(pivote1, n-2)
    H1=copy.deepcopy(X)
    H2=copy.deepcopy(Y)
    H1[pivote1:pivote2]=copy.deepcopy(Y[pivote1:pivote2])
    H2[pivote1:pivote2]=copy.deepcopy(X[pivote1:pivote2])
    return [H1, H2]




def Half_uniform(X,Y,tam):
    diferentes=[ i for i in range(0,tam) if not(X[i]==Y[i])]
    H1, H2= copy.deepcopy(X), copy.deepcopy(Y)
    d=len(diferentes)
    if d>=2:
        t=int(d/2)
        for d in diferentes[:t]:
            H1[d]=H2[d]
        for d in diferentes[t:]:
            H2[d]=H1[d]
    return [H1,H2]



def Reduced_surrogate(X,Y,tam):
    diferentes=[ i for i in range(0,tam) if not(X[i]==Y[i])]
    H1, H2= copy.deepcopy(X), copy.deepcopy(Y)
    if not(diferentes==[]):
        pivote1=random.choice(diferentes)
    
        H1[pivote1:]=copy.deepcopy(Y[pivote1:])
        H2[:pivote1]=copy.deepcopy(X[:pivote1])
    return [H1,H2]



def Shuffle_crossover(X,Y,n):
    [H1,H2]= Cruza_punto(X,Y,n)
    H1=H1[::-1]
    H2=H2[::-1]
    return [H1, H2]
    
    
    
    


                
   
#precision, longitud de la subcadena binaria, limite superior ya que el limite inferior sera cero siempre.             
                

def Binario2real(lista, n, precision, logitud, lim):
    Y=[]
    for i in range(0,n-longitud,longitud ):
        real=Binario2decimal(X[i,i+longitud],logitud,lim)
        Y.append(real)
    return Y
        
    
#%-----------------------Mutacion 
def Mutacion_punto(X, n,coef=1):
    indices=random.sample(range(0,n-1),coef)
    for i in indices:
        if X[i]==1:
            X[i]=0
        else: 
            X[i]=1
    return X
      
  

def Hibrida(X, n,coef=1):
    validos = set(range(0,n-1))
    indices=random.sample(validos,2)
    d= validos - set(X)
    if d!={}:
        #print("----",len(set(X)))
        if X[indices[0]]== X[indices[1]]:
            Y= validos-{X[indices[1]]}
            Z=random.sample(Y,1)
            X[indices[0]]= Z[0]
            #print("-~~~~~~~~~~~~~~~~~~~+-")
        #print(len(set(X)))
        
    else:
        X[indices[0]]=X[indices[1]]
    return X






def Mutacion_intercambio(X, n,coef=1):
    for i in range(coef):
        indices=random.sample(range(0,n-1),2)
        aux=X[indices[0]]
        X[indices[0]]=X[indices[1]]
        X[indices[1]]=aux
    return X



def Mutacion_choice(X, n,coef=1):
    indices=random.sample(range(0,n-1),coef)
    for i in indices:
       X[i]=random.choice(range(n))
    return X




