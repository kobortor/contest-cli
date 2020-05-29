from typing import *
from utils import get_session, get_problem_url
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
        print("Error: status code {}".format(r.status))
        return

    soup = BeautifulSoup(r.text, 'html.parser')

    problem_name = "".join(soup.find("div", "problem-title").find("h2").contents)
    content = soup.find("div", "content-description").find("div")

    output_filename = ""
    for child in content.children:
        if child.name == "h4":
            text = child.text.strip()
            if text.startswith("Sample Input "):
                output_filename = os.path.join(os.getcwd(), "data", text[13:] + ".in")
            elif text.startswith("Sample Output "):
                output_filename = os.path.join(os.getcwd(), "data", text[14:] + ".out")
        elif child.name == "pre" and output_filename:
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)
            with open(output_filename, "w") as f:
                f.write(child.find("code").text.strip())
                output_filename = ""
