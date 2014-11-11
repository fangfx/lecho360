import argparse
import json
import os
#import selenium

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
                                                       found in the URL of the video lectures page \
                                                       (e.g. FA2013 CS473's UUID: a0143734-86e8-4d0a-aba1-a44715ec085c)")  # a2d3a94f-573c-464b-840b-b5dde6a12caa
    parser.add_argument("--titles", help="Path to JSON file containing array of titles and dates \
                                          (e.g. [{'date': '', title: ''}...]. With a titles file, \
                                          the naming scheme is <COURSE ID> - <DATE> - <TITLE>.m4v. \
                                          Without a titles file, the naming schem is \
                                          <COURSE ID> - <DATE> - Lecture <number>.m4v")
    parser.add_argument("--output", help="Absolute path to the desired output directory")
    
    args = vars(parser.parse_args())
    uuid = args["uuid"]
    titles = None if args["titles"] == "" else args["titles"] 
    output_dir = "" if args["output"] == "" else args["output"]

    return (uuid, titles, output_dir)

def main():
    course_uuid, titles, output_dir = handle_args()
    if titles is not None and os.path.isfile(titles):
        with open(titles, "r") as titles_json:
            titles = json.loads(titles_json.read())
    else:
        titles = {}

    course = EchoCourse(course_uuid)
    downloader = EchoDownloader(course, titles, output_dir)
    downloader.download_all()


if __name__ == '__main__':
    main()