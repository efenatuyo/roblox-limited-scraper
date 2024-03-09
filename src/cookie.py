import requests

class cookie:
    def __init__(self, proxy):
        self.proxy = proxy
        self._x_token = ''
        self.generate_token()

    def generate_token(self):
        self._x_token = requests.post("https://economy.roblox.com/", proxies={"http": self.proxy.current}).headers.get("x-csrf-token")

    def x_token(self):
        return self._x_token
