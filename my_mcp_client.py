from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage

load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini")

history = [
    SystemMessage(content = "You are Teluko, a helpful coding agent"),
    HumanMessage(content = "Tell me today's date")
]

response = llm.invoke(history)

print(response)
print()
print(response.content)





