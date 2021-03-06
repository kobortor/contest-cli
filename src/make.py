from typing import *
from utils import get_session, get_problem_url, get_problem_api_url, Settings, RegExMatcher
from bs4 import BeautifulSoup
import json
import os


def handle_make(args: List[str]) -> None:
    settings = Settings.get_saved()

    cur_dir_name = os.path.basename(os.getcwd())

    if settings.allowed_paths:
        # Check if path is not allowed
        allowed = False
        basename = os.path.basename(os.getcwd())
        for path in settings.allowed_paths:
            if os.path.expanduser(path).startswith(os.getcwd()) or path == basename:
                allowed = True
                break

        if not allowed:
            print("You don't seem to be in one of these directories: {}".format(settings.allowed_paths))
            return

    if len(args) != 1:
        print("Expected exactly 1 argument after `make`")
        return

    problem_id = args[0]

    if not settings.has_language():
        print("You don't seem to have a template. Please set one up using `dmoj config template`")
        return

    sess = get_session()
    if sess is None:
        print("No session: please log in using `config login`")
        return

    r = sess.get(get_problem_url(problem_id))
    if r.status_code != 200:
        print("Error: status code {}".format(r.status_code))
        return

    soup = BeautifulSoup(r.text, "html.parser")

    r = sess.get(get_problem_api_url(problem_id))

    if r.status_code != 200:
        print("Error: status code {}".format(r.status_code))
        return

    api_data = json.loads(r.text)

    content = soup.find("div", "content-description").find("div")

    dct = {}

    idx = ""
    ext = ""

    for child in content.children:
        if child.name == "h4":
            text = child.text.strip()
            if text.startswith("Sample Input"):
                idx = text[13:].strip()
                if not idx:
                    idx = "unnamed"
                ext = "in"
            elif text.startswith("Sample Output"):
                idx = text[14:].strip()
                if not idx:
                    idx = "unnamed"
                ext = "out"
        elif child.name == "pre" and idx and ext:
            if "{}.{}".format(idx, ext) not in dct:
                code = child.find("code")
                dct["{}.{}".format(idx, ext)] = code.text.strip()

    problem_name = api_data["name"]
    languages = api_data["languages"]

    if settings.language.code not in languages:
        print("Your language ({}) is not supported. Please change to one from {} before submitting.".format(settings.language.code, languages))

    os.makedirs(settings.sample_data_folder, exist_ok=True)
    for (k, v) in dct.items():
        with open(os.path.join(settings.sample_data_folder, k), "w") as f:
            f.write(v)

    json.dump(
        {
            "languages": languages,
            "samples": list(k[:-3] for k in dct.keys() if k.endswith(".in") and k[:-3] + ".out" in dct)
        },
        open(os.path.join(settings.sample_data_folder, "problem_attrs.json"), "w"),
        sort_keys=True, indent=4)

    regex_matcher = RegExMatcher.get_default()
    output_base_filename = regex_matcher(problem_id)
    output_full_filename = os.path.join(os.getcwd(), output_base_filename + "." + settings.language.suffix)

    os.makedirs(os.path.dirname(output_full_filename), exist_ok=True)

    settings.set_problem(problem_id, output_full_filename)
    settings.save()
    
    with open(settings.template_filename, "r") as fin, open(output_full_filename, "w") as fout:
        for line in fin:
            # TODO: replace things like ${username} and whatnot
            fout.write(line)
