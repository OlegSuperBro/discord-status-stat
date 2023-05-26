import requests
import yaml
import json
import re

from time import sleep
from importlib import import_module

DEFAULT_CONFIG = {
    "discord_token": "",
    "game": "",
    "delay": 30,
    "lines": ["Works fine", "Set custom lines"],
    "API_data":
        {

        }
}

try:
    CONFIG = yaml.load(open("config.yaml"), Loader=yaml.Loader)
except FileNotFoundError:
    CONFIG = DEFAULT_CONFIG
    yaml.dump(DEFAULT_CONFIG, open("config.yaml", "w"), Dumper=yaml.Dumper)


def get_from_tree(dictionary: dict, *path: any) -> any:
    value = dictionary
    for key in path:
        try:
            value = value.get(key)
        except KeyError:
            return None
    return value


def set_status(text, token) -> None:
    return requests.patch(
        "https://ptb.discordapp.com/api/v6/users/@me/settings",
        headers={"authorization": token},
        json={"custom_status": {"text": text}}
    )


def is_discord_valid(token: str) -> bool:
    """
    Checks Discord auth token
    IN:
    token - str. Discord token
    OUT:
    True - token is valid
    False - token is invalid
    """

    a = requests.get(
        "https://ptb.discordapp.com/api/v9/users/@me",
        headers={"authorization": token}
    )
    if a.status_code == 401:
        return False
    elif a.status_code == 200:
        return True
    else:
        raise Exception("Not valid discord token")


def format_string(string, data) -> str:
    need2replace = re.findall("{.+?}", string)
    for replacing in need2replace:
        string = string.replace(replacing, str(get_from_tree(data, *replacing.replace("{", "").replace("}", "").split("."))))
    return string


if CONFIG.get("discord_token") == "":
    raise Exception("No Discord token in settings.py")
elif not is_discord_valid(CONFIG.get("discord_token")):
    raise Exception("Non valid Discord token")

if CONFIG.get("game") != "":
    try:
        API = import_module("API.{}".format(CONFIG.get("game"))).API()
    except ModuleNotFoundError:
        raise ModuleNotFoundError("API for \"{}\" don't exist".format(CONFIG.get("game")))
    except AttributeError:
        raise AttributeError("{}.py don't have API class".format(CONFIG.get("game")))

    API.load(CONFIG.get("API_data").get(CONFIG.get("game")))  # give saved data to API

    API.start()  # start API (create tokens, make token updater etc)

    CONFIG["API_data"][CONFIG.get("game")] = API.save()  # save data
    yaml.dump(CONFIG, open("config.yaml", "w"), Dumper=yaml.Dumper)

while True:
    if CONFIG.get("game") != "":
        data = API.data
        json.dump(data, open("current_data.json", "w"), indent=4)
    else:
        data = {}
    for text in CONFIG.get("lines"):
        if CONFIG.get("game") != "":
            print(f"Set status: {format_string(text, data)}")
            set_status(format_string(text, data), CONFIG.get("discord_token"))
        else:
            print(f"Set status: {text}")
            set_status(text, CONFIG.get("discord_token"))
        sleep(int(CONFIG.get("delay")))
