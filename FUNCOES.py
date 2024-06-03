import cv2
from ultralytics import YOLO
import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, regionprops_table
import open3d as o3d
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull, Delaunay
import pyvista as pv
import time
import math
import keyboard
import os
from datetime import datetime
import sqlite3 as sql


class DepthCamera:

    def __init__(self):
        try:
            # Configure depth and color streams
            self.pipeline = rs.pipeline()
            config = rs.config()
            # Get device product line for setting a supporting resolution
            pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
            pipeline_profile = config.resolve(pipeline_wrapper)
            device = pipeline_profile.get_device()
            device.query_sensors()[0].set_option(rs.option.laser_power, 15)
            device_product_line = str(device.get_info(rs.camera_info.product_line))

            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)

                
            # Start streaming
            self.pipeline.start(config)

        except:
            print("Câmera desconectada")

    def get_frame(self):      
        frames = self.pipeline.wait_for_frames(timeout_ms=2000)
        colorizer = rs.colorizer()
        colorized = colorizer.process(frames)
        ply = rs.save_to_ply("1.ply")
        ply.set_option(rs.save_to_ply.option_ply_binary, True)
        ply.set_option(rs.save_to_ply.option_ply_normals, False)
        ply.process(colorized)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        infrared = frames.get_infrared_frame()
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        Abertura = format(math.degrees(2*math.atan(depth_intrin.width/(2*depth_intrin.fx))))
        #print(depth_intrin)
        #print("FOV real da realsense configurado:")
        #print("FoV: {:.2f} x {:.2f}".format(math.degrees(2*math.atan(depth_intrin.width/(2*depth_intrin.fx))), math.degrees(2*math.atan(depth_intrin.height/(2*depth_intrin.fy)))))
        infra_image = np.asanyarray(infrared.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        if not depth_frame or not color_frame:
            return False, None, None
        
        return True, depth_image, color_image, infra_image, Abertura

    def depth(self):
            frames = self.pipeline.wait_for_frames(timeout_ms=2000)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            if not depth_frame or not color_frame:
                return False, None, None
            
            return depth_image
    
    def get_depth_scale(self):
        self.depth_sensor = self.pipeline.get_active_profile().get_device().first_depth_sensor()
        self.depth_scale = self.depth_sensor.get_depth_scale()
        
        return self.depth_scale,self.depth_sensor
    
    def release(self):
        self.pipeline.stop()


dc=DepthCamera() #inicia a camera

def exibir_imagens(foto_app, img_segmentada, img_identificada):
    while True:
        # # Exibições
        cv2.imshow('Imagem Original: ', foto_app)
        cv2.imshow('Imagem segmentada: ', img_segmentada)
        cv2.imshow('Imagem identificada: ', img_identificada)
        
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()


def obter_depth_frame():
    ret, depth_frame, color_frame, infra_image, Abertura = dc.get_frame() # Chamando as propriedades da câmera

    return depth_frame

def tirar_foto(color_frame, infra_image, id_bico):
    data = datetime.now()
    lista_arq = []
    # Formatar a data e hora como parte do nome do arquivo
    diretorio_destino_imgBW = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\fotos_BW'
    nome_arquivo_BW = data.strftime(f'registro_{id_bico}_%d-%m-%Y_%H.%M') + '.png'
    caminho_completo_fotografia_BW = os.path.join(diretorio_destino_imgBW, nome_arquivo_BW)
    
    # Formatar a data e hora como parte do nome do arquivo
    diretorio_destino_imgAPP = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\fotos_app'
    nome_arquivo_APP = data.strftime(f'registro_{id_bico}_%d-%m-%Y_%H.%M') + '.png'
    caminho_completo_fotografia_APP = os.path.join(diretorio_destino_imgAPP, nome_arquivo_APP)
    lista_arq.append(nome_arquivo_APP)

    # Aguardar a tecla para salvar o frame
    if keyboard.is_pressed('ctrl') or keyboard.is_pressed('right control') or keyboard.is_pressed('q'):
        cv2.imwrite(caminho_completo_fotografia_BW, infra_image)
        cv2.imwrite(caminho_completo_fotografia_APP, color_frame)
        
    print('Imagem salva')
    '''print(caminho_completo_fotografia_APP)
    print(caminho_completo_fotografia_BW)
    print(lista_arq)'''

    return lista_arq, caminho_completo_fotografia_BW, caminho_completo_fotografia_APP, nome_arquivo_APP
ret, depth_frame, color_frame, infra_image, Abertura = dc.get_frame() # Chamando as propriedades da câmera

def analisar_imagem(model, imagem, nome, depth_frame, Abertura):
    imagem_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)  # Converter imagem para BGR

    # Análise
    results = model(imagem_bgr,device = 'cpu',retina_masks=True, save = True, save_crop = True,save_frames=True,overlap_mask=True, project =r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\resultados",name = nome, save_txt = True, show_boxes=False)
    
    for result in results:
        img_segmentada = results[0].plot(masks= True, boxes=False) #plotar a segmentação - *resultados_array_bgr
        
        mascaras = result.masks.data # Máscaras extraídas - extracted_masks
        depth_data_numpy_binaria = mascaras.cpu().numpy()   #tranformar array em np.array
        detections = len(result)  #quantidades de detecções
        depth_data_numpy_coordenada=np.argwhere(depth_data_numpy_binaria[0] == 1)#transformar formascara em coordenada nos pontos em que tem mascara
        x = depth_data_numpy_coordenada[0:len(depth_data_numpy_coordenada),0]
        y = depth_data_numpy_coordenada[0:len(depth_data_numpy_coordenada),1]
        z = depth_frame[x,y]
        
        indices_remover = []
        for i, (j_z) in enumerate(zip(z)):
            if j_z[0] == 0 or j_z[0] >= 750:
                indices_remover.append(i)

        # Remover elementos de filtered_x usando os índices calculados
        filtered_x = np.array([v for i, v in enumerate(x) if i not in indices_remover])
        filtered_y = np.array([v for i, v in enumerate(y) if i not in indices_remover])
        filtered_z = np.array([v for i, v in enumerate(z) if i not in indices_remover])

        # Criar a matriz de entrada para a regressão
        X = np.column_stack((np.ones_like(filtered_x), filtered_x, filtered_y, filtered_x**2, filtered_y**2, filtered_x*filtered_y))

        # Calcular os coeficientes da regressão
        coefficients, _, _, _ = np.linalg.lstsq(X, filtered_z, rcond=None)

        for j in range (detections):
            depth_data_numpy_coordenada=np.argwhere(depth_data_numpy_binaria[j] == 1)
            
            for i in range(len(depth_data_numpy_coordenada)): #para o bico de lança
                x = depth_data_numpy_coordenada[i][0].astype(int) #coordenada x da mascara do bico de lança
                y = depth_data_numpy_coordenada[i][1].astype(int) #coordenada y da mascara do bico de lança
                v = (coefficients[0]) + (coefficients[1]*x) + (coefficients[2]*y) + (coefficients[3]*x**2) + (coefficients[4]*y**2) + (coefficients[5]*(x*y))
                depth_data_numpy_binaria[j][x][y] = ((math.tan(float(Abertura)*180/math.pi)*v*2)/640)
    
        lista_diametros = []
        lista_furos= []
        # Exibir os diametros
        area_total = np.sum(depth_data_numpy_binaria)
        diametro_externo = 2*(math.sqrt(area_total/math.pi))
        area_furos = np.sum(depth_data_numpy_binaria[1:7],axis=(1,2))
        diametro_furos = 2*(np.sqrt(area_furos/math.pi))

        # Armazenar todos os diâmetros dos furos em uma lista
        for elemento in diametro_furos:
            diametro_float = float(elemento)
            lista_diametros.append(round(diametro_float, 2))
        
        # Armazenando o diametro externo na lista
        lista_diametros.append(round(diametro_externo, 2)) # Lista com os valores de todos os diâmetros
    
    return lista_diametros, img_segmentada, mascaras, results, imagem_bgr

def extrair_data_e_hora(nome_arquivo):
    lista = nome_arquivo.split("_")

    data_original = lista[2]
    hora_original = lista[3]
    hora_original = hora_original[:5]

    data = data_original.replace("-", "/")
    hora = hora_original.replace(".", ":")

    lista_data_hora = []
    lista_data_hora.append(data)
    lista_data_hora.append(hora)

    return lista_data_hora

def extrair_dados(resultado, mascaras, nome):
    resultado = resultado[0]
    resultado.masks.xyn
    # Extrair nomes das classes
    nomes_classes = resultado.names.values()
    # Extrair caixas delimitadoras
    caixas_detectadas = resultado.boxes.data
    resultado.masks.xy
    caixas_detectadas.shape
     # Extrair classes a partir das caixas identificadas
    infos_classes = caixas_detectadas[:, -1].int().tolist()
    # Armazenando as mascaras por classes
    mascaras_por_classe = {name: [] for name in resultado.names.values()}
    # Iterar pelas mascaras e rotulos de classe
    for mask, class_id in zip(mascaras, infos_classes):
        nome_classe = resultado.names[class_id] 
        mascaras_por_classe[nome_classe].append(mask.cpu().numpy())
    
    lista_proprs = []
    i = -1
    # Iterar por todas as classes
    for nome_classe, masks in mascaras_por_classe.items():
        for mask in masks:
            i+=1
            if i == 0:
                lista_proprs.append({'Classe': f'{nome_classe}','Arquivo': nome})
            else:
                lista_proprs.append({'Classe': f'{nome_classe} {i}','Arquivo': nome})
    
    # Armazenando os nomes das classes em uma lista
    nomes_classes = list(resultado[0].names.values())

    return caixas_detectadas, nomes_classes, lista_proprs

def identificar_furos(caixas_detectadas, nomes_classes, imagem, frame, nome_arquivo_APP):
    # Extrair as coordenadas e centro das caixas delimitadoras
    coordenadas_caixas = []
    pontos = []
    for box in caixas_detectadas:
        x1, y1, x2, y2, sla, classe = box.tolist()
        centro_x = int((x1 + x2) / 2)
        centro_y = int((y1 + y2) / 2)

        ponto = (centro_x, centro_y)
        pontos.append(ponto)
        
        coordenadas_caixas.append({
            'Classe': nomes_classes[int(classe)],
            'Centro': {
                'x': centro_x,
                'y': centro_y
            }
        })

    img = imagem.copy()
    # Adicionar texto para identificar cada objeto detectado (id)
    for i in range(1, len(pontos)):
        imagem_final = cv2.putText(img, f'{i}', pontos[i], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

    #id = str(id_bico)
    #data = datetime.now()
    diretorio_guias = r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\guias'
    caminho = os.path.join(diretorio_guias, nome_arquivo_APP)
    
    cv2.imwrite(caminho, imagem_final)

    imagem_id = cv2.imread(caminho)

    return imagem_id

'''def calcular_angulo(ponto_central, ponto, frame):

    # Obter as dimensões do frame
    altura, largura, _ = frame.shape

    # Calcular as coordenadas do ponto no meio do frame
    mid_x, mid_y = largura // 2, altura // 2
    ponto = (mid_x, mid_y)

    furos = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6)]

    dx = ponto[0] - ponto_central[0]
    dy = ponto[1] - ponto_central[1]
    math.atan2(dy, dx)

    angulos = []
    for furo in furos:
        angulo = calcular_angulo(ponto, furo)
        angulos.append(angulo)

    furos_enum = sorted(enumerate(angulos), key=lambda x: x[1])

    for i, (idx, _) in enumerate(furos_enum):
        print(f"Furo {i+1}: Coordenadas ({furos[idx][0]}, {furos[idx][1]})")'''


def reunir_dados(dados_app, dados_arquivo, dados_diametros):
    lista_completa = []

    # Inserir os dados vindos do app
    for dado in dados_app:
        lista_completa.append(dado)
    # Inserir os dados do arquivo
    for dado in dados_arquivo:
        lista_completa.append(dado)
    # Inserir os dados dos diametros
    for dado in dados_diametros:
        lista_completa.append(dado)

    return lista_completa

def organizar_dados_app(lista):

    lista_APP = [lista[6], lista[5], lista[3], lista[4]]
    x = int(lista[2])
    id = '00' + str(lista[3])

    return lista_APP, id, x


def salvar_registros(lista, x):
    # Conectando ao banco 
    banco = sql.connect(r'C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db') #mudar dps
    cursor = banco.cursor()

    if x == 6:
        comando = "INSERT INTO B6 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        registro = (lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9], lista[10], lista[11], lista[12], lista[13])

        cursor.execute(comando, registro)

        # Grava a transação
        banco.commit()

    else:
        comando = "INSERT INTO B4 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        registro = (lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8], lista[9], lista[10], lista[11])

        cursor.execute(comando, registro)

        # Grava a transação
        banco.commit()

    # Feche a conexão com o banco de dados
    cursor.close()

    print('Dados inseridos no banco com sucesso!')

    