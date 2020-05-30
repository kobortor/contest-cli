from typing import *
from utils import get_session, get_problem_url, get_problem_api_url, get_settings, get_regex_matcher
from bs4 import BeautifulSoup
import pickle
import json
import os

def handle_make(args: List[str]):
    if len(args) != 1:
        print("Expected exactly 1 argument after `make`")
        return

    problem_id = args[0]

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
            if text.startswith("Sample Input "):
                idx = text[13:]
                ext = "in"
            elif text.startswith("Sample Output "):
                idx = text[14:]
                ext = "out"
        elif child.name == "pre" and idx and ext:
            dct["{}.{}".format(idx, ext)] = child.find("code").text.strip()

    settings = get_settings()

    problem_name = api_data["name"]
    languages = api_data["languages"]

    if settings.language not in languages:
        print("Your language ({}) is not supported. Please change to one from {} before submitting.".format(settings.language, languages))

    os.makedirs(settings.sample_data_folder, exist_ok=True)
    for (k, v) in dct.items():
        with open(os.path.join(settings.sample_data_folder, k), "w") as f:
            f.write(v)

    with open(os.path.join(settings.sample_data_folder, "problem_attrs.json"), "w") as f:
        f.write(json.dumps({
            "languages": languages,
            "samples": list(k[:-3] for k in dct.keys() if k.endswith(".in") and k[:-3] + ".out" in dct)
            }))

    regex_matcher = get_regex_matcher()
    output_base_filename = regex_matcher(problem_id)

    print("Get raw name {}".format(output_base_filename))
