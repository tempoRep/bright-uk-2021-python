"""A video player class."""

from os import name
import random
import string
import re
from .video_library import VideoLibrary
from .video_playlist import Playlist

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._is_video_paused = None
        self._playlist_libary = {}
    
    @property
    def current_video(self):
        return self._current_video

    @current_video.setter
    def current_video(self, new_value):
        self._current_video = new_value

        if new_value is None:
            self._is_video_paused = None
        else:
            self._is_video_paused = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = self._video_library.get_all_videos()
        videos.sort(key=lambda x: x.title)

        for video in videos:
            print(f"    {video}")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print(f"Cannot play video: Video does not exist")
            return

        if video.is_flagged():
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag_status()})")
            return
        
        if self.current_video != None:
            print(f"Stopping video: {self.current_video.title}")

        self.current_video = video
        print(f"Playing video: {self.current_video.title}")

    def stop_video(self):
        """Stops the current video."""
        if self.current_video is None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self.current_video.title}")
            self.current_video = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos() 
        videos = list(filter(lambda x: not x.is_flagged(), videos))
        if len(videos) == 0:
            print("No videos available")
            return

        video = random.choice(videos)
        self.play_video(video.video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.current_video is None:
            print("Cannot pause video: No video is currently playing")
            return

        assert self._is_video_paused != None
        if self._is_video_paused:
            print(f"Video already paused: {self.current_video.title}")
        else:
            print(f"Pausing video: {self.current_video.title}")
            self._is_video_paused = True
        
    def continue_video(self):
        """Resumes playing the current video."""
        if self.current_video is None:
            print("Cannot continue video: No video is currently playing")
            return

        assert self._is_video_paused != None
        if self._is_video_paused:
            print(f"Continuing video: {self.current_video.title}")
            self._is_video_paused = False
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.current_video is None:
            print("No video is currently playing")
            return

        assert self._is_video_paused != None
        print(f"Currently playing: {self.current_video}{' - PAUSED' if self._is_video_paused else ''}")

    def __case_insensitive_key_exist(self, dict, key):
        return key.lower() in [key.lower() for key in dict.keys()]

    def __case_insensitive_fetch(self, dict, key):
        for stored in dict.keys():
            if stored.lower() == key.lower():
                return dict[stored]
        raise KeyError

    def __case_insensitive_pop(self, dict, key):
        for stored in dict.keys():
            if stored.lower() == key.lower():
                return dict.pop(stored)
        raise KeyError

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # check for whitespace
        if any(c in playlist_name for c in string.whitespace):
            raise ValueError("Playlist name cannot contain whitespace")
        
        if self.__case_insensitive_key_exist(self._playlist_libary, playlist_name):
            print("Cannot create playlist: A playlist with the same name already exists")
            return
            # should throw error
            # raise ValueError("Playlist name already exist")
        
        self._playlist_libary[playlist_name] = Playlist()
        print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        try:
            playlist = self.__case_insensitive_fetch(self._playlist_libary, playlist_name)
        except KeyError:
            print("Cannot add video to another_playlist: Playlist does not exist")
            return

        video = self._video_library.get_video(video_id)
        if video is None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        if video.is_flagged():
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag_status()})")
            return
        
        try:
            playlist.add_video(video)
            print(f"Added video to {playlist_name}: {video.title}")  
        except ValueError:
            print(f"Cannot add video to {playlist_name}: Video already added")
            
    def show_all_playlists(self):
        """Display all playlists."""
        if not self._playlist_libary:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        for playlist_name in sorted(self._playlist_libary.keys()):
            print(f"    {playlist_name}")
        
    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            playlist = self.__case_insensitive_fetch(self._playlist_libary, playlist_name)
        except KeyError:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        print(f"Showing playlist: {playlist_name}")

        videos = playlist.get_all_videos()
        if not videos:
            print("    No videos here yet")
            return
        
        for video in videos:
            print(f"    {video}")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        try:
            playlist = self.__case_insensitive_fetch(self._playlist_libary, playlist_name)
        except:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        
        video = self._video_library.get_video(video_id)
        if video is None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        try:
            removed_video = playlist.remove_video(video)
            print(f"Removed video from {playlist_name}: {removed_video.title}")
        except KeyError:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            playlist = self.__case_insensitive_fetch(self._playlist_libary, playlist_name)
        except:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return

        playlist.remove_all_videos()
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            self.__case_insensitive_pop(self._playlist_libary, playlist_name)
            print(f"Deleted playlist: {playlist_name}")
        except KeyError:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def __is_not_alpha(self, s):
        pattern = re.compile("^[a-zA-Z]+$")
        return pattern.match(s) is None

    def __is_not_tag(self, s):
        pattern = re.compile("^#?[a-zA-Z]+$")
        return pattern.match(s) is None

    def __ask_user_to_play(self, search_term, searched_videos):
        if not searched_videos:
            print(f"No search results for {search_term}")
            return

        print(f"Here are the results for {search_term}:")
        for index, video in enumerate(searched_videos):
            print(f"{index+1}) {video}")
        
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        number = input()
        try:
            number = int(number)
            played_video = searched_videos[number-1]
            self.play_video(played_video.video_id)
        except ValueError:
            return
        except IndexError:
            return

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        if self.__is_not_alpha(search_term) and len(search_term) != 0:
            raise ValueError("Invalid search terms")

        pattern = re.compile(search_term, re.IGNORECASE)
        searched_videos = [video for video in self._video_library.get_all_videos() if pattern.search(video.title) is not None and not video.is_flagged()]
        searched_videos.sort(key=lambda x: x.title)

        self.__ask_user_to_play(search_term, searched_videos)
        
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        if self.__is_not_tag(video_tag) and len(video_tag) != 0:
            raise ValueError("Invalid tag format")

        searched_videos = []
        pattern = re.compile(f"^{video_tag}$", re.IGNORECASE)
        for video in self._video_library.get_all_videos():
            if any([pattern.match(tag) is not None for tag in video.tags]) and not video.is_flagged():
                searched_videos.append(video)
        searched_videos.sort(key=lambda x: x.title)

        self.__ask_user_to_play(video_tag, searched_videos)
        
    def flag_video(self, video_id, flag_reason=None):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot flag video: Video does not exist")
            return

        try:
            video.flag(flag_reason)

            if self.current_video is not None and self.current_video.video_id == video.video_id:
                self.stop_video()

            print(f"Successfully flagged video: {video.title} (reason: {video.flag_status()})")
        except RuntimeError:
            print("Cannot flag video: Video is already flagged")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot remove flag from video: Video does not exist")
            return

        try:
            video.unflag()
            print(f"Successfully removed flag from video: {video.title}")
        except RuntimeError:
            print("Cannot remove flag from video: Video is not flagged")