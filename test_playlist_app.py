"""Automated tests. Run with: python -m unittest -v"""
import os
import tempfile
import unittest

from authenticator import Authenticator
from library import Library
from playlist import Playlist
from song import Song


class TestMusicSorter(unittest.TestCase):
    def setUp(self):
        """Build a small library for each test."""
        self.lib = Library()
        a = self.lib.get_or_create("Rock")
        a.add(Song("Zebra", "X", "Rock"))
        a.add(Song("Africa", "Toto", "Rock"))
        b = self.lib.get_or_create("Chill")
        b.add(Song("Africa", "Toto", "Pop"))

    def test_authentication(self):
        auth = Authenticator()
        self.assertTrue(auth.check("user123", "Givemetheykey123"))
        self.assertFalse(auth.check("user123", "wrong"))

    def test_login_locks_after_three_failures(self):
        self.assertFalse(Authenticator().login(ask=lambda _: "bad"))

    def test_add_and_remove_song(self):
        pl = Playlist("P")
        pl.add(Song("A", "S", "G"))
        self.assertTrue(pl.remove("a"))
        self.assertFalse(pl.remove("a"))

    def test_change_song(self):
        pl = self.lib.get("Rock")
        self.assertTrue(pl.change("Zebra", "Lion", "", "Jazz"))
        self.assertEqual(str(pl.find("Lion")), "Lion | X | Jazz")

    def test_rename_and_remove_playlist(self):
        self.assertTrue(self.lib.rename("Rock", "Metal"))
        self.assertTrue(self.lib.remove("Metal"))
        self.assertIsNone(self.lib.get("Metal"))

    def test_duplicates_across_playlists(self):
        dups = self.lib.duplicates()
        self.assertEqual(list(dups.values()), [["Rock", "Chill"]])

    def test_sorting(self):
        self.lib.sort()
        self.assertEqual([p.name for p in self.lib.playlists], ["Chill", "Rock"])
        self.lib.get("Rock").sort()
        self.assertEqual([s.name for s in self.lib.get("Rock").songs], ["Africa", "Zebra"])

    def test_shuffle_keeps_songs(self):
        pl = self.lib.get("Rock")
        pl.shuffle()
        self.assertEqual(sorted(s.name for s in pl.songs), ["Africa", "Zebra"])

    def test_export_then_load(self):
        path = os.path.join(tempfile.mkdtemp(), "out.txt")
        self.lib.export(path)
        new = Library()
        self.assertEqual(new.load(path), 2)
        self.assertEqual(len(new.get("Rock").songs), 2)


if __name__ == "__main__":
    unittest.main()