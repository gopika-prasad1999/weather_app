import streamlit as st
import requests
from datetime import datetime

# Replace 'your_api_key' with your actual OpenWeatherMap API key
API_KEY = '930e0a521439b0dcb25e526556c89501'

@st.cache_data
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

def main():
    # Custom CSS for background image and text color
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://m-cdn.phonearena.com/images/article/143515-wide-two_1200/Apple-tests-adding-news-to-the-native-Weather-app-in-iOS-16.2-Beta.webp?1667618530");
            background-size: cover;
            background-position: center;
            color: white;
        }
        .stMarkdown p, .stTitle, .stTextInput, .stButton button {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Weather App")

    city = st.text_input("Enter city name:")

    if st.button("Get Weather"):
        if city:
            with st.spinner('Fetching weather data...'):
                data = get_weather(city)
                if data['cod'] == 200:
                    temp = data['main']['temp']
                    weather = data['weather'][0]['description']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    feels_like = data['main']['feels_like']
                    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime('%H:%M:%S')
                    sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone']).strftime('%H:%M:%S')
                    visibility = data.get('visibility', 0) / 1000

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write(f"*Temperature:* {temp}°C")
                        st.write(f"*Feels Like:* {feels_like}°C")
                        st.write(f"*Weather:* {weather.capitalize()}")

                    with col2:
                        st.write(f"*Humidity:* {humidity}%")
                        st.write(f"*Wind Speed:* {wind_speed} m/s")
                        st.write(f"*Visibility:* {visibility} km")

                    with col3:
                        st.write(f"*Sunrise:* {sunrise}")
                        st.write(f"*Sunset:* {sunset}")
                        icon_code = data['weather'][0]['icon']
                        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
                        st.image(icon_url)
                else:
                    st.error(f"Error: {data['message']}")
        else:
            st.warning("You must enter a city name.")

if __name__ == "__main__":
    main()