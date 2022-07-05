import requests

class Discord:
    def __init__(self, token):
        self.token = token

    def set_status(self, text):
        return requests.patch(
            "https://ptb.discordapp.com/api/v6/users/@me/settings",
            headers={"authorization": self.token},
            json={"custom_status": {"text": text}}
        )