import streamlit as st
import time
import json
from pathlib import Path

st.set_page_config(page_title = "Course Management",
                   page_icon = "",
                   layout="centered",
                   initial_sidebar_state="collapsed")

st.title("Course Management App")

st.divider()

next_assignment_id_number = 3

#Load Data
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

json_path = Path("assignments.json")

#Load the Data from a JSON File
if json_path.exists():
    with json_path.open("r", encoding= "utf-8") as f:
        assignments = json.load(f)



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
                st.dataframe(assignments)


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
        edit_title = st.text_input("Title", key="edit_title", value = assignment_edit["title"])
        edit_description = st.text_area("Description", key= "edit_description" , value = assignment_edit["description"])

    btn_update = st.button("Update", key="update_button", type="secondary", use_container_width=True)
    if btn_update:
        with st.spinner("Updating..."):
            time.sleep(5)
            assignment_edit["title"] = edit_title
            assignment_edit["description"] = edit_description

            with json_path.open("w", encoding="utf-8") as f:
                json.dump(assignments, f)

            st.success("Assignment Updated!")


