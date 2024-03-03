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
books_ratings.dropna(inplace=True)

dataset_book_summary = books_ratings.groupby('ISBN')['Book-Rating'].agg(["count"])
drop_book_list = dataset_book_summary[dataset_book_summary['count'] < 20].index
dataset_cust_summary = books_ratings.groupby('User-ID')['Book-Rating'].agg(["count"])
drop_cust_list = dataset_cust_summary[dataset_cust_summary['count'] < 20].index
books_ratings = books_ratings[~books_ratings['ISBN'].isin(drop_book_list)]
books_ratings = books_ratings[~books_ratings['User-ID'].isin(drop_cust_list)]

booksss = pd.DataFrame(books_ratings['User-ID'].unique(), columns=["User-ID"])


def userid():
    return booksss


def Recommend(y):
    reader = Reader()
    data = Dataset.load_from_df(books_ratings[["User-ID", "ISBN", "Book-Rating"]][:100000], reader)
    model = SVD()
    cross_validate(model, data, measures=['RMSE', 'MAE'], cv=4)
    books_titles = list()
    books_urls = list()
    try:
        books_ratings['Estimate_Score'] = books_ratings['ISBN'].apply(lambda x: model.predict(y, x).est)
        lst_movie_ID = list(books_ratings.sort_values("Estimate_Score", ascending=False)["ISBN"].unique())[:5]

        books_titles = list()
        for val in lst_movie_ID:
            matching_books = list(books_details[books_details.ISBN == val]["Book-Title"])

            if matching_books:
                books_titles.append(matching_books[0])
            else:
                books_titles.append("No Title Found")

        books_urls = list()
        for val1 in lst_movie_ID:
            matching_urls = list(books_details[books_details.ISBN == val1]["Image-URL-S"])

            if matching_urls:
                books_urls.append(matching_urls[0])
            else:
                books_urls.append("No URL Found")
    except:
        st.warning("Invalid user ID")

    def display_images_in_layout(image_links, titles, num_rows=3, num_cols=2, image_size=(200, 200)):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            num_images = len(image_links)
            num_full_rows = num_images // num_cols
            remaining_cols = num_images % num_cols

            for i in range(num_full_rows):
                row_images, row_titles = image_links[i * num_cols:(i + 1) * num_cols], titles[i * num_cols:(i + 1) * num_cols]
                cols = st.columns(num_cols)

                for col, (image_link, title) in zip(cols, zip(row_images, row_titles)):
                    response = requests.get(image_link, headers=headers)
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                    
                    # Resize the image
                    img = img.resize(image_size)
                    col.image(img, caption=f"Title: {title}", use_column_width=True)

            if remaining_cols > 0:
                row_images, row_titles = image_links[-remaining_cols:], titles[-remaining_cols:]
                cols = st.columns(remaining_cols)

                for col, (image_link, title) in zip(cols, zip(row_images, row_titles)):
                    response = requests.get(image_link, headers=headers)
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                    
                    # Resize the image
                    img = img.resize(image_size)
                    col.image(img, caption=f"Title: {title}", use_column_width=True)

        except Exception as e:
            pass

    display_images_in_layout(books_urls, books_titles, num_rows=3, num_cols=2, image_size=(100, 100))
