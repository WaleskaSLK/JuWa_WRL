import tkinter as tk
import colorama as color
import cv2
import imutils
import pyrealsense2 as rs
import os
import pandas as pd
import math
from tkinter.constants import *
from tkinter import ttk
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
from realsense_depth import *
from datetime import datetime
from ultralytics import YOLO
from skimage.measure import regionprops
import keyboard
import FUNCOES as f
import FUNCOES_APK as fun
import numpy as np

from APK import aba_dados

'''#### AVISOS IMPORTANTES ##
1) Na linha 124 tem a lista simulada de informações que virão do login; Pode modificar os dados, caso queira;
2) No arquivo FUNCOES.py tem diretórios declarados, como o caminho das imagens, fique atento em alterar esses trechos de acordo com a sua máquina;
'''

model = YOLO(r'C:\Users\labga\OneDrive\Documentos\IC_WRL\PROJETO_WRL\pesos\best.pt')

# Define the DepthCamera class
class DepthCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device.query_sensors()[0].set_option(rs.option.laser_power, 12)
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames(timeout_ms=2000)
        color_frame = frames.get_color_frame()
        infrared = frames.get_infrared_frame()
        depth_frame = frames.get_depth_frame()
        infra_image = np.asanyarray(infrared.get_data())
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        Abertura = format(math.degrees(2 * math.atan(depth_intrin.width / (2 * depth_intrin.fx))))
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if not color_frame:
            return False, None, None, None, None
        return True, color_image, infra_image, Abertura, depth_frame

    def release(self):
        self.pipeline.stop()

# Initialize the DepthCamera
dc = DepthCamera()

def voltar(aba_1, aba_2):
    aba_1.deiconify()  # Exiba a janela da aba 1
    aba_2.destroy()  # Destrua a janela da aba 2
# Define global variables for storing the results
global lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW, stop
lista_arq = caminhoBW = caminhoAPP = nome_arquivo_BW = None
stop = False

def tela(inp_janela):
    inp_janela.title("Camêra WRL")
    inp_janela.configure(background='#9BCD9B')
    inp_janela.attributes("-fullscreen", True)
    inp_janela.overrideredirect(True)

def frames_da_tela(inp_janela):
    global frame_um, frame_dois
    frame_um = tk.Frame(inp_janela, bd=2, bg='#B4EEB4', highlightbackground='#668B8B', highlightthickness=1)
    frame_um.place(relx=0.72, rely=0.02, relwidth=0.27, relheight=0.96)
    frame_dois = tk.Frame(inp_janela, bd=2, bg='#B4EEB4', highlightbackground='#668B8B', highlightthickness=1)
    frame_dois.place(relx=0.01, relwidth=0.7, relheight=0.96)
    return frame_um, frame_dois

def componentes_frame1(inp_frame,inp_janela, inp_menu):
    # bt_fechar_aba_menu = tk.Button(inp_frame, text="X", command=inp_janela.destroy, bg="red")
    # bt_fechar_aba_menu.place(relx=0.90, relwidth=0.05, relheight=0.05)
    
    bt_voltar = fun.CRIAR_BOTAO(inp_frame, "Voltar",'#258D19', 'white',3,'20','',"hand2", lambda: voltar( inp_menu, inp_janela))# #TOPLEVEL
    bt_voltar.place(relx=0.05, rely=0.88, relwidth=0.2, relheight=0.08)
    
    btfoto_pg2 = tk.Button(inp_frame, text='Click', relief="ridge", cursor="circle", bd=4, bg='#545454', fg='white', font=("arial", 13))
    btfoto_pg2.place(relx=0.5, rely=0.93, anchor=CENTER)

def componentes_frame2(inp_frame, lista):
    global lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW, stop

    borda = tk.Label(inp_frame, bg="black")
    borda.place(relx=0, rely=0, relwidth=1, relheight=1)

    def exibir_video():
        global lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW, stop, lista_APP, qtd_furos, Abertura, infra_image
        ret, color_frame, infra_image, Abertura, depth_frame = dc.get_frame()
        lista_APP, id_bico, qtd_furos = f.organizar_dados_app(lista)

        if ret:
            frame = cv2.cvtColor(infra_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            altura = borda.winfo_height()
            largura = borda.winfo_width()
            img = img.resize((largura, altura))
            image = ImageTk.PhotoImage(image=img)
            borda.configure(image=image)
            borda.image = image

            if keyboard.is_pressed('ctrl') or keyboard.is_pressed('right control') or keyboard.is_pressed('q'):
                lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW = f.tirar_foto(color_frame, infra_image, id_bico)
                stop = True
                return

        if not stop:
            borda.after(10, exibir_video)

    exibir_video()

def aba_camera(inp_janela,dados):
    global lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW, stop, lista_APP, qtd_furos, Abertura, infra_image
    print('aaaaaaa',dados)
    lista_wl = dados
    # lista_wl = ['MINERADORA/BH/BRASIL', 'Bloco 2', '6', '5', '30/5', '81', 'JOICE']
    janela_tres = tk.Toplevel(inp_janela)
    # janela_tres = tk.Tk()
    
    tela(janela_tres)
    frames_da_tela(janela_tres)
    componentes_frame1(frame_um,janela_tres, inp_janela)
    componentes_frame2(frame_dois, lista_wl)
    
    def aba_camera2():
        # Esperar até que a variável `stop` seja definida como True
        while not stop:
            janela_tres.update_idletasks()
            janela_tres.update()

        #print(lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW)
        janela_tres.destroy()

        return lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW, lista_APP, qtd_furos, Abertura, infra_image

    lista_arq, caminhoBW, caminhoAPP, nome_arquivo_BW, lista_APP, qtd_furos, Abertura, infra_image = aba_camera2()

    Depth_Frame = f.obter_depth_frame()
    lista_dh = f.extrair_data_e_hora(lista_arq[0])
    lista_diametros, img_segmentada, mascaras, resultados, foto_original = f.analisar_imagem(model, cv2.imread(caminhoBW), lista_arq[0], Depth_Frame, Abertura)
    caixas_detectadas, nomes_classes, propriedades = f.extrair_dados(resultados, mascaras, nome_arquivo_BW)
    img_identificada = f.identificar_furos(caixas_detectadas, nomes_classes, foto_original, infra_image)

    for dado in lista_dh:
        lista_arq.append(dado)

    lista_completa = f.reunir_dados(lista_APP, lista_arq, lista_diametros)
    f.salvar_registros(lista_completa, qtd_furos)
    # f.exibir_imagens(cv2.imread(caminhoAPP), img_segmentada, img_identificada)
    
    
    
    janela_cadastro = aba_dados(inp_janela, dados[3], dados[4], lista_arq[0])
    janela_cadastro.deiconify()
    
    return janela_tres

print("\n\n", color.Fore.GREEN + "Iniciando o código - Tela da câmera" + color.Style.RESET_ALL)
print(color.Fore.RED + "Finalizando o código - Tela da câmera" + color.Style.RESET_ALL, "\n")