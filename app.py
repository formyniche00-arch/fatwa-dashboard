import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

API_URL = "http://138.199.142.170:8001/ask"

st.set_page_config(page_title="Fatwa API Dashboard", layout="wide")

st.title("📊 Fatwa API Evaluation Dashboard")

# ==========================================================
# 1. LIVE TEST
# ==========================================================
st.header("🔎 Live API Test")

user_question = st.text_input("Enter a question")

if st.button("Ask API"):
    if user_question:
        res = requests.post(API_URL, json={"question": user_question})
        data = res.json() if res.status_code == 200 else {}

        st.subheader("Response")
        st.json(data)

# ==========================================================
# 2. TEST DATASET
# ==========================================================
st.header("🧪 Run Evaluation")

questions = [
    "السلام عليكم يا شيخ أنا أذهب مع أختي نشتغل في الصالات لنسرح النساء ويكون لنا غرفة إلا أننا نسمع صوت الموسيقى فما رأيكم",
    "عن أبي هريرة قال سمعت رسول الله صلى الله عليه وسلم يقول من أنفق زوجين من شيء من الأشياء في سبيل الله دعي من أبواب الجنة ما صحة ومعنى هذا الحديث",
    "السلام عليكم عندنا دكتورة في الجامعة تطلب من الطالبات أموالا لتساعد بها بعض المحتاجين وتطلب منا أن لا نخبر أحدا فما رأيكم بذلك",
    "السلام عليكم ورحمة الله عندي برنامج عن الموت وعملت مجسم جنازة فهل هذا بدعة",
    "يا شيخ بنك التسليف يعطي قرض زواج ويشترط ذلك لمن راتبه أقل من 10000 ريال وأنا راتبي 10200 ريال مع البدلات فهل يجوز لي تقديم راتبي دون البدلات كي أستحق القرض",
    "السلام عليكم ورحمة الله وبركاته حصل لي حادث مروري وتم تعويضي عن طريق شركة تأمين بمبلغ تم تقديره عن طريق ورش إصلاح ولم أقم بإصلاح السيارة وصرفت المبلغ ثم بعد فترة حصل حادث آخر في نفس موقع الصدمة الأولى وتم تعويضي مرة أخرى وتم تقدير المبلغ ثم أصلحت السيارة بمبلغ أقل فما حكم المبلغ الأول وما حكم الزائد في المرة الثانية",
    "يا شيخ عندي خبرة في التكنولوجيا وأعمل هكر ولدي قناة أنشر فيها شروحات فهل يجوز ذلك",
    "يا شيخ امرأة طلبت من زوجها مالا لتقضي دينها لكنها أعطته لأهلها فهل عليها شيء",
    "السلام عليكم هل طلب المرأة الطلاق لا يجوز بينما الزوج إذا طلق بدون سبب يكره له الطلاق وما سبب هذا الاختلاف",
    "السلام عليكم ورحمة الله وبركاته هل هذا الدعاء صحيح اللهم لا تحرمنا خير ما عندك بشر ما عندنا",
    "والدي في المستشفى منذ سنوات وزوجي يمنعني من زيارته بحجة أنه لا يشعر بمن حوله فهل علي إثم إذا لم أزره",
    "السلام عليكم هل التاتو يمنع الوضوء والغسل من الجنابة",
    "فضيلة الشيخ جمعية تحفيظ القرآن تجمع تبرعات لشراء عقار وتدعم الحلقات بنسبة من التبرعات فهل هذا جائز",
    "ما حكم تخريم الذقن للنساء لوضع الزينة",
    "نريد استقدام خادمة فهل يجوز إرسال مال لها أم يعد رشوة",
    "يا شيخ أبي يرفض تناول الدواء فهل يجوز وضعه له في الطعام دون علمه",
    "أمي لا تستطيع الحركة وسريرها ليس باتجاه القبلة فهل يجوز أن تصلي كما هي",
    "السلام عليكم زميلي اشترى سيارة بنظام التأجير المنتهي بالتمليك ويريد بيعها لي مع بقاء العقد باسمه فهل يجوز ذلك",
    "أعيش مع زوجتي وخرجت إلى بيت خالها وأخشى من الاختلاط والخلوة فماذا أفعل",
    "السلام عليكم علي نذر أن أذبح ذبيحة فهل يجوز الأكل منها",
    "السلام عليكم ما حكم بيع الدين بأن أشتري بالدين ثم أبيع لآخر وأسدد",
    "ما حكم الصلاة إلى سترة صغيرة وما مقدارها",
    "هل يجوز خلط الزكاة مع الصدقة وتوزيعها معا",
    "هل يشرع رفع اليدين في تكبيرات صلاة الجنازة",
    "أنا أشرف على مشاريع خيرية فهل يجوز أخذ نسبة من التبرعات",

    "هل التدخين حرام",
    "هل يجوز الصلاة بدون وضوء",
    "ما حكم الربا",
    "هل الموسيقى حلال",
    "كيف حالك",
    "ما معنى إنما تبطل إذا خرج المصلي عن سمتها بحيث من رآه يقول لا يصلي",
    "عندي أسهم في البنك بعتها والمال في الحساب وأخرجت زكاتها من مال آخر فهل تصح الزكاة أم يجب أن تكون منها",
    "كيف يتم الوضوء الصحيح",
    "كم عدد ركعات صلاة الفجر",
    "ما هي شروط الصلاة",
    "هل يجوز الكذب",
    "هل يجوز العمل في بنك",
    "هل كل بدعة أشد وأغلظ من كل كبيرة",
    "هل يجوز رقية مريض بالصلاة على النبي فقط والنفث بها",
    "أختي حجت وجمعت طواف الإفاضة مع الوداع بنية الوداع جهلا فهل حجها صحيح",
    "في قوله اهبطوا منها جميعا هل يدخل معهم الحية وهل هناك دليل",
    "ما هي سنة الوضوء وكيف تصلى وهل تصلى في وقت النهي",
    "شخص يعمل في محل تمر ويأكل منه أثناء العمل ثم يبيعه فهل عليه إثم",
    "شخص نوى الصيام قبل المغرب ثم نسي النية ليلا وشرب بعد الفجر ناسيا فهل يتم صومه",
    "هل يجب طاعة الوالدين في الأمور الخاصة مثل العطر أو وقت الاغتسال",
    "سائق يعمل مع أجانب ولا يستطيع التوقف للصلاة ويخرج وقت الصلاة بسبب العمل فما الحكم",

    "ما حكم تأخير الصلاة عن وقتها بدون عذر",
    "هل يجوز الجمع بين الصلوات في العمل",
    "ما حكم التعامل بالعملات الرقمية",
    "هل يجوز قراءة القرآن بدون وضوء"
]

