import tkinter as tk
import colorama as color
import cv2
import imutils
import pyrealsense2
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
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

# inp_janela = tk.Tk()
# video = None
class DepthCamera: ###AQUI RETIREI AS FUNCOES DE CALCULO DE DISTANCIA PARA MOSTRAR UMA IMAGEM MAIS FLUÍDA###
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()
        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device.query_sensors()[0].set_option(rs.option.laser_power, 12)
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames(timeout_ms=2000)
        color_frame = frames.get_color_frame()
        infrared = frames.get_infrared_frame()
        infra_image = np.asanyarray(infrared.get_data())
        if not color_frame:
            return False, None  # Retorna falso se não houver quadro de cor
        color_image = np.asanyarray(color_frame.get_data())
        return True, color_image, infra_image  # Retorna a imagem colorida

    def release(self):
        self.pipeline.stop()

def voltar(aba_1, aba_2):
    aba_1.deiconify()  # Exiba a janela da aba 1
    aba_2.destroy()  # Destrua a janela da aba 2
    
def tela(inp_janela): # {=======================Configuração de tela=========================}
    inp_janela.title("Camêra WRL")
    inp_janela.configure(background= '#9BCD9B')
    inp_janela.geometry("1600x900")
    inp_janela.resizable(True, True) #se quiser impedir que amplie ou diminua a tela, altere para False
    # inp_janela.maxsize(width=1920, height=1080) #limite máximo da tela
    inp_janela.minsize(width=700, height=450) #limite minimo da tela

def frames_da_tela(inp_janela):
    global frame_um, frame_dois
    # {=======================Frame da Direita=========================}
    frame_um = tk.Frame(inp_janela, bd=2,
                            bg= '#B4EEB4',
                            highlightbackground= '#668B8B', 
                            highlightthickness=1)
    frame_um.place(relx=0.72, rely=0.02,relwidth=0.27, relheight=0.96)

    # {=======================Frame da Esquerda=========================}
    frame_dois = tk.Frame(inp_janela, bd=2,
                            bg= '#B4EEB4',
                            highlightbackground= '#668B8B', 
                            highlightthickness=1)
    frame_dois.place(relx=0.01, rely=0.02,relwidth=0.7, relheight=0.96)
    
    return frame_um, frame_dois


def componentes_frame1(inp_frame, inp_janela, inp_menu ):
    # {=======================Botão Voltar=========================}
    btvoltar_pg2 = tk.Button(inp_frame,
                            text='Voltar',
                            relief = "raised",
                            cursor = "hand2",
                            bd = 3,
                            bg = '#545454',
                            fg = 'white',
                            font= ("arial", 13),
                            command = lambda: voltar( inp_menu, inp_janela) )
    btvoltar_pg2.place(relx=0.7, rely=0.02, relwidth=0.25, relheight=0.05)
    
    # {=======================Message box=========================}
    # messagebox.showinfo(title = "",message="OIOI")
    
    
    
    
    
    # {=======================Botão Foto=========================}
    # image_btfoto_pg2 = tk.PhotoImage(file = "fotoclick.png")
    # image_btfoto_pg2 = image_btfoto_pg2.subsample(1, 2)

    btfoto_pg2 = tk.Button(inp_frame,
                                text='Click',
                                relief = "ridge",
                                cursor = "circle",
                                bd = 4,
                                bg = '#545454',
                                fg = 'white',
                                font= ("arial", 13)
                                #   image = image_btfoto_pg2
                                )
    btfoto_pg2.place(relx=0.5, rely=0.93, anchor=CENTER)

