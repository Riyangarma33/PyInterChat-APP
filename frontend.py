from os import get_terminal_size
from time import sleep

from clear_screen import clear
from console.utils import pause

from backends.server import ConnectionError, server
from backends.session import session


def __header() -> None:
    clear()
    print("PyInterChat APP".center(get_terminal_size().columns))
    if server.url:
        print(f"Server: {server.url}".center(get_terminal_size().columns))
    if session.Username:
        print(session.Username.center(get_terminal_size().columns))
    print("".center(get_terminal_size().columns, "="))


def __set_server() -> None:
    __header()
    try:
        new_url: str = input(f"Enter Your Server URL{f' [{server.url}]' if server.url else ''}: ")
        if new_url and new_url != server.url:
            server.url = new_url
            print("Server Added Successfully!")
        else:
            print("Server Not Changed!")
    except ValueError as err:
        print(str(err))
    except ConnectionError:
        print("Server Connection Error!")
    finally:
        sleep(2)


def __main_menu() -> None:
    while True:
        __header()
        print("\nWelcome to Main Menu.")
        print("\nSelect Options:")
        print("1. Set Server")
        print("2. Register")
        print("3. Login")
        print("4. Exit")
        sel = int(input("\nSelect: "))
        if sel == 1:
            __set_server()
        elif sel == 4:
            pause()
            return


def main_menu() -> None:
    __main_menu()
