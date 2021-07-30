import PyPDF2 
import re
import csv
def extraer():
  pdfFileObj = open('dic.pdf', 'rb') 
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
      
  # Numero de paginas de PDF "pdfReader.numPages" 
  for i in range(pdfReader.numPages):    
    pageObj = pdfReader.getPage(i) 
        
    # Extraer texto de la pagina
    text = pageObj.extractText()
    text = re.findall('(\w+\s\w+|\w+)\s\[',text)

    with open('prueba.csv', 'a', encoding="utf-8") as archivo:
      for x,i in enumerate(text):
        archivo.write(i.replace(' [','')+"\n")
  pdfFileObj.close() 

def comparar():
  dic1 = []
  prueba = []
  with open('dic1.csv', 'r',encoding='utf-8') as csvfile:
    leer = csv.DictReader(csvfile, delimiter=',')
    for row in leer:
      dic1.append(row['Kichwa'])
  with open('prueba.csv', 'r',encoding='utf-8') as txtfile:
    for txt in txtfile.readlines():
      prueba.append(txt.strip('\n'))
  
  #comparar
  cont = 0
  with open('total.csv', 'a', encoding="utf-8") as archivo:        
    for d1 in prueba:
      tmp = False
      for p in dic1:
        if(p == d1):
          tmp = True
          break
      if not tmp:
        cont+=1  
        print("la palabra no se encontro: "+d1)
        archivo.write(str(cont+2419)+","+d1+"\n")
    
    print("Dic1: "+ str(len(dic1))+ " Prueba: "+str(len(prueba))+" Cantidad: "+str(cont))

  
#extraer()
#comparar()