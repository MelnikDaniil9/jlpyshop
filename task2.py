from get_score import get_score

import unittest

game_stamps = [
    {"offset": 0, "score": {"away": 0, "home": 0}},
    {"offset": 2, "score": {"away": 1, "home": 0}},
    {"offset": 6, "score": {"away": 1, "home": 1}},
    {"offset": 8, "score": {"away": 1, "home": 1}},
    {"offset": 9, "score": {"away": 1, "home": 1}},
    {"offset": 11, "score": {"away": 1, "home": 2}},
    {"offset": 12, "score": {"away": 1, "home": 2}},
    {"offset": 13, "score": {"away": 2, "home": 2}},
]


class TestGetScore(unittest.TestCase):
    def test_start_game(self):
        self.assertEqual((0, 0), get_score(game_stamps, 0))

    def test_score_not_changed(self):
        self.assertEqual((0, 1), get_score(game_stamps, 2))
        self.assertEqual((0, 1), get_score(game_stamps, 3))
        self.assertEqual((0, 1), get_score(game_stamps, 4))
        self.assertEqual((0, 1), get_score(game_stamps, 5))

    def test_score_changed(self):
        self.assertEqual((0, 0), get_score(game_stamps, 1))
        self.assertEqual((0, 1), get_score(game_stamps, 2))

    def test_end_game(self):
        self.assertEqual((2, 2), get_score(game_stamps, 13))

    def test_incorrect_offset(self):
        self.assertEqual((2, 2), get_score(game_stamps, -1))
        self.assertEqual((2, 2), get_score(game_stamps, 14))
        self.assertEqual((2, 2), get_score(game_stamps, "foo"))
        self.assertEqual((2, 2), get_score(game_stamps, []))
