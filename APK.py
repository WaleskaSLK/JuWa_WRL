from tkinter import ttk, CENTER
import tkinter as tk
import sqlite3 as sql
import colorama as color
import customtkinter
from PIL import Image, ImageTk
import FUNCOES_APK as fun

"""Linha de raciocinio:
Antes de tirar a foto o funcionaria já informou o ID, que nele já esta contido Furos,
Grupo, SIte e BOF. Sendo assim, nesta aba, o Grupo, site e bof estão com seu ID, e os 
Registros estarão vindo do banco de dados.
"""

# pasta = r'C:\Users\20221CECA0402\Documents'
# {=======================Comando para o Banco de Dados=========================}

def selecao(inp_ID, inp_tipo): # {=========Leitura Grupo, SIte, BOF e ID(FRAME 1)=========}
    global ID
    
    inp_ID = int(inp_ID)
    ID = inp_ID
    
    conn, cursor = fun.CONECTA_BD(r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db")
    comando = f"SELECT * FROM DADOS_EMPRESAS WHERE ID = {inp_ID} AND TIPO = '{inp_tipo}' "
    cursor.execute(comando)
    dados = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    grupo_completo = list(dados[0])
    dados = [item for sublist in dados for item in sublist]
    grupo_completo = grupo_completo[0]
    lista_grupo = grupo_completo.split('/')
    
    return  dados, lista_grupo

    
def tabela(int_arquivo): # {=========Informações da tabela(FRAME 2)=========}
    global registro_foto
    print('\narquivo =',int_arquivo )
    conn, cursor = fun.CONECTA_BD(r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db")
    comando = f"SELECT * FROM B6 WHERE ARQUIVO = '{int_arquivo}' "
    cursor.execute(comando)
    dados2 = cursor.fetchone()
    fun.DESCONECTA_BD(conn)
    
    registro_foto = int_arquivo
    
    return dados2
    
    # dados2_filtrados = [resultado[2:] for resultado in dados2]

def imagens(registro_foto):  # {=========Informações para imagens(FRAME 2)=========}
    
    endereco_pastafotos = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\fotos_app"
    endereco_pastaguias = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\guias"
    # local_image = '\\'+ registro_foto
    #local_image = '\\'+ dados2[0][2] #+'.png'   (esta linha caso for usar '.fetchall' no 'def tabela' assim fazendo uma tupla e não uma lista)
        
    arquivofoto = endereco_pastafotos +'\\' +registro_foto
    arquivoguia = endereco_pastaguias +'\\' +registro_foto
    return arquivofoto, arquivoguia

def tela(inp_janela): # {=======================Configuração de tela=========================}
    inp_janela.title("Where Register Lances (WRL)")
    inp_janela.configure(background= '#9BCD9B')
    inp_janela.geometry("1280x700")
    inp_janela.resizable(True, True) #se quiser impedir que amplie ou diminua a tela, altere para False
    # inp_janela.maxsize(width=1920, height=1080) #limite máximo da tela
    inp_janela.minsize(width=700, height=450) #limite minimo da tela

def frames_da_tela(inp_janela): 
    global frame_1, frame_2
    # {=======================Frame da Direita=========================}
    frame_1 = tk.Frame(inp_janela, bd=2,
                            bg= '#B4EEB4',
                            highlightbackground= '#668B8B', 
                            highlightthickness=1)
    frame_1.place(relx=0.4, rely=0.02,relwidth=0.59, relheight=0.96)
    
    # {=======================Frame da Esquerda=========================}
    frame_2 = tk.Frame(inp_janela, bd=2,
                            bg= '#B4EEB4',
                            highlightbackground= '#668B8B', 
                            highlightthickness=1)
    frame_2.place(relx=0.01, rely=0.02,relwidth=0.38, relheight=0.96)

def componentes_frame1(inp_ID, inp_tipo, int_arquivo):
    dados, lista_grupo = selecao(inp_ID,inp_tipo)
    grupo = lista_grupo[0]
    
    site = dados[1]
    BOF = dados[2]
    tipo = dados[3]
    ID = dados[4]
    
    # {=======================Título=========================}
    titulo1_pg1 = tk.Label(frame_1,
                                text="Dados do Bico",
                                font=('arial', '25', 'bold'),
                                bg= '#B4EEB4',
                                fg="#2F4F4F")
    titulo1_pg1.place(relx=0.32, rely=0.03)
    
    # {=======================Grupo=========================}
    grupo_pg1 = tk.Label(frame_1,
                                text="Grupo:",
                                font=('verdana', '20','bold'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    grupo_pg1.place(relx=0.05, rely=0.15)

    grupo_pg1 = tk.Label(frame_1,
                                text = grupo,
                                font=('verdana', '20'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    grupo_pg1.place(relx=0.2, rely=0.15)

    # {=======================Site=========================}
    site_pg1 = tk.Label(frame_1,
                                text="Site:",
                                font=('verdana', '20','bold'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    site_pg1.place(relx=0.05, rely=0.25)

    site_pg1 = tk.Label(frame_1,
                                text=site,
                                font=('verdana', '20'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    site_pg1.place(relx=0.15, rely=0.25)

    # {=======================BOF=========================}
    BOF_pg1 = tk.Label(frame_1,
                        text="BOF:",
                        font=('verdana', '20','bold'),
                        bg= '#B4EEB4',
                        fg="#1C1C1C")
    BOF_pg1.place(relx=0.05, rely=0.35)

    site_pg1 = tk.Label(frame_1,
                        text=BOF,
                        font=('verdana', '20'),
                        bg= '#B4EEB4',
                        fg="#1C1C1C")
    site_pg1.place(relx=0.15, rely=0.35)
    
    # {=======================ID=========================}
    ID_pg1 = tk.Label(frame_1,
                        text="ID:",
                        font=('verdana', '20','bold'),
                        bg= '#B4EEB4',
                        fg="#1C1C1C")
    ID_pg1.place(relx=0.05, rely=0.45)

    ID_informado_pg1 = tk.Label(frame_1,
                                text = ID,
                                font=('verdana', '20'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    ID_informado_pg1.place(relx=0.12, rely=0.45)
    
    
    dados2 = tabela(int_arquivo)
    vida = dados2[1]
    data_foto = dados2[5]
    hora_foto = dados2[6]
    medidas_foto = dados2[7:]
   
    # {=======================Data=========================}
    ID_pg1 = tk.Label(frame_1,
                        text="Data:",
                        font=('verdana', '20','bold'),
                        bg= '#B4EEB4',
                        fg="#1C1C1C")
    ID_pg1.place(relx=0.05, rely=0.55)

    ID_informado_pg1 = tk.Label(frame_1,
                                text = data_foto,
                                font=('verdana', '20'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    ID_informado_pg1.place(relx=0.17, rely=0.55)
    
    # {=======================Hora=========================}
    ID_pg1 = tk.Label(frame_1,
                                text="Hora:",
                                font=('verdana', '20','bold'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    ID_pg1.place(relx=0.05, rely=0.65)

    ID_informado_pg1 = tk.Label(frame_1,
                                text = hora_foto,
                                font=('verdana', '20'),
                                bg= '#B4EEB4',
                                fg="#1C1C1C")
    ID_informado_pg1.place(relx=0.17, rely=0.65)
    
    # {=======================Registros=========================}

    tabela_pg1 = ttk.Treeview(frame_1, height=10,column=("col1", "col2"),style="mystyle.Treeview")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Verdana', 14,'bold'))
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 12))

    tabela_pg1.heading("#0", text="")
    tabela_pg1.heading("#1", text="Classe")
    tabela_pg1.heading("#2", text="Diametro(px)")
    
    tabela_pg1.column("#0", width=1)
    tabela_pg1.column("#1", width=180)
    tabela_pg1.column("#2", width=200)
    
    cont = int(BOF) + 1
    cont2 = 1
    
    for dado in medidas_foto:
        if cont2 == cont:
            tabela_pg1.insert("", tk.END, values=('Bico', dado))
        else:
            tabela_pg1.insert("", tk.END, values=(f'Furo {cont2}', dado))
        cont2 += 1
                
    tabela_pg1.place(relx=0.45, rely=0.15, relwidth=0.5, relheight=0.7)

    # scroolLista = tk.Scrollbar(frame_1, orient ='vertical')
    # tabela_pg1.configure(yscroll = scroolLista.set)
    # scroolLista.place(relx=0.93, rely=0.15, relwidth=0.03, relheight=0.7)
    
    # {=======================Botão Repetir=========================}
    btRepetir_pg1 = tk.Button(frame_1,
                                    text='Repetir',
                                    cursor = "exchange",
                                    bd = 4,
                                    bg = '#545454',
                                    fg = 'white',
                                    font= ("arial", 13,'bold'))
    btRepetir_pg1.place(relx=0.35, rely=0.9, relwidth=0.12, relheight=0.08)

    # {=======================Botão Continuar=========================}
    btContinuar_pg1 = tk.Button(frame_1,
                                    text='Continuar',
                                    cursor = "hand2",
                                    bd = 4,
                                    bg = '#545454',
                                    fg = 'white',
                                    font= ("arial", 13,'bold'))
    btContinuar_pg1.place(relx=0.55, rely=0.9, relwidth=0.12, relheight=0.08)


def componentes_frame2(): # {=========Componentes da direita=========}
    #  # {=======================Título=========================}
    # furos_pg1 = tk.Label(frame_2,
    #                             text = ID,
    #                             font = ('verdana', '23'),
    #                             bg = '#B4EEB4',
    #                             fg = "#2F4F4F")
    # furos_pg1.place(relx=0.32, rely=0.03)
    arquivofoto, arquivoguia = imagens(registro_foto)
    
    print('\nArquivo_foto=',arquivofoto,'\narquivo guia = ', arquivoguia)
    # {=======================Imagem 1=========================}
    img1_pg1 = tk.PhotoImage(file = arquivofoto)
    img1_pg1 = img1_pg1.subsample(2, 2)

    fotoimg1_pg1 = tk.Label(frame_2,
                                    bg= '#B4EEB4',
                                    bd =0,
                                    image = img1_pg1)
    fotoimg1_pg1.place(relx=0.5, rely=0.25, anchor=CENTER)
    

    # {=======================Imagem 2=========================}
    img2_pg1 = tk.PhotoImage(file = arquivoguia)
    img2_pg1 = img2_pg1.subsample(2, 2)

    fotoimg2_pg1 = tk.Label(frame_2,
                                    bg= '#B4EEB4',
                                    bd =0,
                                    image = img2_pg1)
    fotoimg2_pg1.place(relx=0.5, rely=0.7, anchor=CENTER)

    # {=======================WRL=========================}
    titulo2_pg1 = tk.Label(frame_2,
                                text="Where Register Lances(WRL)",
                                font=('italic', '18'),
                                bg= '#B4EEB4',
                                fg="#2F4F4F")
    titulo2_pg1.place(relx=0.01, rely=0.94)

def aba_dados(inp_janela,inp_ID,inp_tipo, int_arquivo):
    # janela = tk.Tk()
    janela = tk.Toplevel(inp_janela)
    
    tela(inp_janela)
    frames_da_tela(inp_janela)
    componentes_frame1(inp_ID, inp_tipo, int_arquivo)
    componentes_frame2()
    
    janela.transient(inp_janela) #TOPLEVEL
    janela.focus_force() #TOPLEVEL
    janela.grab_set() #TOPLEVEL
    
    return janela
    

print("\n\n", color.Fore.GREEN + "Iniciando o código - Dados do bico" + color.Style.RESET_ALL)
print(color.Fore.RED + "Finalizando o código - Dados do bico" + color.Style.RESET_ALL, "\n")