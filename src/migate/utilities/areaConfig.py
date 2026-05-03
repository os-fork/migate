import json
from migate.config import CONFIG_URL, console
from migate.requester import session, get

def get_areaConfig(country_code: str) -> dict:

    try:
        params = {'key': 'areaConfig'}
        response = get(CONFIG_URL, params=params)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]{e}[/]\n")
        return None

    areas = response_text.get("areaConfig")

    if not areas:
        console.print(f"\n[red]Failed to get areaConfig | Response: {response_text}[/]\n")
        return None

    for letter, countries in areas.items():
        for country in countries:
            if country["B"] == country_code:
                return {
                    "code": country["B"],
                    "name": country["C"],
                    "dial": country["N"]
                }

    return None