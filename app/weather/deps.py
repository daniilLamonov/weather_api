
import httpx
from fastapi import HTTPException

base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
api_key = "S8DVYAQSJV5HPK6KZBSWHY2LD"

def from_f_to_c_degrees(farengeit: int) -> int:
    return round((farengeit - 32) / 1.8)

async def get_weather(location: str):
    url = f"{base_url}{location}?key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            description = data["description"]
            today = data['days'][0]
            tempmax = from_f_to_c_degrees(today['tempmax'])
            tempmin = from_f_to_c_degrees(today['tempmin'])
            return {"description": description, "tempmin": tempmin, "tempmax": tempmax}
        return HTTPException(status_code=response.status_code)
