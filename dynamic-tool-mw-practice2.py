import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
from langchain_core.tools import tool

#import the secret key
load_dotenv()

#reconfigure the terminal
sys.stdout.reconfigure(encoding='utf-8')

#create the necessary tools
@tool
def commercial(mass:str)->str:
    """Here if someone ask the mass movies then use this tool"""
    return f"This is the best commercial mass movie we have right now baasha one of the best by rajini"

@tool
def non_commercial(non:str)->str:
    """Use this function for the non commercial movies"""
    return f"This is one of the best non commercial movies by kamal sir nayakan"

COMM_TOOL = [commercial]

NON_COMM_TOOL = [non_commercial]

COMMERCIAL_WORDS = (
    "mass",
    "rajini",
    "kind",
    "commercial"
)

#take the last question asked by the user
def latest_question(messages):

    for message in reversed(messages):
        if type(message).__name__ == "HumanMessage":
            return str(message.content).lower()

    return ""

#create the hook or middleware
@wrap_model_call
def pick_tool(request,handler):

    question = latest_question(request.messages)

    if any(word in COMMERCIAL_WORDS for word in question):

        request = request.override(
            tools = COMM_TOOL
        )

    else:

        request = request.override(
            tools = NON_COMM_TOOL
        )

    return handler(request)

#create agent
agent = create_agent(
    model = "gpt-4o-mini",
    tools = [commercial,non_commercial],
    middleware = [pick_tool],
    system_prompt = "you are a supportive agent.dont guess use the tools to answer the question"
)

#helper function
def ask(question):
    result = agent.invoke(
        {
            "messages":[
                {
                    "role":"user",
                    "content":question
                }
            ]
        }
    )

    print(result["messages"][-1].content)
    print("-"*100)


while(True):
    question = input("Enter the question: ")
    ask(question)

