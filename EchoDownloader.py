import os
import sys
import urllib2

from selenium import webdriver

# TODO
#  1. download_range
#  2. download_before
#  3. download_after
class EchoDownloader(object):

    def __init__(self, course, titles, output_dir):
        self._course = course

        self._driver = webdriver.PhantomJS()
        self._driver.get(self._course.url) # Initialize to establish the 'anon' cookie that Echo360 sends.
        
        self._output_dir = output_dir or ""
        self._titles = titles
        self._useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"
        self._videos = []

    def download_all(self):
        for i, video in enumerate(self._course.get_videos(self._driver).videos):
            title = video.title if (video.title != "") else "Lecture {}.m4v".format(i+1)
            filename = self._get_filename(self._course.course_id, video.date, video.title)

            print "Downloading {} of {}: {}".format(i+1, len(self._course.get_videos(self._driver).videos), video.url)
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