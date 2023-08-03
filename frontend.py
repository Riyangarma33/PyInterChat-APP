from os import get_terminal_size
from time import sleep

from clear_screen import clear
from console.utils import pause
from pwinput import pwinput
from pydantic import SecretStr

from backends.account import account
from backends.server import ConnectionError, server


def __header() -> None:
    clear()
    print("PyInterChat APP".center(get_terminal_size().columns))
    if server.url:
        print(f"Server: {server.url}".center(get_terminal_size().columns))
    if account.username:
        print(f"Username: {account.username}".center(get_terminal_size().columns))
    print("".center(get_terminal_size().columns, "="))


def __set_server() -> None:
    __header()
    try:
        new_url: str = input(
            f"Enter Your Server URL (Type 'remove' to Remove Server URL){f' [{server.url}]' if server.url else ''}: "
        )
        if new_url:
            if new_url.lower() == "remove":
                server.url = None
                print("Server URL Removed!")
            elif new_url != server.url:
                server.url = new_url
                print("Server Added Successfully")
        else:
            print("Server Not Changed!")
    except ValueError as err:
        # ValueError if url is invalid
        print(str(err))
    except ConnectionError:
        print("Server Connection Error!")
    finally:
        sleep(2)


def __login() -> None:
    __header()
    print("\nEnter Login Credentials!")
    identity: str = input("\nEmail/Username\t: ")
    password: SecretStr = SecretStr(pwinput("Password\t: ", mask="*"))
    try:
        account.login(Identity=identity, Password=password)
        print(f"\nLogin Success! Welcome {account.username}")
    except (AssertionError, ValueError) as err:
        print(f"\nLogin Failed! Error = {err.args}")
    finally:
        sleep(2)


def __logout() -> None:
    __header()
    print("\nLogging Out!")
    try:
        account.logout()
        print("\nLogout Success!")
    except RuntimeError as err:
        print(f"Logout Failed! Error = {str(err)}")
    finally:
        sleep(2)


def __main_menu() -> None:
    while True:
        __header()
        print("\nWelcome to Main Menu.")
        print("\nSelect Options:")
        if not account.username:
            print("1. Set Server")
            print("2. Register")
            print("3. Login")
            print("4. Exit")
            try:
                sel = int(input("\nSelect: "))
                if sel == 1:
                    __set_server()
                elif sel == 3:
                    __login()
                elif sel == 4:
                    pause()
                    return
            except ValueError:
                pass
        else:
            print("1. Logout")
            print("2. Exit")
            try:
                sel = int(input("\nSelect: "))
                if sel == 1:
                    __logout()
                if sel == 2:
                    pause()
                    return
            except ValueError:
                pass


def main_menu() -> None:
    __main_menu()
