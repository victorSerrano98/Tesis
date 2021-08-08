import streamlit as st
import pandas as pd
import Tesis1


def main():
    st.title('Chatbot:')
    st.sidebar.header('Universidad Nacional de Loja')
    pregunta=st.text_input('ingrese pregunta:')

    if st.button('Aceptar'):
        traducido = Tesis1.traductor(pregunta)
        query = Tesis1.spa(traducido)
        #articulos = Tesis1.vespa(query)
        #respuesta = Tesis1.respuesta(traducido, articulos)
        st.success(traducido+ "   :   " query)
if __name__ == '__main__':
    main()
 
