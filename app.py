import streamlit as st
from textblob import TextBlob
import re
from collections import Counter

st.set_page_config(
    page_title="AI Text Analyzer",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Text Analyzer")
st.write("Analyze your text for statistics, sentiment, keywords and readability.")

text = st.text_area(
    "Enter your text here:",
    height=250,
    placeholder="Type or paste your text..."
)

if st.button("Analyze Text"):

    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        # Basic statistics
        words = re.findall(r'\b\w+\b', text)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]

        word_count = len(words)
        character_count = len(text)
        sentence_count = len(sentences)

        # Sentiment analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        if polarity > 0.1:
            sentiment = "😊 Positive"
        elif polarity < -0.1:
            sentiment = "😞 Negative"
        else:
            sentiment = "😐 Neutral"

        # Keywords
        clean_words = [
            word.lower()
            for word in words
            if len(word) > 3
        ]

        stop_words = {
            "this", "that", "with", "from", "have",
            "your", "they", "will", "what", "about",
            "there", "which", "their", "would",
            "could", "should", "were", "been"
        }

        keywords = [
            word for word in clean_words
            if word not in stop_words
        ]

        keyword_counts = Counter(keywords)
        top_keywords = keyword_counts.most_common(10)

        # Display statistics
        st.subheader("📊 Text Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Words", word_count)
        col2.metric("Characters", character_count)
        col3.metric("Sentences", sentence_count)
        col4.metric("Sentiment", sentiment)

        # Sentiment details
        st.subheader("🎭 Sentiment Analysis")

        st.write(f"**Sentiment:** {sentiment}")
        st.write(f"**Polarity:** {polarity:.2f}")
        st.write(f"**Subjectivity:** {subjectivity:.2f}")

        # Keywords
        st.subheader("🔑 Top Keywords")

        if top_keywords:
            for word, count in top_keywords:
                st.write(f"• **{word}** — {count} time(s)")
        else:
            st.write("No keywords found.")