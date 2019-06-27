import os
import urllib.request, json

COCKPIT_FILE = "cockpit.json"


def has_cockpit():
    return os.path.isfile(COCKPIT_FILE)


def load_cockpit():
    with open(COCKPIT_FILE, 'r') as c:
        return json.load(c)


def title_to_permalink(title):
    return title.replace(" ", "-").lower()


def request(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def ensure_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)
