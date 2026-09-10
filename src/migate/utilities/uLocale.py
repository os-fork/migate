import json
from migate.config import CONFIG_URL, console, RED
from migate.requester import session, get

def get_uLocale():

    try:
        params = {'key': 'uLocale'}
        response = get(CONFIG_URL, params=params)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[{RED}]{e}[/]\n")
        return None
    finally:
        session.cookies.clear()

    uLocale = response_text.get("uLocale")

    if not uLocale:
        console.print(f"\n[{RED}]Failed to get uLocale | Response: {response_text}[/]\n")
        return None

    return uLocale
