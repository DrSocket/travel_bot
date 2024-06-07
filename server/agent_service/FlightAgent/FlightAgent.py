from agency_swarm import Agency, Agent, BaseTool


class FlightAgent(Agent):
    def __init__(self):
        super().__init__(
            name="FlightAgent",
            description="This agent is responsible for providing flight options to the DashboardAgent based on the customer's preferences and budget. It ensures that the flight options are filtered and sorted according to the customer's requirements.",
            instructions="./flight_agent.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        return message