import dateutil.parser
import sys

class EchoVideo(object):

    def __init__(self, video_json, title):
        self._title = title

        try:
            self._url = "{}/mediacontent.m4v".format(video_json["richMedia"].encode("ascii"))
            self._date = dateutil.parser.parse(video_json["startTime"]).date()
        except KeyError as e:
            self._blow_up("Unable to parse video data from JSON (course_data)", e)

    @property
    def title(self):
        return self._title

    @property
    def date(self):
        return self._date

    @property
    def url(self):
        return self._url

    def _blow_up(self, str, e):
        print str
        print "Exception: {}".format(str(e))
        sys.exit(1)