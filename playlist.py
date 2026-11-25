"""Playlist class."""
import random


class Playlist:
    """A named, ordered collection of songs."""

    def __init__(self, name):
        self.name = name
        self.songs = []

    def find(self, name):
        """Return the song with this name (case-insensitive) or None."""
        return next((s for s in self.songs if s.name.lower() == name.lower()), None)

    def add(self, song):
        """Append a song to the playlist."""
        self.songs.append(song)

    def remove(self, name):
        """Remove a song by name. Returns True if it existed."""
        song = self.find(name)
        if song:
            self.songs.remove(song)
        return song is not None

    def change(self, old_name, name, singer, genre):
        """Update song details; blank values keep the old value."""
        song = self.find(old_name)
        if not song:
            return False
        song.name, song.singer, song.genre = name or song.name, singer or song.singer, genre or song.genre
        return True

    def sort(self):
        """Sort songs by name, ascending."""
        self.songs.sort(key=lambda s: s.name.lower())

    def shuffle(self):
        """Randomly reorder songs."""
        random.shuffle(self.songs)

    def __str__(self):
        return f"{self.name}: " + " ; ".join(str(s) for s in self.songs)