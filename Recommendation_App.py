#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from book_recommendation_final import Recommend

def main():
    st.title("Book Recommendation System")

    # Get user input for user id
    user_id = st.number_input("User ID", value=27672)
    
    Recommend(user_id)

if __name__ == "__main__":
    main()

