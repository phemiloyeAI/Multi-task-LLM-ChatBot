import os
import streamlit as st

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY'] # openai_api_key
os.environ['SERPAPI_API_KEY'] = st.secrets['SERPAPI_API_KEY'] # serp_api_key

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(
                    chunks,
                    embeddings
                )
    return vector_store

def questionAnsweringWithDocument(vector_store):
    model = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    qaBOT = ConversationalRetrievalChain.from_llm(model, vector_store.as_retriever(),  memory=memory)

    return qaBOT
