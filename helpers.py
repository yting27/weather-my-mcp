import httpx
from typing import Any
from datetime import datetime


def format_weather(weather_res: dict) -> str:
    """Format a weather json response into a readable string."""
    location = weather_res["location"]
    return f"""
Location ID: {location.get('location_id', 'Unknown')}
Location Name: {location.get('location_name', 'Unknown')}
Date: {weather_res.get('date', 'Unknown')}
Morning Forecast: {weather_res.get('morning_forecast', 'Unknown')}
Afternoon Forecast: {weather_res.get('afternoon_forecast', 'Unknown')}
Night Forecast: {weather_res.get('night_forecast', 'Unknown')}
Minimum Temperature: {weather_res.get('min_temp', 'Unknown')}
Maximum Temperature: {weather_res.get('max_temp', 'Unknown')}
"""

def format_warning(warning_res: dict) -> str:
    """Format a warning json response into a readable string."""
    warning_issue = warning_res["warning_issue"]
    return f"""
Warning Issue Date: {warning_issue.get('issued', 'Unknown')}
Title: {warning_issue.get('title_en', 'Unknown')}
Is Valid From: {warning_res.get('valid_from', 'Unknown')}
Is Valid To: {warning_res.get('valid_to', 'Unknown')}
Heading: {warning_res.get('heading_en', 'Unknown')}
Details: {warning_res.get('text_en', 'Unknown')}
Instruction: {warning_res.get('instruction_en', 'Unknown')}
"""

def format_earthquake_data(earthquake_res: dict) -> str:
    """Format an earthquake news into a readable string."""
    return f"""
UTC Datetime: {earthquake_res.get('utcdatetime', 'Unknown')}
Local Datetime: {earthquake_res.get('localdatetime', 'Unknown')}
Latitude: {earthquake_res.get('lat', 'Unknown')}
Longitude: {earthquake_res.get('lon', 'Unknown')}
Depth: {earthquake_res.get('depth', 'Unknown')}
Location: {earthquake_res.get('location', 'Unknown')}
Default Magnitude: {earthquake_res.get('magdefault', 'Unknown')}
Default Magnitude Type: {earthquake_res.get('magtypedefault', 'Unknown')}
Status: {earthquake_res.get('status', 'Unknown')}
Distance/direction to a Malaysian location: {earthquake_res.get('n_distancemas', 'Unknown')}
Distance/direction to a non-Malaysian location: {earthquake_res.get('n_distancerest', 'Unknown')}
"""

def format_water_level(water_level_res: dict) -> str:
    """Format water level and rainfail data into a readable string."""
    return f"""
Monitoring Station ID: {water_level_res.get('station_id', 'Unknown')}
Monitoring Station Name: {water_level_res.get('station_name', 'Unknown')}
Latitude: {water_level_res.get('latitude', 'Unknown')}
Longitude: {water_level_res.get('longitude', 'Unknown')}
District: {water_level_res.get('district', 'Unknown')}
State: {water_level_res.get('state', 'Unknown')}
Sub-basin: {water_level_res.get('sub_basin', 'Unknown')}
Main River Basin: {water_level_res.get('main_basin', 'Unknown')}
Current Water Level: {water_level_res.get('water_level_current', 'Unknown')}
Current Water Level Indicator: {water_level_res.get('water_level_indicator', 'Unknown')}
Current Water Level Increment: {water_level_res.get('water_level_increment', 'Unknown')}
Current Water Level Trend (rising, falling, or steady): {water_level_res.get('water_level_trend', 'Unknown')}
Water Level - Normal (Reference): {water_level_res.get('water_level_normal_level', 'Unknown')}
Water Level - Alert (Reference): {water_level_res.get('water_level_alert_level', 'Unknown')}
Water Level - Warning (Reference): {water_level_res.get('water_level_warning_level', 'Unknown')}
Water Level - Danger (Reference): {water_level_res.get('water_level_danger_level', 'Unknown')}
Current Water Level Updated Datetime: {water_level_res.get('water_level_update_datetime', 'Unknown')}
Clean Rainfall: {water_level_res.get('rainfall_clean', 'Unknown')}
Latest 1 Hour Rainfall: {water_level_res.get('rainfall_latest_1hr', 'Unknown')}
Total Rainfall Today: {water_level_res.get('rainfall_total_today', 'Unknown')}
Rainfall Indicator: {water_level_res.get('rainfall_indicator', 'Unknown')}
Rainfall Updated Datetime: {water_level_res.get('rainfall_update_datetime', 'Unknown')}
"""

async def make_api_request(url: str, params: dict[str, str]) -> dict[str, Any] | None:
    """Make a request to the Malaysia Government API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0, follow_redirects=True)
            print(response)
            response.raise_for_status()
            return response.json()
        except Exception as ex:
            return None

def validate_date(date_text: str) -> bool:
    """Validate date string format."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_datetime(datetime_text: str) -> bool:
    """Validate date string format."""
    try:
        datetime.strptime(datetime_text, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def current_date() -> str:
    """Get current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")
