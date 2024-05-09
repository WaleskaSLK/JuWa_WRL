import cv2
import pyrealsense2
from realsense_depth import *
import os
from datetime import datetime
from ultralytics import YOLO
import pandas as pd
from skimage.measure import regionprops
import math
import sqlite3 as sql
import numpy as np

# Iniciando a camera
dc = DepthCamera()

ret, depth_frame, frame, depth_scale = dc.get_frame()

def analisar_imagem(image):
    modelo = YOLO(r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\Versao_3\YOLOv8\YOLOv8_versao2\weights\best.pt')
    resultados = modelo.predict(image, conf=0.2)

    resultados_array = resultados[0].plot() # imagem plotada com os resultados da detecção
    resultados_array_bgr = cv2.cvtColor(resultados_array, cv2.COLOR_RGB2BGR) # converte a imagem plotada de RGB para BGR

    return resultados_array_bgr, resultados



def extrair_dados(resultados, nome, distancia):
    resultados = resultados[0]
    resultados.masks.xyn
    extracted_masks = resultados.masks.data
    resultados.masks.xy
    extracted_masks.shape

    # Converter tensor PyTorch para numpy
    masks_array = extracted_masks.cpu().numpy()

    classes_nomes = resultados.names.values()

    # Extrair caixas delimitadoras
    detected_boxes = resultados.boxes.data
    # Extrair classes a partir das caixas identificadas
    notas_classes = detected_boxes[:, -1].int().tolist()
    # Armazenando as mascaras por classes
    masks_by_class = {name: [] for name in resultados.names.values()}

    # Iterar pelas mascaras e rotulos de classe
    for mask, class_id in zip(extracted_masks, notas_classes):
        nome_classe = resultados.names[class_id] 
        masks_by_class[nome_classe].append(mask.cpu().numpy())

    bico_masks = masks_by_class['Bico']
    furo_masks = masks_by_class['Furo']

    props_lista = []
    i=-1
    # Iterar por todas as classes
    for nome_classe, masks in masks_by_class.items():
        for mask in masks:
            mask = mask.astype(int)
            props = regionprops(mask) # retorna uma lista de propriedades encontradas nas mascaras
            i+=1

            # Extrair propriedades
            for prop in props:
                area = prop.area

                # Calcula a profundidade média na região de interesse em metros
                profundidade_media_metros = np.mean(depth_frame[mask])

                # Converte a profundidade média para milímetros usando o depth_scale
                profundidade_media_mm = profundidade_media_metros * depth_scale

                # Calcula a área em milímetros quadrados
                area_mm2 = area * profundidade_media_mm

                # Calcula o diâmetro do círculo em milímetros
                raio_mm = math.sqrt(area_mm2 / math.pi)
                diametro_mm = 2 * raio_mm

                if i == 0:
                    props_lista.append({'Classe': f'{nome_classe}','Arquivo': nome,'Diametro[mm]': f'{diametro_mm:.2f}', 'Altura': f'{distancia/10}'})
                else:
                    props_lista.append({'Classe': f'{nome_classe} {i}','Arquivo': nome, 'Diametro[mm]': f'{diametro_mm:.2f}', 'Altura': f'{distancia/10}'})

    # Converter para DataFrame
    props_df = pd.DataFrame(props_lista)

    return props_df, detected_boxes, resultados, props_lista




# Função para extrair as coordenadas e centro das caixas delimitadoras
def extrair_coordenadas_centro(detected_boxes, classes_nomes):

    coordenadas_caixas = []
    pontos = []

    for box in detected_boxes:
        x1, y1, x2, y2, sla, classe = box.tolist()
        centro_x = int((x1 + x2) / 2)
        centro_y = int((y1 + y2) / 2)

        ponto = (centro_x, centro_y)
        pontos.append(ponto)
        
        coordenadas_caixas.append({
            'Classe': classes_nomes[int(classe)],
            'Centro': {
                'x': centro_x,
                'y': centro_y
            }
        })

        
    # Converter para DataFrame
    coordenadas_df = pd.DataFrame(coordenadas_caixas)
    
    return coordenadas_df, pontos


def salvar_dados(novos_dados, excel_filename):
        # Carregar o DataFrame existente da planilha Excel
        props_df = pd.read_excel(excel_filename)

        # Converter os novos dados em DataFrame
        novos_df = pd.DataFrame(novos_dados)

        # Adicionar novos dados ao DataFrame existente
        props_df = pd.concat([props_df, novos_df], ignore_index=True)

        # Salvar o DataFrame atualizado na planilha Excel
        props_df.to_excel(excel_filename, index=False)

        print(f'Novos dados adicionados com sucesso em {excel_filename}')

def extrair_data_e_hora(nome_registro):

    data = nome_registro[13:15] + '/' + nome_registro[16:18] + '/' + nome_registro[19:23]
    hora = nome_registro[24:26] + ':' + nome_registro[27:29]

    return data, hora
