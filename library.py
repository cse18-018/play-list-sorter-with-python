"""Library class: all playlists and operations spanning them."""
from playlist import Playlist
from song import Song


class Library:
    """Holds all playlists and the operations that span them."""

    def __init__(self):
        self.playlists = []

    def get(self, name):
        """Return the playlist with this name or None."""
        return next((p for p in self.playlists if p.name.lower() == name.lower()), None)

    def get_or_create(self, name):
        """Return an existing playlist or create a new one."""
        pl = self.get(name)
        if not pl:
            pl = Playlist(name)
            self.playlists.append(pl)
        return pl

    def rename(self, old, new):
        """Rename a playlist. Returns True on success."""
        pl = self.get(old)
        if pl:
            pl.name = new
        return pl is not None

    def remove(self, name):
        """Delete a playlist and all its songs. Returns True on success."""
        pl = self.get(name)
        if pl:
            self.playlists.remove(pl)
        return pl is not None

    def sort(self):
        """Sort playlists by name, ascending."""
        self.playlists.sort(key=lambda p: p.name.lower())

    def duplicates(self):
        """Return {song: [playlist names]} for songs that occur more than once overall."""
        found = {}
        for pl in self.playlists:
            for s in pl.songs:
                found.setdefault(s.key(), []).append(pl.name)
        return {k: v for k, v in found.items() if len(v) > 1}

    def load(self, path):
        """Load playlists from a file; returns number of lines loaded."""
        count = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                name, _, rest = line.strip().partition(":")
                if not name or not rest:
                    continue
                pl = self.get_or_create(name.strip())
                for item in rest.split(";"):
                    parts = [p.strip() for p in item.split("|")]
                    if len(parts) in (3, 4) and parts[0]:
                        pl.add(Song(*parts))
                count += 1
        return count

    def export(self, path):
        """Write every playlist and its songs to a text file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(str(p) for p in self.playlists) + "\n")