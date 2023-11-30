import streamlit as st
import os
import sqlite3
from datetime import datetime
import uuid
import pandas as pd


# Function to create SQLite connection and table if not exists
def create_db_table():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            birth_date DATE,
            address TEXT,
            ig_username TEXT,
            whatsapp_number TEXT,
            photo_path TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Function to check if a user with the same information already exists
def user_exists(name, birth_date, address, ig_username, whatsapp_number):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute(
        """
        SELECT id FROM users
        WHERE name=? AND birth_date=? AND address=? AND ig_username=? AND whatsapp_number=?
    """,
        (name, birth_date, address, ig_username, whatsapp_number),
    )
    user_id = c.fetchone()
    conn.close()
    return user_id is not None


# Function to insert data into SQLite database
def insert_data(name, birth_date, address, ig_username, whatsapp_number, photo_path):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()

    if not user_exists(name, birth_date, address, ig_username, whatsapp_number):
        c.execute(
            """
            INSERT INTO users (name, birth_date, address, ig_username, whatsapp_number, photo_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (name, birth_date, address, ig_username, whatsapp_number, photo_path),
        )
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


# Function to update data in SQLite database
def update_data(
    user_id, name, birth_date, address, ig_username, whatsapp_number, photo_path
):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute(
        """
        UPDATE users
        SET name=?, birth_date=?, address=?, ig_username=?, whatsapp_number=?, photo_path=?
        WHERE id=?
    """,
        (name, birth_date, address, ig_username, whatsapp_number, photo_path, user_id),
    )
    conn.commit()
    conn.close()


# Function to delete data from SQLite database
def delete_data(user_id, photo_path):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    os.remove(photo_path)


# Function to retrieve data from SQLite database
def get_user_data(user_id):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    data = c.fetchone()
    conn.close()
    return data


# Function to display data in a table
def display_data():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()

    if data:
        for row in data:
            (
                user_id,
                name,
                birth_date,
                address,
                ig_username,
                whatsapp_number,
                photo_path,
            ) = row

            # Data column on the left
            with st.container():
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write(f"User ID: {user_id}")
                    st.write(f"Name: {name}")
                    st.write(f"Birth Date: {birth_date}")
                    st.write(f"Address: {address}")
                    st.write(f"Instagram Username: {ig_username}")
                    st.write(f"WhatsApp Number: {whatsapp_number}")

                # Photo column on the right
                with col2:
                    st.image(photo_path, caption="Uploaded Photo", width=200)

            col3, col4 = st.columns(2)
            with col3:
                # Delete button

                if st.button(
                    f"Delete User {user_id}", type="secondary", use_container_width=True
                ):
                    delete_data(user_id, photo_path)
                    st.success(f"User {user_id} deleted successfully.")

            with col4:
                # Edit button

                if st.button(
                    f"Edit User {user_id}", type="secondary", use_container_width=True
                ):
                    st.subheader(f"Edit User {user_id}")
                    edit_name = st.text_input("Name", name)
                    edit_birth_date = st.date_input(
                        "Birth Date", datetime.strptime(birth_date, "%Y-%m-%d")
                    )
                    edit_address = st.text_area("Address", address)
                    edit_ig_username = st.text_input("Instagram Username", ig_username)
                    edit_whatsapp_number = st.text_input(
                        "WhatsApp Number", whatsapp_number
                    )

                    # Update button
                    if st.button("Update"):
                        update_data(
                            user_id,
                            edit_name,
                            edit_birth_date,
                            edit_address,
                            edit_ig_username,
                            edit_whatsapp_number,
                            photo_path,
                        )
                        st.success(f"User {user_id} updated successfully.")
            # with col5:
            st.markdown(
                '<hr style="border: 5px solid #ffffff; margin: 20px 0;">',
                unsafe_allow_html=True,
            )
    else:
        st.info("No data available.")


def main():
    create_db_table()

    st.title("Photo Upload and Save")

    # Input form
    name = st.text_input("Name")
    birth_date = st.date_input("Birth Date", min_value=pd.to_datetime("1900-01-01"))
    address = st.text_input("Address", "")
    ig_username = st.text_input("Instagram Username", "")
    whatsapp_number = st.text_input("WhatsApp Number", "")

    # Photo upload
    uploaded_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
    st.markdown(
        '<hr style="border: 2px solid #ffffff; margin: 20px 0;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <style>
        .input-values-section {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 3px;
            margin-top: 20px;
        }
        .input-label {
            font-weight: bold;
        }
        .input-value {
            margin-bottom: 10px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Display input values
    st.subheader("Input Values:")
    table_data = {
        "Labels": [
            "Name",
            "Birth Date",
            "Address",
            "Instagram Username",
            "WhatsApp Number",
            "Foto",
        ],
        "Data": [
            name,
            birth_date,
            address,
            ig_username,
            whatsapp_number,
            uploaded_file,
        ],
    }
    st.table(table_data)

    if st.button("Save", type="primary", use_container_width=True):
        # Save and display uploaded photo
        if uploaded_file is not None:
            # Generate a unique filename using a combination of timestamp and a random string
            unique_filename = str(uuid.uuid4()) + "_" + uploaded_file.name

            # Save uploaded photo to a directory with the unique filename
            save_path = os.path.join("uploads", unique_filename)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Insert data into SQLite database if user doesn't already exist
            if insert_data(
                name, birth_date, address, ig_username, whatsapp_number, save_path
            ):
                st.success("Data saved successfully.")
                st.rerun
            else:
                st.warning("User with the same information already exists.")

    # Display user data table
    st.markdown(
        '<hr style="border: 2px solid #ffffff; margin: 20px 0;">',
        unsafe_allow_html=True,
    )
    display_data()


if __name__ == "__main__":
    main()
