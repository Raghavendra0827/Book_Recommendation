import streamlit as st
from book_recommendation_final import userid, Recommend

background_image = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fdribbble.com%2Fshots%2F6688091-Book-App-Icon&psig=AOvVaw1W2vGDT-xsVc9StaEqlv--&ust=1706713299911000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCJCT2NqwhYQDFQAAAAAdAAAAABAd'
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
    user_id = st.number_input("User ID", value=242)
    if st.button("Recommend Book"):
        if user_id in list(u_id["User-ID"]):
            Recommend(user_id)
        else:
            st.warning("Invalid User_ID")
if __name__ == "__main__":
    main()
