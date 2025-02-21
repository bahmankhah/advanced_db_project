import streamlit as st
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

API_URL = "http://127.0.0.1:8000/api/apps"
CATEGORIES_URL = "http://127.0.0.1:8000/api/categories"
RATINGS_DISTRIBUTION_URL = "http://127.0.0.1:8000/api/ratings-distribution"
AVERAGE_RATINGS_URL = "http://127.0.0.1:8000/api/average-ratings"
CONTENT_RATINGS_URL = "http://127.0.0.1:8000/api/content-ratings"


st.title("Play Store Apps Dashboard")

@st.cache_data
def fetch_categories():
    response = requests.get(CATEGORIES_URL)
    if response.status_code == 200:
        return [category['name'] for category in response.json()]
    else:
        st.error("Failed to fetch categories.")
        return []


@st.cache_data
def fetch_content_ratings():
    response = requests.get(CONTENT_RATINGS_URL)
    if response.status_code == 200:
        return [rating for rating in response.json()]
    else:
        st.error("Failed to fetch content ratings.")
        return []
    

category_options = fetch_categories()

content_rating_options = fetch_content_ratings()

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox("Select Category", ["All Categories"] + category_options)

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0)
max_price = st.sidebar.number_input("Maximum Price", min_value=0.0, step=0.1)
content_rating = st.sidebar.selectbox("Select Content Rating", ["All Content Ratings"] + content_rating_options)

params = {
    "category": selected_category if selected_category != "All Categories" else None,
    "rating": min_rating,
    "price": max_price,
    "content_rating": content_rating if content_rating != "All Content Ratings" else None,
    "per_page": 1000,
    "page": 1
}

def fetch_data(page):
    params["page"] = page
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching page {page} data from API.")
        return {}

def load_paginated_data():
    all_data = []
    page = 1

    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            futures = [executor.submit(fetch_data, page) for page in range(page, page+5)]  # Fetch 5 pages concurrently
            for future in futures:
                result = future.result()
                if "data" in result:
                    all_data.extend(result["data"])
                else:
                    break
            page += 5
            yield pd.DataFrame(all_data)
            time.sleep(5)


ratings_response = requests.get(RATINGS_DISTRIBUTION_URL)
if ratings_response.status_code == 200:
    ratings_data = pd.DataFrame(ratings_response.json())
    st.subheader("Distribution of App Ratings")
    st.bar_chart(ratings_data.set_index('rating')['count'])
else:
    st.error("Failed to fetch ratings distribution.")

avg_ratings_response = requests.get(AVERAGE_RATINGS_URL)
if avg_ratings_response.status_code == 200:
    avg_ratings_data = pd.DataFrame(avg_ratings_response.json())
    
    avg_ratings_data = avg_ratings_data.dropna(subset=['category_name', 'average_rating'])
    
    avg_ratings_data['average_rating'] = pd.to_numeric(avg_ratings_data['average_rating'], errors='coerce')
    avg_ratings_data = avg_ratings_data.sort_values(by='average_rating', ascending=False)
    
    st.subheader("Average Ratings by Category")
    st.bar_chart(avg_ratings_data.set_index('category_name')['average_rating'])
else:
    st.error("Failed to fetch average ratings.")


table = None
for df in load_paginated_data():
    if not df.empty:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').dropna()
        df['rating'] = df['rating'].astype(float)

        if(table is None):
            st.write("Filtered Results:")
            table = st.dataframe(df)
        else:
            table.dataframe(df)
    else:
        break