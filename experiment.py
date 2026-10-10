import sys
from dotenv import load_dotenv
from langchain.agents import create_agent

#import the secret key
load_dotenv()

#reconfigure the terminal to print the string properly
sys.stdout.reconfigure(encoding = 'utf-8')

#create the agent
agent = create_agent(
    model = "gpt-4o-mini",
    system_prompt = "greet the user."
)

#create the first request 
result = agent.invoke({
    "mesages":[
        {
            "role":"user",
            "content":"Hello World"
        }
    ]
})

print(result["messages"])
