def get_weather_icon(weather_condition):
    """
    Get emoji icon based on weather condition
    
    Args:
        weather_condition: Weather condition string from API
        
    Returns:
        str: Emoji icon representing the weather condition
    """
    weather_icons = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Smoke': '🌫️',
        'Haze': '🌫️',
        'Dust': '🌫️',
        'Fog': '🌫️',
        'Sand': '🌫️',
        'Ash': '🌫️',
        'Squall': '💨',
        'Tornado': '🌪️'
    }
    
    return weather_icons.get(weather_condition, '❓')

def get_weather_color(weather_condition):
    """
    Get color based on weather condition
    
    Args:
        weather_condition: Weather condition string from API
        
    Returns:
        str: Hex color code representing the weather condition
    """
    weather_colors = {
        'Clear': '#FFD700',      # Gold
        'Clouds': '#A9A9A9',     # Dark Gray
        'Rain': '#4682B4',       # Steel Blue
        'Drizzle': '#87CEEB',    # Sky Blue
        'Thunderstorm': '#483D8B', # Dark Slate Blue
        'Snow': '#E0FFFF',       # Light Cyan
        'Mist': '#D3D3D3',       # Light Gray
        'Smoke': '#C0C0C0',      # Silver
        'Haze': '#F0E68C',       # Khaki
        'Dust': '#BDB76B',       # Dark Khaki
        'Fog': '#D3D3D3',        # Light Gray
        'Sand': '#F4A460',       # Sandy Brown
        'Ash': '#A9A9A9',        # Dark Gray
        'Squall': '#778899',     # Light Slate Gray
        'Tornado': '#800000'     # Maroon
    }
    
    return weather_colors.get(weather_condition, '#808080')  # Default: Gray

def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit
    
    Args:
        celsius: Temperature in Celsius
        
    Returns:
        float: Temperature in Fahrenheit
    """
    return (celsius * 9/5) + 32