if st.button("Run Full Evaluation"):

    results = []

    with st.spinner("Running evaluation..."):
        for q in questions:
            try:
                start_time = time.time()
                res = requests.post(API_URL, json={"question": q})

                latency = time.time() - start_time

                data = res.json()
            except:
                data = {}
                latency = None

            results.append({
                "question": q,
                "status": data.get("status"),
                "answer": data.get("chatbot_reply"),
                "has_source": "source" in data,
                "answer_length": len(data.get("chatbot_reply", "")) if data.get("chatbot_reply") else 0,
                "latency": latency
            })

    df = pd.DataFrame(results)

    # ==========================================================
    # 3. METRICS (IMPORTANT FOR CEO)
    # ==========================================================
    st.header("📊 Key Metrics")

    total = len(df)
    high = (df["status"] == "high").sum()
    medium = (df["status"] == "medium").sum()
    low = (df["status"] == "low").sum()
    simple = (df["status"] == "simple_llm").sum()
    chat = (df["status"] == "chat").sum()

    coverage = (high / total) * 100 if total > 0 else 0
    source_rate = (df["has_source"].sum() / total) * 100 if total > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Questions", total)
    col2.metric("High Confidence", high)
    col3.metric("High Confidence Rate %", f"{coverage:.1f}%")
    col4.metric("Source Usage %", f"{source_rate:.1f}%")

    st.header("⚡ Performance Metrics")
    df["latency"] = df["latency"].fillna(0)
    avg_latency = df["latency"].mean()
    max_latency = df["latency"].max()
    min_latency = df["latency"].min()

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Latency (s)", f"{avg_latency:.2f}")
    col2.metric("Max Latency (s)", f"{max_latency:.2f}")
    col3.metric("Min Latency (s)", f"{min_latency:.2f}")
    grounded_high = df[(df["status"] == "high") & (df["has_source"] == True)].shape[0]

    st.metric("Grounded High Answers", grounded_high)

    # ==========================================================
    # 4. DISTRIBUTION CHART
    # ==========================================================
    st.header("📈 Response Distribution")

    fig, ax = plt.subplots()
    df["status"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("Response Types")
    ax.set_xlabel("Status")
    ax.set_ylabel("Count")

    st.pyplot(fig)

    st.header("⏱️ Latency Distribution")

    fig2, ax2 = plt.subplots()
    df["latency"].plot(kind="hist", bins=10, ax=ax2)
    ax2.set_title("Latency Distribution")
    ax2.set_xlabel("Seconds")

    st.pyplot(fig2)


    # ==========================================================
    # 5. TABLE RESULTS
    # ==========================================================
    st.header("📋 Full Results")

    st.dataframe(df)
    st.header("🐢 Slow Responses (>2s)")

    slow_df = df[df["latency"] > 2]

    st.dataframe(slow_df)

    # ==========================================================
    # 6. FAILURE ANALYSIS (VERY IMPORTANT)
    # ==========================================================
    st.header("⚠️ Weak Cases (Needs Improvement)")

    weak_df = df[df["status"].isin(["medium", "low"])]

    st.dataframe(weak_df)

    st.header("🔥 Worst Cases (Lowest Confidence)")

    worst_df = df[df["status"].isin(["medium", "low"])].head(10)

    st.dataframe(worst_df)

    # ==========================================================
    # 7. INSIGHTS (AUTO GENERATED)
    # ==========================================================
    st.header("🧠 Insights")

    st.write(f"- {high} out of {total} questions answered with high confidence.")
    st.write(f"- {medium + low} questions need improvement.")
    st.write(f"- {simple} answered using fallback LLM (not from fatwa DB).")
    st.write(f"- {chat} were non-religious queries.")
    st.write(f"- Average response time: {avg_latency:.2f} seconds")

    if coverage < 60:
        st.warning("⚠️ Coverage is low → retrieval needs improvement")
    else:
        st.success("✅ Coverage is good")

    if source_rate < 70:
        st.warning("⚠️ Many answers are not grounded in fatwas")
    else:
        st.success("✅ Strong grounding in fatwa sources")
