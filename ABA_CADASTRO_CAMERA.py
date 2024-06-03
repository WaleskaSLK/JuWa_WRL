# from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import colorama as color
#from customtkinter import *
# from PIL import Image, ImageTk
import sqlite3 as sql
import FUNCOES_APK as fun
from APP2 import aba_camera

def USINAS():
    caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"
    conn, cursor = fun.CONECTA_BD(caminho)
    comando = f"SELECT Grupo FROM DADOS_EMPRESAS "
    cursor.execute(comando)
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    dados_filtrados = list(set(item[0] for item in dados_banco))
    return dados_filtrados

def USINA_SITE(usina):
    caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"
    conn, cursor = fun.CONECTA_BD(caminho)
    comando = f"SELECT Site FROM DADOS_EMPRESAS WHERE Grupo = ?"
    cursor.execute(comando, (usina,))
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    dados_filtrados = list(set(item[0] for item in dados_banco))
    return dados_filtrados

def SITE():
    caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"
    conn, cursor = fun.CONECTA_BD(caminho)
    comando = f"SELECT Site FROM DADOS_EMPRESAS "
    cursor.execute(comando)
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    dados_filtrados = list(set(item[0] for item in dados_banco))
    return dados_filtrados

def FUROS_ID():
    caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"
    
    conn, cursor = fun.CONECTA_BD(caminho)
    ID = f"SELECT ID FROM DADOS_EMPRESAS "
    cursor.execute(ID)
    dados_ID = cursor.fetchall()
    
    FUROS = f"SELECT FUROS FROM DADOS_EMPRESAS "
    cursor.execute(FUROS)
    dados_FUROS = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    dados_filtrados = [f"{furos[0]} - {id[0]}" for furos, id in zip(dados_FUROS, dados_ID)]
    return dados_filtrados

def TIPO():
    caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"
    conn, cursor = fun.CONECTA_BD(caminho)
    comando = f"SELECT TIPO FROM DADOS_EMPRESAS "
    cursor.execute(comando)
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    dados_filtrados = list(set(item[0] for item in dados_banco))
    return dados_filtrados

def ENTRY_INT(inp_text):
    if inp_text == "": return True
    try:
        value = int(inp_text)
    except ValueError: return False
    
    return 0 <= value <= 100000000000 #Qual a vida máxima geralmente?

def ENTRY_STRING(inp_text):
    return all(char.isalpha() or char.isspace() for char in inp_text) or inp_text == ""


def validador(input):
    comando = (input.register(ENTRY_INT), "%P") 
    return comando

# def ABA_CAMERA(janela_menu):
#         return (aba_camera(janela_menu))

def voltar(aba_1, aba_2):
    aba_1.deiconify()  # Exiba a janela da aba 1
    aba_2.destroy()  # Destrua a janela da aba 2
    
def comandos_botao_continuar(inp_janela,menu_inicial,inp_usina_grupo, inp_site, inp_furos_ID, inp_tipo, inp_vida, inp_nome):
    dados = adquirir_dados(inp_usina_grupo, inp_site, inp_furos_ID, inp_tipo, inp_vida, inp_nome)
    janela_cadastro = aba_camera(inp_janela, dados,menu_inicial)
    janela_cadastro.deiconify()
    
    
def adquirir_dados(inp_usina_grupo, inp_site, inp_furos_ID, inp_tipo, inp_vida, inp_nome): #juliaaaaaa
    DADOS_INSERIDOS = []
    try: 
        usina_grupo = inp_usina_grupo.get()
        site = inp_site.get()
        furos_ID = inp_furos_ID.get()
        separacao_furos_ID = furos_ID.split('-')
        
        furos = separacao_furos_ID[0].strip()
        ID = separacao_furos_ID[1].strip()
        
        tipo = inp_tipo.get()
        vida = inp_vida.get()
        nome = inp_nome.get().upper()
        
        for dado in [usina_grupo, site, furos, ID, tipo, vida, nome]:
            DADOS_INSERIDOS.append(dado)
            
        return DADOS_INSERIDOS
    except:
        messagebox.showwarning("AVISO","Selecione ID-Bico")
    
