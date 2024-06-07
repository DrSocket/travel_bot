from math import log
import os
from venv import logger
from dotenv import load_dotenv
import requests
from agency_swarm import Agency, Agent, BaseTool
load_dotenv()
from agency_swarm import set_openai_key
set_openai_key(os.getenv("OPENAI_API_KEY"))
RAPID_KEY = "e6a9c0777cmsh786946f3c98e21ep1dc15cjsn237e1c3abf88"
from typing import Optional
import requests
import logging
from typing import Optional
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class BookingTool(BaseTool, BaseModel):
    """
    This tool is responsible for searching for hotels.
    """
    location_name: Optional[str] = Field(default=None, title="Location Name")
    checkout_date: Optional[str] = Field(default=None, title="Checkout Date")
    order_by: str = Field(default="popularity", title="Order By")
    filter_by_currency: str = Field(default="EUR", title="Currency")
    room_number: int = Field(default=1, title="Room Number")
    dest_id: Optional[int] = Field(default=None, title="Destination ID")
    dest_type: str = Field(default="city", title="Destination Type")
    adults_number: int = Field(default=1, title="Number of Adults")
    checkin_date: Optional[str] = Field(default=None, title="Checkin Date")
    locale: str = Field(default="en-gb", title="Locale")
    units: str = Field(default="metric", title="Units of Measurement")
    include_adjacency: bool = Field(default=True, title="Include Adjacency")
    children_number: Optional[int] = Field(default=None, title="Number of Children")
    categories_filter_ids: Optional[str] = Field(default=None, title="Categories Filter IDs")
    page_number: int = Field(default=0, title="Page Number")
    children_ages: Optional[str] = Field(default=None, title="Children Ages")

    def run(self):
        """Executes the main functionality: searches for hotels."""
        loc = self.search_location(self.location_name)
        dest_id = loc[0]["dest_id"] if loc and isinstance(loc, list) and len(loc) > 0 else None
        if not dest_id:
            logger.error("Destination ID could not be found.")
            return []

        hotels = self.search_hotels(dest_id=dest_id)
        # with open ("hotels.json", "w") as f:
        #     f.write(hotels)
        logger.info(f"Found {len(hotels['result'])} hotels.")
        return hotels['result']

    def search_location(self, location_name: str):
        """Search for the location ID based on the location name."""
        url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
        querystring = {"name": location_name, "locale": self.locale}
        headers = {
            "X-RapidAPI-Key": RAPID_KEY,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()

    def search_hotels(self, dest_id: int):
        """
        Search for hotels based on the destination ID and other provided parameters.
        """
        url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
        querystring = dict(
            dest_id=dest_id,
            dest_type=self.dest_type,
            adults_number=self.adults_number,
            room_number=self.room_number,
            order_by=self.order_by,
            filter_by_currency=self.filter_by_currency,
            checkin_date=self.checkin_date,
            checkout_date=self.checkout_date,
            children_number=self.children_number if self.children_number and self.children_number > 0 else None,  # Adjusting children number condition
            children_ages=self.children_ages,
            locale=self.locale,
            units=self.units,
            include_adjacency=self.include_adjacency,
            categories_filter_ids=self.categories_filter_ids,
            page_number=self.page_number
        )
        # Filter out None values
        querystring = {key: value for key, value in querystring.items() if value is not None}

        headers = {
            "X-RapidAPI-Key": RAPID_KEY,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        # with open("response.json", "w") as f:
        #     f.write(response.text)
        return response.json()

# if __name__ == "__main__":
#     tool = BookingTool(
#         location_name="Paris",  # Example parameter
#         checkin_date="2024-12-20",
#         checkout_date="2024-12-25",
#         room_number=2,
#         adults_number=2,
#     )
#     result = tool.run()
#     print(result)