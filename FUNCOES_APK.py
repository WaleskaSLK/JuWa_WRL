import tkinter as tk
import sqlite3 as sql
import colorama as color
from tkinter import ttk
from customtkinter import *
from PIL import Image, ImageTk

def CONECTA_BD(inp_caminho):
    conn = sql.connect(inp_caminho)
    cursor = conn.cursor(); print("Conectando ao banco de dados")
    return conn, cursor
    
def DESCONECTA_BD(conn):
    conn.close(); print("Desconectando do banco de dados")

def CRIAR_FRAME(inp_frame, inp_bg, inp_light = NONE):
    frame = tk.Frame(inp_frame,
                    bg= inp_bg,
                    highlightbackground= inp_light)
    return frame

def CRIAR_BOTAO(inp_frame, inp_texto, inp_bg, inp_fg, inp_borda = NONE,inp_tamanho= NONE, inp_style = NONE, inp_cursor = NONE, inp_comando = NONE):
    """Retorna um botão seguindo o parametros comentados"""
    botao = tk.Button(  inp_frame, # frame
                        text = inp_texto, # texto
                        bg = inp_bg, # background
                        fg = inp_fg, # 
                        bd = inp_borda, #borda do botão
                        font= ("arial", inp_tamanho ,inp_style), #fonte, tamanho, style
                        cursor = inp_cursor, # estilo do cursor
                        command = inp_comando) # comando
    return botao
    
def CRIAR_LABEL(inp_frame, inp_texto, inp_bg, inp_fg, inp_fonte = NONE, inp_tam_fonte = NONE, inp_style = NONE):
    label = tk.Label(inp_frame, # frame
                    text = inp_texto, # texto
                    bg = inp_bg, # background
                    fg = inp_fg, # cor da letra
                    font = (inp_fonte, inp_tam_fonte, inp_style))#fonte, tamanho, style
    return label