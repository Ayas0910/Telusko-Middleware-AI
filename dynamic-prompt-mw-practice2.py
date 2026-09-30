import sys
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt
from langchain_core.tools import tool

#import the secret key
load_dotenv()

#encode the terminal in utf-8
sys.stdout.reconfigure(encoding="utf-8")

#create the class to  store the customer data here
@dataclass
class Student:
    name: str
    standard: str
    bloodgroup: str

#Create the tool
@tool
def class_info(teacher_info:str)->str:
    """this tool is used by the llm to get the class teacher name"""
    return "your class teacher name is "

#create the dynamic prompt
@dynamic_prompt
def system_prompt(request):

    student = request.runtime.context

    Lines = [
        f"Your are the school bot",
        "you need to answer the question asked by the student",
        "you need to say the class teacher name for the particular standard",
        "You can add few more lines like greeting them and answer the question"
    ]

    if student.standard == "10":
        Lines.append("Your class teacher name is Janani. and add you need to study properly because you have board exams also")
    elif student.standard == "5":
        Lines.append("Your class teacher name is Ayas. He is one of the best teacher in the school.")

    prompt = " ".join(Lines)
    return prompt

#create the agent
agent = create_agent(
    model = "gpt-4o-mini",
    tools = [class_info],
    middleware = [system_prompt],
    context_schema= Student
)

question = {
    "messages":[
        {
            "role":"user",
            "content": "Who is my class teacher."
        }
    ]
}

for student in [
    Student(name= "abi", standard= "10", bloodgroup= "o+"),
    Student(name= "abib", standard= "5", bloodgroup= "o+"),
]:
    result = agent.invoke(question,context = student)
    print(result["messages"][-1].content)



