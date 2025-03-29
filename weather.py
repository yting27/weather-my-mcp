from mcp.server.fastmcp import FastMCP
from constants import *
from helpers import *


# Initialize FastMCP server
mcp = FastMCP("weather-server")

@mcp.tool()
async def get_water_level_condition(district: str = "", state: str = "") -> str:
    """Retrieve the water level conditions associated with flood warnings for a specified district or state.
    If both district and state are provided, the district takes precedence.
    If district or state is not specified, use an empty string for that field.

    Args:
        district: The name of the district within the specified state for which to retrieve flood warning conditions.
        state: The name of the state in Malaysia for which to retrieve flood warning conditions.
    """

    contain_str = ""
    district = district.strip()
    state = state.strip()
    if district:
        contain_str = f"{district}@district"
    elif state:
        contain_str = f"{state}@state"

    water_level_url = f"{GOV_API_BASE}/flood-warning"
    water_level_data = await make_api_request(water_level_url, {
                                            "meta": "true",
                                            "sort": "-water_level_update_datetime,-rainfall_update_datetime",
                                            "icontains": contain_str,
                                            "filter": "ON@water_level_status",
                                            "limit": 20
                                        })

    if not water_level_data or "data" not in water_level_data:
        return "Unable to fetch water level data for this state or district."

    if not water_level_data["data"]:
        return "No active water level data for this state or district."

    water_levels = [format_water_level(warn) for warn in water_level_data["data"]]
    return "\n---\n".join(water_levels)

@mcp.tool()
async def get_warning(datetime_start: str = None, datetime_end: str = None) -> str:
    """Retrieve general weather warnings issued within a specified date range.

    Args:
        datetime_start: The earliest timestamp in the form of <YYYY-MM-DD HH:mm:ss> (inclusive) from which to retrieve weather warnings. If omitted, defaults to the current date.
        datetime_end: The latest timestamp in the form of <YYYY-MM-DD HH:mm:ss> (inclusive) to stop retrieving the weather warnings. If omitted, defaults to the current date.
    """
    if not datetime_start:
        datetime_start = current_date() + " 00:00:01"
    elif not validate_datetime(datetime_start):
        return "Wrong `datetime_start` format given. Accepted format is 'YYYY-MM-DD HH:mm:ss'."

    if not datetime_end:
        datetime_end = current_date() + " 23:59:59"
    elif not validate_datetime(datetime_end):
        return "Wrong `datetime_end` format given. Accepted format is 'YYYY-MM-DD HH:mm:ss'."

    warning_url = f"{GOV_API_BASE}/weather/warning"
    warning_data = await make_api_request(warning_url, {
                                            "meta": "true",
                                            "sort": "-warning_issue__issued",
                                            "timestamp_start": f"{datetime_start}@warning_issue__issued",
                                            "timestamp_end": f"{datetime_end}@warning_issue__issued",
                                        })

    if not warning_data or "data" not in warning_data:
        return "Unable to fetch warning data for this time period."

    if not warning_data["data"]:
        return "No active warning data for this time period."

    warnings = [format_warning(warn) for warn in warning_data["data"]]
    return "\n---\n".join(warnings)

@mcp.tool()
async def get_weather_forecast(location_name: str, date_start: str = None, date_end: str = None) -> str:
    """Retrieve a weather forecast for a specific location within a given date range.

    Args:
        location_name: The name or identifier of the location for which the forecast is retrieved.
        date_start: The earliest date (inclusive) to begin retrieving the weather forecast. If omitted, defaults to the current date.
        date_end: The latest date (inclusive) to stop retrieving the weather forecast. If omitted, defaults to the current date.
    """
    if not date_start:
        date_start = current_date()
    elif not validate_date(date_start):
        return "Wrong `date_start` format given. Accepted format is 'YYYY-MM-DD'."

    if not date_end:
        date_end = current_date()
    elif not validate_date(date_end):
        return "Wrong `date_end` format given. Accepted format is 'YYYY-MM-DD'."

    forecast_url = f"{GOV_API_BASE}/weather/forecast"
    forecast_data = await make_api_request(forecast_url, {
                                            "meta": "true",
                                            "sort": "-date",
                                            "icontains": f"{location_name}@location__location_name",
                                            "date_start": f"{date_start}@date",
                                            "date_end": f"{date_end}@date",
                                        })

    if not forecast_data or "data" not in forecast_data:
        return "Unable to fetch weather forecast data for this location."

    if not forecast_data["data"]:
        return "No active weather forecast data for this time period."

    forecasts = [format_weather(forecast) for forecast in forecast_data["data"]]
    return "\n---\n".join(forecasts)

@mcp.tool()
async def get_earthquake_news(location: str, datetime_start: str = None, datetime_end: str = None) -> str:
    """Fetch earthquake news for a given location within a specified date range.

    Args:
        location: Name or identifier of the place where the earthquake(s) occurred.
        date_start: The earliest timestamp in the form of <YYYY-MM-DD HH:mm:ss> (inclusive) to start searching for earthquake news. If omitted, defaults to the current date.
        date_end: The latest timestamp in the form of <YYYY-MM-DD HH:mm:ss> (inclusive) to stop searching for earthquake news. If omitted, defaults to the current date.
    """
    if not datetime_start:
        datetime_start = current_date() + " 00:00:01"
    elif not validate_datetime(datetime_start):
        return "Wrong `datetime_start` format given. Accepted format is 'YYYY-MM-DD HH:mm:ss'."

    if not datetime_end:
        datetime_end = current_date() + " 23:59:59"
    elif not validate_datetime(datetime_end):
        return "Wrong `datetime_end` format given. Accepted format is 'YYYY-MM-DD HH:mm:ss'."

    earthquake_url = f"{GOV_API_BASE}/weather/warning/earthquake"
    data = await make_api_request(earthquake_url, {
                                    "meta": "true",
                                    "sort": "-utcdatetime",
                                    "timestamp_start": f"{datetime_start}@utcdatetime",
                                    "timestamp_end": f"{datetime_end}@utcdatetime",
                                    "icontains": f"{location}@location"
                                })

    if not data or "data" not in data:
        return "Unable to fetch earthquake news or no earthquake news found."

    if not data["data"]:
        return "No active earthquake news for this location."

    earthquakes = [format_earthquake_data(earthquake_desc) for earthquake_desc in data["data"]]
    return "\n---\n".join(earthquakes)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')