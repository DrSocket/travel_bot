from agency_swarm import Agent

from agent_service.SharedTools.get_time import TimeTool


class DashboardAgent(Agent):
    def __init__(self):
        super().__init__(
            name="DashboardAgent",
            description="This agent's primary function is to receive filtered travel options from the HotelAgent and FlightAgent, and display them effectively on the customer dashboard of the TravelOptionsHub agency. It ensures the data is presented in an engaging and user-friendly manner.",
            instructions="./dashboard_agent.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[TimeTool],
            tools_folder="",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        return message

