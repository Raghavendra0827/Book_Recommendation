#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from book_recommendation_final import userid, Recommend

background_image = 'data:image/png;base64,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'
html_code = f"""
    <style>
        body {{
            background-image: url('{background_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .stApp {{
            background: none;
        }}
    </style>
"""

def main():
    st.title("Book Recommendation System")
    u_id = userid()
    st.write(u_id["User-ID"])

    # Get user input for user id
    user_id = st.number_input("User ID", value=626)
    if user_id not in list(u_id["User-ID"]):
        main()
    if st.button("Recommend Book"):
        Recommend(user_id)

if __name__ == "__main__":
    main()
