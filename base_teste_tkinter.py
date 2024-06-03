
import webbrowser
import colorama as color
import sqlite3 as sql
import tkinter as tk, tkinter.messagebox, tkinter.ttk as ttk

from tkcalendar import Calendar, DateEntry
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from PIL import ImageTk , Image

aba = tk.Tk()

class Validadores:
    def validate_entry2(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:  # oops, couldn't convert to int

            return False
        return 0 <= value <= 100

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.input_nome.get()
        self.foneRel = self.input_fone.get()
        self.cidadeRel = self.input_cidade.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 630, 'Telefone: ')
        self.c.drawString(50, 600, 'Cidade: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.foneRel)
        self.c.drawString(150, 600, self.cidadeRel)

        self.c.rect(20, 720, 550, 200, fill= False, stroke=True) #Borda no "Ficha Técnica"(Aula 13, min 18:00)

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, tk.END)
        self.input_fone.delete(0, tk.END)
        self.input_nome.delete(0, tk.END)
        self.input_cidade.delete(0, tk.END)
    def conecta_bd(self):
        self.conn = sql.connect(r"C:\Users\labga\OneDrive\Documentos\IC_Julia\PROJETO_IC_IFES_BICO_DE_LANCA\GitHub_com_Waleska\JuWa_WRL\clientes.db")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando do banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40) );""")
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.input_nome.get()
        self.fone = self.input_fone.get()
        self.cidade = self.input_cidade.get()
    def OnDoubleClick(self, event):
        self.limpa_cliente()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(tk.END, col1)
            self.input_nome.insert(tk.END, col2)
            self.input_fone.insert(tk.END, col3)
            self.input_cidade.insert(tk.END, col4)

    def add_cliente(self):
        self.variaveis()
        if self.input_nome.get() == "":
            msg = "Para cadastrar um novo cliente é necessário \n"
            msg += "que seja digitado pelo menos um nome"
            tk.messagebox.showinfo("Cadastro de clientes - Aviso!!!", msg)
        else:
            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                VALUES (?, ?, ?)""", (self.nome, self.fone, self.cidade))
            self.conn.commit()

            self.desconecta_bd()
            self.select_lista()
            self.limpa_cliente()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ? """, (self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()

        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()

        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", tk.END, values=i)
        self.desconecta_bd()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.input_nome.insert(tk.END, '%')
        nome = self.input_nome.get()
        self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" %nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", tk.END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()
    
    def calendario(self):
        self.calendario1 = Calendar(self.frame_1, fg='gray75', bg="blue",
            font=('Times', '9', 'bold'), locale='pt_br')
        self.calendario1.place(relx=0.5, rely=0.1)

        self.calDataInicio = tk.Button(self.frame_1, text='Inserir data inicial',
            fg='gray35', font=('Times', '10', 'bold'),command=self.print_calInicio)
        self.calDataInicio.place(relx=0.55, rely=0.85, height=25, width=150)
    
    def print_calInicio(self):
        dataInicio = self.calendario1.get_date()
        self.calendario1.destroy()
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(tk.END, dataInicio)
        self.calDataInicio.destroy()

class Application(Funcs, Relatorios,Validadores):
    def __init__(self):
        self.aba = aba
        self.validaEntradas()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.deleta_cliente()
        self.altera_cliente()
        self.Menus()
        # criando o Loop
        aba.mainloop()
    def tela(self):
        self.aba.title("Cadastro de Clientes")
        self.aba.configure(background= '#1e3743')
        self.aba.geometry("700x600")
        self.aba.resizable(True, True) #se quiser impidir que amplie ou diminua a tela, altere para False
        self.aba.maxsize(width=800, height=700)
        self.aba.minsize(width=500, height=300)
    
    def frames_da_tela(self):
        self.frame_1 = tk.Frame(self.aba, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        #place(posição especifica ), pack(mais simples), grid(planilha)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46) #rel é como porcentagem , que varia de 0 até 1 

        self.frame_2 = tk.Frame(self.aba, bd=4, bg='#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    
    def widgets_frame1(self):
        # self.canvas_bt = tk.Canvas(self.frame_1, bd=0, bg='#1e3743', highlightbackground = 'gray',
        #     highlightthickness=5)
        # self.canvas_bt.place(relx= 0.19, rely= 0.08, relwidth= 0.22, relheight=0.19)

        ### Criação do botão limpar
        self.bt_limpar = tk.Button(self.frame_1, text= 'Limpar', bd=4,
                                bg = '#107db2', fg = 'white',
                                activebackground='#108ecb', activeforeground="white"
                                , font= ("verdana", 10), command=self.limpa_cliente)
        self.bt_limpar.place(relx=0.14, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botao buscar
        self.bt_buscar = tk.Button(self.frame_1, text='Buscar' , bg = '#107db2', fg = 'white', command = self.janela2)
        self.bt_buscar.place(relx=0.26, rely=0.08, relwidth=0.1, relheight=0.14)

        # self.balao_buscar = tix.Balloon(self.frame_1) #não funciona
        # self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg = "Digite no campo Nome o cliente que deseja pesquisar")

        ### Criação do botao novo
        # self.btnovo = tk.PhotoImage(file = r"C:\Users\20211MPECA0020\Documents\Projeto\Aplicativo\botaonovo.gif")
        # self.btnovo = self.btnovo.subsample(2, 2)

        # self.bt_novo = tk.Button(self.frame_1, bd =0, image = self.btnovo, command= self.add_cliente)
        # self.bt_novo.place(relx=0.5, rely=0.08, width=60, height=40)

        ### Criação do botao alterar
        self.bt_alterar = tk.Button(self.frame_1, text='Alterar' , bg = '#107db2', fg = 'white', command=self.altera_cliente)
        self.bt_alterar.place(relx=0.62, rely=0.08, relwidth=0.1, relheight=0.14)

        ### Criação do botao apagar
        self.bt_apagar = tk.Button(self.frame_1, text='Apagar' , bg = '#107db2', fg = 'white',command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.74, rely=0.08, relwidth=0.1, relheight=0.14)

        ## Criação da label e entrada do codigo
        self.codigo = tk.Label(self.frame_1,text="Código", font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        # self.codigo.configure(text="Código", font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.codigo.place(relx=0.01, rely=0.02, relwidth=0.1, relheight=0.1)

        self.codigo_entry = tk.Entry(self.frame_1, validate="key",validatecommand=self.vcmd2)
        self.codigo_entry.place(relx=0.02, rely=0.12, relwidth=0.1, relheight=0.1)
        
        ### Criação da label e entry nome
        self.lb_nome = tk.Label(self.frame_1, text='Nome', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_nome.place(relx=0.01, rely=0.32, relwidth=0.1, relheight=0.14)

        self.input_nome = tk.Entry(self.frame_1)
        self.input_nome.place(relx=0.02, rely=0.44, relwidth=0.8, relheight=0.14)

        ### Criação da label e entry telefone
        self.lb_fone = tk.Label(self.frame_1, text='Telefone', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_fone.place(relx=0.02, rely=0.6, relwidth=0.1, relheight=0.14)

        self.input_fone = tk.Entry(self.frame_1)
        self.input_fone.place(relx=0.02, rely=0.72, relwidth=0.2, relheight=0.14)

        ### Criação da label e entry cidade
        self.lb_cidade = tk.Label(self.frame_1, text='Cidade', font=('Verdana', '8', 'bold'), bg='#dfe3ee', fg='#3b5998')
        self.lb_cidade.place(relx=0.31, rely=0.6, relwidth=0.1, relheight=0.14)

        self.input_cidade = tk.Entry(self.frame_1)
        self.input_cidade.place(relx=0.32, rely=0.72, relwidth=0.5, relheight=0.14)
        ### drop down button
        self.Tipvar = tk.StringVar(self.aba)
        self.TipV = ("Solteiro(a)", "Casado(a)", "Viuvo(a)")
        self.Tipvar.set("Solteiro(a)")
        self.popupMenu = tk.OptionMenu(self.aba, self.Tipvar,*self.TipV)
        self.popupMenu.place(relx=0.1, rely=0.1, relwidth=0.4, relheight=0.3)
        self.estado_civil = self.Tipvar.get

        self.bt_calendario = tk.Button(self.frame_1, text= "Data", command= self.calendario)
        self.bt_calendario.place(relx=0.5 ,rely=0.02)
        self.entry_data = tk.Entry(self.frame_1, width= 10)
        self.entry_data.place(relx=0.5 ,rely=0.2)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")
        
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)
        
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = tk.Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    
    def validaEntradas(self):
        ### Naming input validators
        # self.vcmd8 = (self.aba.register(self.validate_entry8), "%P")
        # self.vcmd6 = (self.aba.register(self.validate_entry6), "%P")
        # self.vcmd4 = (self.aba.register(self.validate_entry4), "%P")
        self.vcmd2 = (self.aba.register(self.validate_entry2), "%P")
        # self.vcmd8float = (self.aba.register(self.validate_entry8float), "%P")
        # self.vcmd9float = (self.aba.register(self.validate_entry9float), "%P")
        # self.vcmd4float = (self.aba.register(self.validate_entry4float), "%P")


    def Menus(self):
        menubar = tk.Menu(self.aba)
        self.aba.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        filemenu2 = tk.Menu(menubar)

        def Quit(): self.aba.destroy()

        menubar.add_cascade(label= "Opções", menu=filemenu)
        menubar.add_cascade(label= "Relatorios", menu=filemenu2)

        filemenu.add_command(label= "Sair", command=Quit)
        filemenu.add_command(label= "Limpa cliente", command= self.limpa_cliente)

        filemenu2.add_command(label= "Ficha do cliente", command=self.geraRelatCliente)
    def janela2(self):
        self.aba2 = tk.Toplevel()
        self.aba2.title(" Janela 2  ")
        self.aba2.configure(background='gray75')
        self.aba2.geometry("360x160")
        self.aba2.resizable(True, True)
        self.aba2.transient(self.aba)
        self.aba2.focus_force() #não consegue digitar na aba anterior
        self.aba2.grab_set() #mantem na frente da aba anterior

print("\n\n", color.Fore.GREEN + "Iniciando o código" + color.Style.RESET_ALL)
Application() 
print(color.Fore.RED + "Finalizando o código" + color.Style.RESET_ALL, "\n")