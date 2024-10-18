import streamlit as st
import sqlite3
import pandas as pd
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import csv
import streamlit.components.v1 as components


#BACKLOG

# definir praias para cada estação
# inserir informação sobre a praia
#- contador de visita
#https://stackoverflow.com/questions/77377439/how-to-change-font-size-in-streamlit
#from geopy.geocoders import Nominatim
#import  geopy
#icones streamlit https://www.webfx.com/tools/emoji-cheat-sheet/
#https://geopy.readthedocs.io/en/stable/
#https://folium.streamlit.app/ exemplos usando folium
#https://python-graph-gallery.com/312-add-markers-on-folium-map/
#**** folium está utilizando a versão v4 do font awesome: https://fontawesome.com/v4/icons/


st.set_page_config(
    page_title="Praiômetro - Descubra o paraíso em todas as estações!",
    page_icon="🏖",
    layout = "wide",                                 #wide , centered
    initial_sidebar_state ="expanded" ,             #expanded, auto,  collapsed
    menu_items=None
)

database = "./data/praiometro.db"
csv_visitors = "./data/visitors.csv"

st.sidebar.markdown("""<head></head>""",unsafe_allow_html=True,)

st.title('Descubra o paraíso em todas as estações com o Praiômetro!')
st.subheader('Planeje suas férias perfeitas, escolhendo as melhores praias para cada mês.')
st.subheader('Encontre as praias ideais para sua viagem, escolhendo o mês perfeito para garantir férias ensolaradas, com pouca chuva e temperaturas agradáveis.')
st.subheader('Afinal, viajar é uma experiência única e merece ser vivida sob o sol radiante.*')


# Função para renderizar o código de rastreamento
def render_analytics():
    st.markdown(
        '''
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-YVNH934KXN"></script>
        <script>
           window.dataLayer = window.dataLayer || [];
           function gtag(){{dataLayer.push(arguments);}}
           gtag('js', new Date());
           gtag('config', 'G-YVNH934KXN');
        </script>
        ''', unsafe_allow_html=True
    )

def change_label_style(label, font_size='12px', font_color='black', font_family='sans-serif'):
    html = f"""<script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
    </script>
    """
    st.components.v1.html(html)

def load_data(selected_date,praia):
    conn = sqlite3.connect(database)
    if praia == 'Não':
        query = f"select * from estacao_view where mes_medicao = '{selected_date}'"
    else:
        query = f"select  codigo,  ev.nome as nome ,  latitude, longitude, mes_medicao, media_dias_chuva, media_temperatura_media, media_precipitacao_total from estacao_view  as ev inner join praia_view as pv where mes_medicao = '{selected_date}'  and ev.nome = pv.nome GROUP BY ev.nome"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def cidades_selecionadas(data,chuva,temperatura,precipitacao,praia):
    conn = sqlite3.connect(database)
    if praia == 'Não':
        query = f"select * from estacao_view where mes_medicao = '{data}' and media_dias_chuva  < {chuva} and media_temperatura_media > {temperatura} and media_precipitacao_total < {precipitacao}"
    else: 
        query = f"select  codigo,  ev.nome as nome ,  latitude, longitude, mes_medicao, media_dias_chuva, media_temperatura_media, media_precipitacao_total from estacao_view  as ev inner join praia_view as pv where mes_medicao = '{data}' and media_dias_chuva < {chuva} and media_temperatura_media > {temperatura} and media_precipitacao_total < {precipitacao} and ev.nome = pv.nome GROUP BY ev.nome"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def new_map_chuva(df,max_chuva):
    m = folium.Map(location=[-15, -55], zoom_start=4)
    for index, row in df.iterrows(): 
        if float(row['media_dias_chuva']) <= float(max_chuva):
            color = 'yellow'
        else:
            color = 'red'     
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,  # Tamanho constante da bola
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['nome']}. Dias de Chuva: {row['media_dias_chuva']}."
        ).add_to(m)

    st_data = st_folium(m,width=500,height=500)

def new_map_temperatura(df,min_temp):
    m = folium.Map(location=[-15, -55], zoom_start=4)
    for index, row in df.iterrows(): 
        if row['media_temperatura_media'] >= int(min_temp):
            color = 'yellow' 
        else:
            color = 'red'     
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,  # Tamanho constante da bola
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['nome']}. Temperatura: {row['media_temperatura_media']}."
        ).add_to(m)

    st_data = st_folium(m,width=500,height=500)


