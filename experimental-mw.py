import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.tools import tool

#import the secret key to use the modle in the openai
load_dotenv()

#reconfigure the terminal to print properly all character in the terminal
sys.stdout.reconfigure(encoding='utf-8')

#create the conversation list
conversation = [
    "Hello, My name is Ayas",
    "I love Rajini movies",
    "Rajini movies like Jailer,Baasha,Muthu,Padayappa"
]

#create the agent
agent = create_agent(
    model = 'gpt-4o-mini',
    tools = [],
    system_prompt = "you are the supportive agent",
    middleware = [
        SummarizationMiddleware(
            model = 'gpt-4o-mini',
            trigger = ("message",6),
            keep = ("message",2)
        )
    ]
)

#Create the another list to store the conversation
message = []

#Now experiment how to stores the conversation in the list
for question in conversation:

    message.append({"role":"user","content":question})

    result = agent.invoke({"messages":message})

    message = result["messages"]





