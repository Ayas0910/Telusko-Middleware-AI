import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware
from langchain_core.tools import tool

#load the secret key
load_dotenv()

#reconfigure the terminal
sys.stdout.reconfigure(encoding='utf-8')

attempt = {"count":0}

#create the tool
@tool
def order_status(order_id:str)->str:
    """Get the status of an order using its id"""

    attempt["count"]+=1

    print(f"{attempt['count']} to reach the order status")

    if attempt["count"] < 3:
        raise RuntimeError("order service unavailable")

    return f"{order_id.upper()} packed and shiped tomorrow"


#create the agent
agent = create_agent(
    model = 'gpt-4o-mini',
    tools=[order_status],
    middleware = [ToolRetryMiddleware(
        max_retries = 5,
        initial_delay = 0.2,
        backoff_factor = 5
    )],
    system_prompt = "you are the support agent. look up the order before offering"
)

#helper function
def ask(question):

    result = agent.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content": question
                }
            ]
        }
    )

    print(result["messages"][-1].content)

question = input("ask question related to the order status? ")

ask(question)