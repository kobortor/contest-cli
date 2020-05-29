import os
from typing import *
import dmoj_urls
from getpass import getpass
import requests
import pickle
from help import handle_help
from urllib.parse import urlparse

def _handle_login(args: List[str]):
    login_session_filename = os.path.expanduser("~/.config/dmoj-cli/login.pkl")
    if os.path.exists(login_session_filename):
        print("Warning: Existing login will be overriden. Continue? [y/n]")
        while True:
            choice = input().strip()
            if choice.lower() == "y":
                break
            elif choice.lower() == "n" or choice.lower() == "":
                return
            else:
                print("Input not understood, try again")

    s = requests.session()

    r1 = s.get(dmoj_urls.get_login_url())

    if r1.status_code != 200:
        print("Cannot connect to dmoj.ca: error code [{}]".format(r.status_code))
        return

    if "csrftoken" not in r1.cookies:
        print("Missing CSRF token")
        return

    username = ""
    while not username:
        username = input("Enter your username: ")
        if not username:
            print("Username cannot be empty. To stop, press Ctrl-D.")

    password = ""
    while not password:
        password = getpass("Enter your password: ")
        if not password:
            print("Password cannot be empty. To stop, press Ctrl-D.")

    r2 = s.post(
            r1.url, 
            data={"username": username, "password": password, "csrfmiddlewaretoken": r1.cookies["csrftoken"]},
            headers={'referer':r1.url})

    if '<p class="error">Invalid username or password.</p>' in r2.text:
        print("Error: Login Failed")
        return
        
    if r2.url.startswith("https://dmoj.ca/accounts/2fa"):
        code_2fa = ""
        while not code_2fa:
            code_2fa = input("Enter your 2FA code: ").strip().lower()
            if len(code_2fa) == 6 and code_2fa.isdigit():
                pass
            else:
                print("The 2FA code should be 6-digits. To quit, press Ctrl-D")
                code_2fa = ""

        r3 = s.post(
                r2.url,
                data={"totp_token": code_2fa, "csrfmiddlewaretoken": r2.cookies["csrftoken"]},
                headers={'referer':r2.url})
        if r3.status_code != 200:
            print("Error: Status Code {}".format(r3.status_code))
            return
        if '<p class="error">Invalid two-factor authentication token.</p>' in r3.text:
            print("2 Factor Authentication Failed")
            return

    print("Login Successful!")
    os.makedirs(os.path.dirname(login_session_filename), exist_ok=True)
    pickle.dump(s, open(login_session_filename, "wb"))

def handle_config(args: List[str]):
    if not args:
        handle_help()

    if args[0] == "login":
        _handle_login(args[1:])
