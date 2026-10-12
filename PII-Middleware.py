import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMatch,PIIMiddleware,PIIDetectionError

#import the secret key
load_dotenv()

#reconfigure the terminal to print the string properly
sys.stdout.reconfigure(encoding='utf-8')

#create the agent
agent = create_agent(
    model = "gpt-4o-mini",
    tools = [],
    system_prompt = "you are the supportive agent for the online store",
    middleware = [
        PIIMiddleware("email",strategy="redact"),
        PIIMiddleware("credit_card",strategy="block")
    ]
)

#invoke the agent
try:
    result = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":"My name is Ayas. and my phone number is 9999999999. and my emial is hello@gmail.com and my "
                "credit card number is 1111-2222-3333-4444 you know my name"
            }
        ]
    })
except PIIDetectionError:
    print("Please dont write the credit card number")

