import time
import datetime
import argparse

import docker
import tabulate
import humanize

import dim.common as common

SORT_BY_TO_KEY = {
    'age': lambda (image, age): age,
    'image': lambda (image, age): image
}


def get_history(history, whitelist, reference_time, min_age=0, quiet=False, sort_by='age', reverse=False):
    """Return the image usage history using the given configuration.

    :param dict history: image usage history, of format {image name, last usage timestamp}.
    :param set whitelist: whitelist image names (repo+tag).
    :param int reference_time: reference time as epoch timestamp.
    :param int min_age: minimum image age in seconds.
    :param bool quiet: if set, returns only the image names.
    :param sort_by: one of (image, age), if set images will be sorted by that attribute.
    :param bool reverse: if set, the sort order will be reversed.

    :return list: images details by the required config.
    """
    history = filter_images(history, whitelist)

    # Get the image information form history - filter by min age
    data = [(image, reference_time - timestamp) for image, timestamp in history.items()
            if reference_time - timestamp >= min_age]

    if sort_by:
        # Sort by required attribute - supported attributes (age, image)
        data = sorted(data, key=SORT_BY_TO_KEY[sort_by], reverse=reverse)

    if quiet:
        # Keep only image names
        return [image for image, age in data]

    return [(image, humanize.naturaltime(datetime.timedelta(seconds=age))) for image, age in data]


def show_image_history(whitelist, quiet, sort_by, reverse, min_age):
    """Print the image history to the screen.

    :param set whitelist: whitelist image names (repo+tag).
    :param int min_age: minimum image age in seconds.
    :param bool quiet: if set, returns only the image names.
    :param sort_by: one of (image, age), if set images will be sorted by that attribute.
    :param bool reverse: if set, the sort order will be reversed.
    """
    history_data = get_history(
        quiet=quiet,
        min_age=min_age,
        sort_by=sort_by,
        reverse=reverse,
        whitelist=whitelist,
        reference_time=time.time(),
        history=common.load_history()
    )
    if quiet:
        print('\n'.join(history_data))

    else:
        print(tabulate.tabulate(tabular_data=history_data, headers=['Image', 'Last Start Time'], tablefmt='grid'))


def filter_images(history, whitelist):
    """Return a filtered history.

    - Remove images in whitelist.
    - Remove images which no longer exists.

    :param  list whitelist: whitelist image names (repo+tag).
    :param dict history: image usage history, of format {image name, last usage timestamp}
    """
    docker_client = docker.client.APIClient()
    local_images = common.get_local_images(docker_client)
    approved_images = set(local_images) - set(whitelist)
    return {image: timestamp for image, timestamp in history.items() if image in approved_images}


def main():
    """Image history display entry point."""
    parser = argparse.ArgumentParser(description='Display Images Last Start Time.')
    parser.add_argument('-q', '--quiet', action='store_true', help='If set, returns only the image names')
    parser.add_argument('-w', '--whitelist', type=argparse.FileType('r'), help='Images whitelist file')
    parser.add_argument('-m', '--min-age', type=int, default=0, help='Minimum image age in seconds')
    parser.add_argument('-r', '--reverse', action='store_true', help='If set images will be sorted by reversed order')
    parser.add_argument('-s', '--sort-by', type=str, choices=['age', 'image'], default='age',
                        help='If set images will be sorted by that attribute')
    args = parser.parse_args()

    whitelist = set()
    if args.whitelist:
        whitelist = set([image.strip() for image in args.whitelist.readlines()])

    show_image_history(
        whitelist=whitelist,
        quiet=args.quiet,
        min_age=args.min_age,
        sort_by=args.sort_by,
        reverse=args.reverse,
    )


if __name__ == '__main__':
    main()
