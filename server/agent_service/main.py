# %%
import os
from dotenv import load_dotenv
from agent_service.DashboardAgent.DashboardAgent import DashboardAgent
from agent_service.HotelAgent.HotelAgent import HotelAgent
from agent_service.FlightAgent.FlightAgent import FlightAgent

load_dotenv()
from agency_swarm import set_openai_key
set_openai_key(os.getenv("OPENAI_API_KEY"))
RAPID_KEY = "e6a9c0777cmsh786946f3c98e21ep1dc15cjsn237e1c3abf88"
from agency_swarm import Agency, Agent, BaseTool
import requests

# %%

dashboardAgent = DashboardAgent()
hotelAgent = HotelAgent()
flightAgent = FlightAgent()


agency = Agency(
        [dashboardAgent, flightAgent, hotelAgent, [dashboardAgent, hotelAgent],
        [dashboardAgent, flightAgent]
    ],
        shared_instructions='./agency_manifesto.md', # shared instructions for all agents
        max_prompt_tokens=20000, # default tokens in conversation for all agents
        temperature=0.2, # default temperature for all agents
    )


def createAgency():
    dashboardAgent = DashboardAgent()
    hotelAgent = HotelAgent()
    flightAgent = FlightAgent()
    agency = Agency(
        [dashboardAgent, flightAgent, hotelAgent, [dashboardAgent, hotelAgent],
        [dashboardAgent, flightAgent]],
        shared_instructions='./agency_manifesto.md', # shared instructions for all agents
        max_prompt_tokens=2048, # default tokens in conversation for all agents
        temperature=0.2, # default temperature for all agents

    )
    return agency

# agency.run_demo()
# agency.demo_gradio()

#i want to book a hotel in madrid next weekend from friday to sunday for 2-300 usd
