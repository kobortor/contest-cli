import os
import re
import json
import pickle


class Settings:
    def __init__(self, dct):
        self.sample_data_folder = dct.get("sample_data_folder", "data")
        self.language = dct.get("language", "CPP17")
        self.allowed_paths = dct.get("allowed_paths", [])

def get_settings():
    setting_filename = os.path.expanduser("~/.contest-cli/dmoj-defaults/settings.json")
    if os.path.exists(setting_filename):
        return Settings(json.load(open(setting_filename, "r")))
    else:
        return Settings({})



class RegExMatcher:
    def __init__(self, lst):
        self.lst = [(d["regexp"], d["replacement"]) for d in lst]

    def __call__(self, s):
        for (regexp, replacement) in self.lst:
            tmp = re.subn(regexp, replacement, s)
            if tmp[1] != 0:
                return tmp[0]

        raise KeyError("No matching regular expressions found")

def get_regex_matcher():
    regex_pattern_filename = os.path.expanduser("~/.contest-cli/dmoj-defaults/patterns.json")
    if os.path.exists(regex_pattern_filename):
        return RegExMatcher(json.load(open(regex_pattern_filename, "r")))
    else:
        return RegExMatcher([{
                "regexp": "^(.*)$",
                "replacement": "uncategorized/\\1"
            }])

def get_login_url():
    return "https://dmoj.ca/accounts/login/"

def get_problem_url(problem):
    return "https://dmoj.ca/problem/{}".format(problem)

def get_problem_api_url(problem):
    return "https://dmoj.ca/api/problem/info/{}".format(problem)

def get_session():
    login_session_filename = os.path.expanduser("~/.contest-cli/dmoj/login.pkl")
    if os.path.exists(login_session_filename):
        # TODO: check for sanity
        return pickle.load(open(login_session_filename, "rb"))
    else:
        return None

def delete_session():
    login_session_filename = os.path.expanduser("~/.contest-cli/dmoj/login.pkl")
    os.remove(login_session_filename)

def save_session(s):
    login_session_filename = os.path.expanduser("~/.contest-cli/dmoj/login.pkl")
    os.makedirs(os.path.dirname(login_session_filename), exist_ok=True)
    pickle.dump(s, open(login_session_filename, "wb"))


