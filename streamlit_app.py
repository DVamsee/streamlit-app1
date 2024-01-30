import streamlit as st
import streamlit_authenticator as stauth

from dependencies import is_admin, is_staff, is_user
import os

import yaml
from yaml.loader import SafeLoader
import pandas as pd 
import numpy as np

st.set_page_config(layout="wide")

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
        df = pd.read_csv('data/list_of_orders.csv')
        # st.dataframe(df.head(10))
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('State wise orders')
            st.line_chart(df.groupby('State').count()['Order ID'])
            with st.expander("view source table", expanded=False):
                st.dataframe(df.groupby('State').count()['Order ID'], use_container_width=True)

        with col2:
            st.subheader('City wise orders')
            st.line_chart(df.groupby('City').count()['Order ID'])
            with st.expander("view source table", expanded=False):
                st.dataframe(df.groupby('City').count()['Order ID'], use_container_width=True)
        

        order_df = pd.read_csv('data/order_details.csv')
        # st.dataframe(order_df.head(10))
        with col1:
            st.subheader('Most profit by order category')
            st.bar_chart(order_df.groupby('Category').sum()['Profit'])
            with st.expander("view source table", expanded=False):
                st.dataframe(order_df.groupby('Category').sum()['Profit'], use_container_width=True)

        with col2:
            st.subheader('Most profit by order sub-category')
            st.bar_chart(order_df.groupby('Sub-Category').sum()['Profit'])
            with st.expander("view source table", expanded=False):
                st.dataframe(order_df.groupby('Sub-Category').sum()['Profit'], use_container_width=True)








elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


