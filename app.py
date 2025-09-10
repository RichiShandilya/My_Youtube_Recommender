import streamlit as st
import pandas as pd
from Rec_Sys import fetch_youtube_videos, fetch_trending_videos

st.set_page_config(page_title="YouTube Recommender", layout="wide")
st.title("🎥 YouTube Video Recommendation System")

# Default text
query = st.text_input("Enter a topic to search videos:", "Search what you want")

# ✅ Agar user ne search dabaya
if st.button("Search"):
    if query.strip() == "" or query == "Search what you want":
        df = fetch_trending_videos(max_results=15)   # Default = Trending
        st.subheader("🔥 Trending Videos")
    else:
        df = fetch_youtube_videos(query, max_results=15)
        st.subheader(f"📌 Top Results for: {query}")

    if not df.empty:
        st.dataframe(df.head())  # Optional: debugging

        # ✅ Directly show all recommended videos (no extra button)
        for _, row in df.iterrows():
            st.markdown(f"### {row['title']}")
            
            if row["thumbnail"]:
                st.image(row["thumbnail"], width=300)
            
            st.markdown(f"[▶ Watch on YouTube]({row['video_url']})")
            st.write("---")
