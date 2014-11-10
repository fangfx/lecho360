import argparse
import dateutil.parser
import json
import os
import urllib2
import selenium

from selenium import webdriver

# Python requirements
# - dateutil
# - selenium
# NodeJS requirements
# - PhantomJS

def blow_up(str, e):
    print str
    print "Exception: %s" % str(e)
    sys.exit(1) 

def get_user_agent():
    return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"

def get_hostname():
    return "http://recordings.engineering.illinois.edu"

def get_course_data_url(course_uuid):
    return "{}/ess/client/api/sections/{}/section-data.json?pageSize=100".format(get_hostname(), course_uuid)

def get_course_url(course_uuid):
    return "{}/ess/portal/section/{}".format(get_hostname(), course_uuid)

def get_course_data(driver, url):
    try:
        driver.get(url)
        json_str = driver.find_element_by_tag_name("pre").text

        return json.loads(json_str)

    except ValueError as e:
        blow_up("Unable to retrieve JSON from url", e)

def get_course_id(course_data):
    try:
        return course_data["section"]["course"]["identifier"]
    except KeyError as e:
        blow_up("Malformed presenstation JSON (course id)", e)

def get_all_prez_data(course_data):
    try:
        return course_data["section"]["presentations"]["pageContents"]
    except KeyError as e:
        blow_up("Malformed presenstation JSON (presentations list)", e)

def get_prez_url(prez_data):
    try:
        return "{}/mediacontent.m4v".format(prez_data["richMedia"].encode("ascii"))
    except KeyError as e:
        blow_up("Malformed presenstation JSON (presentation url)", e)

def get_prez_date(prez_data):
    try:
        return dateutil.parser.parse(prez_data["startTime"]).date()

    except KeyError as e:
        blow_up("Malformed presenstation JSON (presentation date)", e)

def get_title(titles, prez_date):
    if titles is None:
        return ""

    try:
        for title in titles:
            if prez_date == dateutil.parser.parse(title["date"]).date():
                return title["title"]

        return ""

    except KeyError as e:
        blow_up("Malformed presenstation JSON (title)", e)


def get_filename(course, date, title):
    return "{} - {} - {}.m4v".format(course, date, title)

def download_as(url, filename):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', get_user_agent())
        opener = urllib2.build_opener()

        with open(filename.encode("ascii"), "wb") as local_file:
            local_file.write(opener.open(request).read())

    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url

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
    args = vars(parser.parse_args())
    uuid = args["uuid"]
    titles = None if args["titles"] == "" else args["titles"] 
    
    return (uuid, titles)

def main():
    course_uuid, titles = handle_args()
    if titles is not None:
        with open(titles, "r") as titles_json:
            titles = json.loads(titles_json.read())

    # Initialize our session so we can get the cookies loaded from their stupid iframe
    driver = webdriver.PhantomJS()
    driver.get(get_course_url(course_uuid))

    # Grab the JSON course data
    course_data = get_course_data(driver, get_course_data_url(course_uuid))
    prezs = get_all_prez_data(course_data)

    # Start downloading
    for i in xrange(0, len(prezs)):
        url = get_prez_url(prezs[i])
        user_agent = get_user_agent()

        course_id = get_course_id(course_data)
        prez_date = get_prez_date(prezs[i])

        title = get_title(titles, get_prez_date(prezs[i]))
        title = "Lecture {}.m4v".format(i+1) if (title == "") else title

        filename = get_filename(course_id, prez_date, title)

        print "Downloading {} of {}: {}".format(i+1, len(prezs), url)
        print "  to {}\n".format(filename)
        download_as(url, filename)


if __name__ == '__main__':
    main()