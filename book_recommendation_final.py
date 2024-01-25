import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import math
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

books_ratings = pd.read_csv("books_ratings.csv", encoding="ISO-8859-1")
books_details = pd.read_csv("books_details.csv", encoding="ISO-8859-1")
books_ratings.dropna(inplace = True)

dataset_book_summary =books_ratings.groupby('ISBN')['Book-Rating'].agg(["count"])
dataset_book_summary.sort_values(["count"], ascending = False)
dataset_book_summary["count"].value_counts()
dataset_book_summary["count"].unique()
drop_book_list=dataset_book_summary[dataset_book_summary['count']<10].index
dataset_cust_summary=books_ratings.groupby('User-ID')['Book-Rating'].agg(["count"])
dataset_cust_summary.sort_values(["count"], ascending = False)
drop_cust_list=dataset_cust_summary[dataset_cust_summary['count']<10].index
books_ratings=books_ratings[~books_ratings['ISBN'].isin(drop_book_list)]
books_ratings=books_ratings[~books_ratings['User-ID'].isin(drop_cust_list)]
books_ratings.shape
books_ratings

def Recommend(y):
    reader=Reader()
    data=Dataset.load_from_df(books_ratings[["User-ID","ISBN","Book-Rating"]][:100000], reader)
    model=SVD()
    cross_validate(model, data, measures=['RMSE','MAE'], cv=4)
    books_titles = list()
    books_urls = list()
    books_ratings['Estimate_Score']=books_ratings['ISBN'].apply(lambda x: model.predict(y, x).est)
    lst_movie_ID = list(books_ratings.sort_values("Estimate_Score", ascending = False)["ISBN"].unique())[:5]

    # lst_movie_ID
    
    books_titles = list()
    for val in lst_movie_ID:
        matching_books = list(books_details[books_details.ISBN == val]["Book-Title"])

        if matching_books:
            # If the list is not empty, append the first element
            books_titles.append(matching_books[0])
        else:
            # Handle the case where no matching book is found
            books_titles.append("No Title Found")

    # books_titles

    books_urls = list()
    for val1 in lst_movie_ID:
        matching_urls = list(books_details[books_details.ISBN == val1]["Image-URL-S"])

        if matching_urls:
            # If the list is not empty, append the first element
            books_urls.append(matching_urls[0])
        else:
            # Handle the case where no matching URL is found
            books_urls.append("No URL Found")

# Now 'books_urls' contains the URLs or "No URL Found" for each ISBN in 'lst_movie_ID'


    def display_image_from_link_with_title(image_link, title):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            # Fetch the image from the link with headers
            response = requests.get(image_link, headers=headers)
            response.raise_for_status()  # Check for request errors

            # Open the image using PIL
            img = Image.open(BytesIO(response.content))

            # Display the image in the Streamlit app with the title
            st.image(img, caption=f"Title: {title}", use_column_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

    # Iterate over the zipped lists and display images with titles in Streamlit
    for image_link, title in zip(books_urls, books_titles):
        display_image_from_link_with_title(image_link, title)
