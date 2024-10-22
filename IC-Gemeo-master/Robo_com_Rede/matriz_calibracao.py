import cv2
import numpy as np

# Definir dimensões do tabuleiro de xadrez (número de quadrados internos)
num_linhas = 6  # quadrados internos por linha
num_colunas = 9  # quadrados internos por coluna
dimensao_quadrado = 25  # tamanho do quadrado do tabuleiro em mm

# Preparar os pontos 3D do tabuleiro de xadrez em coordenadas do mundo (eixo Z é 0)
pontos_objeto = np.zeros((num_linhas * num_colunas, 3), np.float32)
pontos_objeto[:, :2] = np.mgrid[0:num_colunas, 0:num_linhas].T.reshape(-1, 2)
pontos_objeto *= dimensao_quadrado

# Vetores para armazenar pontos 3D (no mundo real) e pontos 2D (na imagem)
pontos_objetos = []  # Pontos 3D
pontos_imagem = []   # Pontos 2D

# Iniciar captura de vídeo com maior resolução
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha na captura do frame")
        break

    # Converter para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Encontrar os cantos do tabuleiro de xadrez
    ret, cantos = cv2.findChessboardCorners(gray, (num_colunas, num_linhas), None)

    if ret:
        print("Tabuleiro encontrado!")

        # Ajustar critérios para refinar a detecção dos cantos
        criterios = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        cantos_precisos = cv2.cornerSubPix(gray, cantos, (11, 11), (-1, -1), criteria=criterios)

        # Armazenar pontos para calibração
        pontos_objetos.append(pontos_objeto)
        pontos_imagem.append(cantos_precisos)

        # Desenhar e exibir os cantos encontrados
        frame_cantos = cv2.drawChessboardCorners(frame, (num_colunas, num_linhas), cantos_precisos, ret)
        cv2.imshow("Tabuleiro de Xadrez", frame_cantos)
    else:
        print("Tabuleiro não encontrado.")

    cv2.imshow("Captura", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a câmera
cap.release()
cv2.destroyAllWindows()

# Verificar se há pontos suficientes para a calibração
if pontos_objetos and pontos_imagem:
    # Calibrar a câmera
    ret, matriz_camera, dist, rvecs, tvecs = cv2.calibrateCamera(pontos_objetos, pontos_imagem, gray.shape[::-1], None, None)

    # Exibir os resultados
    print("Matriz da Câmera:")
    print(matriz_camera)
    print("\nCoeficientes de Distorção:")
    print(dist)
else:
    print("Não foram encontrados pontos suficientes para calibração.")
