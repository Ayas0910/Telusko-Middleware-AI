import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool

#encoding
sys.stdout.reconfigure(encoding="utf-8")

#load the api key
load_dotenv()

#create the tool here

@tool
def order_id(order_id: str)->str:
    """"Get the status of the order using its ID"""
    return f"{order_id.upper()} packed and shiped tomorrow"

