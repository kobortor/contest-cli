import os
import re
import json
import pickle


class Language:
    def __init__(self, name, compile_fmt_str, run_fmt_str, suffix):
        self.name = name
        self.compile_fmt_str = compile_fmt_str
        self.run_fmt_str = run_fmt_str
        self.suffix = suffix

    @staticmethod
    def get_by_name(name):
        languages_filename = os.path.expanduser("~/.contest-cli/dmoj/languages.json")
        if os.path.exists(languages_filename):
            data = json.load(open(languages_filename, "r"))
            if name in data:
                return Language(name, data[name]["compile_fmt_str"], data[name]["run_fmt_str"], data[name]["suffix"])

        return None

    @staticmethod
    def get_all():
        languages_filename = os.path.expanduser("~/.contest-cli/dmoj/languages.json")
        if os.path.exists(languages_filename):
            return json.load(open(languages_filename, "r"))
        else: 
            return []


class Settings:
    def __init__(self, dct):
        self.sample_data_folder = dct.get("sample_data_folder", "data")
        self.allowed_paths = dct.get("allowed_paths", [])

        if "language" in dct:
            self.language = Language.get_by_name(dct["language"])
        else:
            self.language = None

        self.template_filename = dct.get("template_filename", None)

    @staticmethod
    def get_saved():
        setting_filename = os.path.expanduser("~/.contest-cli/dmoj/settings.json")
        if os.path.exists(setting_filename):
            return Settings(json.load(open(setting_filename, "r")))
        else:
            return Settings({})

    def save(self):
        setting_filename = os.path.expanduser("~/.contest-cli/dmoj/settings.json")
        os.makedirs(os.path.dirname(setting_filename), exist_ok=True)
        dct = {
            "sample_data_folder": self.sample_data_folder,
            "allowed_paths": self.allowed_paths
            }

        if self.language is not None:
            dct["language"] = self.language.name

        if self.template_filename is not None:
            dct["template_filename"] = self.template_filename

        with open(setting_filename, "w") as f:
            f.write(json.dumps(dct, sort_keys=True, indent=4))

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
    regex_pattern_filename = os.path.expanduser("~/.contest-cli/dmoj/patterns.json")
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


