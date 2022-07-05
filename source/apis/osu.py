import sys
import threading
import requests
import time

"""
API for osu
"""

class api:
    api_url = "https://osu.ppy.sh/api/v2"
    redirect_url = "https://example.com/"

    def __init__(self, save_data):
        self.save_data = save_data

        self.start()

    def start(self, load = False):
        if not load and (input("Import saved data? [y]/n >>> ").lower() in ["n", "no"] or not self.save_data):
            print("Game mode:\n1)Osu\n2)Catch\n3)Taiko\n4)Mania")
            while True:
                match input():
                    case "1":
                        self.mode = "osu"
                        break
                    case "2":
                        self.mode = "fruits"
                        break
                    case "3":
                        self.mode = "taiko"
                        break
                    case "4":
                        self.mode = "mania"
                        break
                    case _:
                        print("Please, input valid mode.")

            self.username      = input("Input your username (i'm too stupid) >>>")
            self.client_id     = input("Input client id >>> ")
            self.client_secret = input("Input client secret >>> ")
            print(f"Go to this page: {self.get_code_link()}")
            self.code          = self.code_from_link(input("Input link after verification >>> "))
        else:
            try:
                self.username      = self.save_data["username"]
                self.mode          = self.save_data["mode"]
                self.client_id     = self.save_data['client_id']
                self.client_secret = self.save_data['client_secret']
                self.code          = self.save_data['code']
            except KeyError as e:
                raise AttributeError(f"{e}\nNot enought data.")
            print("Load successful")
        
        self.token, self.token_expires = self.get_token()

        self.headers = {
            "Content-Type"  : "application/json",
            "Accept"        : "application/json",
            "Authorization" : f"Bearer {self.token}"
        }

        timer = threading.Thread(target = self.token_updater)
        timer.daemon = True
        timer.start()

    def get_data(self):
        return requests.get(f"{self.api_url}/users/{self.username}/{self.mode}", headers = self.headers).json()

    def get_code_link(self):
        return f"https://osu.ppy.sh/oauth/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_url}&scope=public"

    def code_from_link(self, link):
        return link.replace(f"{self.redirect_url}?code=", "")

    def get_token(self):
        data = requests.post("https://osu.ppy.sh/oauth/token/",
                data = {
                    "redirect_url"  : self.redirect_url,    # ???
                    "grant_type"    : "client_credentials", # idk why works with this. Docs says here should be "authorization_code"
                    "scope"         : "public",             # it's just works
                    "client_id"     : self.client_id,       # id of client app
                    "client_secret" : self.client_secret,   # secret of client app
                    "code"          : self.code             # code (recived from app autorization)
                },
                headers = {
                    "Accept": "application/json"
                }
        ).json()
        return (data["access_token"],int(data["expires_in"]))

    def token_updater(self):
        try:
            print("Timer start successful")
            while True:
                time.sleep(self.token_expires)
                try:
                    self.update_osu_token() 
                except Exception:
                    print("Error to connect Osu api. Retryng after 10 seconds")
                    self.token_expires = 10
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

if __name__ == '__main__':
    pass