import streamlit as st
from time import sleep
from crud import read_usuarios


def login():
    with st.container(border= True):
        st.markdown('Bem-vindo a tela de login')
        usuarios = read_usuarios()
        users = {usuario.nm_usuario: usuario for usuario in usuarios}
        nome_usuario = st.selectbox(
            'Selecione o usuário',
            list(users.keys())
        )
        senha = st.text_input('Digite sua senha', type = 'password')

        if st.button('Login'):
            usuario = users[nome_usuario]
            if usuario.verifica_password(senha):
                st.success('Login efetuado com sucesso!')
                st.session_state['usuario'] = usuario
                st.session_state['logado'] = True
                sleep(1)
                st.rerun()
            else:
                st.error('Senha incorreta!')


def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not st.session_state['logado']:
        login()

    else:
        st.markdown('Bem-Vindo ao WebbApp')



if __name__ == '__main__':
    main()