def componentes_frame2(inp_frame):
    borda = tk.Label(inp_frame, bg="black")
    borda.place(relx=0, rely=0, relwidth=1, relheight=1) #o tamanho do frame é w1114 h858
    try:
        dc = DepthCamera() #pra ficar mais bonitinho    
        def exibir_video():
            ret, color_frame, infra_image= dc.get_frame() # Captura um novo quadro da câmera
            if ret:
                img = Image.fromarray(infra_image)  # Converte o quadro em uma imagem Pillow
                altura = borda.winfo_height()
                largura = borda.winfo_width()
                img = img.resize((largura,altura))
                image = ImageTk.PhotoImage(image=img)  # Converte a imagem Pillow em um objeto ImageTk
                borda.configure(image=image)  # Atualiza a imagem exibida na Label
                borda.image = image  # Mantém uma referência para evitar a coleta de lixo
                
                # Chama esta função novamente após 10 milissegundos para exibir o próximo quadro
                borda.after(10, exibir_video)
        # Inicia o loop para exibir o vídeo
        exibir_video()
    except:
        print('CAMERA DESCONECTADA') #não esta exibindo a imagem que eu queria, mas ao menos da pra testar outras funcionalidades que não estejam envolvidas diretamente com a camera
        #img = Image.open(r'C:\Users\20221CECA0402\Documents\Projeto_WRL\Aplicativo_WRL\arquivos\molde.png')
        altura = borda.winfo_height() #atualiza altura e largura da borda para que a imagem da camera sempre preencha o espaço
        largura = borda.winfo_width()
        img = img.resize((largura, altura))  # Redimensiona a imagem para o tamanho da borda
        image = ImageTk.PhotoImage(image=img)
        borda.configure(image=image)  # Atualiza a imagem exibida na Label
        borda.image = image  # Mantém uma referência para evitar a coleta de lixo

    # # num = int(input('Selecione o molde: \n1- Quatro furos \n2- Seis furos \nResposta: '))

    # # if num == 1:
    # overlay_image = cv2.imread(r'C:\Users\20221CECA0402\Documents\Projeto_WRL\Aplicativo_WRL\arquivos\molde2.png', cv2.IMREAD_UNCHANGED)
    # # else:
    # #     overlay_image = cv2.imread(r'C:\Users\20211MPECA0020\Documents\Projeto\Aplicativo\arquivos\molde.png', cv2.IMREAD_UNCHANGED)

    # while True:

    #     ret, depth_frame, frame, depth_scale, abertura = dc.get_frame()

    #     back_frame = frame.copy()

    #     # Redimensionar a imagem se necessário
    #     overlay_image_resized = cv2.resize(overlay_image, (frame.shape[1], frame.shape[0]))

    #     # Definir a região de interesse (ROI) onde a imagem será sobreposta
    #     roi = back_frame[0:overlay_image_resized.shape[0], 0:overlay_image_resized.shape[1]]
        
    #     # Sobrepor a imagem na região de interesse
    #     for c in range(0, 3):
    #         roi[:, :, c] = overlay_image_resized[:, :, c] * (overlay_image_resized[:, :, 3] / 255.0) + roi[:, :, c] * (1.0 - overlay_image_resized[:, :, 3] / 255.0)
        
    #     # Obter as dimensões do frame
    #     altura, largura, _ = frame.shape

    #     # Calcular as coordenadas do ponto no meio do frame
    #     mid_x, mid_y = largura // 2, altura // 2
    #     ponto = (mid_x, mid_y)

    #     # Coordenadas do canto superior direito
    #     canto_superior_direito = (largura - 115, 30)

    #     # Mostrar a distancia de um ponto especifico
    #     cv2.circle(back_frame, ponto, 4, (0, 0, 255))
    #     distancia = depth_frame[ponto[1], ponto[0]]
        
    #     cv2.putText(back_frame, '{}cm'.format(distancia/10), canto_superior_direito, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
        

    #     diretorio_destino = r'C:\Users\20221CECA0402\Documents\Projeto_WRL\Aplicativo_WRL\fotos'
        
    #     agora = datetime.now()
        
    #     # Formatar a data e hora como parte do nome do arquivo
    #     nome_arquivo = agora.strftime('registro_%d-%m-%Y_%H.%M') + '.png'

    #     caminho_completo = os.path.join(diretorio_destino, nome_arquivo)


    #     # Aguardar a tecla 'q' para salvar o frame e encerrar o programa
    #     key = cv2.waitKey(1)
    #     if key == ord('q'):
    #         # Salvar o frame como imagem 
    #         cv2.imwrite(caminho_completo, frame)
    #         break

    #     # cv2.imshow('Color frame', back_frame)
    #     # key = cv2.waitKey(1)
    #     # if key == 27:
    #     #     break
    #-------------------------------------------------

    # def up():
        
        
    #         # frame = imutils.resize(frame,width=1000)
    #         # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
    #         img = Image.fromarray(back_frame)
    #         imagetk = ImageTk.PhotoImage(image=img)
            
    #         marcador_cima.configure(image = imagetk)
    #         marcador_cima.image = imagetk
    #         marcador_cima.after(10,up)

    # up() 
    
     
    
def aba_camera(inp_janela):
    janela_tres = tk.Toplevel()

    tela(janela_tres)
    frames_da_tela(janela_tres)
    componentes_frame1(frame_um, janela_tres, inp_janela)
    componentes_frame2(frame_dois)
    
    janela_tres.transient(inp_janela)
    janela_tres.focus_force() #era pra janela ser o foco
    janela_tres.grab_set()
    

print("\n\n", color.Fore.GREEN + "Iniciando o código - Tela da câmera" + color.Style.RESET_ALL)

print(color.Fore.RED + "Finalizando o código - Tela da câmera" + color.Style.RESET_ALL, "\n")