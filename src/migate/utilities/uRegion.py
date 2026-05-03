import json
from migate.config import CONFIG_URL, console
from migate.requester import session, get

def get_uRegion():

    try:
        params = {'key': 'uRegion'}
        response = get(CONFIG_URL, params=params)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]{e}[/]\n")
        return None

    uRegion = response_text.get("uRegion")

    if not uRegion:
        console.print(f"\n[red]Failed to get uRegion | Response: {response_text}[/]\n")
        return None

    return uRegion