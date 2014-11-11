import json
import sys

from selenium import webdriver
from EchoVideos import EchoVideos


class EchoCourse(object):

    def __init__(self, uuid, titles=None):
        self._course_id = ""
        self._uuid = uuid
        self._titles = titles
        self._videos = None
        
        self._hostname = "http://recordings.engineering.illinois.edu"
        self._url = "{}/ess/portal/section/{}".format(self._hostname, self._uuid)
        self._video_url = "{}/ess/client/api/sections/{}/section-data.json?pageSize=100".format(self._hostname, self._uuid)

    def get_videos(self, driver):
        if not self._videos:
            try:
                course_data_json = self._get_course_data(driver)
                videos_json = course_data_json["section"]["presentations"]["pageContents"]
                self._videos = EchoVideos(videos_json, self._titles)
            except KeyError as e:
                self._blow_up("Unable to parse course videos from JSON (course_data)", e)

        return self._videos

    @property
    def uuid(self):
        return self._uuid

    @property
    def hostname(self):
        return self._hostname

    @property
    def url(self):
        return self._url

    @property
    def video_url(self):
        return self._video_url

    @property
    def course_id(self):
        if self._course_id == "":
            try:
                driver = webdriver.PhantomJS() #TODO Redo this. Maybe use a singleton factory to request the lecho360 driver?s
                driver.get(self._url) # Initialize to establish the 'anon' cookie that Echo360 sends.
                driver.get(self._video_url) # Initialize to establish the 'anon' cookie that Echo360 sends.
                course_data_json = self._get_course_data(driver)

                self._course_id = course_data_json["section"]["course"]["identifier"]
            except KeyError as e:
                self._blow_up("Unable to parse course id (e.g. CS473) from JSON (course_data)", e)

        return self._course_id

    def _get_course_data(self, driver):
            try:
                driver.get(self.video_url)
                json_str = driver.find_element_by_tag_name("pre").text

                return json.loads(json_str)
            except ValueError as e:
                self._blow_up("Unable to retrieve JSON (course_data) from url", e)

    def _blow_up(self, msg, e):
        print msg
        print "Exception: {}".format(str(e))
        sys.exit(1)     