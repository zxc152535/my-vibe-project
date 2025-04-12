import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from weather_service import WeatherService
from utils import get_weather_icon, get_weather_color, celsius_to_fahrenheit

# Set page configuration
st.set_page_config(
    page_title="IAN的天氣預報應用",
    page_icon="🌤️",
    layout="wide"
)

password = st.text_input("請輸入密碼進入系統", type="password")
if password != "12345":
    st.warning("密碼錯誤或尚未輸入，請聯絡作者")
    st.stop()

# Initialize weather service
api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
if not api_key:
    st.error("未設置API密鑰。請設置OPENWEATHERMAP_API_KEY環境變量。")
    st.stop()

weather_service = WeatherService(api_key)

# App title
st.title("🌤️ IAN 的天氣預報應用")

# Sidebar for city search
with st.sidebar:
    st.header("搜尋城市")
    city_name = st.text_input("輸入城市名稱", "Taipei")
    search_button = st.button("搜尋")
    
    # Unit selection
    st.header("設置")
    temperature_unit = st.radio("溫度單位", ["攝氏 (°C)", "華氏 (°F)"], index=0)
    is_celsius = temperature_unit.startswith("攝氏")
    
    # About section
    st.header("關於")
    st.info(
        "這個應用程式由 IAN 開發，使用OpenWeatherMap API獲取天氣數據。"
        "它提供實時天氣信息和五天預報。"
    )

# Main content
if search_button or 'city_name' not in st.session_state:
    st.session_state.city_name = city_name

try:
    # Display spinner while fetching data
    with st.spinner("獲取天氣資料中..."):
        # Get current weather
        current_weather = weather_service.get_current_weather(st.session_state.city_name)
        
        # Get 5-day forecast
        forecast = weather_service.get_forecast(st.session_state.city_name)
    
    # Current Weather Section
    st.header(f"📍 {current_weather['name']}, {current_weather['sys']['country']} 的當前天氣")
    
    # Format current time
    current_time = datetime.fromtimestamp(current_weather['dt'])
    st.subheader(f"⏰ 更新時間: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Create columns for current weather display
    col1, col2, col3 = st.columns(3)
    
    # Temperature data
    temp_c = current_weather['main']['temp']
    temp_f = celsius_to_fahrenheit(temp_c)
    feels_like_c = current_weather['main']['feels_like']
    feels_like_f = celsius_to_fahrenheit(feels_like_c)
    
    # Display temperature based on unit selection
    if is_celsius:
        temp_display = f"{temp_c:.1f} °C"
        feels_like_display = f"{feels_like_c:.1f} °C"
    else:
        temp_display = f"{temp_f:.1f} °F"
        feels_like_display = f"{feels_like_f:.1f} °F"
    
    # Weather description and icon
    weather_desc = current_weather['weather'][0]['description']
    weather_main = current_weather['weather'][0]['main']
    weather_icon_emoji = get_weather_icon(weather_main)
    
    with col1:
        st.markdown(f"### {weather_icon_emoji} {weather_desc.capitalize()}")
        st.markdown(f"### 溫度: {temp_display}")
        st.markdown(f"體感溫度: {feels_like_display}")
    
    with col2:
        st.markdown(f"### 濕度: {current_weather['main']['humidity']}%")
        st.markdown(f"### 氣壓: {current_weather['main']['pressure']} hPa")
        
    with col3:
        wind_speed = current_weather['wind']['speed']
        wind_deg = current_weather.get('wind', {}).get('deg', 0)
        st.markdown(f"### 風速: {wind_speed} m/s")
        st.markdown(f"### 風向: {wind_deg}°")
        if 'clouds' in current_weather:
            st.markdown(f"### 雲量: {current_weather['clouds']['all']}%")
    
    # Forecast Section
    st.header("🔮 5天天氣預報")
    
    # Create forecast data for plotting
    forecast_data = []
    
    for item in forecast['list']:
        dt = datetime.fromtimestamp(item['dt'])
        temp_c = item['main']['temp']
        temp_f = celsius_to_fahrenheit(temp_c)
        temp = temp_f if not is_celsius else temp_c
        
        forecast_data.append({
            'datetime': dt,
            'date': dt.strftime('%Y-%m-%d'),
            'time': dt.strftime('%H:%M'),
            'temp': temp,
            'weather': item['weather'][0]['main'],
            'description': item['weather'][0]['description'],
            'humidity': item['main']['humidity'],
            'wind_speed': item['wind']['speed']
        })
    
    df = pd.DataFrame(forecast_data)
    
    # Temperature chart
    st.subheader("溫度趨勢")
    unit_symbol = "°C" if is_celsius else "°F"
    fig = px.line(
        df, 
        x='datetime', 
        y='temp', 
        title=f'未來5天溫度趨勢 ({unit_symbol})',
        labels={'datetime': '日期時間', 'temp': f'溫度 ({unit_symbol})'}
    )
    fig.update_layout(xaxis_title="日期時間", yaxis_title=f"溫度 ({unit_symbol})")
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily forecast cards
    st.subheader("每日預報")
    
    # Get daily summary (taking mid-day forecast for each day)
    daily_forecasts = {}
    for item in forecast_data:
        date = item['date']
        time = item['time']
        # Pick the forecast around noon for the daily summary
        if time in ['12:00', '15:00']:
            if date not in daily_forecasts:
                daily_forecasts[date] = item
    
    # Display daily forecast cards
    cols = st.columns(len(daily_forecasts))
    for i, (date, forecast_item) in enumerate(daily_forecasts.items()):
        with cols[i]:
            weather_color = get_weather_color(forecast_item['weather'])
            weather_icon = get_weather_icon(forecast_item['weather'])
            
            st.markdown(f"**{datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d %a')}**")
            st.markdown(f"{weather_icon} {forecast_item['description'].capitalize()}")
            
            temp_display = f"{forecast_item['temp']:.1f} {unit_symbol}"
            st.markdown(f"溫度: {temp_display}")
            st.markdown(f"濕度: {forecast_item['humidity']}%")
            st.markdown(f"風速: {forecast_item['wind_speed']} m/s")
            
            # Use the color to create a simple background indicator
            st.markdown(
                f"""
                <div style="background-color: {weather_color}; height: 5px; width: 100%;"></div>
                """, 
                unsafe_allow_html=True
            )

except Exception as e:
    st.error(f"獲取天氣數據時出錯: {str(e)}")
    st.info("請檢查城市名稱是否正確，並確保API密鑰有效。")

# Footer
st.markdown("---")
st.markdown("數據由 OpenWeatherMap API 提供")
st.markdown("© 2025 由 IAN 開發")
