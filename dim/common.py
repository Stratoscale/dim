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
        image_repo_tag = image.get('RepoTags')
        if image_repo_tag:
            local_images.extend(image_repo_tag)

    return local_images


def save_history(data):
    """Save history to file."""
    json.dump(data, open(HISTORY_PATH, "w"))


def load_history():
    """Load history from file, on failure start fresh"""
    try:
        return json.load(open(HISTORY_PATH, "r"))
    except:
        return {}


def setup_history():
    """Create the history directory and file if they don't exists."""
    dir_path = os.path.dirname(HISTORY_PATH)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'w') as history_file:
            json.dump({}, history_file)
