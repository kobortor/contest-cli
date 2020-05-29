from typing import *
from utils import get_session, get_problem_url, get_settings
from bs4 import BeautifulSoup
import pickle
import os

def handle_make(args: List[str]):
    if len(args) != 1:
        print("Expected exactly 1 argument after `make`")
        return

    sess = get_session()
    if sess is None:
        print("No session: please log in using `config login`")
        return

    url = get_problem_url(args[0])
    r = sess.get(url)
    if r.status_code != 200:
        print("Error: status code {}".format(r.status_code))
        return

    soup = BeautifulSoup(r.text, 'html.parser')

    problem_name = "".join(soup.find("div", "problem-title").find("h2").contents)
    content = soup.find("div", "content-description").find("div")

    print("Pull data for `{}`".format(problem_name))

    dct = {}

    idx = ""
    ext = ""

    settings = get_settings()

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
            filename = os.path.join(settings.sample_data_folder, "{}.{}".format(idx, ext))
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(child.find("code").text.strip())
                output_filename = ""
