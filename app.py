import streamlit as st
import requests
import threading
import time

API_URL = "https://fake-news-api-ise0.onrender.com/predict"

# Configure the Streamlit page
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered"
)

# Send the news article to the FastAPI backend and get the prediction
def predict_news(text):

    # try:
        response = requests.post(
            API_URL,
            json={"text": text},
            timeout=60
        )   
        
        response.raise_for_status()

        result = response.json()

        return result["prediction"], result["confidence"]

    # except requests.exceptions.RequestException:
    #     st.error(
    #         "The request timed out. " \
    #         "The backend may be starting after being idle. " \
    #         "Please wait a moment and try again."
    #     )
    #     st.stop()


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

    result = {}

    def worker():
        prediction, confidence = predict_news(news)
        result["prediction"] = prediction
        result["confidence"] = confidence

    # Start prediction in the background
    thread = threading.Thread(target=worker)
    thread.start()

    progress = st.progress(
        0,
        text="🚀 Starting backend... (This may take up to a minute on the first request)"
    )

    value = 0

    while thread.is_alive():

        if value < 20:
            message = "🚀 Starting backend..."
        elif value < 30:
            message = "📦 Loading model..."
        elif value < 40:
            message = "🧠 Analyzing article..."
        else:
            message = "⏳ Finalizing prediction..."

        value = min(value + 1, 95)
        progress.progress(value, text=message)

        time.sleep(0.4)

    thread.join()

    progress.progress(100, text="✅ Analysis complete!")
    time.sleep(0.5)
    progress.empty()

    prediction = result["prediction"]
    confidence = result["confidence"]
    
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
- **Training Accuracy:** 98.0%

### Deployment

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **API:** REST
""")