
import os
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

from conversation import conversationChat
from question_answering import questionAnsweringWithDocument, create_vector_store

from utils import preprocess_file

## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input", placeholder="Send a message.")
    return input_text

st.set_page_config(page_title=" Multi-task LLM App")
st.markdown('<style>body { font-size: 16px; }</style>', unsafe_allow_html=True)

# Sidebar contents
with st.sidebar:
    st.title('Multi-task LLM Applications by')
    st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown('''
        <style>
            .blue-color {
                color: blue;
            }
            .teal-color {
                color: teal;
            }

        </style>
        <div style="margin-top: auto;">
            <h2 style="color: white; margin-bottom: 10px;"><em>Femiloye Oyerinde</em></h2>
            <a href="https://www.linkedin.com/in/femiloye-oyerinde-b82663134/" target="_blank" style="color: white; font-size: 16px; text-decoration: none;">
                <i class="fa fa-linkedin blue-color" style="vertical-align: middle; margin-right: 5px;"></i> LinkedIn
            </a>
            <br>
            <a href="https://github.com/phemiloyeAI" target="_blank" style="color: white; text-decoration: none;">
                <i class="fa fa-github teal-color" style="vertical-align: middle; margin-right: 5px;"></i> GitHub
            </a>    
        </div>
        ''', unsafe_allow_html=True)    
    
    add_vertical_space(2)

    st.markdown('''
    <div>
        <h2 style="background-color: white; color: black; padding: 5px; border-radius: 5px; margin-bottom: 15px;">About</h2>
        This Multi-task application built on-top of LangChain API can do the following tasks:
        <ul style="color: white; line-height: 2.0;">
            <li>Question & Answering over Document.</li>
            <li>A smart ChatBot using an Agent to search the internet for improved reasoning.</li>
        </ul>
    ''', unsafe_allow_html=True)

    add_vertical_space(2)

# Initialize session state variables
if 'qa_generated' not in st.session_state:
    st.session_state['qa_generated'] = ["Hi there, Ask me any question about this document!"] 

if 'qa_past' not in st.session_state:
    st.session_state['qa_past'] = [""] 

if 'chat_generated' not in st.session_state:
    st.session_state['chat_generated'] = ["Hi there, How can I assist you today?"] 

if 'chat_past' not in st.session_state:
    st.session_state['chat_past'] = [""] 

if "uploadbtn_state" not in st.session_state:
    st.session_state.uploadbtn_state = False
            
if 'vector_store_index' not in st.session_state:
    st.session_state['vector_store_index'] = True

if 'vector_store' not in st.session_state:
    st.session_state['vector_store'] = True

if 'extract_chunks' not in st.session_state:
    st.session_state['extract_chunks'] = True


