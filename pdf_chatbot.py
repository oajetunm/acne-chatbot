import streamlit as st
import PyPDF2
import fitz  # PyMuPDF
import os
import re
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# ---------------------- CONFIG ---------------------- #

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pdf_file_path = "OTC.pdf"

# ---------------------- IMAGE + TEXT EXTRACTION ---------------------- #

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return "".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_images_and_generate_map(pdf_path, output_folder="images", keywords=None):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    product_image_map = {}
    all_image_paths = []

    if keywords is None:
        keywords = [
            "benzoyl peroxide", "salicylic acid", "cerave", "differin", "retinoid", "pimple", "zit", "acne", "adapalene", "cleanser", "moisturizer", "acne patch", "niacinamide", "pimple patch", "wrinkle"
            "adapalene", "cleanser", "moisturizer", "acne patch", "niacinamide", "blackheads", "black heads", "breakouts", "wrinkles", "acne scars", "sensitive skin", "dry skin", "oily skin", "combination skin", "sun damage", "hair"
        ]

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text().lower()
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{output_folder}/page{page_num + 1}_img{img_index + 1}.{image_ext}"
            with open(image_filename, "wb") as f:
                f.write(image_bytes)
            all_image_paths.append(image_filename)

            # Auto-link image to keyword if present on page
            for keyword in keywords:
                if re.search(rf"\b{re.escape(keyword)}\b", text):
                    if keyword not in product_image_map:
                        product_image_map[keyword] = image_filename

    return product_image_map, all_image_paths

# ---------------------- VECTORSTORE + LLM ---------------------- #

def create_vectorstore_from_text(text, api_key):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_text(text)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    return FAISS.from_texts(texts, embedding=embeddings)

def generate_response(input_text, vectorstore, api_key):
    model = ChatOpenAI(temperature=0.7, openai_api_key=api_key)
    retriever = vectorstore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=model, retriever=retriever)
    return qa.run(input_text)

# ---------------------- STYLING + BUBBLES ---------------------- #

def user_bubble(text):
    st.markdown(f"""
    <div style="background-color:#DCF8C6;padding:10px;border-radius:10px;margin-bottom:10px">
        <b>You:</b> {text}
    </div>
    """, unsafe_allow_html=True)

def bot_bubble(text):
    st.markdown(f"""
    <div style="background-color:#F1F0F0;padding:10px;border-radius:10px;margin-bottom:10px">
        <b>Bot:</b> {text}
    </div>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Acne Skincare Over the Counter Product Chatbot", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stTextInput>div>div>input {
        border: 2px solid #008080;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- APP UI ---------------------- #

st.title("📄🧠 Acne Skincare Chatbot")
st.subheader("Ask product or treatment questions — responses are powered by a dermatologist PDF guide.")

with st.expander("ℹ️ About this app"):
    st.markdown("""
    This chatbot uses AI to answer questions based on a preloaded PDF with product descriptions and images.
    Images are automatically extracted and matched to answers when relevant.
    """)

# Main Logic
if os.path.exists(pdf_file_path) and openai_api_key:
    with st.spinner("🔍 Loading PDF, extracting text and images..."):
        raw_text = extract_text_from_pdf(pdf_file_path)
        product_image_map, _ = extract_images_and_generate_map(pdf_file_path)
        vectorstore = create_vectorstore_from_text(raw_text, openai_api_key)

    with st.form("chat_form"):
        query = st.text_input("💬 Ask your acne skincare question here:")
        submitted = st.form_submit_button("Submit")

        if submitted and query:
            user_bubble(query)
            with st.spinner("🤖 Thinking..."):
                answer = generate_response(query, vectorstore, openai_api_key)
            bot_bubble(answer)

            # Dynamically display images if product keywords appear in the answer
            for keyword, image_path in product_image_map.items():
                if keyword.lower() in answer.lower() and os.path.exists(image_path):
                    st.image(image_path, caption=f"🔍 Related: {keyword.title()}", use_container_width=True)
else:
    st.error("🚫 Missing `acne_guide.pdf` or OpenAI API key. Please check your files.")
