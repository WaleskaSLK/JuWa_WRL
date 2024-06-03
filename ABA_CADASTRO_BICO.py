from tkinter import ttk, CENTER, messagebox
import tkinter as tk
# import sqlite3 as sql
import colorama as color
from customtkinter import *
# from PIL import Image, ImageTk
import FUNCOES_APK as fun

caminho = r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\REGISTROS_WRL.db"

def USINAS():
    conn, cursor = fun.CONECTA_BD(caminho)
    comando = f"SELECT Grupo FROM DADOS_EMPRESAS "
    cursor.execute(comando)
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    dados_filtrados = list(set(item[0] for item in dados_banco))
    return dados_filtrados

def SITE():
    conn, cursor = fun.CONECTA_BD(caminho)
    comando = f"SELECT Site FROM DADOS_EMPRESAS "
    cursor.execute(comando)
    dados_banco = cursor.fetchall()
    fun.DESCONECTA_BD(conn)
    
    dados_filtrados = list(set(item[0] for item in dados_banco))
    return dados_filtrados

def tabela(): # {=========Informações da tabela(FRAME 2)=========}
    conn, cursor = fun.CONECTA_BD(caminho)
    comando = f"SELECT * FROM DADOS_EMPRESAS "
    cursor.execute(comando)
    dados_tabela =cursor.fetchall()
    fun.DESCONECTA_BD(conn)

    return dados_tabela

def ENTRY_INT(inp_text):
    if inp_text == "": return True
    try:
        value = int(inp_text)
    except ValueError: return False
    
    return 0 <= value <= 10000000000 #Qual a vida máxima geralmente?

def validador(input):
    return input.register(ENTRY_INT), "%P"

def voltar(aba_1, aba_2):
    aba_1.deiconify()  # Exiba a janela da aba 1
    aba_2.destroy()  # Destrua a janela da aba 2
    
def tela(inp_janela):
    inp_janela.title("Where Register Lances (WRL)")
    inp_janela.configure(background= '#9BCD9B')
    inp_janela.geometry("1280x800")
    inp_janela.resizable(False, False) #se quiser impedir que amplie ou diminua a tela, altere para False
    # janela.maxsize(width=1920, height=1080) #limite máximo da tela
    inp_janela.minsize(width=700, height=450) #limite minimo da tela

def frames_da_tela(inp_janela): 
        global frame_1, frame_2
        frame_1 = tk.Frame(inp_janela,
                            bg= '#B4FF9A',
                            highlightbackground= '#668B8B')
        frame_1.place(relx=0.01, rely=0.02,relwidth=0.48, relheight=0.96)

        frame_2 = tk.Frame(inp_janela,
                            bg= '#B4FF9A',
                            highlightbackground= '#668B8B')
        frame_2.place(relx=0.5, rely=0.02,relwidth=0.49, relheight=0.96)
        
        return frame_1, frame_2


