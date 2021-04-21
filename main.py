import pickle
import time
from EA_arboles import*
from EA_erdos import*
from Crossover import*
import copy
from comunes import*
from operaciones_matrices import*



def Contar(indices, Energias, EPS):
    equ=[]
    cuasi=[]
    for conjunto in indices:
        i=conjunto[0]
        j=conjunto[1]
        dif= abs(Energias[i]-Energias[j])
        if dif< 1.0e-13:
            equ.append(conjunto)
        else:
            cuasi.append(conjunto)
    return  cuasi, equ




def Separacion(pares, P, Energias):
    for p in pares:
        for i in p:
           x,v= Energia(P[i])        
    return [(P[x[0]], P[x[1]]) for x in pares]





def Cargar_datos(nombre):
    f=open(nombre,"rb")
    lista=[]
    try:
        while True:
            x=pickle.load(f)
            lista.append(x)
    except EOFError:
        pass
    f.close()
    return lista
  
  
  
  
  
def Experimets(generaciones, nodos, tam_poblacion, ejecuciones, cruza,coe, coef_mutacion, mutacion, Algoritmo,modo,  EPS):
    rangos, difs, Equs,cs, Total= [],[],[],[],[]
    inicio= time.time()
    Nombre1="Cuasi_"+str(nodos)+".pkl"
    Nombre2="Equi_"+str(nodos)+".pkl"
    Cuasi_equienergic=open(Nombre1,"bw")
    Equienergic=open(Nombre2,"bw")
    convergencia=open("Convergencia"+str(nodos)+".pkl", "bw")
    contar=[]
    for i in range(ejecuciones):
            print("Run:",i)
            inicio=time.time()
           
            P, Energias, Eigen, minimos = Algoritmo(tam_poblacion,nodos, Energia,generaciones,cruza, mutacion,coe,coef_mutacion, EPS)
            aux= copy.deepcopy(Energias)
            aux.sort()
            aux2= [abs(aux[i+1]-aux[i]) for i in range(len(aux)-1)]
            aux2.sort
            
            
            cuasi, sobras, distancias,j = Almost(Energias, tam_poblacion, Eigen, P, nodos, modo, EPS)
            total=[v for val in cuasi for v in val]
            
            cuasi, Equ = Contar(cuasi, Energias, EPS)
            Equs.append(len(Equ))
            cs.append(len(cuasi))
            Total.append(total)
            pickle.dump(minimos, convergencia)
            pickle.dump(Separacion(cuasi, P, Energias), Cuasi_equienergic)
            pickle.dump(Separacion(Equ, P, Energias), Equienergic)
            
    print("---------------------------\n\n\n")    
    print("Cuasi-equienergeticas: ",round(np.mean(cs),5),"$\\pm$", round(np.std(cs),5), "\nEquienergeticas:", round(np.mean(Equs),5),"$\\pm$",round(np.std(Equs),5))
    print("Total", round(np.mean(total),5), "\pm", round(np.std(total),5))
    
    
    Cuasi_equienergic.close()
    Equienergic.close()
    convergencia.close()
    return Nombre1, Nombre2, np.mean(Total)







def Proscarga(ejecuciones, n):
    for poblacion in ejecuciones:
        print("Graficas encontradas en la ejecucion:", len(poblacion))
        print("----------------------------------")
        for p in poblacion:
            x=p[0]
            y=p[1]
            
            xx= Crear_grafica(Obtener_aristas(x, n))
            yy= Crear_grafica(Obtener_aristas(y, n))
            x1,v1=Energia(x)
            x2,v2=Energia(y)
            values=abs(v1)/sum(abs(v1))
            
            #nx.draw(xx, cmap = plt.get_cmap('jet'), node_color = values, label=True)
            v1.sort()
            v2.sort()
            print("Energia 1:",x1,"\nEnergia 2:",x2, "\nDifferencia",sum(abs(v1-v2)))
            #plt.show()
            
            
            
    if len(poblacion)>0:
        print("Dibujemos un ejemplo :)")
        ejemplo=poblacion[0]
        x=ejemplo[0]
        y=ejemplo[1]
        xx= Crear_grafica(Obtener_aristas(x, n))
        yy= Crear_grafica(Obtener_aristas(y, n))
        nx.draw(xx, cmap = plt.get_cmap('jet'), node_color = values, label=True)
        plt.show()
        nx.draw(yy, cmap = plt.get_cmap('jet'), node_color = values, label=True)
        plt.show()
        
        
        
        
def Convergency(Nombre):
    datos=Cargar_datos(Nombre)
    mitad = int(len(datos)/2)
    suma= [(sum(d), int(i)) for i,d in enumerate(datos)]
    suma.sort()
    indice= suma[mitad][1]
    datos=datos[indice]
    plt.plot(datos, linewidth= 5)
    plt.xlabel("Generations", size=12)
    plt.ylabel("$NG(P_f)$", size=13)
    plt.show()
    
    
    
    
    
    
    
    
    
