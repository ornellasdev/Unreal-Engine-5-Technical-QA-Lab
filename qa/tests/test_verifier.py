"""Replay selected Unreal log lines recorded during RUN-006."""

import unittest
from pathlib import Path

from qa.run_functional import verify


FIXTURES = Path(__file__).parent / "fixtures"


class VerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.closed = (FIXTURES / "TC-001.txt").read_text(encoding="utf-8")
        cls.opened = (FIXTURES / "TC-004.txt").read_text(encoding="utf-8")

    def test_accepts_recorded_blocked_player(self):
        self.assertIsNone(verify(1, self.closed))

    def test_accepts_recorded_single_opening(self):
        self.assertEqual(verify(4, self.opened), 29)

    def test_rejects_duplicate_opening(self):
        opening = next(line for line in self.opened.splitlines() if line.endswith("Door opening."))
        log = self.opened.replace(opening, opening + "\n" + opening, 1)
        with self.assertRaisesRegex(ValueError, "^messages:"):
            verify(4, log)

    def test_rejects_missing_player_sample(self):
        first_sample = next(line for line in self.closed.splitlines() if ".RelativeLocation =" in line)
        log = self.closed.replace(first_sample + "\n", "", 1)
        with self.assertRaisesRegex(ValueError, "^blocked position samples:"):
            verify(1, log)

    def test_rejects_player_crossing_closed_door(self):
        # Preserve the first blocked sample. Move only the second beyond the door.
        before, marker, after = self.closed.rpartition("X=176.551110")
        self.assertTrue(marker)
        log = before + "X=454.550948" + after
        with self.assertRaisesRegex(ValueError, "^closed door should stop the player"):
            verify(1, log)
