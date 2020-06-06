#!/usr/bin/env python3

import time
from typing import *
from utils import Settings, get_problem_submit_url, get_session, get_submission_url, get_submission_update_url
from bs4 import BeautifulSoup, element
from cfscrape import CloudflareScraper

STATUS_TO_COLOR_MAPPING = {
    "AC": '\033[0;32m',
    "WA": '\033[0;31m',
    "TLE": '\033[0;37m',
    "RTE": '\033[0;33m',
}


# Returns a string
def _format_case_row(case_row: element.Tag, color=True):
    testcase_data = list(case_row.find_all("td"))
    testcase_name = testcase_data[0].text.strip()
    testcase_status = testcase_data[1].text.strip()

    if testcase_status not in STATUS_TO_COLOR_MAPPING:
        return ""

    if color:
        testcase_status = "{}{}{}".format(
            STATUS_TO_COLOR_MAPPING[testcase_status],
            testcase_status,
            '\033[0m'
        )

    return "{} {}".format(testcase_name, testcase_status)


def _handle_submission_results(submission_id: str, session: CloudflareScraper):
    submission_update_url = get_submission_update_url(submission_id)

    finished_strings = [
        "Final score:",
        "An internal error occurred while grading."
        "Submission Aborted!",
        "Compilation Error"
    ]

    failed_tries = 0
    max_fail_attempts = 5
    last_attempt_time = 0
    delay = 0.5

    batch_index = 0
    testcase_index = 0

    while True:
        while time.time() - last_attempt_time < delay:
            pass

        last_attempt_time = time.time()
        # Tudor plz give better interface. Maybe JSON string?
        data = session.get(submission_update_url)
        if not data or data.status_code != 200:
            failed_tries += 1
            if failed_tries > max_fail_attempts:
                print("Something went wrong... Breaking!")
                break

            print("Failed attempt: re-attempt {} of {}".format(failed_tries, max_fail_attempts))

        soup = BeautifulSoup(data.text, "html.parser")
        batches = soup.find_all("table", "submissions-status-table")

        while batch_index < len(batches):
            testcases = list(batches[batch_index].find_all("tr", {"class": "case-row"}))
            if testcase_index == len(testcases):
                if batch_index + 1 < len(batches):
                    batch_index += 1
                    print("Batch ${}".format(batch_index))
                else:
                    break

            else:
                print("\t{}".format(_format_case_row(testcases[testcase_index])))
                testcase_index += 1

        if any(s in data.text for s in finished_strings):
            print("Finished")
            break


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

    submission_id = r2.url[r2.url.rfind("/") + 1:]
    if r2.url != get_submission_url(submission_id):
        print("Something went wrong with our submission. We were redirected to {}".format(r2.url))
        return

    _handle_submission_results(submission_id, session)
