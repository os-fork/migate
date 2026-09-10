import json

from migate.config import VERIFY_EM, VERIFY_PH, console, WHITE, ORANGE, RED
from migate.requester import post


def verify_code_ticket(addressType, label):
    url = VERIFY_EM if addressType == "EM" else VERIFY_PH

    while True:
        console.print(f"[{WHITE}]Check your {label} for the code.[/]")
        ticket = console.input(f"[{ORANGE}]Enter code (or type 'r' to resend): [/]").strip()

        if not ticket:
            continue

        if ticket == "r":
            return "RESEND"

        try:
            response      = post(url, data={"ticket": ticket, "trust": "true", "_json": "true"})
            response_text = json.loads(response.text[11:])
        except Exception as e:
            return {"error": str(e)}

        if response_text.get("code") == 0:
            return response_text.get("location")

        if response_text.get("code") == 70014:
            console.print("Invalid code provided.", style=RED)
            continue

        return {"error": response_text}