def new_map_precipitacao(df,max_precipitacao):
    m = folium.Map(location=[-15, -55], zoom_start=4)
    for index, row in df.iterrows(): 
        if int(row['media_precipitacao_total']) >= int(max_precipitacao):
            color = 'red' 
        else:
            color = 'yellow'
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,  # Tamanho constante da bola
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['nome']}. Precipitação: {row['media_precipitacao_total']}."
        ).add_to(m)

    st_data = st_folium(m,width=500,height=500)

def new_map(df):
    m = folium.Map(location=[ -12,  -38.5124], zoom_start=4)

    for index, row in df.iterrows(): 
        temperatura = str(float("{:.1f}".format(row['media_temperatura_media']))) + " °C"
        chuvas = str(abs(float("{:.1f}".format(row['media_dias_chuva']))))
        precipitacao = str(float("{:.1f}".format(row['media_precipitacao_total']))) + " mm"
        html = """
            <b><h2>%s</h2></b>
            Temperatura: %s <br>
            Dias de chuva: %s <br>
            Precipitação: %s <br>
            """  % (row['nome'], temperatura, chuvas, precipitacao)            
        
        icone1 = folium.Icon(icon="sun-o", icon_color="yellow", color="cadetblue", prefix="fa")
        folium.Marker(
            [row['latitude'], row['longitude']],
            #popup=f"{row['nome']}. Dias de Chuva: {row['media_dias_chuva']}.   Temperatura média: {row['media_temperatura_media']}. Precipitação: {row['media_precipitacao_total']}",
            popup=html,
            icon=icone1
        ).add_to(m)

    st_data = st_folium(m, width="30%")


# Função para verificar se o cookie de visita já existe
def is_visited():
    return "visited" in st.session_state

# Função para obter o IP do visitante
def get_visitor_ip():
    request = Request("https://api64.ipify.org?format=json")
    response = urlopen(request)
    data = response.read()
    ip = data.decode("utf-8").split('"')[3]
    return ip

