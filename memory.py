# Import library yang diperlukan
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory, CombinedMemory, ConversationSummaryMemory
import os
import gradio as gr
import time

# Mengatur API key
openai_api_key = "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"  # Ganti dengan API key kamu
os.environ["OPENAI_API_KEY"] = openai_api_key

# Mengatur memori percakapan
# Memori ini akan menyimpan k banyak percakapan
conv_memory = ConversationBufferWindowMemory(
    memory_key="chat_history_lines",
    input_key="input",
    k=1
)

# Memori ini akan menyimpan rangkuman dari percakapan
summary_memory = ConversationSummaryMemory(llm=ChatOpenAI(), input_key="input")

# Menggabungkan dua memori
memory = CombinedMemory(memories=[conv_memory, summary_memory])

# Mendefinisikan template untuk prompt percakapan
_DEFAULT_TEMPLATE = """Berikut percakapan persahabatan antara manusia dan AI. AI ini banyak bicara dan memberikan banyak detail spesifik dari konteksnya. Jika AI tidak mengetahui jawaban atas sebuah pertanyaan, AI dengan jujur mengatakan bahwa ia tidak mengetahuinya.
Ringkasan percakapan:
{history}
Percakapan saat ini:
{chat_history_lines}
Manusia: {input}
AI:"""

# Create the prompt from the template
PROMPT = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"], template=_DEFAULT_TEMPLATE
)

# Set up the language model
llm = ChatOpenAI(temperature=0)

# Set up the conversation chain
# This object will handle the conversation flow
conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=memory,
    prompt=PROMPT
)

# Set up the Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()  # The chatbot object
    msg = gr.Textbox(label="pesan")  # The textbox for user input
    clear = gr.Button("Clear")  # The button to clear the chatbox
    
    # Define the function that will handle user input and generate the bot's response
    def respond(message, chat_history):
        bot_message = conversation.run(message)  # Run the user's message through the conversation chain
        chat_history.append((message, bot_message))  # Append the user's message and the bot's response to the chat history
        time.sleep(1)  # Pause for a moment
        return "", chat_history  # Return the updated chat history
    
    # Connect the respond function to the textbox and chatbot
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    
    # Connect the "Clear" button to the chatbot
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(server_name="0.0.0.0", server_port= 7860, share=True)