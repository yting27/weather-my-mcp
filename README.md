
# Weather MCP Server

A basic Model Context Protocol (MCP) server that provides weather information retrieved from Open API of Malaysia's official open data portal.
This server enables LLMs to get weather forecast, warnings, water level associated with flood, and earthquake reports.

API Documentation: [data.gov.my](https://developer.data.gov.my/)

## Components

### Tools

1. get_water_level_condition
    - Retrieve the water level conditions associated with flood warnings for a specified district or state.
        If both district and state are provided, the district takes precedence.
        If district or state is not specified, use an empty string for that field.

    - Args:
        - district: The name of the district within the specified state for which to retrieve flood warning conditions.
        - state: The name of the state in Malaysia for which to retrieve flood warning conditions.

2. get_warning
    - Retrieve general weather warnings issued within a specified date range.

    - Args:
        - datetime_start: The earliest timestamp in the form of `YYYY-MM-DD HH:MM:SS` (inclusive) from which to retrieve weather warnings. If omitted, defaults to the current date.
        - datetime_end: The latest timestamp in the form of `YYYY-MM-DD HH:MM:SS` (inclusive) to stop retrieving the weather warnings. If omitted, defaults to the current date.

3. get_weather_forecast
    - Retrieve a weather forecast for a specific location within a given date range.

    - Args:
        - location_name: The name or identifier of the location for which the forecast is retrieved.
        - date_start: The earliest date (inclusive) to begin retrieving the weather forecast. If omitted, defaults to the current date.
        - date_end: The latest date (inclusive) to stop retrieving the weather forecast. If omitted, defaults to the current date.

4. get_earthquake_news
    - Fetch earthquake news for a given location within a specified date range.

    - Args:
        - location: Name or identifier of the place where the earthquake(s) occurred.
        - date_start: The earliest date (inclusive) to start searching for earthquake news. If omitted, defaults to the current date.
        - date_end: The latest date (inclusive) to stop searching for earthquake news. If omitted, defaults to the current date.

## Claude Desktop configuration

Add the following into `claude_desktop_config.json` file. For more information, refer to [For Claude Desktop Users](https://modelcontextprotocol.io/quickstart/user).

```json
{
    "mcpServers": {
        "weather": {
            "command": "uv",
            "args": [
                "--directory",
                "weather-my-mcp",
                "run",
                "weather.py"
            ]
        }
    }
}
```

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
