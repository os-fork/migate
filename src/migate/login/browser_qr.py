import json
import os
import platform
import webbrowser
import time

from migate.config import LONGPOLLING_URL, console
from migate.requester import get


def handle_browser_qr(auth_data: dict, choice: str) -> dict:

    auth_data["_hasLogo"] = True
    #  auth_data["_qrsize"] = 720 # captcha size ex

    while True:
        try:
            response = get(LONGPOLLING_URL, params=auth_data)
            response_text = json.loads(response.text[11:])
        except Exception as e:
            console.print(f"\n[red]Connection error: {e}[/]\n")
            raise SystemExit(1)

        timeout = response_text["timeout"]

        if choice == "2":
            url = response_text["loginUrl"]
            delay = 7
        elif choice == "3":
            url = response_text["qr"]
            qrTips = response_text["qrTips"]
            console.print(f"\n[white]{qrTips}[/]\n")
            delay = 14

        with console.status("") as status:
            for i in range(delay, 0, -1):
                status.update(f"\nUrl will open automatically in your default browser in {i}s...")
                time.sleep(1)

        if platform.system() in ("Linux", "Android"):
            os.system(f"xdg-open '{url}' 2>/dev/null")
        else:
            webbrowser.open(url)

        lp = response_text["lp"]

        try:
            response = get(lp, timeout=timeout, retries=1)
            if response is None:
                console.print("\n[red]The time limit has expired. Please try again.[/]\n")
                continue
        except Exception as e:
            console.print(f"\n[red]Connection error: {e}[/]\n")
            raise SystemExit(1)

        break

    response_text = json.loads(response.text[11:])

    return response_text