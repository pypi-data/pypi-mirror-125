from logging import getLogger
from json_database import JsonStorageXDG
from tutubo.models import Channel, Playlist, Video
from youtube_archivist.exceptions import VideoUnavailable

LOG = getLogger("youtube_archivist")


class YoutubeArchivist:
    def __init__(self, db_name=None, required_kwords=None, blacklisted_kwords=None):
        self.required_kwords = required_kwords or []
        self.blacklisted_kwords = blacklisted_kwords or []
        self.db = JsonStorageXDG(db_name, subfolder="youtube_archivist")

    @property
    def video_urls(self):
        return list(self.db.keys())

    def archive(self, url):
        if "/watch" in url:
            return self.archive_video(url)
        if "/playlist" in url:
            return self.archive_playlist(url)
        return self.archive_channel(url)

    def archive_video(self, url, extra_data=None):
        urls = self.video_urls
        if isinstance(url, str):
            video = Video(url)
        else:
            video = url
        if video.watch_url not in urls:
            try:
                if any(k.lower() in video.title.lower() for k in
                       self.blacklisted_kwords):
                    return
                if any(k.lower() not in video.title.lower() for k in
                       self.required_kwords):
                    return
                print("Parsing video ", video.title)
                self._update_video(video, extra_data)
            except:
                # accessing the title property might cause a 404 if
                # video was removed
                raise

    def archive_playlist(self, url):
        c = Playlist(url)
        for video in c.videos:
            meta = {}
            try:
                meta = {"playlist": c.title}
            except:
                pass
            self.archive_video(video, meta)

    def archive_channel(self, url):
        c = Channel(url)
        for video in c.videos:
            meta = {}
            self.archive_video(video, meta)

    def archive_channel_playlists(self, url):
        c = Channel(url)
        for pl in c.playlists:
            for video in pl.videos:
                meta = {}
                try:
                    meta = {"playlist": pl.title}
                except:
                    pass

                try:
                    self.archive_video(video, meta)
                except VideoUnavailable:
                    continue

    def _update_video(self, entry, extra_data=None):
        if not entry:
            return
        url = entry.watch_url
        # format data for saving
        entry = {
            "author": entry.author,
            "title": entry.title,
            "url": entry.watch_url,
            "duration": entry.length,
            "upload_ts": entry.publish_date.timestamp(),
            "tags": entry.keywords,
            'thumbnail': entry.thumbnail_url
        }
        if extra_data:
            entry.update(extra_data)
        self.db[url] = entry
        self.db.store()

    # DB interaction
    def remove_unavailable(self):
        for url, entry in self.db.items():
            vid = Video(url)
            try:
                vid_data = {
                    "videoId": vid.video_id,
                    "url": vid.watch_url,
                    "image": vid.thumbnail_url,
                    "title": vid.title
                }
            except VideoUnavailable:
                self.db.pop(url)
                LOG.info("Removed entry: " + url)
        self.db.store()

    def remove_keyword(self, kwords):
        bad_urls = []
        for url, entry in self.db.items():
            name = entry["title"]
            if any([k.lower() in name.lower() for k in kwords]):
                bad_urls.append(url)

        for url in bad_urls:
            self.db.pop(url)
            LOG.info("Removed entry: " + url)
        self.db.store()

    def remove_missing(self, kwords):
        bad_urls = []
        for url, entry in self.db.items():
            if any([not entry.get(k) for k in kwords]):
                bad_urls.append(url)
        for url in bad_urls:
            self.db.pop(url)
            LOG.info("Removed entry: " + url)
        self.db.store()

    def remove_below_duration(self, minutes=30):
        bad_urls = []
        for url, entry in self.db.items():
            dur = entry.get("duration") or 0
            if dur <= minutes * 60:
                bad_urls.append(url)
        for url in bad_urls:
            self.db.pop(url)
            LOG.info("Removed entry: " + url)
        self.db.store()
