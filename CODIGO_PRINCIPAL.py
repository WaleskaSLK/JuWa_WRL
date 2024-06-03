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
import FUNCOES as f
import APP2 as a

# Carregando modelo da YOLOv8
model = YOLO(r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\best.pt')
pi_value = np.pi
sqrt = np.sqrt

# Dados fornecidos pelo código do APP
lista_wl = ['MINERADORA/BH/BRASIL', 'Bloco 1', '6', '5', '30/5', '230', 'JULIA']

class DepthCamera:

    def __init__(self):
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


dc = DepthCamera() #inicia a camera

while True:
    ret, depth_frame, color_frame, infra_image, Abertura = dc.get_frame() # Chamando as propriedades da câmera

    lista_APP, id_bico, qtd_furos = f.organizar_dados_app(lista_wl)
     
    data = datetime.now()
    lista_arq = []
    # Formatar a data e hora como parte do nome do arquivo
    diretorio_destino_imgBW = r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\FOTOS_ANALISE'
    nome_arquivo_BW = data.strftime(f'analise_{id_bico}_%d-%m-%Y_%H.%M') + '.png'
    caminho_completo_fotografia_BW = os.path.join(diretorio_destino_imgBW, nome_arquivo_BW)
    
    # Formatar a data e hora como parte do nome do arquivo
    diretorio_destino_imgAPP = r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\FOTOS_REGISTRO'
    nome_arquivo_APP = data.strftime(f'registro_{id_bico}_%d-%m-%Y_%H.%M') + '.png'
    caminho_completo_fotografia_APP = os.path.join(diretorio_destino_imgAPP, nome_arquivo_APP)
    lista_arq.append(nome_arquivo_APP)

    # Aguardar a tecla para salvar o frame
    if keyboard.is_pressed('ctrl') or keyboard.is_pressed('right control') or keyboard.is_pressed('q'):
        cv2.imwrite(caminho_completo_fotografia_BW, infra_image)
        cv2.imwrite(caminho_completo_fotografia_APP, color_frame)
        break

    pressedKey = cv2.waitKey(1) & 0xFF #definir uma tecla do waitKey
    cv2.imshow('Camera', infra_image)   
    if pressedKey == 27:
        break
    def release(self):
        self.pipeline.stop()()

foto_analise = cv2.imread(caminho_completo_fotografia_BW)
foto_app= cv2.imread(caminho_completo_fotografia_APP)
print('Fotografia salva')

lista_dh = f.extrair_data_e_hora(nome_arquivo_APP)
lista_diametros, img_segmentada, mascaras, resultados, foto_original = f.analisar_imagem(model, foto_analise, nome_arquivo_BW, depth_frame, Abertura)
caixas_detectadas, nomes_classes, propriedades = f.extrair_dados(resultados, mascaras, nome_arquivo_BW)
img_identificada = f.identificar_furos(caixas_detectadas, nomes_classes, foto_original, infra_image)

for dado in lista_dh:
    lista_arq.append(dado)

lista_completa = f.reunir_dados(lista_APP, lista_arq, lista_diametros)
f.salvar_registros(lista_completa, qtd_furos)

while True:
    # # Exibições
    cv2.imshow('Imagem Original: ', foto_app)
    cv2.imshow('Imagem segmentada: ', img_segmentada)
    cv2.imshow('Imagem identificada: ', img_identificada)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

print('Todos os dados da análise: ', lista_completa)

cv2.destroyAllWindows()