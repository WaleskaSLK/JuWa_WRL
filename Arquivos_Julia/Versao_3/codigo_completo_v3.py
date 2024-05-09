import cv2
import pyrealsense2
from realsense_depth import *
import os
from datetime import datetime
from ultralytics import YOLO
import pandas as pd
from skimage.measure import regionprops
import math
import funcoesv3 as f

# Iniciando a camera
dc = DepthCamera()

lista_dados = []

num = int(input('Selecione o molde: \n1- Quatro furos \n2- Seis furos \nResposta: '))

diretorio_molde_1 = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\Versao_3\moldes\molde2.png'
diretorio_molde_2 = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\Versao_3\moldes\molde1.png'

if num == 1:
    overlay_image = cv2.imread(diretorio_molde_1, cv2.IMREAD_UNCHANGED)
else:
    overlay_image = cv2.imread(diretorio_molde_2, cv2.IMREAD_UNCHANGED)

while True:

    ret, depth_frame, frame, depth_scale = dc.get_frame()

    back_frame = frame.copy()

    # Redimensionar a imagem para o tamanho do frame
    overlay_image_resized = cv2.resize(overlay_image, (frame.shape[1], frame.shape[0]))

    # Definir a região de interesse onde a imagem será sobreposta
    roi = back_frame[0:overlay_image_resized.shape[0], 0:overlay_image_resized.shape[1]]
    
    # Sobrepor a imagem na região de interesse
    for c in range(0, 3):
        roi[:, :, c] = overlay_image_resized[:, :, c] * (overlay_image_resized[:, :, 3] / 255.0) + roi[:, :, c] * (1.0 - overlay_image_resized[:, :, 3] / 255.0)
    
    # Obter as dimensões do frame
    altura, largura, _ = frame.shape

    # Calcular as coordenadas do ponto no meio do frame
    mid_x, mid_y = largura // 2, altura // 2
    ponto = (mid_x, mid_y)

    # Coordenadas do canto superior direito
    canto_superior_direito = (largura - 115, 30)

    # Mostrar a distancia de um ponto especifico (meio do frame)
    cv2.circle(back_frame, ponto, 4, (0, 0, 255))
    distancia = depth_frame[ponto[1], ponto[0]]
    
    cv2.putText(back_frame, '{}cm'.format(distancia/10), canto_superior_direito, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
    
    data = datetime.now()
    diretorio_destino = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\Versao_3\fotos'
    
    # Formatar a data e hora como parte do nome do arquivo
    nome_arquivo = data.strftime('registro_%d-%m-%Y_%H.%M') + '.png'

    caminho_completo_fotografia = os.path.join(diretorio_destino, nome_arquivo)

    # Aguardar a tecla 'q' para salvar o frame e encerrar o programa
    key = cv2.waitKey(1)
    if key == ord('q'):
        # Salvar o frame como imagem 
        cv2.imwrite(caminho_completo_fotografia, frame)
        break

    cv2.imshow('Color frame', back_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break


print('Fotografia salva')

fotografia = cv2.imread(caminho_completo_fotografia)

resultados_masks_BGR, resultados_masks = f.analisar_imagem(fotografia)

diretorio_planilha = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\Versao_3\dados_bicos.xlsx'

dados_extraidos, caixas_delimitadoras, img_resultados_masks = f.extrair_dados(resultados_masks, nome_arquivo, distancia)
x = f.salvar_dados(dados_extraidos, diretorio_planilha)

print(dados_extraidos)

# Armazenando os nomes das classes em uma lista
nomes_classes = list(img_resultados_masks[0].names.values())

# Extrair coordenadas e centro das caixas delimitadoras
coordenadas_df, lista_pontos = f.extrair_coordenadas_centro(caixas_delimitadoras, nomes_classes)

img_masks_BGR_copia = resultados_masks_BGR.copy()

# Adicionar texto para identificar cada objeto detectado (id)
for i in range(1, len(lista_pontos)):
    imagem_final = cv2.putText(img_masks_BGR_copia, f'{i}', lista_pontos[i], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

diretorio_guias = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\Versao_3\guias'
nome_arquivo = data.strftime('registro_%d-%m-%Y_%H.%M') + '.png'
caminho = os.path.join(diretorio_guias, nome_arquivo)

# Extrair do nome_arquivo a data e hora do registro nos formatos DD/MM/AA e HH:MM
data, hora = f.extrair_data_e_hora(nome_arquivo)

cv2.imwrite(caminho, imagem_final)

while True:

    cv2.imshow('Foto', fotografia)
    cv2.imshow('Imagem com Texto', imagem_final)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()