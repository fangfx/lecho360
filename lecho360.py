import argparse
import json
import os

from EchoCourse import EchoCourse
from EchoDownloader import EchoDownloader

# Python requirements
# - dateutil
# - selenium
# NodeJS requirements
# - PhantomJS


def handle_args():
    parser = argparse.ArgumentParser(description="Download lectures from UIUC's Echo360 portal.")
    parser.add_argument("--uuid", required=True, help="The Echo360 UUID for the course, which is \
                                                       found in the URL of the video lecture's page \
                                                       (e.g. FA2013 CS473's UUID: a0143734-86e8-4d0a-aba1-a44715ec085c)")
    parser.add_argument("--titles", help="Path to JSON file containing array of titles and dates \
                                          (e.g. { ... titles: [{'date': '', title: ''}...] }. With a titles file, \
                                          the naming scheme is <COURSE ID> - <DATE> - <TITLE>.m4v. \
                                          Without a titles file, the naming schem is \
                                          <COURSE ID> - <DATE> - Lecture <number>.m4v")
    parser.add_argument("--output", help="Absolute path to the desired output directory")

    args = vars(parser.parse_args())
    course_uuid = args["uuid"]
    titles_path = None if args["titles"] == "" else args["titles"]
    output_dir = "" if args["output"] == "" else args["output"]

    return (course_uuid, titles_path, output_dir)

def main():
    course_uuid, titles_path, output_dir = handle_args()
    titles = None

    if titles_path is not None and os.path.isfile(titles_path):
        with open(titles_path, "r") as titles_json:
            data = json.load(titles_json)
            try:
                titles = data["titles"]
            except KeyError as e:
                titles = None

    course = EchoCourse(course_uuid, titles)
    downloader = EchoDownloader(course, output_dir)
    downloader.download_all()

def _blow_up(self, str, e):
    print str
    print "Exception: {}".format(str(e))
    sys.exit(1)


if __name__ == '__main__':
    main()
