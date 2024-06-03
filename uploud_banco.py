# import sqlite3 as sql
# import pandas as pd
import FUNCOES_APK as fun
# banco = sql.connect(r'C:\Users\20221CECA0402\Documents\Projeto_WRL\REGISTROS_WRL.db')
# cursor = banco.cursor()


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

caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"
conn, cursor = fun.CONECTA_BD(caminho)
comando = f"SELECT Grupo FROM DADOS_EMPRESAS "
cursor.execute(comando)
dados_banco = cursor.fetchall()
fun.DESCONECTA_BD(conn)

print(dados_banco)