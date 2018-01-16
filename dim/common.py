import os
import json


HISTORY_PATH = "/usr/share/dim/.history.json"


def get_local_images(docker_client):
    """Return a list of local images names (repo+tag).

    :param docker.client.APIClient docker_client: docker api client.
    :return list local_images: local images names (repo+tag).
    """
    local_images = []
    for image in docker_client.images():
        local_images.extend(image['RepoTags'])

    return local_images


def save_history(data):
    """Save history to file."""
    dir_path = os.path.dirname(HISTORY_PATH)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    json.dump(data, open(HISTORY_PATH, "w"))


def load_history():
    """Load history from file, on failure start fresh"""
    if not os.path.exists(HISTORY_PATH):
        return {}
    try:
        return json.load(open(HISTORY_PATH, "r"))
    except:
        return {}
