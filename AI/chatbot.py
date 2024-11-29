from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub

def get_conversation_chain(vectorstore):
    """Set up the conversational retrieval chain."""
    llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5, "max_length": 512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def chat_interface(conversation_chain):
    """Interactive chat interface."""
    print("Chatbot is ready! Type 'exit' to end the conversation.")
    while True:
        user_question = input("\nYou: ")
        if user_question.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        response = conversation_chain({'question': user_question})
        print("\nBot:", response['answer'])
