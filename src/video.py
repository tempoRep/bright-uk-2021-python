"""A video class."""

import re
from typing import Optional, Sequence

class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)


        self._flag = False
        self._flag_reason = None

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    def __is_valid_reason(self, s):
        pattern = re.compile("^[a-zA-Z_]+$")
        return pattern.match(s) is not None

    def flag(self, reason=None):
        if self._flag:
            raise RuntimeError("Video has already been flagged")
        
        assert(reason is None or (isinstance(reason, str) and self.__is_valid_reason(reason)))
        self._flag = True
        self._flag_reason = reason

    def unflag(self):
        if not self._flag:
            raise RuntimeError("Video is not flagged")

        self._flag = False
        self._flag_reason = None

    def is_flagged(self) -> bool:
        return self._flag

    def flag_status(self) -> Optional[str]:
        if not self._flag:
            return None

        return "Not supplied" if self._flag_reason is None else self._flag_reason

    def __str__(self):
        formatted_tags = ' '.join([f"{tag}" for tag in self.tags])
        return f"{self.title} ({self.video_id}) [{formatted_tags}]{' - FLAGGED (reason: ' + self.flag_status() + ')' if self.is_flagged() else ''}"