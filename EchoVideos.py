import dateutil.parser
import operator
import sys

from EchoVideo import EchoVideo

class EchoVideos(object):

    def __init__(self, videos_json, titles=None):
        assert(videos_json is not None)

        self._videos = []
        for video_json in videos_json:
            self._videos.append(EchoVideo(video_json, self._get_title(titles, video_json)))

        self._videos.sort(key=operator.attrgetter("date"))

    @property
    def videos(self):
        return self._videos

    def _get_title(self, titles, date):
        if titles is None:
            return ""

        try:
            for title in titles:
                if date == dateutil.parser.parse(title["date"]).date():
                    return title["title"]
            return ""

        except KeyError as e:
            blow_up("Unable to parse either titles or course_data JSON", e)

    def _blow_up(self, str, e):
        print str
        print "Exception: {}".format(str(e))
        sys.exit(1)