
import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun   
from datetime import datetime

#for brightness
#import screen_brightness_control as sbc
#import logging


@function_tool()
async def get_weather(context: RunContext, city: str) -> str:
    """
    Get the current weather for a given city.
    Uses wttr.in for simple text-based weather info.
    """
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            weather_info = response.text.strip()
            logging.info(f"Weather for {city}: {weather_info}")
            return weather_info
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."



@function_tool()
async def search_web(context: RunContext, query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        search = DuckDuckGoSearchRun()
        results = search.run(tool_input=query)
        short_results = results[:1000]  # Prevents overly long logs
        logging.info(f"Search results for '{query}': {short_results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."



#@function_tool()
#async def set_brightness(context: RunContext, level: int) -> str:
  #  """
  #  Set screen brightness to a specific percentage (0–100).
   # """
   # try:
   #     if not 0 <= level <= 100:
   #         return "Brightness level must be between 0 and 100."

     #   sbc.set_brightness(level)

     #   logging.info(f"Screen brightness set to {level}%")
      #  return f"Brightness set to {level}%."

   # except Exception as e:
   #     logging.error(f"Error setting brightness: {e}")
   #     return "An error occurred while setting brightness."


