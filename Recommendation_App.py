import streamlit as st
from book_recommendation_final import userid, Recommend

background_image = 'https://cdn.dribbble.com/users/1236773/screenshots/6688091/book-icon_4x.png'
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
st.markdown(html_code, unsafe_allow_html=True)

def main():
    st.title("Book Recommendation System")
    u_id = userid()

    # Get user input for user id
    user_id = st.selectbox("User ID", u_id["User-ID"].to_list())
    if st.button("Recommend Book"):
        if user_id in list(u_id["User-ID"]):
            Recommend(user_id)
        else:
            st.warning("Invalid User_ID")
if __name__ == "__main__":
    main()