def botao_continuar_foto(inp_furos_ID, inp_tipo, inp_vida, inp_nome):
    
    str_furos_ID = inp_furos_ID.split('-')
    Furos = str_furos_ID[0]
    ID = str_furos_ID[1]
    
    caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"
    conn, cursor = fun.CONECTA_BD(caminho)
    
    tabela = 'B' + Furos 
    comando = f"INSERT INTO {tabela} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    registro = (inp_nome, inp_vida, ID, inp_tipo, inp_vida, inp_nome)
    
    cursor.execute(comando)
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
def tela(inp_janela):
    inp_janela.title("Where Register Lances (WRL)")
    inp_janela.configure(background= '#9BCD9B')
    inp_janela.attributes("-fullscreen", True)
    # inp_janela.geometry("1000x600")
    # inp_janela.resizable(True, True) #se quiser impedir que amplie ou diminua a tela, altere para False
    # # janela.maxsize(width=1920, height=1080) #limite máximo da tela
    # inp_janela.minsize(width=700, height=450) #limite minimo da tela

def frames_da_tela(inp_janela): 
        global frame_1
        
        frame_1 = tk.Frame(inp_janela,
                            bg= '#B4FF9A',
                            highlightbackground= '#668B8B')
        frame_1.place(relx=0.01, rely=0.02,relwidth=0.98, relheight=0.96)
        
        return frame_1

