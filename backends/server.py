from dataclasses import dataclass
from typing import Optional

from requests import get
from requests.exceptions import ConnectionError
from starlette.status import HTTP_200_OK
from validators.url import url as validate_url


@dataclass
class __server:
    url: str

    @property
    def url(self) -> Optional[str]:
        # print("getter")
        return self._url

    @url.setter
    def url(self, url_in: str = None) -> None:
        # print(f"setter, url_in = {isinstance(url_in, str)}")
        if isinstance(url_in, str):
            if validate_url(url_in):
                self._url = (
                    url_in if not url_in.endswith("/") else url_in.rstrip(url_in[-1])
                )
                self.ping()
            else:
                raise ValueError("Invalid URL!")
        else:
            self._url = None

    def ping(self):
        header = {"accept": "application/json"}
        try:
            response = get(self._url + "/ping", headers=header, allow_redirects=False)
            try:
                if response.headers["Location"].startswith("https://"):
                    self._url = self._url.replace("http://", "https://")
            except KeyError:
                pass
            finally:
                response = get(self._url + "/ping", headers=header)
                if response.status_code != HTTP_200_OK:
                    self._url = None
        except ConnectionError as err:
            self._url = None
            raise err


server = __server()
