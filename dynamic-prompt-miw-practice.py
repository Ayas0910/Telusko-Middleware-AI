import sys
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt
from langchain_core.tools import tool

#First I load the secret key here
load_dotenv()

#I encode the terminal properly here
sys.stdout.reconfigure(encoding="utf-8")

#Now I create the dataclass for the customer which will help me to pass the information about the customer to the model
@dataclass
class Customer:
    """What we know about the person asking, before the model sees anything."""

    name: str
    membership: str
    language: str

#now I am going to create the tool here
@tool
def order_status(order_id: str)->str:
    """Get the status of an order and print it"""
    return f"{order_id.upper()}: packed, ships tomorrow"


#Creating the dynamic prompt middleware here
@dynamic_prompt
def support_prompt(request):

    customer = request.runtime.context

    Lines = [
        f"The customer name is {customer.name}.",
        "Never guess the delivery status, use the tool",
        "answer lika a short message",
        f"reply in {customer.language}"
    ]

    if customer.membership == "gold":
        Lines.append("Mention sorry for the delay and offer a callback.")
    elif customer.membership == "regular":
        Lines.append("Just answer in few sentence")

    prompt = " ".join(Lines)
    print(prompt)
    return prompt

#now I am going to create the agent here
agent = create_agent(
    model="gpt-4o-mini",
    tools=[order_status],
    middleware=[support_prompt],
    context_schema=Customer,
)

question = {
    "messages":[
        {
            "role":"user",
            "content":"where is my order FOOD-123"
        }
    ]
}
for customer in [
    Customer(name="Abideen",membership="gold",language="English"),
    Customer(name="Ayas",membership="regular",language="Tamil")
]:
    result = agent.invoke(question,context = customer)
    print(result["messages"][-1].content)



    