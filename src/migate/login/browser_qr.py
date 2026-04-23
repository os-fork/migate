import json
import os
import platform
import webbrowser
import qrcode
from migate.config import LONGPOLLING_URL, console
from migate.requester import get

def handle_browser_qr(auth_data: dict, choice: str) -> dict:

    auth_data["_json"] = False

    while True:
        try:
            response = get(LONGPOLLING_URL, params=auth_data)
            response_text = json.loads(response.text[11:])
        except Exception as e:
            console.print(f"\n[red]Connection error: {e}[/]\n")
            raise SystemExit(1)

        timeout = response_text["timeout"]
        url = response_text["loginUrl"]
        lp = response_text["lp"]

        if choice == "1":
            if platform.system() in ("Linux", "Android"):
                os.system(f"xdg-open '{url}' 2>/dev/null")
            else:
                webbrowser.open(url)
        elif choice == "3":
            qrTips = response_text["qrTips"]
            console.print(f"\n[white]{qrTips}[/]\n")
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
            qr.add_data(url)
            qr.print_ascii()

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