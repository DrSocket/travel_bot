from agency_swarm import Agency, Agent, BaseTool
from instructor import llm_validator
from agent_service.HotelAgent.tools.BookingTool import BookingTool
from agent_service.SharedTools.get_time import TimeTool
from agent_service.SharedTools.vector_tool import VectorTool

class HotelAgent(Agent):
    def __init__(self):
        super().__init__(
            name="HotelAgent",
            description="This agent is responsible for providing hotel options to the DashboardAgent based on the customer's preferences and budget. It ensures that the hotel options are filtered and sorted according to the customer's requirements.",
            instructions="./hotel_agent.md",
            files_folder="",
            schemas_folder="",
            tools=[BookingTool, TimeTool, VectorTool],
            tools_folder="",
            temperature=0.2,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        try:
            # message = llm_validator(message)
            return message
        except Exception as e:
            return f"An error occurred: {str(e)}"
