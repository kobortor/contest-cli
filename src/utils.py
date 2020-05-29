import os
import pickle

def get_login_url():
    return "https://dmoj.ca/accounts/login/"

def get_problem_url(problem):
    return "https://dmoj.ca/problem/{}".format(problem)

def get_session():
    login_session_filename = os.path.expanduser("~/.config/dmoj-cli/login.pkl")
    if os.path.exists(login_session_filename):
        # TODO: check for sanity
        return pickle.load(open(login_session_filename, "rb"))
    else:
        return None

def save_session(s):
    os.makedirs(os.path.dirname(login_session_filename), exist_ok=True)
    pickle.dump(s, open(login_session_filename, "wb"))
