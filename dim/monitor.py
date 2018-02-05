import logging
import datetime

import docker

import dim.common as common

logger = logging.getLogger('dim')
logging.basicConfig(level=logging.INFO)


def monitor(docker_client):
    """Listen on docker events and register image usage time.

    :param docker.client.APIClient docker_client: docker api client.
    """
    common.setup_history()
    history = common.load_history()

    logger.info("Starting image-monitor")
    for event in docker_client.events(since=0, filters={"event": "start"}, decode=True):

        try:
            image, timestamp = get_event_details(event)

            if timestamp <= history.get(image, 0):
                logger.debug("Past event: usage time %s image %r, skipping", ts_to_string(timestamp), image)
                continue

            logger.info("Usage time %s image %r", ts_to_string(timestamp), image)
            history[image] = timestamp
            clean_missing_images(docker_client, history)
            common.save_history(data=history)

        except:
            logger.exception("Failed processing event, skipping")


def get_event_details(event):
    """Extract event image and timestamp - image with no tag will be tagged as latest.

    :param dict event: start container event dictionary.
    :return tuple: (container image, last use timestamp).
    """
    image = str(event['from'] if ":" in event['from'] else event['from'] + ":latest")
    timestamp = event['time']
    return image, timestamp


def clean_missing_images(docker_client, history):
    """Remove images which no longer exists from history.

    :param docker.client.APIClient docker_client: docker api client.
    :param dict history: image usage history, of format {image name, last usage timestamp}
    """
    local_images = common.get_local_images(docker_client)
    images_to_clean = [image for image in history if image not in local_images]
    for image in images_to_clean:
        history.pop(image)


def ts_to_string(timestamp):
    """Convert timestamp to date-time string."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def main():
    monitor(docker_client=docker.client.APIClient())


if __name__ == '__main__':
    main()
