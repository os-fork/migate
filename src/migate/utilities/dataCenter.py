import json
from migate.config import CONFIG_URL, CONFIGURATION_URL, console
from migate.requester import session, get

def select_manually():
    _ZONES = ["Singapore", "China", "Russia", "India", "Europe"]
    console.print("\n[white]Select dataCenterZone:[/white]")
    console.print("[white]" + "─" * 40 + "[/white]")
    for i, zone in enumerate(_ZONES, 1):
        console.print(f"  [orange]{i}.[/orange] [white]{zone}[/white]")
    console.print("[white]" + "─" * 40 + "[/white]\n")

    while True:
        choice = console.input(f"[white]Select (1-{len(_ZONES)}): [/white]").strip()

        if not choice.isdigit():
            console.print("[red]Invalid input. Enter a number.[/red]\n")
            continue

        idx = int(choice) - 1
        if 0 <= idx < len(_ZONES):
            Zone = _ZONES[idx]
            console.print(f"\n[green]dataCenterZone selected: {Zone}[/green]\n")
            return Zone

        console.print(f"[red]Out of range. Enter 1–{len(_ZONES)}.[/red]\n")


def get_with_userId(userId):

    try:
        response = get(CONFIGURATION_URL, params={'keys': 'idc'})
        response_text = json.loads(response.text)
    except Exception as e:
        console.print(f"\n[red]{e}[/]\n")
        return None

    idc = response_text["data"]["idc"]

    for name, info in idc.items():
        ranges = [{"min": info["userId.min"], "max": info["userId.max"]}]
        for ext in info.get("extend.idRange", []):
            ranges.append({"min": ext["userId.min"], "max": ext["userId.max"]})
        for r in ranges:
            if r["min"] <= userId <= r["max"]:
                return name

    console.print(f"\n[red]Failed to get dataCenterZone with userId[/]\n")
    return None


def get_with_region(region):

    try:
        response = get(CONFIG_URL, params={'key': 'regionConfig'})
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]{e}[/]\n")
        return None

    Zone = next(
        (k for k, v in response_text.get("regionConfig", {}).items()
         if v.get("region.codes") and region in v["region.codes"]),
        None
    )

    if Zone is None:
        console.print(f"\n[red]Failed to get dataCenterZone from region account[/]\n")

    return Zone


def get_dataCenterZone(value=None):
    value_str = str(value).strip() if value is not None else ""

    if value_str.isdigit():
        Zone = get_with_userId(int(value_str))
    elif value_str.isalpha():
        Zone = get_with_region(value_str)
    else:
        Zone = select_manually()

    session.cookies.clear()
    return Zone