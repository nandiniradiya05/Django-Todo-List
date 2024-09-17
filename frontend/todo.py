import streamlit as st
import requests

# API URL endpoints
SIGNUP_LOGIN_URL = "http://127.0.0.1:8000/task/signup-login/"
TASKS_URL = "http://127.0.0.1:8000/task/tasks/"
OTHERS_TASKS_URL= "http://127.0.0.1:8000/task/tasks/other/"


# Function to handle signup
def signup(name, email, password):
    response = requests.post(SIGNUP_LOGIN_URL, data={"name": name, "email": email, "password": password})
    response.raise_for_status()
    return response.json()

# Function to handle login
def login(email, password):
    payload = {"email": email, "password": password}
    response = requests.post(SIGNUP_LOGIN_URL, data=payload)
    response.raise_for_status()
    return response.json()

# Function to fetch tasks
def get_tasks(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(TASKS_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def create_tasks(title, description, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(TASKS_URL, headers=headers, data={"title": title, "description": description})
    response.raise_for_status()
    return response.json()
    
def get_others_tasks(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(OTHERS_TASKS_URL, headers=headers)
    response.raise_for_status()
    return response.json()


# Create a header with the app name on the left and buttons on the right
def create_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# To Do List")
    with col2:
        # Apply custom CSS to center the buttons vertically
        st.markdown("""
        <style>
        .centered-content {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

        # Use a container with the centered-content class to align vertically
        with st.container():
            st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                signup_clicked = st.button("Signup", key="header_signup_button")
            with col4:
                login_clicked = st.button("Login", key="header_login_button")
            st.markdown("</div>", unsafe_allow_html=True)

            if signup_clicked:
                st.session_state['show_login'] = False
            if login_clicked:
                st.session_state['show_login'] = True

# Main function to control the app flow
def main():
    # Display the header
    if 'access_token' not in st.session_state:
        create_header()

    # Check if the user is logged in
    if 'access_token' in st.session_state:
        # Display sidebar with options
        with st.sidebar:
            st.header("Navigation")
            if st.button("Create Task", key="sidebar_create_task"):
                st.session_state['show_create_task'] = True
                st.session_state['show_your_tasks'] = False
                st.session_state['show_others_tasks'] = False
            if st.button("View Your Tasks", key="sidebar_view_your_tasks"):
                st.session_state['show_create_task'] = False
                st.session_state['show_your_tasks'] = True
                st.session_state['show_others_tasks'] = False
            if st.button("View Others' Tasks", key="sidebar_view_others_tasks"):
                st.session_state['show_create_task'] = False
                st.session_state['show_your_tasks'] = False
                st.session_state['show_others_tasks'] = True

        st.write("## Welcome to your To Do List!")

        # Display the "Your Tasks" page by default
        if 'show_create_task' not in st.session_state:
            st.session_state['show_your_tasks'] = True

        # Display content based on the selected option
        if st.session_state.get('show_create_task'):
            st.write("## Create a Task")
            # Logic to create a task can go here
            try:
                access_token = st.session_state['access_token']
                title = st.text_input("Title", key="task_title")
                description = st.text_input("Description", key="task_description")
                submit_task = st.button("Create", key="submit_task")
                if submit_task:
                    task = create_tasks(title, description, access_token)
                    print(task)
                    # for task in tasks['data']:
                    st.write(f"- {task['data']['title']}: {task['data']['description']}")
                    
            except requests.exceptions.HTTPError as e:
                st.error(f"Failed to create tasks: {e.response.json().get('message', 'Error creating tasks')}")

        elif st.session_state.get('show_your_tasks'):
            st.write("## Your Tasks")
            try:
                access_token = st.session_state['access_token']
                tasks = get_tasks(access_token)
                for task in tasks['data']:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"- {task['title']}: {task['description']}")
                    with col2:
                        st.markdown("""
                            <style>
                            .centered-content {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100%;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                        with st.container():
                            st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
                            col3, col4 = st.columns(2)
                            with col3:
                                edit_clicked = st.button("Edit", key=f"edit_button_{task['id']}")
                            with col4:
                                del_clicked = st.button("Delete", key=f"delete_button_{task['id']}")
                            st.markdown("</div>", unsafe_allow_html=True)

                            if edit_clicked:
                                pass
                            if del_clicked:
                                pass

                    # st.write(f"- {task['title']}: {task['description']}")
            except requests.exceptions.HTTPError as e:
                st.error(f"Failed to fetch tasks: {e.response.json().get('message', 'Error fetching tasks')}")

        elif st.session_state.get('show_others_tasks'):
            st.write("## Others' Tasks")
            # Logic to view others' tasks can go here
            try:
                access_token = st.session_state['access_token']
                tasks = get_others_tasks(access_token)
                for task in tasks['data']:
                    st.write(f"- {task['title']}: {task['description']}")
            except requests.exceptions.HTTPError as e:
                st.error(f"Failed to fetch tasks: {e.response.json().get('message', 'Error fetching tasks')}")

    else:
        # Display login/signup forms
        if 'show_login' not in st.session_state:
            st.session_state['show_login'] = False

        # Toggle between signup and login forms
        if st.session_state['show_login']:
            st.write("## Login")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            login_button = st.button("Login", key="form_login_button")
            
            if login_button:
                try:
                    login_response = login(login_email, login_password)
                    st.success("Login successful!")
                    st.session_state['access_token'] = login_response.get("access")
                    st.session_state['refresh_token'] = login_response.get("refresh")
                    st.session_state['show_tasks'] = True
                    st.session_state['show_your_tasks'] = True  # Set default to show your tasks
                except requests.exceptions.HTTPError as e:
                    st.error(f"Login failed: {e.response.json().get('message', 'Invalid credentials')}")
        else:
            st.write("## Signup")
            name = st.text_input("Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            signup_button = st.button("Signup", key="form_signup_button")
            
            if signup_button:
                try:
                    signup_response = signup(name, email, password)
                    st.session_state['access_token'] = signup_response.get("access")
                    st.session_state['refresh_token'] = signup_response.get("refresh")
                    st.success("Signup successful! You can now log in.")
                    st.session_state['show_login'] = True  # Switch to login form
                    st.session_state['show_tasks'] = True
                    st.session_state['show_your_tasks'] = True  # Set default to show your tasks
                except requests.exceptions.HTTPError as e:
                    st.error(f"Signup failed: {e.response.json().get('message', 'Unknown error')}")

if __name__ == "__main__":
    main()
