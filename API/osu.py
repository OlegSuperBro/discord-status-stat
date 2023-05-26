import requests  # if you want something simple, you can use only this module
import webbrowser
import threading
import sys

from time import sleep

"""
API for osu!

For using this you need osu! app.
To get it go to your profile settings, scroll down and press "New OAuth Application"
Type anything for "Application name" and "https://example.com/" for "Application Callback URLs"
Now in new app click "Edit" and copy client id and client secret. You will need it when program started.
Now run program, and input requred data.
"""


class API:
    api_url = "https://osu.ppy.sh/api/v2"
    redirect_url = "https://example.com/"

    # MAIN FUNCS
    def load(self, config: dict) -> None:
        # loading saved data / ask data from user

        # try to read
        try:
            self.client_id = config.get("client_id")
            self.client_secret = config.get("client_secret")
            self.code = config.get("code")

            self.username = config.get("username")
            self.mode = config.get("mode")

        # we don't have something? Ask user for new information
        except AttributeError:
            self.username = input("Your username >>> ")

            self.mode = None
            while self.mode not in ("osu", "fruits", "catch", "mania"):
                self.mode = input("Game mode (osu/fruits/catch/mania) >>> ")

            self.client_id = input("Client id >>> ")
            self.client_secret = input("Client secret >>> ")

            webbrowser.open(self.get_code_link())  # open generated link in browser
            self.code = self.code_from_link(input("Check browser and input link after verification >>> "))

    def start(self) -> None:
        # setting up some expirable data

        self.update_token()  # update token for API auth

        # make headers for data retrieving
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        # start token updater, because token can expire
        timer = threading.Thread(target=self.token_updater)
        timer.daemon = True
        timer.start()

    def save(self) -> dict:
        # return info for save
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "username": self.username,
            "mode": self.mode,
        }

    @property
    def data(self) -> dict:
        # return dict with data from game API
        # you can do something with this data, BUT dict should be returned
        return requests.get(f"{self.api_url}/users/{self.username}/{self.mode}", headers=self.headers).json()

    # OTHER FUNCS
    def get_code_link(self) -> str:
        # get link for auth
        return f"https://osu.ppy.sh/oauth/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_url}&scope=public"

    def code_from_link(self, link) -> str:
        # get code from link
        return link.replace(f"{self.redirect_url}?code=", "")

    def update_token(self) -> None:
        # request token from API
        data = requests.post("https://osu.ppy.sh/oauth/token/",
                             data={
                                 "redirect_url": self.redirect_url,
                                 "grant_type": "client_credentials",  # idk why works with this. Docs says here should be "authorization_code"
                                 "scope": "public",  # it's just works
                                 "client_id": self.client_id,  # id of client app
                                 "client_secret": self.client_secret,  # secret of client app
                                 "code": self.code  # code (recived from app auth)
                             },
                             headers={
                                 "Accept": "application/json"
                             }).json()

        self.token = data["access_token"]
        self.token_expires = int(data["expires_in"])

    def token_updater(self) -> None:
        # update token. Need to be different func just to run it asynchronous
        try:
            print("Osu! API: Timer start successful")
            while True:
                sleep(self.token_expires)
                try:
                    self.update_token()
                except Exception:
                    print("Osu! API: Error to connect Osu api. Retryng after 10 seconds")
                    self.token_expires = 10
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
