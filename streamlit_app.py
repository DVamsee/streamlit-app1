# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

import streamlit as st
import streamlit_authenticator as stauth

from dependencies import is_admin, is_staff, is_user

import yaml
from yaml.loader import SafeLoader

with open('src/streamlit-app1/config.yaml') as file:
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
    with st.sidebar:
        reset_password = st.button('Reset Password',on_click=reset_password_form)
        authenticator.logout()
    
    st.title('Home Page')
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
            


elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


