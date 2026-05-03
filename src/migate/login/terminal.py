import getpass
import hashlib
import json
from urllib.parse import urlparse, parse_qs
from migate.login.captcha import handle_captcha
from migate.login.verify import handle_verify
from migate.config import SERVICELOGINAUTH2_URL, console
from migate.requester import post

from migate.utilities.uRegion import get_uRegion
from migate.utilities.areaConfig import get_areaConfig

def handle_terminal(auth_data: dict) -> dict:

    uRegion = get_uRegion()
    if uRegion:
        areaConfig = get_areaConfig(uRegion)
        if areaConfig:
            dial = f"(ex> {areaConfig['dial']}XXXXXXXXX)"
        else:
            dial = ""
    else:
        dial = ""

    while True:
        console.print(f"\n[white]Enter your:\n  Xiaomi Account ID, Email, or Phone {dial}[/]")
        user = console.input("[white]> [/]").strip()
        pwd_input = getpass.getpass("\nPassword> ").strip()
        pwd = hashlib.md5(pwd_input.encode()).hexdigest().upper()

        auth_data["user"] = user
        auth_data["hash"] = pwd

        try:
            response = post(SERVICELOGINAUTH2_URL, data=auth_data)
            response_text = json.loads(response.text[11:])
        except Exception as e:
            console.print(f"\n[red]{e}[/]\n")
            return None

        if response_text.get("code") == 70016:
            console.print("\nInvalid password or username! Please try again.\n", style="red")
            continue

        if response_text.get("code") == 87001:
            console.print("\nCAPTCHA verification required!\n", style="orange")
            response = handle_captcha(SERVICELOGINAUTH2_URL, response, auth_data, "captCode")

            if isinstance(response, dict) and "error" in response:
                console.print(f"\n[red]{response['error']}[/]\n")
                return None

            response_text = json.loads(response.text[11:])

            if response_text.get("code") == 70016:
                console.print("\nInvalid password or username! Please try again.\n", style="red")
                continue

        break

    if "notificationUrl" in response_text:
        notification_url = response_text["notificationUrl"]
        if any(x in notification_url for x in ["callback", "SetEmail", "BindAppealOrSafePhone"]):
            console.print(f"\n[red]Action required at: {notification_url}[/]\n")
            return None

        context  = parse_qs(urlparse(notification_url).query)["context"][0]
        response = handle_verify(context, auth_data)

        if isinstance(response, dict) and "error" in response:
            console.print(f"\n[red]{response['error']}[/]\n")
            return None

        response_text = json.loads(response.text[11:])

    return response_text