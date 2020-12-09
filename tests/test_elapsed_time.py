"""時間差計算クラスのテスト"""

import unittest
from datetime import datetime

from modules.elapsed_time import ElapsedTime


class TestElapsedTime(unittest.TestCase):
    def test_minutes(self):
        test_ptn = [(0, 0), (5, 5), (10, 10), (59, 59)]
        for minutes, expected in test_ptn:
            with self.subTest(f"fail case minutes: {minutes}, expected: {expected}"):
                start = datetime.strptime("12:00:00", "%H:%M:%S")
                end = datetime.strptime(f"12:{minutes}:00", "%H:%M:%S")

                elapsed_time = ElapsedTime(start=start, end=end)
                actual = elapsed_time.minutes
                self.assertEqual(actual, expected)

    def test_seconds(self):
        test_ptn = [(0, 0), (5, 5), (10, 10), (59, 59)]
        for seconds, expected in test_ptn:
            with self.subTest(f"fail case seconds: {seconds}, expected: {expected}"):
                start = datetime.strptime("12:00:00", "%H:%M:%S")
                end = datetime.strptime(f"12:00:{seconds}", "%H:%M:%S")

                elapsed_time = ElapsedTime(start=start, end=end)
                actual = elapsed_time.seconds
                self.assertEqual(actual, expected)

    def test_over_10_minutes(self):
        test_ptn = [(0, False), (9, False), (10, True)]
        for minutes, expected in test_ptn:
            with self.subTest(f"fail case minutes: {minutes}, expected: {expected}"):
                start = datetime.strptime("12:00:00", "%H:%M:%S")
                end = datetime.strptime(f"12:{minutes}:00", "%H:%M:%S")

                elapsed_time = ElapsedTime(start=start, end=end)
                actual = elapsed_time.is_over_10_minute()
                self.assertEqual(actual, expected)

    def test_to_hhmm(self):
        test_ptn = [
            ((0, 0), "00:00"),
            ((5, 5), "05:05"),
            ((10, 10), "10:10"),
            ((59, 59), "59:59"),
        ]
        for arg, expected in test_ptn:
            with self.subTest(f"fail case arg: {arg}, expected: {expected}"):
                start = datetime.strptime("12:00:00", "%H:%M:%S")
                end = datetime.strptime(f"12:{arg[0]}:{arg[1]}", "%H:%M:%S")

                elapsed_time = ElapsedTime(start=start, end=end)
                actual = elapsed_time.generate_hhmm()
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
