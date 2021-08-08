import streamlit as st
import pandas as pd
import Tesis1

def classify(num):
    if num == 0:
        return 'setosa'
    else:
        return 'virginica'

def main():
    st.title('Chatbot:')
    st.sidebar.header('Universidad Nacional de Loja')
    pregunta=""
    def parametros():
        pregunta=st.text_input('ingrese pregunta:')
        return pregunta
    p=parametros()

    if st.button('Aceptar'):
        traducido = Tesis1.traductor(pregunta)
        #query = Tesis1.spa(traducido)
        #articulos = Tesis1.vespa(query)
        #respuesta = Tesis1.respuesta(traducido, articulos)
        st.success(pregunta)
if __name__ == '__main__':
    main()
 
