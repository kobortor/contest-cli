import os
import re
import json
import pickle
from typing import *
from cfscrape import CloudflareScraper


class Language:
    def __init__(self, code: str, is_compiled: bool, compile_fmt_str: str, run_fmt_str: str, suffix: str, outfile: str,
                 name: str):
        self.code = code
        self.is_compiled = is_compiled
        self.compile_fmt_str = compile_fmt_str
        self.run_fmt_str = run_fmt_str
        self.suffix = suffix
        self.outfile = outfile
        self.name = name

    @staticmethod
    def get_by_code(code: str) -> Optional["Language"]:
        languages_filename = os.path.expanduser("~/.contest-cli/dmoj/languages.json")
        if os.path.exists(languages_filename):
            data = json.load(open(languages_filename, "r"))
            if code in data:
                return Language(
                        code,
                        data[code]["is_compiled"],
                        data[code].get("compile_fmt_str", ""),
                        data[code]["run_fmt_str"],
                        data[code]["suffix"],
                        data[code].get("outfile", ""),
                        data[code]["name"])

        return None

    @staticmethod
    def get_all() -> Dict[str, "Language"]:
        languages_filename = os.path.expanduser("~/.contest-cli/dmoj/languages.json")
        if os.path.exists(languages_filename):
            return json.load(open(languages_filename, "r"))
        else: 
            return {}


class Settings:
    def __init__(self, dct: Dict[str, str]):
        self.sample_data_folder = dct.get("sample_data_folder", "data")
        self.allowed_paths = dct.get("allowed_paths", [])

        if "language_code" in dct:
            self.language = Language.get_by_code(dct["language_code"])
        else:
            self.language = None

        self.template_filename = dct.get("template_filename", None)

        self.working_problem_id = dct.get("problem_id", None)
        self.working_file = dct.get("working_file", None)
        self.last_build_time = dct.get("last_build_time", None)
        self.problem_id = dct.get("problem_id", None)

    @staticmethod
    def get_saved() -> "Settings":
        setting_filename = os.path.expanduser("~/.contest-cli/dmoj/settings.json")
        if os.path.exists(setting_filename):
            return Settings(json.load(open(setting_filename, "r")))
        else:
            return Settings({})

    def save(self) -> None:
        setting_filename = os.path.expanduser("~/.contest-cli/dmoj/settings.json")
        os.makedirs(os.path.dirname(setting_filename), exist_ok=True)
        dct = {
            "sample_data_folder": self.sample_data_folder,
            "allowed_paths": self.allowed_paths
        }

        if self.language is not None:
            dct["language_code"] = self.language.code

        if self.template_filename is not None:
            dct["template_filename"] = self.template_filename

        if self.working_file is not None:
            dct["working_file"] = self.working_file

        if self.problem_id is not None:
            dct["problem_id"] = self.problem_id

        if self.last_build_time is not None:
            dct["last_build_time"] = self.last_build_time

        json.dump(dct, open(setting_filename, "w"), sort_keys=True, indent=4)

    def has_language(self) -> bool:
        return self.language and self.template_filename

    def set_language(self, language: Language, template_filename: str) -> None:
        self.language = language
        self.template_filename = template_filename
        self.working_file = None
        self.last_build_time = None

    def has_problem(self) -> bool:
        return  self.has_language() and \
                self.working_file and self.problem_id

    def set_problem(self, problem_id: str, working_file: str) -> None:
        self.problem_id = problem_id
        self.working_file = working_file
        self.last_build_time = None


class RegExMatcher:
    def __init__(self, lst):
        self.lst = [(d["regexp"], d["replacement"]) for d in lst]

    def __call__(self, s):
        for (regexp, replacement) in self.lst:
            tmp = re.subn(regexp, replacement, s)
            if tmp[1] != 0:
                return tmp[0]

        raise KeyError("No matching regular expressions found")

    @staticmethod
    def get_default():
        regex_pattern_filename = os.path.expanduser("~/.contest-cli/dmoj/patterns.json")
        if os.path.exists(regex_pattern_filename):
            return RegExMatcher(json.load(open(regex_pattern_filename, "r")))
        else:
            return RegExMatcher([{
                    "regexp": "^(.*)$",
                    "replacement": "uncategorized/\\1"
                }])


def get_login_url() -> str:
    return "https://dmoj.ca/accounts/login/"


def get_problem_url(problem_id: str) -> str:
    return "https://dmoj.ca/problem/{}".format(problem_id)


def get_problem_submit_url(problem_id: str) -> str:
    return "https://dmoj.ca/problem/{}/submit".format(problem_id)


def get_problem_api_url(problem_id: str) -> str:
    return "https://dmoj.ca/api/problem/info/{}".format(problem_id)


def get_submission_url(submission_id: str) -> str:
    return "https://dmoj.ca/submission/{}".format(submission_id)


def get_submission_update_url(submission_id: str) -> str:
    return "https://dmoj.ca/widgets/submission_testcases?id={}".format(submission_id)


def get_session() -> Optional[CloudflareScraper]:
    login_session_filename = os.path.expanduser("~/.contest-cli/dmoj/login.pkl")
    if os.path.exists(login_session_filename):
        # TODO: check for sanity
        return pickle.load(open(login_session_filename, "rb"))
    else:
        return None


def delete_session() -> None:
    login_session_filename = os.path.expanduser("~/.contest-cli/dmoj/login.pkl")
    os.remove(login_session_filename)


def save_session(s) -> None:
    login_session_filename = os.path.expanduser("~/.contest-cli/dmoj/login.pkl")
    os.makedirs(os.path.dirname(login_session_filename), exist_ok=True)
    pickle.dump(s, open(login_session_filename, "wb"))
