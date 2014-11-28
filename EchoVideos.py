import dateutil.parser
import operator
import sys

from EchoVideo import EchoVideo

class EchoVideos(object):

    def __init__(self, videos_json, titles):
        assert(videos_json is not None)

        self._videos = []
        for video_json in videos_json:
            video_date = EchoVideo.get_date(video_json)
            video_title = self._get_title(titles, video_date)
            self._videos.append(EchoVideo(video_json, video_title))

        self._videos.sort(key=operator.attrgetter("date"))

    @property
    def videos(self):
        return self._videos

    def _get_title(self, titles, date):
        if titles is None:
            return ""

        try:
            for title in titles:
                title_date = dateutil.parser.parse(title["date"]).date()
                if date == title_date:
                    return title["title"].encode("ascii")
            return ""

        except KeyError as e:
            blow_up("Unable to parse either titles or course_data JSON", e)

    def _blow_up(self, str, e):
        print str
        print "Exception: {}".format(str(e))
        sys.exit(1)
