import json
from pathlib import Path
from migate.config import REGION_URL, console
from migate.requester import session, get


def get_region(auth_cookies):

    userId = auth_cookies['userId']

    region_file = Path.home() / ".mi_region" / "region.json"

    if region_file.exists():
        try:
            with open(region_file, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            region_file.unlink()
            data = {}

        region = data.get(userId)

        if region:
            console.print(f"\nAccount Region: {region}", style="green")
            return region

    for k, v in auth_cookies.items():
        session.cookies.set(k, v)

    try:
        response      = get(REGION_URL)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]Connection error: {e}[/]\n")
        raise SystemExit(1)

    region = response_text.get("data", {}).get("region")

    if not region:
        console.print(f"\n[red]Failed to get account region | Response: {response_text}[/]\n")
        raise SystemExit(1)

    session.cookies.clear()

    region_file.parent.mkdir(parents=True, exist_ok=True)

    existing = {}
    if region_file.exists():
        try:
            with open(region_file, "r") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass

    existing[userId] = region

    with open(region_file, "w") as f:
        json.dump(existing, f)

    console.print(f"\nAccount Region: {region}", style="green")

    return region