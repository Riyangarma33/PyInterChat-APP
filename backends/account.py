from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, Optional

from email_validator import EmailNotValidError, validate_email
from pydantic import EmailStr, SecretStr
from requests import delete, post

from backends.server import server


class __account:
    def __init__(self) -> None:
        self.__session = self.__sess()

    @property
    def username(self) -> Optional[str]:
        return self.__session.Username

    def login(self, Identity: str, Password: SecretStr) -> None:
        # Check if Identity is Email
        email: bool = False
        try:
            validate_email(Identity, check_deliverability=False)
            email = True
        except EmailNotValidError:
            pass
        # Check If Url is Set
        if not server.url:
            raise ValueError("Server Is Not Configured!")
        # Login process
        data: Dict[str, str] = {
            "Email": Identity if email else "",
            "Username": Identity if not email else "",
        }
        response: Dict = post(
            server.url + "/login",
            headers=self.__session.Header(input_data=True),
            data=data | {"Password": Password.get_secret_value()},
        ).json()
        if response["message"] == "Login Success!":
            self.__session.Username = response["data"]["username"]
            self.__session.Token = response["data"]["token"]
        else:
            raise AssertionError(response["message"])

    def logout(self) -> None:
        response: Dict[str, str] = delete(
            server.url + "/logout", headers=self.__session.Auth_Header()
        ).json()
        if response["message"] == "Logout Success":
            self.__session.Username = None
            self.__session.Token = None
        else:
            raise RuntimeError(response["message"])

    def register(
        self, Name: str, Email: EmailStr, Username: str, Password: SecretStr
    ) -> None:
        pass

    @dataclass
    class __sess:
        Username: str = None
        Token: str = None

        def Header(self, input_data: bool = False) -> Dict[str, str]:
            if input_data:
                return {
                    "accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            return {"accept": "application/json"}

        def Auth_Header(self, input_data: bool = False) -> Dict[str, str]:
            return self.Header(input_data) | {"X-UserToken": self.Token}


account = __account()
