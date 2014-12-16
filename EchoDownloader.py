import dateutil.parser
import os
import sys
import urllib2

from selenium import webdriver


class EchoDownloader(object):

    def __init__(self, course, output_dir, date_range):
        self._course = course
        self._output_dir = output_dir
        self._date_range = date_range

        self._useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"
        self._driver = webdriver.PhantomJS()
        # Initialize to establish the 'anon' cookie that Echo360 sends.
        self._driver.get(self._course.url)

        self._videos = []

    def download_all(self):
        videos = self._course.get_videos(self._driver).videos
        filtered_videos = [video for video in videos if self._in_date_range(video.date)]
        total_videos = len(filtered_videos)

        # Download the newest video first but maintain it's original index
        # in case a JSON file isn't passed (and we need to label them as
        # Lecture 1, 2, ...)
        for i, video in reversed(list(enumerate(filtered_videos))):
            # TODO Check if the lecture number is included in the JSON object.
            lecture_number = self._find_pos(videos, video)
            title = video.title if (video.title != "") else "Lecture {}".format(lecture_number+1)
            filename = self._get_filename(self._course.course_id, video.date, title)

            print "Downloading {} of {}: {}".format(total_videos - i, total_videos, video.url)
            print "  to {}\n".format(filename)
            self._download_as(video.url, filename)

    @property
    def useragent(self):
        return self._useragent

    @useragent.setter
    def useragent(self, useragent):
        self._useragent = useragent

    def _download_as(self, video, filename):
        try:
            request = urllib2.Request(video)
            request.add_header('User-Agent', self._useragent)
            opener = urllib2.build_opener()

            with open(os.path.join(self._output_dir, filename), "wb") as local_file:
                local_file.write(opener.open(request).read())

        except urllib2.HTTPError, e:
            print "HTTP Error:", e.code, video
        except urllib2.URLError, e:
            print "URL Error:", e.reason, video

    def _initialize(self, echo_course):
        self._driver.get(self._course.url)

    def _get_filename(self, course, date, title):
        return "{} - {} - {}.m4v".format(course, date, title)

    def _in_date_range(self, date_string):
        the_date = dateutil.parser.parse(date_string).date()
        return self._date_range[0] <= the_date and the_date <= self._date_range[1]


    def _find_pos(self, videos, the_video):
        for i, video in enumerate(videos):
            if video.date == the_video.date:
                return i

        return -1
