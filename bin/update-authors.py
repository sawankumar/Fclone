#!/usr/bin/env python3
"""
Update the authors.md file with the authors from the git log
"""

import re
import subprocess

AUTHORS = "docs/content/authors.md"
IGNORE = "bin/.ignore-emails"

def load(filename):
    """
    returns a set of emails already in the file
    """
    with open(filename) as fd:
        authors = fd.read()
    return set(re.findall(r"<(.*?)>", authors))

def add_email(name, email):
    """
    adds the email passed in to the end of authors.md
    """
    print("Adding %s <%s>" % (name, email))
    with open(AUTHORS, "a+") as fd:
        print("  * %s <%s>" % (name, email), file=fd)
    subprocess.check_call(["git", "commit", "-m", "Add %s to contributors" % name, AUTHORS])
    
def main():
    out = subprocess.check_output(["git", "log", '--reverse', '--format=%an|%ae', "master"])
    out = out.decode("utf-8")

    ignored = load(IGNORE)
    previous = load(AUTHORS)
    previous.update(ignored)
    for line in out.split("\n"):
        line = line.strip()
        if line == "":
            continue
        name, email = line.split("|")
        if email in previous:
            continue
        previous.add(email)
        add_email(name, email)

if __name__ == "__main__":
    main()
