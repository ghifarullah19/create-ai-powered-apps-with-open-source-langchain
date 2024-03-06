import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI 
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.utilities import PythonREPL

openai_api_key = "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"
os.environ["OPENAI_API_KEY"] = openai_api_key

gpt3 = ChatOpenAI(model_name='gpt-3.5-turbo')

# Equipting the agent with some tools
tools = load_tools([ "llm-math" ,"requests_all","human"], llm=gpt3)
tools.append(PythonREPLTool())

# Defining the agent
agent = initialize_agent(tools, llm=gpt3, agent="zero-shot-react-description", verbose=True)
result = agent.invoke("buatlah matplotlib sederhana yang menampilkan fungsi sin dan tampilkan plot nya")

print(result)