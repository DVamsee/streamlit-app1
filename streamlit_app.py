import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

import streamlit as st
import streamlit_authenticator as stauth
import numpy as np
import pandas as pd
import os
from streamlit_folium import st_folium
import folium


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

st.title('Home Page')


authenticator.login()


if st.session_state["authentication_status"]:
    with st.sidebar:
        username = st.session_state["username"]
        if is_admin(config, username) or is_staff(config, username):
            with st.expander('Register new User'):
                try:
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
        
    tab1, tab2 = st.tabs(["Maps", "Uber"])

    with tab1:
        # map representation
        map_data = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon']
        )
        st.map(map_data)

    # with tab2:
        # DATE_COLUMN = 'date/time'
        # DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
        #         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
        
        # def load_data(nrows):
        #     data = pd.read_csv(DATA_URL, nrows=nrows)
        #     lowercase = lambda x: str(x).lower()
        #     data.rename(lowercase, axis='columns', inplace=True)
        #     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        #     return data


        # data = load_data(10000)

        # if st.checkbox('Show raw data'):
        #     st.subheader('Raw data')
        #     st.write(data)

        # st.subheader('Number of pickups by hour')
        # hist_values = np.histogram(
        #     data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
        # st.bar_chart(hist_values)

        # """
        # ## Map of all pickups
        # """
        # hour_to_filter = st.slider('hour', 0, 23, 17) # min: 0h, max: 23h, default: 17h
        # filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
        # st.subheader(f'Map of all pickups at {hour_to_filter}:00')
        # st.map(filtered_data)

            


elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


