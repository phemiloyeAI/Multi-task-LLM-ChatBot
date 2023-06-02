import os
import streamlit as st

from langchain.chat_models import ChatOpenAI

from langchain.memory import ConversationBufferMemory

from langchain.agents import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY'] # openai_api_key
os.environ['SERPAPI_API_KEY'] = st.secrets['SERPAPI_API_KEY'] # serp_api_key


def conversationChat():
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name = "Current Search",
            func=search.run,
            description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
        ),
    ]

    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    return agent_chain 

# prompt = ChatPromptTemplate.from_messages([
# SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
# MessagesPlaceholder(variable_name="history"),
# HumanMessagePromptTemplate.from_template("{input}")
# # ])
# conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
#conversation
