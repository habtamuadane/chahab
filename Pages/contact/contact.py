import streamlit as st

class Contact:
    def show_contact_page(self):
        st.title("📞 Contact Us")
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        message = st.text_area("Message")

        if st.button("Send Message"):
            st.success("Thank you for contacting us! We'll get back soon.")