def componentes_frame1(inp_frame,inp_janela, inp_menu):
    # {=======================Título=========================}
    titulo = fun.CRIAR_LABEL(inp_frame, "Cadastrar Bico", '#B4FF9A', "#005200", 'arial', '25', 'bold')
    titulo.place(relx=0.3, rely=0.05) 

    # {=======================USINA=========================}
    label_usina = fun.CRIAR_LABEL(inp_frame, "Usina: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_usina.place(relx=0.03, rely=0.2)
    
    Var_Usina = tk.StringVar(inp_frame)
    
    input_Usina = tk.OptionMenu(inp_frame, Var_Usina, *USINAS())
    input_Usina.config(font=("Arial", 18))
    input_Usina.place(relx=0.2, rely=0.2, relwidth=0.75, relheight=0.05)
    
    # {=======================SITE=========================}
    label_site = fun.CRIAR_LABEL(inp_frame, "Site: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_site.place(relx=0.03, rely=0.35)
    
    Var_site = tk.StringVar(inp_frame)
    input_site = tk.OptionMenu(inp_frame, Var_site, *SITE()) 
    
    input_site.config(font=("Arial", 18))
    input_site.place(relx=0.15, rely=0.35, relwidth=0.8, relheight=0.05)

    # {=======================FUROS=========================}
    label_furos = fun.CRIAR_LABEL(inp_frame, "Furos: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold' )
    label_furos.place(relx=0.03, rely=0.5)

    input_furos = tk.Entry(inp_frame, validate= "key",font=("Arial", 18), validatecommand= validador(inp_frame))
    input_furos.place(relx=0.18, rely=0.5, relwidth=0.27, relheight=0.05)
    
    # {=======================TIPO=========================}
    label_tipo = fun.CRIAR_LABEL(inp_frame, "Tipo: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_tipo.place(relx=0.47, rely=0.5)

    input_tipo = tk.Entry(inp_frame,font=("Arial", 18))
    input_tipo.place(relx=0.6, rely=0.5, relwidth=0.35, relheight=0.05)
    
    # {=======================ID=========================}
    label_ID = fun.CRIAR_LABEL(inp_frame, "ID: ", '#B4FF9A', "#1C1C1C", 'arial', '20', 'bold')
    label_ID.place(relx=0.03, rely=0.65)

    input_ID = tk.Entry(inp_frame, validate= "key",font=("Arial", 18), validatecommand= validador(inp_frame))
    input_ID.place(relx=0.11, rely=0.65, relwidth=0.85, relheight=0.05)
    
    # {=======================Botão Voltar e Continuar=========================}
    dados_obtidos = []
    
    def salvar(aba_1, aba_2):
        try:
            dados_obtidos.append(Var_Usina.get())
            dados_obtidos.append(Var_site.get())
            # furos_aux = input_furos.get()
            dados_obtidos.append(input_furos.get())
            dados_obtidos.append(input_tipo.get())
            # ID_aux = input_ID.get()
            dados_obtidos.append(input_ID.get())
            
        except:  
            todos_tabela = tabela()
            print('sccr', dados_obtidos)
            for tupla in todos_tabela:
                ultimo_algarismo_tupla = str(tupla[-1])[-1]  # Obtém o último dígito da tupla
                if dados_obtidos[-1] == ultimo_algarismo_tupla:
                    messagebox.showwarning("AVISO","Este ID já existe")
            
            if tuple(dados_obtidos) in todos_tabela:
                messagebox.showwarning("AVISO","Já existe este registro")
            
            param = 0
            for dado in dados_obtidos:
                if dado == '':
                    param += 1
            
            if param > 0:
                messagebox.showwarning("AVISO","Preencha todos os espaços")
            
            else:
                conn, cursor = fun.CONECTA_BD(caminho)
                conn.commit()
                comando = f"INSERT INTO DADOS_EMPRESAS VALUES (?, ?, ?, ?, ?) "
                registros = (dados_obtidos[0], dados_obtidos[1], dados_obtidos[2], dados_obtidos[3], dados_obtidos[4])
                cursor.execute(comando, registros)
                conn.commit()
                print("\n\n", color.Fore.CYAN + "DADOS SALVOS - ABA_CADASTRO_BICO" + color.Style.RESET_ALL)
                fun.DESCONECTA_BD(conn)

                aba_1.deiconify()  # Exiba a janela da aba 1
                aba_2.destroy() 
    
    bt_voltar = fun.CRIAR_BOTAO(inp_frame, "VOLTAR",'#258D19', 'white',3,'20','',"hand2",lambda: voltar( inp_menu, inp_janela))
    bt_voltar.place(relx=0.05, rely=0.89, relwidth=0.2, relheight=0.08)

    bt_continuar = fun.CRIAR_BOTAO(inp_frame, "SALVAR",'#258D19', 'white',3,'20','',"hand2",lambda: salvar(inp_menu, inp_janela))
    bt_continuar.place(relx=0.65, rely=0.89, relwidth=0.3, relheight=0.08)

def componentes_frame2(inp_frame):
    # {=======================Título=========================}
    titulo = fun.CRIAR_LABEL(inp_frame, "Bicos Registrados", '#B4FF9A', "#005200", 'arial', '25', 'bold')
    titulo.place(relx=0.3, rely=0.05) 
    
    Tabela = ttk.Treeview(inp_frame, height=10,column=("col1", "col2", "col3", "col4", "col2 5"),style="mystyle.Treeview")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Verdana', 12,'bold'))
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 10))

    Tabela.heading("#0", text="")
    Tabela.heading("#1", text="Grupo")
    Tabela.heading("#2", text="Site")
    Tabela.heading("#3", text="Furos")
    Tabela.heading("#4", text="Tipo")
    Tabela.heading("#5", text="ID")
    
    Tabela.column("#0", width=1)
    Tabela.column("#1", width=150)
    Tabela.column("#2", width=100)
    Tabela.column("#3", width=30)
    Tabela.column("#4", width=60)
    Tabela.column("#5", width=20)
    
    for dado in tabela():
        Tabela.insert("", tk.END, values=(dado[0], dado[1], dado[2], dado[3], dado[4]))
        
    Tabela.place(relx=0.05, rely=0.12, relwidth=0.9, relheight=0.85)
        
        
    
def aba_cadastro_bico(inp_janela): # AVISO -> passar a variavel "inp_janela" dentro dos ()
    janela_atual = tk.Toplevel(inp_janela)
    # janela_atual = tk.Tk() #AVISO ->tirar esta linha e manter a de cima
    tela(janela_atual)
    frames_da_tela(janela_atual)
    componentes_frame1(frame_1, janela_atual, inp_janela)
    componentes_frame2(frame_2)
    
    janela_atual.transient(inp_janela)
    janela_atual.focus_force() #era pra janela ser o foco
    janela_atual.grab_set()
    
    # janela_atual.mainloop() #AVISO ->tirar esta linha
    return janela_atual


# aba_cadastro_bico() #AVISO ->tirar esta linha
