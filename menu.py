"""Menu class: console interface."""
from player import Player
from song import Song


class Menu:
    """Console interface that dispatches numbered options."""

    def __init__(self, library, player=None):
        self.lib, self.player = library, player or Player()
        self.options = {
            "1": ("Add song to a playlist", self.add_song),
            "2": ("Change song in a playlist", self.change_song),
            "3": ("Rename a playlist", self.rename),
            "4": ("Remove a playlist", self.remove_playlist),
            "5": ("Remove song from a playlist", self.remove_song),
            "6": ("Show duplicated songs", self.duplicates),
            "7": ("Sort playlists by name", self.sort_playlists),
            "8": ("Sort songs in each playlist", self.sort_songs),
            "9": ("Shuffle songs in each playlist", self.shuffle),
            "10": ("Export playlists to file", self.export),
            "11": ("Play a song", self.play),
            "12": ("Show all playlists", self.show),
            "13": ("Load playlists from file", self.load),
            "0": ("Exit", None),
        }

    def _playlist(self):
        """Ask for a playlist name; return it or None with a message."""
        pl = self.lib.get(input("Playlist name: ").strip())
        if not pl:
            print("Playlist not found.")
        return pl

    def add_song(self):
        pl = self.lib.get_or_create(input("Playlist name: ").strip())
        pl.add(Song(input("Song: ").strip(), input("Singer: ").strip(), input("Genre: ").strip(),
                    input("Audio file path (blank for none): ").strip()))
        print("Song added.")

    def change_song(self):
        pl = self._playlist()
        if pl:
            old = input("Song to change: ").strip()
            ok = pl.change(old, input("New name (blank=keep): ").strip(),
                           input("New singer (blank=keep): ").strip(),
                           input("New genre (blank=keep): ").strip())
            print("Song updated." if ok else "Song not found.")

    def rename(self):
        ok = self.lib.rename(input("Current name: ").strip(), input("New name: ").strip())
        print("Renamed." if ok else "Playlist not found.")

    def remove_playlist(self):
        print("Removed." if self.lib.remove(input("Playlist name: ").strip()) else "Playlist not found.")

    def remove_song(self):
        pl = self._playlist()
        if pl:
            print("Removed." if pl.remove(input("Song name: ").strip()) else "Song not found.")

    def duplicates(self):
        dups = self.lib.duplicates()
        if not dups:
            print("No duplicated songs.")
        for (name, singer), pls in dups.items():
            print(f"'{name}' by {singer} appears in: {', '.join(pls)}")

    def sort_playlists(self):
        self.lib.sort()
        print("Playlists sorted.")

    def sort_songs(self):
        for pl in self.lib.playlists:
            pl.sort()
        print("Songs sorted.")

    def shuffle(self):
        for pl in self.lib.playlists:
            pl.shuffle()
        print("Songs shuffled.")

    def export(self):
        self.lib.export(input("File name: ").strip())
        print("Exported.")

    def play(self):
        pl = self._playlist()
        if pl:
            song = pl.find(input("Song name: ").strip())
            self.player.play(song) if song else print("Song not found.")

    def show(self):
        print("\n".join(str(p) for p in self.lib.playlists) or "No playlists.")

    def load(self):
        try:
            print(f"Loaded {self.lib.load(input('File name: ').strip())} playlist line(s).")
        except OSError:
            print("Could not read that file.")

    def run(self):
        """Main loop: show options, run the chosen one until Exit."""
        while True:
            print("\n" + "\n".join(f"Option {k}. {v[0]}" for k, v in self.options.items()))
            choice = input("Choose: ").strip()
            if choice == "0":
                break
            action = self.options.get(choice)
            action[1]() if action else print("Invalid option.")