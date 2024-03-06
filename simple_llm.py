import os
from langchain_openai import ChatOpenAI
import gradio as gr

# Mengatur environment variable "OPENAI_API_KEY" dengan OpenAI API key milikmu. ini diperlukan untuk proses autentikasi ke OpenAI API.
os.environ["OPENAI_API_KEY"] = "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"

# Mendefinisikan jenis model 
gpt3 = ChatOpenAI(model_name="gpt-3.5-turbo" )
# text = "Berikan fakta menarik tentang kentang!"
# print(gpt3.invoke(text).content)

def chatbot(prompt):
    return gpt3.invoke(prompt).content

demo = gr.Interface(fn=chatbot, inputs="text", outputs="text")
demo.launch(server_name="0.0.0.0", server_port= 7860, share=True)