# {=======================Video aula 1-P1=========================}

# import tkinter as tk
# from tkinter import messagebox

# # Função a ser chamada quando o botão é clicado
# def exibir_mensagem():
#     messagebox.showinfo("Mensagem", "Olá, mundo!")

# # Criação da janela principal
# root = tk.Tk()
# root.title("Exemplo Tkinter")

# # Criando um rótulo
# label = tk.Label(root, text="Bem-vindo ao Tkinter!")
# label.pack(pady=100)

# # Criando um botão
# button = tk.Button(root, text="Clique aqui", command=exibir_mensagem)
# button.pack(pady=5)

# # Executando o loop principal da aplicação
# root.mainloop()

# {=======================Video aula 1-P2=========================}

# from functools import partial
# import tkinter as tk

# # {=======================Funções=========================}
# def click(bot):
#     print(bot["text"]) #nome do botao
#     print (ed.get()) #O que foi escrito no Entry
#     lb["text"] = ed.get()

# {=======================Inicio/título=========================}
# janela = tk.Tk()
# janela.title("Teste 1")
# # https://www.plus2net.com/python/tkinter-colors.php
# janela["background"] = "springgreen2"

# # {=======================Ferramentas=========================}
# titulo = tk.Label(janela, text = "Seja bem-vindo ao prototipo", bg = "white")
# lateral = tk.Label(janela, text = "", bg = "white")

# titulo.pack(side= "top", fill = "x")
# lateral.pack(side= "right", fill = "y")

# lb1 = tk.Label(janela, text ="uno", background= "gray" )
# lb1.pack(side="right") #ou anchor = "W" ( n, ne, e, se, s, sw, w, nw, or center)

# num1 = tk.Label(janela, text= "Login:")
# num2 = tk.Label(janela, text= "Senha:")

# res1 = tk.Entry(janela)
# res2 = tk.Entry(janela)

# bt1 = tk.Button(janela, text = "Go")

# num1.pack(pady=3)
# res1.pack(pady=5)
# num2.pack(pady=5)
# res2.pack(pady=5)
# bt1.pack(pady=5)

# bt = tk.Button(janela, width =10, text = "Correto")
# bt["command"] = partial(click,bt)
# bt.place(x=205, y= 630)

# ed = tk.Entry(janela)
# ed.place(x=180,y=600)
# # {=======================Dimensão/fim=========================}
# #Largura x Altura + Margem Esq. + Topo
# janela.geometry("500x700")

# janela.mainloop() 


# # {=======================selecox chatgpt=========================}
# import tkinter as tk

# # Função chamada quando a seleção é alterada
# def selecionar_opcao(event):
#     print("Opção selecionada:", var_opcao.get())

# # Criar janela
# janela = tk.Tk()
# janela.title("Exemplo de Selectbox")

# # Lista de opções
# opcoes = ["Opção 1", "Opção 2", "Opção 3"]

# # Variável para armazenar a opção selecionada
# var_opcao = tk.StringVar(janela)
# var_opcao.set(opcoes[0])  # Definir o valor padrão

# # Criação do OptionMenu
# selectbox = tk.OptionMenu(janela, var_opcao, *opcoes, command=selecionar_opcao)
# selectbox.pack()

# # Exibindo a janela
# janela.mainloop()

# from tkinter import *
# from tkinter import ttk

# root = Tk()
# root.title("Paned Window")
# root.geometry("500x400")

# panel1 = PanedWindow(bd=4, relief='raised', bg= 'red')
# panel1.pack(fill=BOTH, expand=1)

# left_label = Label(panel1, text = 'Painel Esquerdo')
# panel1.add(left_label)

# panel2 = PanedWindow(panel1, orient=VERTICAL, bd=4, relief='raised', bg='red')
# panel1.add(panel2)

# top = Label(panel2, text= "Top")
# panel2.add(top)

# bottom = Label(panel2, text = 'Bottom')
# panel2.add(bottom)

# root.mainloop()

#============= hot bar de escolhas ==================
#melhorar aparência no trecho das proximas 10 linhas 
        # self.selecao_usuario_pg1 = tk.StringVar(self.frame_1)
        # self.clientes_pg1= ttk.Combobox(self.frame_1,
        #                                 # textvariable='',
        #                                 justify ='left',
        #                                 textvariable = self.selecao_usuario_pg1) 
  
        # self.clientes_pg1['values'] = ("Eduardo","MArcio","Juliana","Felipe","Chefão")
        # self.clientes_pg1.place(relx=0.02, rely=0.45, relwidth=0.88, relheight=0.4)
        # self.clientes_pg1.current()

