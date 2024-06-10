import streamlit as st
import utils.authentication as auth_functions

st.set_page_config(
    page_title='EuroBox24: Home Page',
    page_icon=':house:',
    layout="wide"
)


st.title('Welcome to the EuroBox24 game')

st.subheader('Use the panel on the left to navigate between pages')

if 'user_info' not in st.session_state:

    login, signup, forgot_password = st.tabs(['Log in', 'Sign up', 'Forgot password'])

    login_form = login.form(key='login-form', clear_on_submit=False)
    login_email = login_form.text_input(label='Email')
    login_password = login_form.text_input(label='Password', type='password')
    # login_notification = login.empty()

    signup_form = signup.form(key='signup-form', clear_on_submit=False)
    signup_username = signup_form.text_input(label='Username')
    signup_email = signup_form.text_input(label='Email')
    signup_password = signup_form.text_input(label='Password', type='password')
    # signup_notification = signup.empty()

    forgot_password_form = forgot_password.form(key='forgot-password-form', clear_on_submit=False)
    forgot_password_email = forgot_password_form.text_input(label='Email')
    # forgot_password_notification = forgot_password.empty()

    auth_notification = st.empty()

    if login_form.form_submit_button(label='Log in', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Logging in'):
            auth_functions.sign_in(login_email, login_password)

    if signup_form.form_submit_button(label='Sign up', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Signing up'):
            auth_functions.create_account(signup_username, signup_email, signup_password)

    if forgot_password_form.form_submit_button(label='Reset password', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Resetting password'):
            auth_functions.reset_password(forgot_password_email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

else:
    # Success message
    st.success(f"### Hello, _{st.session_state['user_info']['displayName']}_!")

    # st.write(st.session_state['user_info']['localId'])

    # Sign out
    st.header('Sign out:')
    st.button(label='Sign Out', on_click=auth_functions.sign_out, type='primary')

    # Delete Account
    st.header('Delete account:')
    password = st.text_input(label='Confirm your password', type='password')
    st.button(label='Delete Account', on_click=auth_functions.delete_account, args=[password], type='primary')
