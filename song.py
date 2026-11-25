"""Song class."""


class Song:
    """A single song with a name, singer, genre and optional audio file path."""

    def __init__(self, name, singer, genre, path=""):
        self.name, self.singer, self.genre, self.path = name, singer, genre, path

    def key(self):
        """Identity used to detect duplicates (name + singer, case-insensitive)."""
        return (self.name.lower(), self.singer.lower())

    def __str__(self):
        base = f"{self.name} | {self.singer} | {self.genre}"
        return f"{base} | {self.path}" if self.path else base