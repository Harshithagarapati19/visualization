import streamlit as st
import PyPDF2
import docx
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# --- Text Extraction ---
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# --- Word Frequency ---
def get_word_frequencies(text):
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

# --- Streamlit UI ---
st.title("📊 Text Analysis App")
st.write("Upload a PDF or DOCX file to visualize word frequencies.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    st.subheader("📄 Extracted Text Preview")
    st.text(text[:1000] + "..." if len(text) > 1000 else text)

    word_freq = get_word_frequencies(text)
    top_words = word_freq.most_common(20)
    df = pd.DataFrame(top_words, columns=["Word", "Frequency"])

    # --- WordCloud ---
    st.subheader("☁️ WordCloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis("off")
    st.pyplot(fig_wc)

    # --- Bar Chart ---
    st.subheader("📊 Top 20 Words - Bar Chart")
    fig_bar, ax_bar = plt.subplots()
    sns.barplot(x="Frequency", y="Word", data=df, ax=ax_bar, palette="viridis")
    st.pyplot(fig_bar)

    # --- Heatmap ---
    st.subheader("🔥 Word Frequency Heatmap")
    fig_heat, ax_heat = plt.subplots()
    sns.heatmap(df.set_index("Word").T, annot=True, cmap="YlGnBu", ax=ax_heat)
    st.pyplot(fig_heat)
