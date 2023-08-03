from http import HTTPStatus
from typing import Dict, Optional

from dotenv import dotenv_values, find_dotenv, set_key, unset_key
from requests import get
from requests.exceptions import ConnectionError
from validators.url import url as validate_url


class __server_rev:
    def __init__(self) -> None:
        self.__prev_url: Optional[str] = None
        if not find_dotenv():
            with open(".env", "w") as env:
                pass
        try:
            if self.url:
                self.ping()
        except ConnectionError:
            self.url = None

    @property
    def url(self) -> Optional[str]:
        env: Dict[str, str] = dotenv_values(".env")
        try:
            return env["SERVER"]
        except KeyError:
            return None

    @url.setter
    def url(self, url_in: str = None) -> None:
        if isinstance(url_in, str):
            if validate_url(url_in):
                self.__prev_url = self.url
                set_key(
                    ".env",
                    "SERVER",
                    url_in if not url_in.endswith("/") else url_in.rstrip(url_in[-1]),
                )
                self.ping()
            else:
                raise ValueError("Invalid URL!")
        else:
            unset_key(".env", "SERVER")

    def ping(self):
        header = {"accept": "application/json"}
        try:
            response = get(self.url + "/ping", headers=header, allow_redirects=False)
            try:
                if response.headers["Location"].startswith(
                    "https://"
                ) and response.headers["Location"].endswith("/ping"):
                    self.url = self.url.replace("http://", "https://")
            except KeyError:
                pass
            finally:
                response = get(self.url + "/ping", headers=header)
                if response.status_code != HTTPStatus.OK:
                    self.url = None
                    raise ValueError("Invalid Server!")
        except ConnectionError as err:
            self.url = self.__prev_url if self.__prev_url else None
            raise err


server = __server_rev()
