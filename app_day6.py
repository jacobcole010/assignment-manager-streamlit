import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Course Manager", layout="centered")
st.title("Course Manager Application")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "role" not in st.session_state:
    st.session_state["role"] = None

users = [
        {
        "id": "1",
        "email": "admin@school.edu",
        "full_name": "System Admin",
        "password": "123ssag@43AE",
        "role": "Admin",
        "registered_at": "..."
    }
]

#Load Assignments
assignments = [
    {
        "id" : "HW1",
        "title" : "Intro to Database",
        "description" : "Basics of Database Design",
        "points" : 100,
        "type" : "Homework"
    } ,
    {
        "id" : "HW2",
        "title" : "Normalization",
        "description" : "Normalizing",
        "points" : 100,
        "type" : "Homework"
    }
]

if st.session_state["role"] == "Admin":
    st.markdown("This is the Admin UI- Dashboard")

    if st.button("Log Out"):
        with st.spinner("logging out..."):
            time.sleep(4)
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.rerun()


elif st.session_state["role"] =="Instructor":
    st.markdown("This is the Instrcuctor Dashboard")
    if st.session_state["page"] == "home":
        st.markdown(f"Welcome {st.session_state['user']['email']}")
        if st.button("Go to Dashboard", type="primary", key="view_dash_btn"):
            st.session_state["page"] = "dashboard"
            st.rerun()
    elif st.session_state["page"] == "dashboard":

        tab1, tab2, tab3 = st.tabs(["View Assignments", "Add New Assignment", "Update an Assignment"])

    with tab1:

    tab_option = st.radio("View/Search", ["View", "Search"], horizontal=True)
    if tab_option == "View":
        st.dataframe(assignments)
    else:
        titles = []
        for assignment in assignments:
            titles.append(assignment["title"])

        selected_title = st.selectbox("Select a Title", titles, key="Selected_Title")

        selected_assignment = {}

        for assignment in assignments:
            if assignment["title"] == selected_title:
                selected_assignment = assignment
                break



        if selected_assignment:
            with st.expander("Assignment Details", expanded=True):
                st.markdown(f"### Title: {selected_assignment['title']}")
                st.markdown(f"**Description**: {selected_assignment['description']}")
                st.markdown(f"Type: **{selected_assignment['type']}**")





    with tab2:
    st.markdown("## Add New Assignment")
    #st.markdown("### Add New Assignment")

    title = st.text_input("Title")
    description = st.text_area("Description", placeholder = "Normalization is Covered Here",
                            help = "Here You are Entering the Assignment Details")
    points = st.number_input("Points")

    #assignment_type = st.text_input("Assignment Type")
    assignment_type = st.radio("Type", ["Homework", "Lab"], horizontal = True)
    st.caption("Homework Type")

    assignment_type2 = st.selectbox("Select an Option", ["Homework", "Lab", "Other"])
    if assignment_type2 == "Other":
        assignment_type2 = st.text_input("Type", placeholder = "Enter the Assignment Type")

    due_date = st.date_input("Due Date")

    btn_save = st.button("Save Assignment", width="stretch", disabled = False)


    if btn_save:
        if not title:
            st.warning("Title Needs to be Provided")
        else:
            with st.spinner("Assignment is Being Recorded...."):
                time.sleep(5)

                new_assignment_id = "HW" + str(next_assignment_id_number)
                next_assignment_id_number += 1

                assignments.append(
                    {
                        "id" : new_assignment_id,
                        "title" : title,
                        "description" : description,
                        "points" : points,
                        "type" : assignment_type
                    }
                )

                #Record into JSON File
                with json_path.open("w", encoding="utf-8") as f:
                    json.dump(assignments, f)

                st.success("New Assignment is Recorded!")
                st.info("This is a New Assignment")
                time.sleep(3)
                #st.dataframe(assignments)
                st.rerun()


    with tab3:
    st.markdown("## Update an Assignment")
    titles = []
    for assignment in assignments:
        titles.append(assignment["title"])

    selected_item = st.selectbox("Select an Assignment", titles, key="selected_title_edit")


    assignment_edit = {}
    for assignment in assignments:
        if assignment["title"] == selected_item:
            assignment_edit = assignment
            break


    if assignment_edit:
        edit_title = st.text_input("Title", key=f"edit_title_{assignment_edit['id']}",
                                    value = assignment_edit["title"])
        edit_description = st.text_area("Description", key= f"edit_description_{assignment_edit['id']}",
                                        value = assignment_edit["description"])

        type_options = ["Homework", "Lab"]
        selected_index = type_options.index(assignment_edit["type"])


        edit_type = st.radio("Type", ["Homework", "Lab"],
                            key= f"edit_type_{assignment_edit['id']}")

    btn_update = st.button("Update", key="update_button", type="secondary", use_container_width=True)
    if btn_update:
        with st.spinner("Updating..."):
            time.sleep(3)
            assignment_edit["title"] = edit_title
            assignment_edit["description"] = edit_description

            with json_path.open("w", encoding="utf-8") as f:
                json.dump(assignments, f)

            st.success("Assignment Updated!")
            time.sleep(3)
            st.rerun()

else:
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email Address", key = "email_address_login")
        password_input = st.text_input("Password", type="password", key = "password_login")
        
        if st.button("Log In", type="primary",use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2) # Fake backend delay
                
                # Find user
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break
                
                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"]= True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user['role']
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    st.subheader("New Instructor Account")
    with st.container(border=True):
        new_email = st.text_input("Email Address", key="email_address_register")
        new_password = st.text_input("Password", type="password" , key = "password_reg")
        
        if st.button("Create Account", type="secondary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2) # Fake backend delay
                # ... (Assume validation logic here) ...
                users.append({
                    "id": str(uuid.uuid4()),
                    "email": new_email,
                    "password": new_password,
                    "role": "Instructor"
                })
                #with open(json_file, "w") as f:
                #   json.dump(users, f, indent=4)
                st.success(f"Account created! {new_email}")
                time.sleep(4)
                st.rerun()

    st.write("---")
    st.dataframe(users)

with st.sidebar:
    if "logged_in" in st.session_state and st.session_state["logged_in"] != False:
        user = st.session_state["user"]
        st.markdown(f"Welcome {user['email']}")
    else:
        st.markdown("Welcome! - Login")