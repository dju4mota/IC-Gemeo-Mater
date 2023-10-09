from robodk.robolink import *      # RoboDK's API
from robodk.robomath import *      # Math toolbox for robots
from tkinter import *
import numpy as np
import cv2
import json


def empty(a):
    pass

def calibrar(image):

    cv2.namedWindow("calibracao")
    cv2.resizeWindow("calibracao",640,240)
    cv2.createTrackbar("hue min", "calibracao", 0,179,empty)
    cv2.createTrackbar("hue max", "calibracao", 179,179,empty)
    cv2.createTrackbar("sat min", "calibracao", 0,255,empty)
    cv2.createTrackbar("sat max", "calibracao", 255,255,empty)
    cv2.createTrackbar("val min", "calibracao", 215,255,empty)
    cv2.createTrackbar("val max", "calibracao", 255,255,empty)
    
    while True: 
        try:
            h_minValue = cv2.getTrackbarPos("hue min", "calibracao")
            h_maxValue = cv2.getTrackbarPos("hue max", "calibracao")
            s_minValue = cv2.getTrackbarPos("sat min", "calibracao")
            s_maxValue = cv2.getTrackbarPos("sat max", "calibracao")
            v_minValue = cv2.getTrackbarPos("val min", "calibracao")
            v_maxValue = cv2.getTrackbarPos("val max", "calibracao")
        except: 
            break
    
        imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
        lower = np.array([h_minValue, s_minValue, v_minValue])
        upper = np.array([h_maxValue, s_maxValue, v_maxValue])
        mask = cv2.inRange(imgHSV, lower, upper)
        imgResult = cv2.bitwise_and(image, image, mask=mask)
        
        cv2.imshow('Image', image)
        cv2.imshow('Mask', mask)
        cv2.imshow('Image Masked', imgResult)
        cv2.waitKey(1)

    return imgResult

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

def getPosition(metodoContorno,alvo):

    #path = 'C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/Localizacao de Objetos/Exemplo/WIN_20230329_19_02_50_Pro.jpg'
    # path = 'C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/Localizacao de Objetos/Exemplo/WIN_20230306_14_38_54_Pro.jpg'
    path = 'C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/Localizacao de Objetos/Exemplo/WIN_20230306_14_42_32_Pro.jpg'
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
                    cv2.putText(img, f"{cx, cy}", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                    print(f'area {area} - vertices {objCor} - pontos [{cx}, {cy}]')
                    lastPoint[0], lastPoint[1] = cx,cy
                    centers.append((cx, cy))

    showImages([image, im_bw, img])
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


# Objetivo identificar:  
#  1. peça
#  2. burcao
#  3. peça no buraco 

# Modos de Identificar 
# 1. cor -> problema: luz e paleta de cores mal definida 
# 2. forma -> problema: angulo da camera 
# 3. area -> problema: forma 


print("Marcando peça")
centers = getPosition(cv2.RETR_EXTERNAL, "p")
aux = 1
for position in centers: 
    print(f"{position[0]}, {position[1]}") 
    aux += 1


print("Marcando encaixe")
cx, cy = interface(cv2.RETR_EXTERNAL, "e")
print(f"{cx} , {cy}")



def calculaPosicaoReal(obj,ref): 
    print(f"X : {obj[0] - ref[0]}  Y: {obj[1] - ref[1]}")


calculaPosicaoReal(centers[0], [cx,cy])