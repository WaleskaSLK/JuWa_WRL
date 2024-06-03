from tkinter import ttk, CENTER
import tkinter as tk
import sqlite3 as sql
import colorama as color
import customtkinter
from PIL import Image, ImageTk
import FUNCOES_APK as fun



# # try:
# #     cursor.execute("""CREATE TABLE "B6" ("ID"	INTEGER NOT NULL,
# #                                         "TIPO"	TEXT NOT NULL,
# #                                         "ARQUIVO"	TEXT NOT NULL,
# #                                         "DATA"	NUMERIC NOT NULL,
# #                                         "HORA"	NUMERIC NOT NULL,
# #                                         "EXTERNO"	INTEGER NOT NULL,
# #                                         "FURO_1"	REAL NOT NULL,
# #                                         "FURO_2"	REAL NOT NULL,
# #                                         "FURO_3"	REAL NOT NULL,
# #                                         "FURO_4"	REAL NOT NULL,
# #                                         "FURO_5"	REAL NOT NULL,
# #                                         "FURO_6"	REAL NOT NULL,
# #                                         PRIMARY KEY("ID")
# #                                         )""")
    
# #     cursor.execute("INSERT INTO B6 VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','27/03/2024','13:27', 479.84 , 80.08 , 83.14, 84.88, 86.38, 79.84, 84.93))
# # except:
# #     print("ta criado mermao 1")

# try:
#     # cursor.execute("""CREATE TABLE "DADOS_EMPRESAS" (
#     #     "Grupo"	TEXT NOT NULL,
#     #     "Site"	TEXT NOT NULL,
#     #     "BOF"	INTEGER NOT NULL,
#     #     "ID"	TEXT NOT NULL,
#     #     PRIMARY KEY("ID")
#     # )""")
#     # cursor.execute("DELETE FROM DADOS_EMPRESAS")
#     cursor.execute("INSERT INTO DADOS_EMPRESAS VALUES(?,?,?,?,?)",('USIMINAS/ES/BRASIL' ,'Ipatinga 1', 6,'30/7','001'))
# except:
#     print("ta criado mermao 2")



# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 1'  , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 2' , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 3'  , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 4'  , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 5' , '27/03/2024','13:27' ))
# # cursor.execute("INSERT INTO REGISTROS_MEDICOES VALUES(?,?,?,?,?,?)",('001' ,'30/5', 'registro_001_27-03-2024_13.27.png','furo 6'  , '27/03/2024','13:27' ))

# # cursor.execute("UPDATE DADOS_EMPRESAS SET GRUPO = 'USIMINAS/ES/BRASIL' WHERE GRUPO = 'Usiminas' ")

# banco.commit()
# print('Feito 4')

# import tkinter as tk
# import FUNCOES_APK as fun
# from teste2 import aba_cadastro

# """ primeira parte"""

# # def INICIAR_INSPECAO(inp_janela):
# #     janela_cadastro = aba_cadastro(inp_janela) #Segunda janela = função na janela dois(janela atual)
# #     janela_cadastro.deiconify()  # Exibe a janela de cadastro
# #     # inp_janela.destroy()  # Destrói a janela atual
    
    
# def tela(inp_janela): # {=======================Configuração de tela=========================}
#     inp_janela.title("Where Register Lances (WRL)")
#     inp_janela.configure(background= '#9BCD9B')
#     inp_janela.geometry("1280x800")
#     inp_janela.resizable(False, False) #se quiser impedir que amplie ou diminua a tela, altere para False
#     # janela.maxsize(width=1920, height=1080) #limite máximo da tela
#     inp_janela.minsize(width=700, height=450)
    
# def frames_da_tela(inp_janela): 
#     global frame_1
#     frame_1 = fun.CRIAR_FRAME(inp_janela, '#B4FF9A', '#668B8B')
#     frame_1.place(relx=0.01, rely=0.02,relwidth=0.98, relheight=0.96)
#     return frame_1

# def componentes_frame1(inp_frame,janela_menu):
    
#     lista = []
#     input_furos = tk.Entry(inp_frame, validate= "key",font=("Arial", 18))
#     input_furos.place(relx=0.18, rely=0.5, relwidth=0.27, relheight=0.05)
    
#     def imprimir_palavra():
#         lista.append(input_furos.get())
#         print(lista)
    
#     bt_voltar = fun.CRIAR_BOTAO(inp_frame, "VOLTAR",'#258D19', 'white',3,'20','',"hand2", imprimir_palavra)
#     bt_voltar.place(relx=0.05, rely=0.89, relwidth=0.2, relheight=0.08)
    

# def open():
#     janela_PG1 = tk.Tk()
#     tela(janela_PG1)
#     frames_da_tela(janela_PG1)
#     componentes_frame1(frame_1,janela_PG1)
#     aba_cadastro = None
#     janela_PG1.mainloop()
    
#     return janela_PG1
    
# open()

inp_janela = tk.Tk()

inp_janela.title("testando")
inp_janela.configure(background= '#9BCD9B')
inp_janela.geometry("1280x700")
inp_janela.resizable(True, True) #se quiser impedir que amplie ou diminua a tela, altere para False
# inp_janela.maxsize(width=1920, height=1080) #limite máximo da tela
inp_janela.minsize(width=700, height=450) #limite minimo da tela
    
frame_2 = tk.Frame(inp_janela, bd=2,
                    bg= '#B4EEB4',
                    highlightbackground= '#668B8B', 
                    highlightthickness=1)
frame_2.place(relx=0.01, rely=0.02,relwidth=0.38, relheight=0.96)

arquivofoto = r'C:\Users\20221CECA0402\Documents\Projeto_WRL\Aplicativo_WRL\fotos_BW\registro_001_03-06-2024_13.01.png'

img1_pg1 = tk.PhotoImage(file = arquivofoto)
img1_pg1 = img1_pg1.subsample(2, 2)

fotoimg1_pg1 = tk.Label(frame_2,
                                bg= '#B4EEB4',
                                bd =0,
                                image = img1_pg1)
fotoimg1_pg1.place(relx=0.5, rely=0.25, anchor=CENTER)
    
# arquivofoto= r'C:\Users\20221CECA0402\Documents\Projeto_WRL\Aplicativo_WRL\fotos_BW\registro_001_29-05-2024_18.58.png'

# img1_pg1 = tk.PhotoImage(file = arquivofoto)
# img1_pg1 = img1_pg1.subsample(2, 2)

# fotoimg1_pg1 = tk.Label(frame_2,
#                                 bg= '#B4EEB4',
#                                 bd =0,
#                                 image = img1_pg1)
# fotoimg1_pg1.place(relx=0.5, rely=0.25, anchor=CENTER)

# arquivoguia =r'C:\Users\20221CECA0402\Documents\Projeto_WRL\Aplicativo_WRL\fotos_segmentada\registro_001_29-05-2024_18.57.png'
# img2_pg1 = tk.PhotoImage(file = arquivoguia)
# img2_pg1 = img2_pg1.subsample(2, 2)

# fotoimg2_pg1 = tk.Label(frame_2,
#                             bg= '#B4EEB4',
#                             bd =0,
#                             image = img2_pg1)
# fotoimg2_pg1.place(relx=0.5, rely=0.7, anchor=CENTER)

inp_janela.mainloop()



