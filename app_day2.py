import streamlit as st

st.title("Course Management App")
st.header("Assigment Management")
st.subheader("Dashboard")

next_assignment_id_number = 3

st.divider()
st.markdown("----------------")

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

#Input

#st.markdown("# Add New Assignment")
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

import time

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
 


            st.success("New Assignment is Recorded!")
            st.info("This is a New Assignment")
            st.dataframe(assignments)





    



