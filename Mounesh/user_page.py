import streamlit as st
from database import get_messages_for_user
from kafka_producer import send_message
import time

# Streamlit App
st.title("Real-Time Messaging App")

# Input username
username = st.text_input("Enter your username", key="username")

if username:
    st.write(f"Welcome, {username}!")

    # Session state setup
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()

    # Reload messages function
    def reload_messages():
        new_messages = get_messages_for_user(username, page=1, page_size=10)
        if new_messages:
            st.session_state.messages = new_messages

    # Periodic refresh
    if time.time() - st.session_state.last_refresh > 5:  # Refresh every 5 seconds
        reload_messages()
        st.session_state.last_refresh = time.time()

    # Display messages
    st.subheader("Messages")
    for msg in st.session_state.messages:
        st.write(f"{msg[0]} -> {msg[1]}: {msg[2]} at {msg[3]}")

    # Pagination
    if st.button("Load More Messages"):
        st.session_state.page += 1
        more_messages = get_messages_for_user(username, page=st.session_state.page, page_size=10)
        if more_messages:
            st.session_state.messages.extend(more_messages)
        else:
            st.warning("No more messages to load.")

    # Send a new message
    st.subheader("Send a Message")
    recipient = st.text_input("Recipient", key="recipient")
    message = st.text_area("Message", key="message")

    if st.button("Send Message"):
        if recipient and message:
            send_message(username, recipient, message)
            st.success(f"Message sent to {recipient}!")
            reload_messages()  # Refresh the message list after sending
        else:
            st.error("Recipient and message cannot be empty.")
