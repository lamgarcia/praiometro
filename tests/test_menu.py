import pytest
import streamlit as st
from streamlit.testing import TestSessionState

@pytest.fixture
def setup_session_state():
    session_state = TestSessionState()
    return session_state

def test_sidebar_options(setup_session_state):
    # Mock Streamlit sidebar elements
    logo_url = "./assets/logo_praiometro_transparente.png"
    st.image(logo_url)
    
    # Mock the selectbox for months
    dfmeses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    setup_session_state["mes_texto"] = "Janeiro"
    
    label = "Selecione o mês da viagem:"
    mes_texto = st.selectbox(label, dfmeses, index=dfmeses.index(setup_session_state["mes_texto"]))
    
    indexmeses = dfmeses.index(mes_texto) + 1
    if indexmeses < 10:
        selected_date_mensal = "0" + str(indexmeses)
    else:
        selected_date_mensal = str(indexmeses)
    
    # Check if selected month is processed correctly
    assert selected_date_mensal == "01"
    
    # Mock the radio button for destination type
    setup_session_state["selected_melhores_destinos"] = "Melhores praias"
    selected_melhores_destinos = st.radio(
        "Tipos de destinos:",
        key="destinos",
        options=["Melhores praias", "Melhores praias + com pouco de chuva"],
        index=["Melhores praias", "Melhores praias + com pouco de chuva"].index(setup_session_state["selected_melhores_destinos"])
    )
    
    if selected_melhores_destinos == "Melhores praias":
        max_chuva = 12
        min_temp = 23
        max_precipitacao = 75
    else:
        max_chuva = 16
        min_temp = 23
        max_precipitacao = 150
    
    assert max_chuva == 12
    assert min_temp == 23
    assert max_precipitacao == 75

    # Mock the sliders
    min_bd_chuva, max_bd_chuva = 0, 30
    min_bd_temp, max_bd_temp = 15, 35
    min_bd_precip, max_bd_precip = 50, 200

    max_chuva = st.slider('Dias de chuva menor que:', min_bd_chuva, max_bd_chuva, max_chuva)
    min_temp = st.slider('Temperatura acima de:', min_bd_temp, max_bd_temp, min_temp)
    max_precipitacao = st.slider('Preciciptação menor que:', min_bd_precip, max_bd_precip, max_precipitacao)
    
    assert max_chuva == 12
    assert min_temp == 23
    assert max_precipitacao == 75

    # Mock the last radio button for "Exibe somente praias?"
    setup_session_state["selected_praia"] = "Sim"
    label = "Exibe somente praias ?"
    selected_praia = st.radio(
        label,
        key="praia",
        options=["Sim", "Não"],
        index=["Sim", "Não"].index(setup_session_state["selected_praia"])
    )
    
    assert selected_praia == "Sim"