def main():

    st.markdown('''
    <h3>App Demo</h3>
    ''', unsafe_allow_html=True)
    demo_video_path = os.path.join(os.getcwd(), 'files\demo_video.mp4')

    st.write("Watch the video below to see a demo of the app.")
    st.video(demo_video_path)

    with st.sidebar:
        st.markdown('''
        <h2 style="background-color:white; color: black; padding: 5px; border-radius: 5px; margin-bottom: 10px;">Select Functionality</h2>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <style>
        div[role="radiogroup"] > :first-child {
            display: none !important;
        }
        </style>
        ''', unsafe_allow_html=True)

        selected_option = st.radio('Choose:', ('no option', 'Chatbot', 'Question & Answering'))

        add_vertical_space(3)
    

    if selected_option == 'Question & Answering':
        st.markdown(
        '''
  
        <div style="background-color: white; color: black; padding: 20px; border-radius: 10px;">
        <h2 style="color: black; font-weight: bold;">QA About</h2>
        <p>
        The Question & Answering over Document application built with LangChain API offers an efficient and intuitive way for users to extract information and gain insights from their document files. It combines the power of language models, \
        embedding techniques, and efficient search capabilities to deliver accurate and contextually relevant answers to user queries.
        </p>
        
        <h2 style="color: black; font-weight: bold;">Features</h2>
        <ol>
            <li><srong>File Upload</strong>: Users can upload document files in PDF, DOCX, or TXT format directly into the application.</li>
            <li><srong>Question Input</strong>: Users can enter their questions in natural language format within the application.</li>
            <li><srong>Answer Generation</strong>: The application utilizes the power of the OpenAI model to process the document content and generate accurate answers to the user's questions.</li>
            <li><srong>Contextual Understanding</strong>: The LangChain API incorporates OpenAI embedding to enable contextual understanding of the document content, enhancing the accuracy of the chat_generated answers.</li>
            <li><srong>Efficient Search</strong>: The application utilizes the Chroma vector store for indexing the document embeddings, enabling quick and efficient search for relevant information.</li>
        </ol>
        </div>
        ''',
        unsafe_allow_html=True
        )
        add_vertical_space(2)

        uploadbtn = st.sidebar.button("Upload Document")
 
        if uploadbtn or st.session_state.uploadbtn_state:
            st.session_state.uploadbtn_state = True
            uploaded_file = st.sidebar.file_uploader("Upload a file", type=["pdf", "txt", "docx"])
            MAX_FILE_SIZE_MB = 10

            if uploaded_file is not None:
                file_size = uploaded_file.size

                if file_size <= MAX_FILE_SIZE_MB * 1024 * 1024:

                    if st.session_state.extract_chunks:
                        with st.spinner('Extracting texts document...'):
                            document_chunks = preprocess_file(uploaded_file.name) # Valid file size, perform preprocessing #os.path.join(os.getcwd(), 'files', 
                            add_vertical_space(1)
                        st.session_state.extract_chunks = False
                        st.session_state['document_chunks'] = document_chunks
                        
                    if st.session_state.vector_store_index:
                        with st.spinner('Creating vector store...'):
                            vector_store = create_vector_store(st.session_state['document_chunks'])
                        
                        # store the embeddings in session state so we don't reload each time.
                        st.session_state.vector_store = vector_store
                        st.session_state.vector_store_index = False

                    
                    st.info("[INFO]   Indexed Embeddings to Chroma vectorstore.")
                    qa_bot = questionAnsweringWithDocument(st.session_state['vector_store'])   # querying bot
                    
                    colored_header(label='', description='', color_name='blue-30') # Layout of input/response containers
                    qa_response_container = st.container()
                    qa_input_container = st.container()

                    ## Applying the user input box
                    with qa_input_container:
                        query = get_text()
                        
                    with qa_response_container:
                        if query:
                            with st.spinner('processing query...'):
                                response = qa_bot({'question': query})
                            st.session_state.qa_past.append(query)
                            st.session_state.qa_generated.append(response['answer'])
                            
                        if st.session_state['qa_generated']:
                            for i in range(len(st.session_state['qa_generated'])):
                                message(st.session_state['qa_past'][i], is_user=True, key=str(i) + '_user')
                                message(st.session_state["qa_generated"][i], key=str(i))

                else:
                    st.warning(f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.")

    elif selected_option == 'Chatbot':
        st.markdown(
        '''
        <div style="background-color: white; color: black; padding: 20px; border-radius: 10px;">
        <h2 style="color: black; font-weight: bold;">About Conversation Bot:</h2>
        <p>The Conversation Bot is an advanced chatbot built using the LangChain API. It combines the power of the OpenAI model, agent capabilities, and external tools to provide users with a versatile conversational experience. With the ability to search the internet using Tools, the bot can retrieve up-to-date information for enhanced interactions.</p>

        <h2 style="color: black; font-weight: bold;">Features:</h2>
        <ol>
        <li>OpenAI Model: The bot utilizes the OpenAI model for generating responses, ensuring natural and contextually relevant conversations.</li>
        <li>Agent Capabilities: The bot is equipped with additional capabilities through agents. These agents enhance the bot's functionality, allowing it to perform tasks beyond basic conversation.</li>
        <li>Tool Integration: The bot leverages external tools, such as the SERP (Search Engine Results Page) API, to expand its capabilities. This integration enables the bot to search the internet and provide accurate answers based on current events or specific search queries.</li>
        <li>LangChain API: The bot's architecture is built using the LangChain API, which provides a comprehensive set of tools and utilities for developing advanced conversational applications.</li>
        </ol>
        </div>
        ''',
        unsafe_allow_html=True)
        add_vertical_space(2)

        colored_header(label='', description='', color_name='blue-30')
        response_container = st.container()
        input_container = st.container()

        with input_container:
            user_input = get_text()

        ## Conditional display of AI chat_generated responses as a function of user provided prompts
        conversation_agent = conversationChat()

        with response_container:
            if user_input:
                with st.spinner('processing query...'):
                    response = conversation_agent.run(input=user_input)
                st.session_state.chat_past.append(user_input)
                st.session_state.chat_generated.append(response)     
                
            if st.session_state['chat_generated']:
                for i in range(len(st.session_state['chat_generated'])):
                    message(st.session_state['chat_past'][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["chat_generated"][i], key=str(i))
        

if __name__ == "__main__":
    main()