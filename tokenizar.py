import re

def toke(conjunto,index,etiquetas):
    if index == 0:
        return
    else:
        print("INDEX: "+str(index))
        inicio = 0
        fin = 0
        while fin < len(conjunto)-1:
            fin = inicio + (index-1)
            temp = [conjunto[i] for i in range(inicio,fin+1)]
            temp = " ".join(temp)
            pos = find(etiquetas,temp)
            if pos != -1: 
                conjunto[inicio:fin+1] = [temp]
            print("inicio: "+str(inicio)+ " fin: "+str(fin) + " palabras: "+temp+ " pos: "+str(pos))
            
            inicio += 1
        toke(conjunto,index-1,etiquetas)
    return conjunto
        
def find(etiquetas,temp):
    pos = 0
    try:
        pos = etiquetas[0].index(temp)
        return pos
    except:
        pos = -1
    try:
        pos = etiquetas[1].index(temp)
        return pos
    except:
        pos = -1
    try:
        pos = etiquetas[2].index(temp)
        return pos
    except:
        pos = -1
    return pos