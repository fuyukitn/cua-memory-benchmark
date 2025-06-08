from flask import session
def init_logs():
    if "logs" not in session:
        session["logs"] = []

def add_log(event):
    init_logs()
    session["logs"].append(event)
    session.modified = True

def get_logs():
    init_logs()
    return session ["logs"]

def reset_logs():
    session["logs"] = []
