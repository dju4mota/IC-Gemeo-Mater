import cv2 
import numpy as np 
import os


def cortar_foto(path, id):

    img = cv2.imread(path)

    # img = rotate_image(img, 1.5)  # raw 1
    # cropped = img[150:1400, 220:1750]  # raw 1

    img = rotate_image(img, 1)  # raw 2
    cropped = img[220:1005, 315:1580]  # raw 2

    cv2.imwrite(f"bancada-{id}.jpg", cropped)

    # cv2.imshow("cropped", cropped)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


# def load_dir(directory_src, directory_target): 
#     for subdir in os.listdir(directory_src):
#         path = directory_src + subdir + "\\"
#         path_tg = directory_target + subdir + "\\"
#         if not os.isdir(path): 
#             continue
#         load_fotos(path,path_tg)

def edita_fotos(directory_src,start):
    
    os.chdir('C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/imagens/fotosPreparadas')

    for filename in os.listdir(directory_src):
        path = directory_src + filename
        start +=1

        try: 
            cortar_foto(path, start)
        except: 
            print(f"Erro na imagem {path}")


# edita_fotos('C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/imagens/raw-1-etapa/',1)
edita_fotos('C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/imagens/raw-2-etapa/', 81)

# cortar_foto('C:/Code/Projetinhos/IC-Gemeo-master/IC-Gemeo-master/imagens/raw-1-etapa/WIN_20231018_21_55_52_Pro.jpg',
# 12)
