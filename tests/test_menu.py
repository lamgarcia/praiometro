import streamlit as st
from streamlit import session_state

def test_sliders(mocker):
    # Mock the Streamlit sliders
    mocker.patch('streamlit.slider', side_effect=lambda label, min_val, max_val, value: value)

    # Defina os valores de teste
    min_bd_chuva = 0
    max_bd_chuva = 100
    max_chuva = 50
    
    min_bd_temp = -10
    max_bd_temp = 40
    min_temp = 20

    min_bd_precip = 0
    max_bd_precip = 200
    max_precipitacao = 100

    # Execute o código que contém os sliders
    st.write("Você pode fazer suas escolhas diretamente:")
    max_chuva = st.slider('Dias de chuva menor que:', min_bd_chuva, max_bd_chuva, max_chuva)
    min_temp = st.slider('Temperatura acima de:', min_bd_temp, max_bd_temp, min_temp)
    max_precipitacao = st.slider('Preciciptação menor que:', min_bd_precip, max_bd_precip, max_precipitacao)

    # Teste se os valores retornados pelos sliders são os esperados
    assert max_chuva == 50
    assert min_temp == 20
    assert max_precipitacao == 100