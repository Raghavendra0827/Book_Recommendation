#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from book_recommendation_final import Recommend

def main():
    st.title("Book Recommendation System")

    # Get user input for book genre
    book_genre = st.numeric_input("User ID")
    Recommend(book_genre)

if __name__ == "__main__":
    main()

