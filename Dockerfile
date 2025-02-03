# Gunakan base image dengan Python
FROM python:3.10

# Set working directory dalam container
WORKDIR /app

# Salin semua file ke dalam container
COPY . /app

# Install dependensi yang dibutuhkan
RUN pip install --no-cache-dir streamlit pandas openpyxl xlrd chromadb langchain ollama langchain-community

# Jalankan aplikasi Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
