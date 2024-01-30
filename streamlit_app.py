import streamlit as st
import streamlit_authenticator as stauth

from dependencies import is_admin, is_staff, is_user

import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def reset_password_form():
    """
    Reset password form
    """
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"],location='sidebar'):
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)


authenticator.login()


if st.session_state["authentication_status"]:
    st.title('Home Page')
    with st.sidebar:
        st.subheader(f' Hi! {st.session_state["name"]}')
        with st.expander("Register new user", expanded=False):
            username = st.session_state["username"]
            if is_admin(config, username) or is_staff(config, username):
                try:
                    st.subheader('Register User')
                    role = st.selectbox(f'Select the type of user to register', ['admin', 'staff', 'user'], index=2)
                    email, username, name = authenticator.register_user(fields={"Form name":''}, preauthorization=False)
                    if username:
                        if role == 'admin':
                            config['roles']['admin'].append(username)
                        if role == 'staff':
                            config['roles']['staff'].append(username)
                        if role == 'user':
                            config['roles']['user'].append(username)
                        with open('config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        st.success(f'User {name} registered as {role}')
                except Exception as e:
                    st.error(e)
        reset_password = st.button('Reset Password',on_click=reset_password_form)
        authenticator.logout()


    tab1, tab2 = st.tabs(["Orders", "Sales"])

    with tab1:
        st.subheader('Orders Analytics')
        st.write('This is the orders page')            
    



elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


