import streamlit as st
import pandas as pd
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
import os

# Konfigurasi halaman
st.set_page_config(page_title="RAG dengan DeepSeek-R1:1.5B", layout="wide")
st.title("📄 RAG dengan DeepSeek-R1:1.5B - Upload Dokumen (TXT, XLSX, XLS, CSV) & Bertanya")

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

vectorstore = None

# Fungsi membaca berbagai format file (TXT, XLSX, XLS, CSV)
def read_file(file):
    file_ext = file.name.split(".")[-1]

    if file_ext == "txt":
        return file.read().decode("utf-8")  # Baca file TXT sebagai string

    elif file_ext in ["xlsx", "xls"]:
        df = pd.read_excel(file)  # Baca file Excel (XLSX/XLS)
        return "\n".join(df.astype(str).apply(lambda row: " | ".join(row), axis=1))  # Gabungkan teks Excel

    elif file_ext == "csv":
        df = pd.read_csv(file)  # Baca file CSV
        return "\n".join(df.astype(str).apply(lambda row: " | ".join(row), axis=1))  # Gabungkan teks CSV

    else:
        return None

# Fungsi untuk memproses dokumen
def process_document(file):
    global vectorstore

    # Baca konten file
    text = read_file(file)
    
    if text is None:
        st.error("❌ Format file tidak didukung! Hanya .txt, .xlsx, .xls, atau .csv")
        return

    # Split teks menjadi bagian kecil
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(text)

    # Gunakan Ollama untuk membuat embedding
    embedding_function = OllamaEmbeddings(model="deepseek-r1:1.5b")

    # Simpan ke ChromaDB
    vectorstore = Chroma.from_texts(texts, embedding_function)

    st.success(f"✅ Dokumen '{file.name}' berhasil diproses dan diindeks!")

# Fungsi untuk mencari jawaban dengan Ollama
def generate_answer(query):
    if vectorstore is None:
        return "❌ Belum ada dokumen yang diunggah!"

    # Cari dokumen yang relevan
    docs = vectorstore.similarity_search(query, k=3)
    retrieved_text = "\n\n".join(docs)

    # Buat prompt untuk DeepSeek-R1:1.5B
    prompt = f"""
    Gunakan informasi berikut untuk menjawab pertanyaan pengguna:

    {retrieved_text}

    Pertanyaan: {query}
    Jawaban:
    """

    # Dapatkan respons dari Ollama dengan model DeepSeek-R1:1.5B
    response = ollama.chat(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]

# Sidebar untuk unggah dokumen
st.sidebar.header("📤 Upload Dokumen (.txt, .xlsx, .xls, .csv)")
uploaded_file = st.sidebar.file_uploader("Unggah file teks atau Excel", type=["txt", "xlsx", "xls", "csv"])

if uploaded_file is not None:
    process_document(uploaded_file)

# Input pertanyaan pengguna
query = st.text_input("💬 Ajukan Pertanyaan Berdasarkan Dokumen:")

if st.button("🔍 Cari Jawaban"):
    if query.strip() == "":
        st.warning("⚠️ Harap masukkan pertanyaan terlebih dahulu!")
    else:
        answer = generate_answer(query)
        st.subheader("📝 Jawaban:")
        st.write(answer)
