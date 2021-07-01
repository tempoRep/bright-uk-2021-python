"""A video playlist class."""

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self):
        self._videos = {}

    def add_video(self, video):
        if video.video_id in self._videos.keys():
            raise ValueError("Video already exist")

        self._videos[video.video_id] = video

    def remove_video(self, video):
        return self._videos.pop(video.video_id)

    def remove_all_videos(self):
        return self._videos.clear()
    
    def get_all_videos(self):
        return self._videos.values()