# import tkinter as tk
# from PIL import Image, ImageTk

# # Função para criar um botão com imagem transparente
# def criar_botao_com_imagem_transparente(master, imagem_path, comando):
#     imagem = Image.open(imagem_path)
    
#     # Criar uma máscara de transparência
#     imagem_com_transparencia = Image.new("RGBA", imagem.size)
#     imagem_com_transparencia.paste(imagem, (0, 0), imagem)

#     # Converter imagem para o formato suportado pelo Tkinter
#     imagem_tk = ImageTk.PhotoImage(imagem_com_transparencia)

#     # Criar botão com imagem
#     botao = tk.Button(master, image=imagem_tk, command=comando, bd=0, highlightthickness=0)
#     botao.imagem_tk = imagem_tk  # Manter uma referência para evitar a coleta de lixo

#     return botao

# # Função de exemplo a ser chamada quando o botão é clicado
# def exemplo_comando():
#     print("Botão clicado")

# # Criar a janela
# janela = tk.Tk()
# # janela =janela.geometry("880x700")

# # Carregar imagem PNG com fundo transparente
# caminho_imagem = "fotoclick.png"

# # Criar botão com imagem transparente
# botao_transparente = criar_botao_com_imagem_transparente(janela, caminho_imagem, exemplo_comando)
# botao_transparente.pack()

# # Executar o loop da interface gráfica
# janela.mainloop()

# from tkinter import *
# class Fatias:
#         def __init__(self,raiz):
#                 self.canvas=Canvas(raiz, width=200, height=200)
#                 self.canvas.pack()
#                 self.frame=Frame(raiz)
#                 self.frame.pack()
#                 self.altura = 200 # Altura do canvas
#                 self.canvas.create_oval(25, self.altura-25,
#                 175, self.altura-175,
#                 fill='deepskyblue', outline='darkblue')
#                 fonte=('Comic Sans MS', '14', 'bold')
#                 Label(self.frame, text='Fatia: ',
#                 font=fonte, fg='blue').pack(side=LEFT)
#                 self.porcentagem=Entry(self.frame, fg='red',
#                 font=fonte, width=5)
#                 self.porcentagem.focus_force()
#                 self.porcentagem.pack(side=LEFT)
#                 Label(self.frame, text='%',
#                 font=fonte, fg='blue').pack(side=LEFT)
#                 self.botao=Button(self.frame, text='Desenhar',
#                 command=self.cortar, font=fonte,
#                 fg='darkblue', bg='deepskyblue')
#                 self.botao.pack(side=LEFT)
                
#         def cortar(self):
#                 arco=self.canvas.create_arc
#                 fatia=float(self.porcentagem.get())*359.9/100.
#                 arco(25, self.altura-25,
#                 175, self.altura-175,

#                 fill='yellow', outline='red',
#                 extent=fatia)
#                 self.porcentagem.focus_force()
# instancia=Tk()
# Fatias(instancia)
# instancia.mainloop()

# from tkinter import *
# import tkinter

# top = Tk()

# B1 = Button(top, text ="FLAT", relief=FLAT )
# B2 = Button(top, text ="RAISED", relief=RAISED )
# B3 = Button(top, text ="SUNKEN", relief=SUNKEN )
# B4 = Button(top, text ="GROOVE", relief=GROOVE )
# B5 = Button(top, text ="RIDGE", relief=RIDGE )

# B1.pack()
# B2.pack()
# B3.pack()
# B4.pack()
# B5.pack()
# top.mainloop()

from customtkinter import *
from PIL import Image


jnl = CTk()
jnl.geometry("600x600")

set_appearance_mode("dark")
img = Image.open("click.png")

bot = CTkButton(master=jnl, text ="Clica ae", corner_radius=30,fg_color='#EE9572',hover_color = '#FFA07A', border_color="#8B5742", border_width=3, image = CTkImage(dark_image =img))

bot.place(relx=0.5,rely=0.5,anchor="center")
jnl.mainloop()

