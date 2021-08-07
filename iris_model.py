import streamlit as st
import pandas as pd


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
        pregunta=st.text_input('ingrese pregunta')
        return pregunta
    P = parametros()

    if st.button('Aceptar'):
        st.success(pregunta)
if __name__ == '__main__':
    main()
