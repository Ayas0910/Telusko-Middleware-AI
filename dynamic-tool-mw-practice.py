import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
from langchain_core.tools import tool

#I import the secret key
load_dotenv()

#I reconfigure the terminal to print properly
sys.stdout.reconfigure(encoding='utf-8')

#I create the 5 tools here
@tool
def box_office_1(commercial:str)->str:
    """This tool is commercial movie from rajini kanth"""
    return f"{commercial} he is the first priority and you can you Rajini movies like padayappa, baasha."

@tool
def box_office_2(commercial:str)->str:
    """This tool is commercial movie from Kamal haasan"""
    return f"{commercial} he is the first priority and you can you Kamal movies like Dasavatharam, Vikram."

@tool
def box_office_3(feel_good:str)->str:
    """This tool is feel good  movie from suriya"""
    return f"{feel_good} he is the first priority and you can you Suriya movies like VAS, Ayan."

@tool
def box_office_4(feel_good:str)->str:
    """This tool is feel good  movie from ajith"""
    return f"{feel_good} he is the first priority and you can you Ajith movies like Kadhal kootai."

@tool
def box_office_5(feel_good:str)->str:
    """This tool is feel good  movie from nivin pauly"""
    return f"{feel_good} he is the first priority and you can you Nivin pauly movies like BKU"

COMMERCIAL_HERO = [
    box_office_1,box_office_2
]

FEEL_GOOD_HERO = [
    box_office_3,box_office_4,box_office_5
]

#words for choose the tool
HERO_WORD = (
    "feel good movie",
    "romantic movie",
    "rom-com movie"
)

def latest_question(messages):

    for message in reversed(messages):
        if type(message).__name__ == "HumanMessage":
            return str(message.content).lower()
    return ""

#middleware or tool call
@wrap_model_call
def pick_tool(request,handler):

    question = latest_question(request.messages)

    if any(word in question for word in HERO_WORD):

        request = request.override(
            tools = FEEL_GOOD_HERO
        )

    else:

        request = request.override(
                    tools = COMMERCIAL_HERO
                )

    print("offered: ",
          [t.name for t in request.tools])

    return handler(request)

#I create one agent
agent = create_agent(
    model="gpt-4o-mini",
    tools=[box_office_1,box_office_2,box_office_3,box_office_4,box_office_5],
    middleware=[pick_tool],
    system_prompt="You are the support agent.Use the tools don't guess and greet the user."
)

#ask question
def ask(question):
    print("Q: ",question)
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
    print("-"*80)


ask("I want to watch one feel good movie can you recommend any movie your choice")




