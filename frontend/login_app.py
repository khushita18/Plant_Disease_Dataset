import streamlit as st
import json
import os
import hashlib

# --- helper for password hashing ---
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed):
    return make_hash(password) == hashed

# --- file to store users ---
USER_DB = "users.json"

if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

with open(USER_DB, "r") as f:
    users = json.load(f)

st.set_page_config(page_title="Login | CropSavior", layout="centered")

st.title("🌿 CropSavior Login")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and "password" in users[username]:
            if check_hash(password, users[username]["password"]):
                st.success(f"✅ Logged in as {username}")
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.switch_page("pages/app.py")

            else:
                st.error("❌ Incorrect password.")
        else:
            st.error("⚠️ User not found. Please sign up first.")


elif choice == "Sign Up":
    st.subheader("Create a new account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_pass != confirm_pass:
            st.warning("⚠️ Passwords do not match!")
        elif new_user in users:
            st.warning("⚠️ Username already exists!")
        else:
            users[new_user] = {"password": make_hash(new_pass)}
            with open(USER_DB, "w") as f:
                json.dump(users, f)
            st.success("🎉 Account created successfully! You can login now.")
