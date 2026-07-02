import streamlit as st
import requests

API_URL = "https://fake-news-detector-cqw3.onrender.com/predict"

# Configure the Streamlit page
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered"
)

# Send the news article to the FastAPI backend and get the prediction
def predict_news(text):

    try:
        response = requests.post(
            API_URL,
            json={"text": text},
            timeout=60
        )   
        
        response.raise_for_status()

        result = response.json()

        return result["prediction"], result["confidence"]

    except requests.exceptions.RequestException:
        st.error("❌ Could not connect to the FastAPI server. " \
                    "Make sure the server is running and try again.")
        st.stop()


# Application title
st.title("📰 Fake News Detector")

# Brief description of the application
st.write(
    "Enter a news article below to determine whether it is likely to be **Real** or **Fake**."
)

# Input area for the news article
news = st.text_area(
    "News Article",
    height=150,
    placeholder="Paste the news article here..."
)

# Trigger prediction when the button is clicked
if st.button("🔍 Predict"):

    # Validate user input
    if not news.strip():
        st.warning("Please enter a news article.")
        st.stop()

    with st.spinner(
        "Analyzing the article... The first request may take up to a minute if the backend is starting."
    ):
        prediction, confidence = predict_news(news)

    st.divider()

    # Display prediction result
    if prediction == "FAKE":
        st.error("🚨 Fake News Detected")
    else:
        st.success("✅ Real News Detected")

    # Display prediction confidence
    st.progress(confidence / 100)

    st.metric(
        label="Confidence",
        value=f"{confidence:.2f}%"
    )

    # Display basic input statistics
    st.write(f"**Word Count:** {len(news.split())}")

# Sidebar with model details
st.sidebar.title("ℹ️ Model Information")

st.sidebar.markdown("""
### Model

- **Algorithm:** LinearSVC
- **Feature Extraction:** TF-IDF
- **N-grams:** Unigrams + Bigrams
- **Dataset:** WELFake Dataset
- **Training Accuracy:** 97.82%

### Deployment

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **API:** REST
""")