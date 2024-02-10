import os
from tkinter import *
import numpy as np
import cv2
import json


def showImages(images):
    for image in images:
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def pegaCalibragem(alvo):
    f = open("IC-Gemeo-master/Localização de Objetos - Mesa Real/calibragem.json")
    data = json.load(f)

#    valores = f.readlines()
    if(alvo == "p"):
        # c = valores[1].find('[')+1
        # s = valores[1].find(']')
        # l = valores[1][c:s].split()
        lower = np.array(data['peca']['lower'])
        upper = np.array(data['peca']['upper'])
        tamanhoMin = data['peca']['areaMin']
        tamanhoMax = data['peca']['areaMax']

    elif(alvo == "e"):
        lower = np.array(data['encaixe']['lower'])
        upper = np.array(data['encaixe']['upper'])
        tamanhoMin = data['encaixe']['areaMin']
        tamanhoMax = data['encaixe']['areaMax']

    return tamanhoMin, tamanhoMax,lower,upper

def getPosition(metodoContorno,alvo, path):

    tamanhoMin, tamanhoMax,lower,upper = pegaCalibragem(alvo)
    image = cv2.imread(path)
    image = cv2.resize(image, (int(image.shape[1] *0.5), int(image.shape[0] *0.5)))
    #maskedImage = calibrar(image)
    
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
    mask = cv2.inRange(imgHSV, lower, upper)
    maskedImage =  cv2.bitwise_and(image, image, mask=mask)

    img = maskedImage.copy()

    blur = cv2.GaussianBlur(img, (5,5), 0)
    im_bw = cv2.Canny(blur, 10, 90)


    contours, hierarchy = cv2.findContours(im_bw, metodoContorno, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    lastPoint = [0,0]

    for c in contours:
        area = cv2.contourArea(c)
        if area > tamanhoMin and area < tamanhoMax: 
            
            # forma
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            objCor = len(approx)

            
            M = cv2.moments(c)
            if M['m00'] != 0:
                # print(f"{M['m00']}, {M['m10']}, {M['m01']}, {M['m11']}" )
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                if lastPoint[0] != cx or lastPoint[1] != cy:
                    cv2.drawContours(img, [c], -1, (0,255,0), 3)
                    cv2.circle(img, (cx, cy), 5, (0,0,255), -1)
                    # cv2.circle(img, (10, 10), 5, (255,0,0), -1)
                    # cv2.circle(img, (500, 500), 5, (0,255,0), -1)
                    cv2.putText(img, f"{cx, cy}", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                    print(f'area {area} - vertices {objCor} - pontos [{cx}, {cy}]')
                    lastPoint[0], lastPoint[1] = cx,cy
                    centers.append((cx, cy))

    # showImages([image, im_bw, img])
    showImages([img])
    return centers

def interface(metodoContorno,alvo):
    centers = getPosition(metodoContorno, alvo)

    master = Tk()
    master.geometry("400x400")
    master.title("Localização de Objetos")
    master.eval('tk::PlaceWindow . center')

    t = Text(master, height=10, width=10)
    for x in centers:
        t.insert(END, x)
        t.insert(END, "\n")
    t.pack()

    indexes = []
    j = 0
    for _ in centers:
        indexes.append(j)
        j += 1
    
    variable = StringVar(master)
    variable.set(indexes[0])

    w = OptionMenu(master, variable, *indexes)
    w.pack()


    def ok():
        result = variable.get()
        #print ("value is: " + result)
        #print(centers[int(result)])
        global cx, cy
        cx, cy = centers[int(result)]
        master.destroy()

    button = Button(master, text="OK", command=ok)
    button.pack()

    mainloop()
    return cx, cy


def calculaPosicaoReal(obj,ref): 
    cmPorPixel = 0.5
    distX = obj[0] - ref[0]
    distY = obj[1] - ref[1]
    print(f"X : {distX}  Y: {distY}")
    print(f"Está a {distX* cmPorPixel} cm em X e {distY* cmPorPixel} cm em Y")

# Objetivo identificar:  
#  1. peça
#  2. burcao
#  3. peça no buraco 

# Modos de Identificar 
# 1. cor -> problema: luz e paleta de cores mal definida 
# 2. forma -> problema: angulo da camera 
# 3. area -> problema: forma 


def encontraPosicoesEmFoto(path):

    print("Peça")
    pecas = getPosition(cv2.RETR_CCOMP , "p", path)
    for position in pecas: 
        print(f"{position[0]}, {position[1]}") 

    # print("Encaixe")
    # encaixes = getPosition(cv2.RETR_EXTERNAL, "e", path)
    # for position in pecas: 
    #     print(f"{position[0]}, {position[1]}") 

    # calculando da peca para o encaixe
    # try: 
    #     calculaPosicaoReal(pecas[0], encaixes[0])
    # except:
    #     print("Nao encontrou") 


def encontraEmTodasAsFotos(directory_src):
        
    for filename in os.listdir(directory_src):
        path = directory_src + filename
        encontraPosicoesEmFoto(path)


encontraEmTodasAsFotos('C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/imagens/fotosPreparadas/')
