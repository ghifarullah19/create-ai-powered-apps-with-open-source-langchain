from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
import wget
import os
import gradio as gr
import pysqlite3
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# mengakses ke dokumen
url = "https://raw.githubusercontent.com/Ichsan-Takwa/Generative-AI-Labs/main/Pembukaan_UUD_1945"
output_path = "pembukaanUUD1945.txt"  # nama file lokal

# Mengecek jika file sudah ada
if not os.path.exists(output_path):
    # mengunduh file menggunakan wget
    wget.download(url, out=output_path)

loader = TextLoader('pembukaanUUD1945.txt')

openai_api_key = "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"
os.environ["OPENAI_API_KEY"] = openai_api_key

# mengakses data
data = loader.load()

# Membuat instance untuk mencari data
index = VectorstoreIndexCreator().from_loaders([loader])

# Menjalankan gradio
def summarize(query):
    return index.query(query)

iface = gr.Interface(fn=summarize, inputs="text", outputs="text")
iface.launch(server_name="0.0.0.0", server_port= 7860, share=True)