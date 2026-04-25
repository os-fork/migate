import json
from pathlib import Path
from migate.config import REGIONCONFIG_URL, console
from migate.requester import session, get


def get_regionConfig(region):

    region_file = Path.home() / ".migatesession" / "regionConfig.json"

    if region_file.exists():
        try:
            with open(region_file, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            region_file.unlink(missing_ok=True)
            data = {}

        regionConfig = data.get(region)

        if regionConfig:
            console.print(f"\nregionConfig: {regionConfig}", style="green")
            return regionConfig

    try:
        params        = {'key': 'regionConfig'}
        response      = get(REGIONCONFIG_URL, params=params)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]Connection error: {e}[/]\n")
        raise SystemExit(1)

    region_config_dict = response_text.get("regionConfig", {})

    if not region_config_dict:
        console.print(f"\n[red]Failed to get regionConfig | Response: {response_text}[/]\n")
        raise SystemExit(1)

    regionConfig = next(
        (k for k, v in region_config_dict.items()
         if v.get("region.codes") and region in v["region.codes"]),
        None
    )

    session.cookies.clear()

    existing = {}
    if region_file.exists():
        try:
            with open(region_file, "r") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    existing[region] = regionConfig

    region_file.parent.mkdir(parents=True, exist_ok=True)
    with open(region_file, "w") as f:
        json.dump(existing, f)

    console.print(f"\nregionConfig: {regionConfig}", style="green")

    return regionConfig