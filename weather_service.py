import requests
import streamlit as st

class WeatherService:
    """
    Service to interact with OpenWeatherMap API
    """
    
    def __init__(self, api_key):
        """
        Initialize the WeatherService with the API key
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    # Use a non-static method with proper parameter names for caching to work
    @st.cache_data(ttl=600, show_spinner=False)  # Cache data for 10 minutes
    def get_current_weather(_self, city):
        """
        Get current weather for a city
        
        Args:
            city: City name
            
        Returns:
            dict: Current weather data
        """
        url = f"{_self.base_url}/weather"
        params = {
            "q": city,
            "appid": _self.api_key,
            "units": "metric",  # Use metric for Celsius
            "lang": "zh_tw"     # Use Traditional Chinese for weather descriptions
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get('message', '未知錯誤')
            raise Exception(f"API錯誤 ({response.status_code}): {error_msg}")
            
        return response.json()
    
    @st.cache_data(ttl=600, show_spinner=False)  # Cache data for 10 minutes
    def get_forecast(_self, city):
        """
        Get 5-day weather forecast for a city
        
        Args:
            city: City name
            
        Returns:
            dict: Forecast data
        """
        url = f"{_self.base_url}/forecast"
        params = {
            "q": city,
            "appid": _self.api_key,
            "units": "metric",  # Use metric for Celsius
            "lang": "zh_tw"     # Use Traditional Chinese for weather descriptions
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get('message', '未知錯誤')
            raise Exception(f"API錯誤 ({response.status_code}): {error_msg}")
            
        return response.json()

