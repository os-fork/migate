import json
from migate.config import REGION_URL, console
from migate.requester import session, get

def get_region(auth_cookies):

    for k, v in auth_cookies.items():
        session.cookies.set(k, v)

    try:
        response = get(REGION_URL)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]{e}[/]\n")
        return None
    finally:
        session.cookies.clear()

    region = response_text.get("data", {}).get("region")

    if not region and response_text.get('code') != 0:
        console.print(f"\n[red]Failed to get account region | Response: {response_text}[/]\n")
        return None
    elif not region:
        console.print(f"\n[red]Failed to get account region[/]\n")
        return None

    return region