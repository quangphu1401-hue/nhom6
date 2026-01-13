import httpx
from app.config import settings
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Lấy thời tiết hiện tại từ OpenWeatherMap"""
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "vi"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data.get("wind", {}).get("speed", 0),
                    "weather_description": data["weather"][0]["description"],
                    "precipitation": data.get("rain", {}).get("1h", 0) if "rain" in data else 0,
                    "location": data["name"],
                    "latitude": lat,
                    "longitude": lon
                }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    async def get_forecast(self, lat: float, lon: float, days: int = 7) -> Optional[list]:
        """Lấy dự báo thời tiết 7 ngày"""
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "vi",
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                forecasts = []
                for item in data.get("list", []):
                    forecast_time = datetime.fromtimestamp(item["dt"])
                    forecasts.append({
                        "forecast_date": forecast_time,
                        "temperature": item["main"]["temp"],
                        "humidity": item["main"]["humidity"],
                        "precipitation": item.get("rain", {}).get("3h", 0) if "rain" in item else 0,
                        "wind_speed": item.get("wind", {}).get("speed", 0),
                        "weather_description": item["weather"][0]["description"],
                        "is_forecast": 1
                    })
                
                return forecasts
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None

weather_service = WeatherService()

