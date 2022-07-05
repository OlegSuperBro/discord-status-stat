import settings
from discord import Discord

import sys
import importlib
import requests
import time

# just empty class
class dummy:
    pass

def dict_to_class(data:dict):
    """
    turn dict into class to use like key1.key2
    IN:
    data - dict
    OUT:
    dum - dummy class
    """

    dum = dummy()

    for i in data.keys():
        if type(data.get(i)) == dict:
            print("DICT")
        else:
            exec("dum.%s = data.get(i)" % i)

def modify_line(line:str, data:dict):
    """
    Replace things in line
    IN:
    line - str. Line to modify
    data - dict with data

    OUT:
    data = {"test" : 123}
    line = "test = #test#" - except "#" can be anything that set in settings.py
    after modification:
    line = "test = 123"
    """
    
    # first of all parse line for data identificator

    formating = False
    dict_level = 0
    ignore = False
    command = ""

    for i in line:
        if ignore:
            ignore = False
            continue

        if i == "\\":
            ignore = True
            continue
        
        if i == "{" and formating:
            raise Exception("Double brakets or no close brakets in line %s" % line)
        
        if i == "}" and not formating:
            raise Exception("Double brakets or no open brakets in line %s" % line)

        if i == "{":
            formating = True
            continue
        
        if i == "}":
            formating = False
            continue
            
        if formating:
            command += i
            

    # keys = []
    # del_keys = []
    # key = ""
    # data_started = False
    # for i in line:
    #     if i == settings.data_start and not data_started:
    #         data_started = True
    #     elif i == settings.data_end and data_started:
    #         del_keys.append(key)
    #         keys.append(key.split(settings.data_sep))
    #         key = ""
    #         data_started = False
    #     elif data_started:
    #         key += i

    # new_data = {}
    # for i2 in keys:
    #     temp = data
    #     for i in i2:
    #         temp = temp[i]
    #     new_data[i] = temp

    # for i1 in del_keys:
    #     try:
    #         line = line.replace(f"{settings.data_start}{i1}{settings.data_end}", str( new_data[ i1.split(settings.data_sep)[-1:][0] ] ))
    #     except KeyboardInterrupt as e:
    #         print(e)
    #         sys.exit()

    # return line

def is_discord_valid(token:str):
    """
    Checks Discord auth token
    IN:
    token - str. Discord token
    OUT:
    True - token is valid
    False - token is invalid
    None - An error
    """

    a = requests.get(
            "https://ptb.discordapp.com/api/v6/users/@me",
            headers={"authorization": token}
        )
    if a.status_code == 401:
        return False
    elif a.status_code == 200:
        return True
    else:
        return None

if settings.discord_token == "":
    raise Exception("No Discord token in settings.py")
elif not is_discord_valid(settings.discord_token):
    raise Exception("Non valid Discord token")
discord = Discord(settings.discord_token)
print("Discord API key get successful")

api = (importlib.import_module(f"apis.{settings.game}")).api(settings.save_data)

print("Starts main program")
while True:
    data = api.get_data()
    for text in settings.lines:
        print(data)
        print(f"Set status: {modify_line(text, data)}")
        discord.set_status(modify_line(text, data))
        time.sleep(settings.wait_time)