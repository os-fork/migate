from migate.login.captcha import handle_captcha
from migate.login.verify import handle_verify
from migate.config import SERVICELOGINAUTH2_URL, console
from migate.requester import post
from migate.utilities.uRegion import get_uRegion
from migate.utilities.areaConfig import get_areaConfig
from urllib.parse import urlparse, parse_qs
import hashlib
import json
import sys

def password_input():
    pwd = []
    if sys.platform == "win32":
        import msvcrt
        while True:
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                break
            elif ch == "\b":
                if pwd:
                    pwd.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                pwd.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    break
                elif ch == "\x7f":
                    if pwd:
                        pwd.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    pwd.append(ch)
                    sys.stdout.write("*")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    sys.stdout.write("\n")
    return "".join(pwd)

def get_credentials(dial=""):
    console.print(f"\n[white]Xiaomi Account ID, Email, or Phone {dial}[/]")
    user = console.input("[white]> [/]").strip()
    console.print("[white]Password> [/]", end="")
    pwd_input = password_input().strip()
    pwd = hashlib.md5(pwd_input.encode()).hexdigest().upper()
    return user, pwd

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
        user, pwd = get_credentials(dial)
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