def componentes_frame1(inp_frame,inp_janela, inp_menu):# #TOPLEVEL
    
    # {=======================Título=========================}
    titulo = fun.CRIAR_LABEL(inp_frame, "Selecionar Bico", '#B4FF9A', "#005200", 'arial', '25', 'bold')
    titulo.place(relx=0.38, rely=0.04) 

    # {=======================Dados à inserir=========================
    # Filtrar os dados
    
    # {=======================USINA=========================}
    label_usina = fun.CRIAR_LABEL(inp_frame, "Usina/Grupo: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_usina.place(relx=0.05, rely=0.2)

    Var_Usina = tk.StringVar(inp_frame)
    
    Menu_Usina = tk.OptionMenu(inp_frame, Var_Usina, *USINAS())
    Menu_Usina.config(font=("Arial", 25))
    Menu_Usina.place(relx=0.05, rely=0.27, relwidth=0.35, relheight=0.06)
    
    Usina_selecionada = Var_Usina.get() 

    # {=======================SITE=========================}
    label_site = fun.CRIAR_LABEL(inp_frame, "Site: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_site.place(relx=0.55, rely=0.2)

    Var_site = tk.StringVar(inp_frame)

    if Usina_selecionada == "":
        Menu_site = tk.OptionMenu(inp_frame, Var_site, "")
        Menu_site['menu'].delete(0, 'end')
        for site in SITE():
            Menu_site['menu'].add_command(label=site, command=tk._setit(Var_site, site))
    
    if Usina_selecionada != "":
        Menu_site = tk.OptionMenu(inp_frame, Var_site, "")
        Menu_site['menu'].delete(0, 'end')
        for site in USINA_SITE(Usina_selecionada):
            Menu_site['menu'].add_command(label=site, command=tk._setit(Var_site, site))
    
    # if Usina_selecionada == "":
    #     Menu_site = tk.OptionMenu(inp_frame, Var_site, *SITE())
    
    # if Usina_selecionada != "":
    #     Menu_site = tk.OptionMenu(inp_frame, Var_site, *USINA_SITE(Usina_selecionada))  
    
    Menu_site.config(font=("Arial", 25))
    Menu_site.place(relx=0.55, rely=0.27, relwidth=0.35, relheight=0.06)

    # {=======================BOF _ ID=========================}
    label_IDTipo = fun.CRIAR_LABEL(inp_frame, "FUROS - ID: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_IDTipo.place(relx=0.05, rely=0.4)

    Var_IDTipo = tk.StringVar(inp_frame)
    """Var_IDTipo.set(FUROS_ID()[0])"""
    
    Menu_IDTipo = tk.OptionMenu(inp_frame, Var_IDTipo, *FUROS_ID())
    Menu_IDTipo.config(font=("Arial", 25))
    Menu_IDTipo.place(relx=0.05, rely=0.47, relwidth=0.27, relheight=0.06)
    
    if Menu_IDTipo == '6 - 1':
        print("foi?")
    # {=======================TIPO=========================}
    label_tipo = fun.CRIAR_LABEL(inp_frame, "Tipo: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_tipo.place(relx=0.35, rely=0.4)

    Var_tipo = tk.StringVar(inp_frame)
    
    Menu_tipo = tk.OptionMenu(inp_frame, Var_tipo, *TIPO())
    Menu_tipo.config(font=("Arial", 25))
    Menu_tipo.place(relx=0.35, rely=0.47, relwidth=0.27, relheight=0.06)
    
    # {=======================VIDA=========================}
    label_vida = fun.CRIAR_LABEL(inp_frame, "Vida: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_vida.place(relx=0.65, rely=0.4)

    input_vida = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand= validador(inp_frame) )
    input_vida.place(relx=0.65, rely=0.47, relwidth=0.27, relheight=0.06)

    # {=======================Usuário=========================}
    label_usuario = fun.CRIAR_LABEL(inp_frame, "Usuário: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_usuario.place(relx=0.05, rely=0.6)

    input_usuario = tk.Entry(inp_frame, validate= "key",font=("Arial", 25), validatecommand="key")
    input_usuario.place(relx=0.05, rely=0.67, relwidth=0.85, relheight=0.06)
    
    
    vcmd = (input_usuario.register(ENTRY_STRING), '%P')
    input_usuario.config(validatecommand=vcmd)

    # {=======================Botão Voltar e Continuar=========================}
    bt_voltar = fun.CRIAR_BOTAO(inp_frame, "MENU",'#258D19', 'white',3,'20','',"hand2", lambda: voltar( inp_menu, inp_janela))# #TOPLEVEL
    bt_voltar.place(relx=0.05, rely=0.88, relwidth=0.2, relheight=0.08)
    # inp_janela.withdraw()

    bt_continuar = fun.CRIAR_BOTAO(inp_frame, "CONTINUAR",'#258D19', 'white',3,'20','',"hand2",lambda: comandos_botao_continuar(inp_janela,inp_menu,Var_Usina,Var_site,Var_IDTipo,Var_tipo,input_vida,input_usuario))
    bt_continuar.place(relx=0.75, rely=0.88, relwidth=0.2, relheight=0.08)
    
    # {=======================FECHAR ABA=========================}
    # bt_fechar_aba_menu = tk.Button(inp_frame, text="X", command=inp_janela.destroy, bg="red").place(relx=0.96, rely=0.02, relwidth=0.03, relheight=0.04) #AVISO ->tirar esta linha

        
def aba_cadastro(inp_janela): 
    # janela_dois = tk.Tk()
    janela_dois = tk.Toplevel(inp_janela) #TOPLEVEL
    
    tela(janela_dois)
    frames_da_tela(janela_dois)
    componentes_frame1(frame_1,janela_dois,inp_janela)#  #TOPLEVEL

    janela_dois.transient(inp_janela) #TOPLEVEL
    janela_dois.focus_force() #TOPLEVEL
    janela_dois.grab_set() #TOPLEVEL
    # janela_dois.mainloop() #AVISO ->tirar esta linha
    
    return janela_dois


print("\n\n", color.Fore.GREEN + "Iniciando o código - Registro pre-medição" + color.Style.RESET_ALL)
# aba_cadastro() #AVISO ->tirar esta linha
print(color.Fore.RED + "Finalizando o código - Registro pre-medição" + color.Style.RESET_ALL, "\n")