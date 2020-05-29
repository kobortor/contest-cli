import os
from typing import *
from utils import get_login_url, get_session, delete_session, save_session
from getpass import getpass
import cfscrape
import pickle
from help import handle_help
from urllib.parse import urlparse

def _handle_login(args: List[str]):
    if args:
        print("Please do not put arguments after `login`")
        return

    if get_session() is not None:
        print("Warning: Existing login will be overriden. Continue? [y/n]")
        while True:
            choice = input().strip()
            if choice.lower() == "y":
                break
            elif choice.lower() == "n" or choice.lower() == "":
                return
            else:
                print("Input not understood, try again")

    s = cfscrape.create_scraper()

    r1 = s.get(get_login_url())

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
            headers={"referer":r1.url})

    if r2.status_code != 200:
        print("Cannot connect to dmoj.ca: error code [{}]".format(r.status_code))
        return

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
                headers={"referer":r2.url})
        if r3.status_code != 200:
            print("Error: Status Code {}".format(r3.status_code))
            return
        if '<p class="error">Invalid two-factor authentication token.</p>' in r3.text:
            print("2 Factor Authentication Failed")
            return

    print("Login Successful!")
    s.cookies["dmoj-cli-username"] = username
    save_session(s)

def _handle_logout(args: List[str]):
    if args:
        print("Please do not put arguments after `login`")
        return
    
    sess = get_session()
    if sess is None:
        print("No session found")
        return

    choice = input("Are you sure you want to delete user {}? [y/n]".format(sess.cookies.get("dmoj-cli-username", "[UNKNOWN USER]")))
    if choice.strip().lower() == "y":
        delete_session()
    else:
        print("Not deleting!")

def handle_config(args: List[str]):
    if not args:
        handle_help(args)
        return

    if args[0] == "login":
        _handle_login(args[1:])
    elif args[0] == "logout":
        _handle_logout(args[1:])
    else:
        print("Unknown config `{}`".format(args[0]))
