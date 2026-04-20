import getpass
import hashlib
import json
from urllib.parse import urlparse, parse_qs
import uuid
from pathlib import Path

from migate.login.captcha import handle_captcha
from migate.login.verify import handle_verify
from migate.config import SERVICELOGINAUTH2_URL, console
from migate.requester import session, post


def _get_device_id(user: str) -> str:
    id_file = Path.home() / f".migate_device_{hashlib.md5(user.encode()).hexdigest()[:8]}.json"
    if id_file.exists():
        return json.loads(id_file.read_text())["deviceId"]
    deviceId = "wb_" + uuid.uuid4().hex
    id_file.write_text(json.dumps({"deviceId": deviceId}))
    return deviceId


def handle_terminal(auth_data: dict) -> dict:

    while True:
        user      = console.input("[white]Account ID / Email / Phone (+): [/]").strip()
        pwd_input = getpass.getpass("Password: ").strip()
        pwd       = hashlib.md5(pwd_input.encode()).hexdigest().upper()

        auth_data["user"] = user
        auth_data["hash"] = pwd

        session.cookies.set("deviceId", _get_device_id(user))

        try:
            response      = post(SERVICELOGINAUTH2_URL, data=auth_data)
            response_text = json.loads(response.text[11:])
        except Exception as e:
            console.print(f"\n[red]Connection error: {e}[/]\n")
            raise SystemExit(1)

        if response_text.get("code") == 70016:
            console.print("\nInvalid password or username! Please try again.\n", style="red")
            continue

        if response_text.get("code") == 87001:
            console.print("\nCAPTCHA verification required!\n", style="orange")
            response = handle_captcha(SERVICELOGINAUTH2_URL, response, auth_data, "captCode")

            if isinstance(response, dict) and "error" in response:
                console.print(f"\n[red]{response['error']}[/]\n")
                raise SystemExit(1)

            response_text = json.loads(response.text[11:])

            if response_text.get("code") == 70016:
                console.print("\nInvalid password or username! Please try again.\n", style="red")
                continue

        break

    if "notificationUrl" in response_text:
        notification_url = response_text["notificationUrl"]
        if any(x in notification_url for x in ["callback", "SetEmail", "BindAppealOrSafePhone"]):
            console.print(f"\n[red]Action required at: {notification_url}[/]\n")
            raise SystemExit(1)

        context  = parse_qs(urlparse(notification_url).query)["context"][0]
        response = handle_verify(context, auth_data)

        if isinstance(response, dict) and "error" in response:
            console.print(f"\n[red]{response['error']}[/]\n")
            raise SystemExit(1)

        response_text = json.loads(response.text[11:])

    return response_text