def Run(Algoritmo,coe, coef_mutacion, tam_poblacion, nodos, generaciones, ejecuciones):
    EPS=1.0e-8
    if Algoritmo==Arboles:
        mutacion= Mutacion_choice
        #mutacion =Hibrida
        modo="Arboles"
    elif Algoritmo==Erdos:
        mutacion =Mutacion_punto
        modo= "Erdos"
    cruza= Adaptation 
    cruza=Cruza_punto
    cruza=Uniform
    inicial=time.time()
    Nombre1, Nombre2, media = Experimets(generaciones, nodos, tam_poblacion, ejecuciones, cruza,coe, coef_mutacion, mutacion, Algoritmo, modo, EPS)
    final= time.time()
    print("Tiempo_total=", final-inicial)
    return media
    
    
    
    
def subset_sum(numbers, target, partial=[]):
    s = sum(partial)

    # check if the partial sum is equals to target
    if s == target: 
        print ("sum(%s)=%s" % (partial, target))
    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]







def Measure(G):
    #e= nx.eccentricity(G)
    #diametro= nx. diameter( G, e=None, usebounds=False)
    #Estrada= nx.estrada_index(G)
    #reach= nx.global_reaching_centrality(G)
    Conec_n= nx.average_node_connectivity(G)
    
    clust=np.mean(list(nx.clustering(G).values()))
    
    m= len(G.edges())
    ei= np.mean(list(nx.eigenvector_centrality_numpy(G).values()))
    bet= np.mean(list(nx.betweenness_centrality(G).values()))
    #bet= np.mean(list(nx.communicability_betweenness_centrality(G).values()))
    ed= nx.edge_connectivity(G)
    no= nx.node_connectivity(G)
    cc= np.mean(list(nx.closeness_centrality(G).values()))
    return Conec_n, clust, m, ei, bet, ed, no, cc
    

def Proscarga(ejecuciones, n):
  
    for poblacion in ejecuciones:
        print("Graficas encontradas en la ejecucion:", len(poblacion))
        print("----------------------------------")
        
        diferencias, d_e, c,C_e, C_n, Ei, Bet, ED, NO, CC= [], [],[],[],[],[],[], [], [], []
        for p in poblacion:
            x=p[0]
            y=p[1]
            xx= Crear_grafica(Obtener_aristas(x, n))
            yy= Crear_grafica(Obtener_aristas(y, n))
            
            x1,v1=Energia(x)
            x2,v2=Energia(y)
            d_e.append(abs(x1-x2))
            
            
            Conec_n1, Conec_e1, m1, ei1, bet1, ed1, no1, cc1= Measure(xx)
            Conec_n2, Conec_e2, m2, ei2, bet2, ed2, no2, cc2= Measure(yy)
            diferencias.append(sum(abs(v1-v2)))
            C_n.append(abs(Conec_n1-Conec_n2))
            C_e.append(abs(Conec_e1-Conec_e2))
            Ei.append(abs(ei1-ei2))
            Bet.append(abs(bet1- bet2))
            ED.append(abs(ed1- ed2))
            NO.append(abs(no1-no2))
            CC.append(abs(cc1-cc2))

        
        print(np.corrcoef(diferencias, C_e)[0][1])
        print(np.corrcoef(diferencias, Bet)[0][1])
        print(np.corrcoef(diferencias, CC)[0][1])
        print(np.corrcoef(diferencias, Ei)[0][1])
        print(np.corrcoef(diferencias, ED)[0][1])
        print(np.corrcoef(diferencias, C_n)[0][1])
    

        







def Aleatorio(nodos):
    pares=[]
    P= Generar_poblacion(176,nodos)
    for uno, dos in zip(P[::1], P[1::2]):
        pares.append([uno, dos])
    return [pares]
    
    


if __name__ == "__main__":

    generaciones = 200
    nodos = 20
    tam_poblacion = 5000
    ejecuciones =1
    coe = 0.0
    coef_mutacion = 1
    
    Algoritmo= Erdos
    Algoritmo= Arboles
    inicio= time.time()
    media = Run(Algoritmo,coe, coef_mutacion, tam_poblacion, nodos, generaciones, ejecuciones)
    fin = time.time()
    
    
    
    
    Nombre1="Cuasi_"+str(nodos)+".pkl"
    Nombre2="Equi_"+str(nodos)+".pkl"
    Cuasi= Cargar_datos(Nombre1)
    Equi_energeticas= Cargar_datos(Nombre2)
    
    #Convergency("Convergencia"+str(nodos)+".pkl")
    ale= Aleatorio(nodos)
    Proscarga(ale, nodos)
    #Proscarga(Equi_energeticas, nodos)
    
