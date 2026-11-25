"""Entry point: log in, then start the menu."""
from authenticator import Authenticator
from library import Library
from menu import Menu

if __name__ == "__main__":
    if Authenticator().login():
        Menu(Library()).run()