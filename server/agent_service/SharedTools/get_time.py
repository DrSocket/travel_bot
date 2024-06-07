
from datetime import datetime
from agency_swarm import BaseTool
from pydantic import BaseModel, Field

class TimeTool(BaseTool, BaseModel):
    """
    This tool is responsible for getting the current time.
    """
    def __init__(self):
        super().__init__(
            name="TimeTool",
            description="This tool is responsible for getting the current time.",
            instructions="Get's the current time.",
            files_folder="",
            schemas_folder="",
            temperature=0,
            max_prompt_tokens=25000,
        )

    def run(self):
        return self.get_time()

    def response_validator(self, message):
        return message

    def get_time(self):
        """
        This method gets the current time.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
