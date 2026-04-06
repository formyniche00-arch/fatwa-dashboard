import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://138.199.142.170:8001/ask"

st.title("📊 Fatwa API Dashboard")

# ----------------------
# Input (LIVE TEST)
# ----------------------
st.subheader("🔎 Test API Live")

user_question = st.text_input("Enter question")

if st.button("Ask API"):
    if user_question:
        res = requests.post(API_URL, json={"question": user_question})
        data = res.json()

        st.write("### Response:")
        st.write(data)

# ----------------------
# Evaluation Button
# ----------------------
st.subheader("🧪 Run Evaluation")

questions = [
    "هل التدخين حرام؟",
    "هل يجوز الصلاة بدون وضوء؟",
    "ما حكم الربا؟",
    "هل الموسيقى حلال؟",
    "كيف حالك؟",
     "ما معنى : إنما تبطل إذا خرج المصلي عن سمتها بحيث من رآه يقول : لا يصلي ؟",
     "عندي أسهم في البنك، بعتها والفلوس في الحساب، وأخرجت زكاتها لكن ليس منها وإنما أخذت مالاً من الوالد وزكيتها، فهل تصح الزكاة أم أزكيها منها؟"
]

if st.button("Run Test Set"):

    results = []

    for q in questions:
        try:
            res = requests.post(API_URL, json={"question": q})
            data = res.json()
        except:
            data = {}

        results.append({
            "question": q,
            "status": data.get("status"),
            "answer": data.get("chatbot_reply"),
            "has_source": "source" in data
        })

    df = pd.DataFrame(results)

    st.subheader("📋 Results")
    st.dataframe(df)

    # ----------------------
    # Metrics
    # ----------------------
    st.subheader("📊 Metrics")

    total = len(df)
    high = (df["status"] == "high").sum()

    st.write(f"Total: {total}")
    st.write(f"High confidence: {high}")
    st.write(f"Coverage: {(high/total)*100:.2f}%")

    # ----------------------
    # Chart
    # ----------------------
    st.subheader("📈 Distribution")

    fig, ax = plt.subplots()
    df["status"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    # ----------------------
    # Failures
    # ----------------------
    st.subheader("⚠️ Weak Cases")

    st.dataframe(df[df["status"].isin(["medium", "low"])])