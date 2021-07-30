import csv
import re
import numpy as np
import json
import math,nltk
import tokenizar as tk
from nltk.corpus import stopwords
nltk.download( 'stopwords' )
#STOPWORDS y STEAMMING
sw = stopwords.words('spanish')
#st = SnowballStemmer('spanish')

#---------------------
#---- LEER CSV -------
#---------------------
def leer():
    vpos = []
    vneu = []
    vneg = []
    with open('BP.csv', 'r', encoding = "utf-8") as archivo:
      fila = csv.DictReader(archivo, delimiter=',')
      for row in fila:
          if row['enfoque'] == 'MODELO BIO MEDICO':
              vpos.append(row['palabra'].lower())
          elif row['enfoque'] == 'ENFOQUE PSICOSOCIAL - COMUNITARIO':
              vneu.append(row['palabra'].lower())
          elif row['enfoque'] == 'ENFOQUE COTIDIANO':
              vneg.append(row['palabra'].lower())
    return vpos,vneu,vneg

#---------------------
#----- PROCESOS ------
#---------------------
def metodo(frase):
    copia = frase
    #------- NLP --------
    frase = frase.lower()
    frase = re.sub('[^A-Za-zñ]+', ' ', frase)
    frase = frase.split()
    #STOPWORDS
    for i in range(len(frase)):
        for w in frase:
            if w in sw:
                #print(word)
                frase.remove(w)
    #print(frase)
    
    vpos,vneu,vneg = leer()
   
    frase = tk.toke(frase,len(frase),[vpos,vneu,vneg])
    print(frase)
    # jaccard positivos neutro positivo
    p = jaccard(frase,[vpos,vneu,vneg])
    #coseno positivos neutro positivo
    cose = np.array([coseno([frase],vpos),coseno([frase],vneu),coseno([frase],vneg)])
    print("coseno:")
    print(cose)
    temp = 1 if  (cose == 0).all() else np.where(cose == np.max(cose))[0][0]
    return json.dumps({'frase':copia,'jaccard':'MODELO BIO MEDICO' if p == 0 else ( 'ENFOQUE PSICOSOCIAL - COMUNITARIO' if p == 1  else 'ENFOQUE COTIDIANO'),'coseno': 'MODELO BIO MEDICO' if temp == 0 else ( 'ENFOQUE PSICOSOCIAL - COMUNITARIO' if temp == 1  else 'ENFOQUE COTIDIANO')})


#---------------------
#------ JACCARD ------
#---------------------
def jaccard(v1,v2):
    matrizjacc = []
    for valor in v2:
        a=set(v1)
        b=set(valor)
        union=a.union(b)
        inter=a.intersection(b)
            
        if len(union)==0:
            if len(inter)==0:
                return -1

        similitud=len(inter)/len(union)
        matrizjacc.append(similitud)
    print("jaccard:")
    print(matrizjacc)
    temp = np.array(matrizjacc)
    if  (temp == 0).all():
        return 1
    else:
        return np.where(temp == np.max(temp))[0][0]


#--------------------
#------ COSENO ------
#--------------------
def coseno(documento,vocabulario):
    documento.insert(0,vocabulario)
    documento.insert(2,documento)
    #lista = [[ vocabulario.append(m) for m in h if m not in vocabulario] for h in documento]
    N = len(documento)
    cuenta=[]
    WTF = []
    idf=[]
    idf_tf = []
    for k in range(len(vocabulario)):
        pal = vocabulario[k]
        a1 = [pe(tok.count(pal)) for tok in documento]
        
        df = 0
        for i in a1:
            if i != 0:
                df += 1
        
        op= [e * idf_M(N, df) for e in a1]
        idf_tf.append(op)

    modul = []
    for i in range(len(idf_tf[0])):
        t = 0
        for j in range(len(idf_tf)):
            t += idf_tf[j][i] ** 2
        modul.append(m(t))
    
    logaritmo = [[resM(idf_tf[j][i], modul[i]) for j in range(len(idf_tf))]for i in range(len(idf_tf[0]))]
    matrizT = [[cose(ks, kr) for ks in logaritmo] for kr in logaritmo]
    return np.array(matrizT)[1, 0]


def pe(n):
    if n > 0:
        return round(1 + math.log10(n), 2)
    else:
        return 0

def idf_M(n, df):
    if df > 0:
        return round(math.log10(n/df), 3)
    else:
        return 0

def m(j):
    return math.sqrt(j)


def cose(h1, h2):
    return round(sum(h1[i] * h2[i] for i in range(len(h1))), 2)

def resM(h1,m):
    if m == 0:
        return 0
    else:
        return round(h1/m,3)