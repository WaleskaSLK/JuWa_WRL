import streamlit as st
import pandas as pd
import BD

from PIL import Image

# @st.cache_data #ele auxilia no site ao carregar os dados mais de uma vez, deixando-o mais rapido
# def DADOS():
#     dados = pd.read_csv('resultados.csv')
#     return dados

# Organizador da página
left_co, cent_co,last_co = st.columns(3)
col1, col2, col3 = st.columns([4, 4, 4])
col_1,col_2 = st.columns([5,10])
    
# Gerador de imagem
image_4F = Image.open(r'C:\Users\20211MPECA0020\Documents\Projeto\Site\4Furos.jpeg')
image_5F = Image.open(r'C:\Users\20211MPECA0020\Documents\Projeto\Site\5Furos.jpeg')
image_6F = Image.open(r'C:\Users\20211MPECA0020\Documents\Projeto\Site\6Furos.jpeg')
imagem_IFES = Image.open(r'C:\Users\20211MPECA0020\Documents\Projeto\Site\ifes.png')
imagem_LUMAR = Image.open(r'C:\Users\20211MPECA0020\Documents\Projeto\Site\LUMAR2.png')


#""" Formato para o SIDEBAR"""
 # radio, selectbox, multiselect ,slider, text_input, number_input, date_input


with st.container():
    st.sidebar.title('Seja bem-vindo')
    st.sidebar.text('Este é um prototipo para o projeto original')
    st.sidebar.caption('Waleska Sulke')
    op = st.sidebar.selectbox('# Selecione uma das opções',('Portal principal','Teste','Dados Semanais','Dados Mensais','Ajuda'))
    
    st.sidebar.image(imagem_IFES, width=200)
    st.sidebar.image(imagem_LUMAR, width=200) 

    if op == 'Portal principal':
        st.title(':green[Registro das medições de Desgaste dos Furos]')
        st.header('Os moldes das lanças possuem este formato Circular, onde cada diâmetro sofre variações conforme o seu uso. ')
        st.text('A Indústria dispõe de alguns moldes, e a seguir está o registro fotográfico de cada um deles')
        
        with col1:
            st.image(image_4F, caption='Lança de Quatro Furos')
        with col2:
            st.image(image_5F, caption='Lança de Cinco Furos')
        with col3:
            st.image(image_6F, caption='Lança de Seis Furos')

    if op == 'Teste':
        
        st.title(':red[Estes são os diâmetros registrados ao longo de um mês:]')
        st.write(BD.tudo())

        dt = pd.DataFrame({'datas':BD.valor_datas(),'Furo 1':BD.dia_1(),'Furo 2':BD.dia_2(),'Furo 3':BD.dia_3(),'Furo 4':BD.dia_4()})
        st.line_chart(dt,x='datas')
        
        col=st.multiselect('selecione',BD.tudo().columns)
        if col:
            st.line_chart(BD.tudo()[col])
       
    if op == 'Dados Semanais':
        st.header(':rainbow[Dados já registrados]:clipboard:') #é importante por um titulo intuitivo para os futuros leitores
        

        # dados1 = pd.read_csv('plan1.csv')
        # st.write(dados1.head())
        # dados1 = dados1.iloc[:,1:]

        # if st.button('Exibir gráfico 1'):
        #     st.line_chart(dados1)
        

    if op == 'Dados Mensais':
        st.markdown("<h1 style='text-align: center; color: blue;'>Tabela dos Furos</h1>", unsafe_allow_html=True)
        opcao = st.multiselect('Escolha:',('1° Diâmetro', '2° Diâmetro' , '3° Diâmetro' , '4° Diâmetro' , '5° Diâmetro' , '6° Diâmetro' , 'Todos'))
        # dados1 = pd.read_csv('plan1.csv')
        # st.write(dados1.head())

        if '1° Diâmetro' in opcao:
            st.write('Todavia não há tabela do primeiro diâmetro')

    if op == 'Ajuda':
        if st.checkbox('Está cansado?'):
            st.write('Toma um café')
        



# with st.chat_message("ai"):
#     st.write("Hello 👋")

