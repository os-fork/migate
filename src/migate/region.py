import json
from pathlib import Path
from migate.config import REGION_URL, REGIONCONFIG_URL, console
from migate.requester import session, get


def get_region(auth_cookies):

    userId = auth_cookies['userId']

    region_file = Path.home() / ".migatesession" / "region.json"

    if region_file.exists():
        try:
            with open(region_file, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            region_file.unlink(missing_ok=True)
            data = {}

        entry = data.get(userId)

        if entry:
            if isinstance(entry, str):
                region, source = entry, "region"
            else:
                region = entry["value"]
                source = entry["source"]
            if source == "uRegion":
                console.print(f"\nuRegion: {region}", style="green")
            else:
                console.print(f"\nAccount Region: {region}", style="green")
            return region

    for k, v in auth_cookies.items():
        session.cookies.set(k, v)

    try:
        response = get(REGION_URL)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]Connection error: {e}[/]\n")
        raise SystemExit(1)

    region = response_text.get("data", {}).get("region")
    source = "region"

    if not region:
        console.print(f"\n[red]Failed to get account region | Response: {response_text}[/]\n")
        try:
            params = {'key': 'uRegion'}
            response = get(REGIONCONFIG_URL, params=params)
            response_text = json.loads(response.text[11:])
        except Exception as e:
            console.print(f"\n[red]Connection error: {e}[/]\n")
            raise SystemExit(1)
        region = response_text.get("uRegion")
        if not region:
            console.print(f"\n[red]Failed to get uRegion | Response: {response_text}[/]\n")
            raise SystemExit(1)
        source = "uRegion"

    session.cookies.clear()

    existing = {}
    if region_file.exists():
        try:
            with open(region_file, "r") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    existing[userId] = {"value": region, "source": source}

    region_file.parent.mkdir(parents=True, exist_ok=True)
    with open(region_file, "w") as f:
        json.dump(existing, f)

    if source == "uRegion":
        console.print(f"\nuRegion: {region}", style="green")
    else:
        console.print(f"\nAccount Region: {region}", style="green")

    return region