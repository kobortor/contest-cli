#!/usr/bin/env python3

from typing import *
from utils import Settings, get_problem_submit_url, get_session, get_submission_url
from bs4 import BeautifulSoup


def handle_submit(args: List[str]):
    if len(args) != 0:
        print("Please do not include any arguments after 'submit'")
        return

    settings = Settings.get_saved()
    if not settings.has_problem():
        print("You don't seem to have a problem set up")
        return

    submit_url = get_problem_submit_url(settings.problem_id)
    session = get_session()
    r1 = session.get(submit_url)

    if r1 is None or r1.status_code != 200 or r1.url != submit_url:
        print("Error getting submit page. Check your internet connection or login.")
        return

    soup = BeautifulSoup(r1.text, 'html.parser')
    options = soup.find("select", {"id": "id_language"}).find_all("option")

    csrfmiddlewaretoken = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    language_id = None
    for option in options:
        if option["data-name"] == settings.language.name:
            language_id = option["data-id"]
            break

    if language_id is None:
        print("Looks like your language is not supported on this language")
        return

    r2 = session.post(submit_url, data={
        "csrfmiddlewaretoken": csrfmiddlewaretoken,
        "source": open(settings.working_file, "r").read(),
        "language": language_id,
        "judge": ""
    }, headers={"referer": r1.url})

    if r2 is None or r2.status_code != 200:
        print("Error submitting")
        return

    submission_id = r2.url[r2.url.rfind("/")+1:]

    print("Check {}".format(get_submission_url(submission_id)))
