# RAG Implementation with Deepseek, Docker, and Streamlit

This repository contains an implementation of a Retrieval-Augmented Generation (RAG) system using the following stack:

- **Deepseek**: A powerful model for natural language processing and text generation.
- **Docker**: Containerization platform to simplify deployment and scalability.
- **Streamlit**: A simple and interactive web framework for building AI applications.

## Features
- Retrieval-Augmented Generation for enhanced response accuracy.
- Containerized deployment using Docker for easy portability.
- Interactive user interface built with Streamlit.

## Installation

Ensure you have Docker installed. Clone this repository and build the Docker container:

```bash
# Clone the repository
git clone https://github.com/satriahelmy/rag_deepseek/
cd rag_deepseek

# Build the Docker image
docker build -t rag-deepseek-app .
```

## Running the Application

1. Start the Docker container:
```bash
docker run -p 8501:8501 rag_deepseek_app
```

2. Open your browser and go to `http://localhost:8501` to access the Streamlit UI.

## Usage
1. Enter a query in the Streamlit interface.
2. The system will retrieve relevant context.
3. Deepseek will generate a response based on retrieved context.
4. The response is displayed in the UI.

## Future Enhancements
- Integration with additional LLMs.
- Optimization of retrieval strategies.
- Deployment options for cloud services.

## Acknowledgements
- [Deepseek](https://deepseek.com/)
- [Docker](https://www.docker.com/)
- [Streamlit](https://streamlit.io/)
