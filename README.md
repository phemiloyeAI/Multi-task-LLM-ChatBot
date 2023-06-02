# Multi-task-LLM-ChatBot

This application is built on top of the LangChain API and provides multi-task functionalities, including Question & Answering over Documents and a smart ChatBot with internet search capabilities. It leverages the power of language models, embedding techniques, and efficient search capabilities to deliver accurate and contextually relevant information to users.

https://github.com/phemiloyeAI/Multi-task-LLM-ChatBot/assets/100911418/ffba0a5c-13f2-4422-99a4-9040e9766f60

## Features

### Question & Answering

The Question & Answering over Documents feature allows users to extract information and gain insights from their document files. It offers the following capabilities:

- **File Upload**: Users can upload document files in PDF, DOCX, or TXT format directly into the application.
- **Question Input**: Users can enter their questions in natural language format within the application.
- **Answer Generation**: The application utilizes the power of the OpenAI model to process the document content and generate accurate answers to user questions.
- **Contextual Understanding**: The LangChain API incorporates OpenAI embedding to enable contextual understanding of the document content, enhancing the accuracy of the generated answers.
- **Efficient Search**: The application utilizes the Chroma vector store for indexing the document embeddings, enabling quick and efficient search for relevant information.

### ChatBot

The ChatBot feature provides users with an interactive conversational experience. It offers the following capabilities:

- **OpenAI Model**: The ChatBot utilizes the OpenAI model for generating responses, ensuring natural and contextually relevant conversations.
- **Agent Capabilities**: The ChatBot is equipped with additional capabilities through agents, enabling it to perform tasks beyond basic conversation.
- **Tool Integration**: The ChatBot leverages external tools, such as the SERP (Search Engine Results Page) API, to expand its capabilities. This integration allows the bot to search the internet and provide accurate answers based on current events or specific search queries.
- **LangChain API**: The ChatBot's architecture is built using the LangChain API, which provides a comprehensive set of tools and utilities for developing advanced conversational applications.

## Installation

To install and run the Multi-task LLM App, follow these steps:

1. Create a virtual environment and activate it:
```
python3 -m venv myenv
source myenv/bin/activate
```
2. Install the required dependencies using the provided requirements file:
```
pip install -r requirements.txt
```

## Run the Streamlit app:
```
streamlit run application.py
```
