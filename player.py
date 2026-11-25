"""Player class."""
import os
import time

try:
    import pygame  # real audio playback (pip install pygame)
except ImportError:
    pygame = None


class Player:
    """Plays a song's audio file with pygame, or simulates playback if there is none."""

    def play(self, song, seconds=3):
        """Play the song's audio file; fall back to a simulated play."""
        print(f"Now playing: {song.name} by {song.singer} [{song.genre}]")
        if song.path:
            if not os.path.isfile(song.path):
                print(f"Audio file not found: {song.path}")
            elif pygame is None:
                print("pygame is not installed. Run: pip install pygame")
            else:
                return self._play_audio(song.path)
        self._simulate(seconds)

    def _play_audio(self, path):
        """Play a real audio file until it ends or the user presses Enter."""
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            input("Playing... press Enter to stop.")
            pygame.mixer.music.stop()
        except pygame.error as err:
            print(f"Could not play audio: {err}")

    def _simulate(self, seconds):
        """Pretend to play for a few seconds (no audio)."""
        for i in range(1, seconds + 1):
            time.sleep(1)
            print(f"  ...{i}s")
        print("Finished.")