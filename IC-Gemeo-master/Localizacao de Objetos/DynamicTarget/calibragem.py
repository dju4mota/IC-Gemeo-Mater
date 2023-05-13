from robodk.robolink import *      # RoboDK's API
from robodk.robomath import *      # Math toolbox for robots
from tkinter import *
import numpy as np
import cv2


def empty(a):
    pass

def calibrar(image):

    cv2.namedWindow("calibracao")
    cv2.resizeWindow("calibracao",640,240)
    cv2.createTrackbar("hue min", "calibracao", 0,179,empty)
    cv2.createTrackbar("hue max", "calibracao", 179,179,empty)
    cv2.createTrackbar("sat min", "calibracao", 0,255,empty)
    cv2.createTrackbar("sat max", "calibracao", 255,255,empty)
    cv2.createTrackbar("val min", "calibracao", 0,255,empty)
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

    return imgResult,lower,upper

def showImages(images):
    for image in images:
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def getHSV(metodoContorno, tamanhoMin, tamanhoMax):
    path = 'C:/Code/IC-Gemeo-master/IC-Gemeo-master/Localizacao de Objetos/Exemplo/WIN_20230306_14_40_20_Pro.jpg'
    #path = 'C:/Code/IC-Gemeo-master/IC-Gemeo-master/Localizacao de Objetos/Exemplo/bancada1.png'
    
    image = cv2.imread(path)
    image = cv2.resize(image, (int(image.shape[1] *0.5), int(image.shape[0] *0.5)))

    maskedImage,lower,upper = calibrar(image)
    img = maskedImage.copy()
    
    #im_bw = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    #im_bw = cv2.cvtColor(im_bw, cv2.COLOR_RGB2GRAY)

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
            #if M['m00'] != 0 and objCor == 4:
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                if lastPoint[0] != cx or lastPoint[1] != cy:
                    cv2.drawContours(img, [c], -1, (0,255,0), 3)
                    cv2.circle(img, (cx, cy), 5, (0,0,255), -1)
                    cv2.putText(img, f"{cx, cy}", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                    print(f'area {area} - vertices {objCor} - pontos [{cx}, {cy}]')
                    lastPoint[0], lastPoint[1] = cx,cy
                    centers.append((cx, cy))

    showImages([image, maskedImage, im_bw, img])
    return lower,upper



f = open("IC-Gemeo-master\Localizacao de Objetos\DynamicTarget\calibragem.txt", "w")
#print(f.read())

print("Calibrando peça:")
lower, upper = getHSV(cv2.RETR_EXTERNAL,180,250)
print(lower)
print(upper)
f.write(f"Peca: \nlower: {lower} \nupper: {upper}")

print("Calibrando alvo:")
lower, upper = getHSV(cv2.RETR_CCOMP,200,300)
print(lower)
print(upper)
f.write(f"\nEncaixe: \nlower: {lower} \nupper: {upper}")
f.close()