import json
from pathlib import Path

from migate.login.terminal import handle_terminal
from migate.login.browser_qr import handle_browser_qr
from migate.config import SERVICELOGIN_URL, console
from migate.requester import session, get


def get_passtoken(auth_data=None):
    if auth_data is None:
        auth_data = {"sid": "passport"}

    sid = auth_data["sid"]
    cookies_file = Path.home() / ".migatesession" / f"{sid}" / "session.json"

    if cookies_file.exists():
        try:
            with open(cookies_file, "r") as f:
                passToken = json.load(f)
        except (json.JSONDecodeError, OSError):
            cookies_file.unlink(missing_ok=True)
            console.print("Session corrupted, please log in again.\n", style="red")
            passToken = None

        if passToken is not None:
            choice = console.input(
                f"\n[green]Already logged in[/][white]\nAccount ID: [/][orange]{passToken['userId']}[/]\n\n"
                f"[white](Enter to continue, [red]2[/red] To log out)[/white][white] > [/white]"
            ).strip().lower()

            if choice == "2":
                cookies_file.unlink(missing_ok=True)
                console.print("Logged out.", style="red")
            else:
                return passToken

    auth_data["_json"] = True

    try:
        response = get(SERVICELOGIN_URL, params=auth_data)
        response_text = json.loads(response.text[11:])
    except Exception as e:
        console.print(f"\n[red]{e}[/]\n")
        return None

    auth_data["serviceParam"] = response_text["serviceParam"]
    auth_data["qs"] = response_text["qs"]
    auth_data["callback"] = response_text["callback"]
    auth_data["_sign"] = response_text["_sign"]

    console.print("\n[bold]How would you like to log in?[/]")
    console.print("\n  [orange]1[/] - Browser [dim](default)[/]")
    console.print("  [orange]2[/] - Terminal")
    console.print("  [orange]3[/] - QR code\n")

    choice = console.input("[white]Choose > [/white]").strip()
    if choice not in ("1", "2", "3"):
        choice = "1"

    if choice == "2":
        response_text = handle_terminal(auth_data)
    else:
        response_text = handle_browser_qr(auth_data, choice)

    cookies  = session.cookies.get_dict()
    required = {"deviceId", "passToken", "userId"}
    missing  = required - cookies.keys()
    if missing:
        console.print(f"\n[red]Missing keys: {', '.join(missing)} | Response: {response_text}[/]\n")
        return None

    passToken = {k: cookies[k] for k in required}

    cookies_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cookies_file, "w") as f:
        json.dump(passToken, f)

    console.print("\nLogin successful", style="green")
    session.cookies.clear()

    return passToken