def atualiza_contador_visitas():
    if not is_visited():
        # Atualiza o cookie de visita
        st.session_state.visited = True

        st.session_state.visit_count = st.session_state.get("visit_count", 0) + 1

        visitor_ip = get_visitor_ip()

        with open(csv_visitors, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([visitor_ip, datetime.now()])
 

# Função principal do Streamlit
def main():

    st.sidebar.markdown(
    """ <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: black;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
     
    max_chuva = 12
    min_temp  = 23
    max_precipitacao = 120
    
    
    # Carrega as datas únicas disponíveis na base de dados
    conn = sqlite3.connect(database)
    unique_months = pd.read_sql_query("select DISTINCT mes_medicao from estacao_view", conn)['mes_medicao'].tolist()

    data_maxmin     = pd.read_sql_query("select min(media_dias_chuva) as min_chuva, max(media_dias_chuva) as max_chuva, min(media_temperatura_media) as min_temp, max(media_temperatura_media) as max_temp ,min(media_precipitacao_total) as min_precip, max(media_precipitacao_total) as max_precip  from estacao_view",conn)
    max_bd_chuva    = int(data_maxmin.max_chuva.values[0])
    min_bd_chuva    = int(data_maxmin.min_chuva.values[0])+1
    max_bd_temp     = int(data_maxmin.max_temp.values[0])-1
    min_bd_temp     = int(data_maxmin.min_temp.values[0])
    max_bd_precip   = int(data_maxmin.max_precip.values[0])
    min_bd_precip   = int(data_maxmin.min_precip.values[0])

    conn.close()

    # FORM SIDEBAR 
    with st.sidebar:

        logo_url = "./assets/logo_praiometro_transparente.png"
        st.image(logo_url)
        dfmeses = ['Janeiro','Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho' , 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
   
        label = "Selecione o mês da viagem:"
        mes_texto  = st.selectbox(label, dfmeses)
        #change_label_style(label, '20px')

        indexmeses = dfmeses.index(mes_texto) + 1
        if indexmeses < 10:
            selected_date_mensal = "0"+str(indexmeses)
        else:
            selected_date_mensal = str(indexmeses)
        
        st.sidebar.divider()  
        
        selected_melhores_destinos = st.radio(
            "Tipos de destinos:",
            key="destinos",
            options=["Melhores praias", "Melhores praias + com pouco de chuva"]
        )

        st.sidebar.divider()

        if selected_melhores_destinos == "Melhores praias":
            max_chuva = 12
            min_temp = 23
            max_precipitacao = 75
        else:
            max_chuva = 16
            min_temp = 23
            max_precipitacao = 150           

        st.write ("Você pode fazer suas escolhas diretamente:")
        max_chuva = st.slider('Dias de chuva menor que:', min_bd_chuva, max_bd_chuva, max_chuva)
        min_temp = st.slider('Temperatura acima de:', min_bd_temp, max_bd_temp, min_temp)
        max_precipitacao = st.slider('Preciciptação menor que:', min_bd_precip, max_bd_precip, max_precipitacao)
        
        st.sidebar.divider()
        
        label = "Exibe somente praias ?"
        selected_praia = st.radio(
            label,
            key="praia",
            options=["Sim", "Não"],
        )
        #change_label_style(label, '20px')

        #https://docs.google.com/forms/d/e/1FAIpQLSd9jrJjYufC7uD3vgXWcHnk7Ej4YnYnKKxXGt-wdU-vqa6C6A/viewform?usp=sf_link
        

        st.write ("Versão Beta")
        st.write("""<div style="width:100%;text-align:center;"><a href='https://docs.google.com/forms/d/e/1FAIpQLSd9jrJjYufC7uD3vgXWcHnk7Ej4YnYnKKxXGt-wdU-vqa6C6A/viewform?usp=sf_link' style="float:center">Versão Beta. <br>Ajude a melhorar!</a></div>""", unsafe_allow_html=True)


    data_mensal = load_data(selected_date_mensal,selected_praia)
    data_cidades_selecionadas = cidades_selecionadas(selected_date_mensal,max_chuva, min_temp,max_precipitacao,selected_praia)


   # TELA PRINCIPAL 
    
    st.header(f"**{mes_texto.upper()}** - MELHORES PRAIAS")

    cola, colb = st.columns(2)
    
    #cola.header(f'Viage para essas cidades no mês {mes_texto}:')
    #colb.header('Clique na cidade:')

    with cola:
        if data_cidades_selecionadas.empty:
            colb.write('Nenhuma cidade encontrada com todos os parâmetros selecionados.')
        new_map(data_cidades_selecionadas)

    with colb:
        df = data_cidades_selecionadas

        for index, row in df.iterrows(): 
            
            with st.expander(row['nome']):
                st.subheader(row['nome'])
                temperatura = str(float("{:.1f}".format(row['media_temperatura_media'])))
                chuvas = str(abs(float("{:.1f}".format(row['media_dias_chuva']))))
                precipitacao = str(float("{:.1f}".format(row['media_precipitacao_total'])))
                colb1,colb2,colb3 = st.columns(3)
                colb1.metric("Temperatura", temperatura + " °C")
                colb2.metric("Chuva",chuvas + " dias")
                colb3.metric("Precipitação", precipitacao + "mm")
       
    col1, col2, col3= st.columns(3) 

    with col1:
        st.header(f"**DIAS DE CHUVA** 🌦")
        new_map_chuva(data_mensal,max_chuva)
        st.write (f"Amarelo se chover menos de {max_chuva} dias.")

    with col2:
        st.header(f"**TEMPERATURA** 🌡")
        new_map_temperatura(data_mensal,min_temp)
        st.write(f"Amarelo se temperatura maior que {min_temp} graus.")

    with col3:
        st.header(f"**PRECIPITAÇÃO** 🌧")
        new_map_precipitacao(data_mensal,max_precipitacao)
        st.write(f"Amarelo se precipita maior que {max_precipitacao} mm .")
      
    # Verifica se o usuário já visitou a página
    
    atualiza_contador_visitas()
    st.session_state.cookie_expires_at = datetime.now() + timedelta(days=1)


    st.write("*Nossos dados são atualizados das estações metereológicas do [INMET](https://portal.inmet.gov.br/) para transformar suas viagens em experiências inesquecíveis. Não fazemos previsões metereológicas, calculamos uma média dos anos passados recentes. Bem como ocorre nas previsões de tempo, não há garantias de 100% de que se repetirá no futuro. As cidades listadas são das estações metereológica, verifique se é perto do seu destino no mapa. As principais cidades de férias estão disponíveis como Fortaleza, Natal, Recife, João Pessoa, Aracaju, Salvador, Maceió, Rio de Janeiro, São Paulo, Florianópolis e outras.")
    render_analytics()

if __name__ == "__main__":
    main()
