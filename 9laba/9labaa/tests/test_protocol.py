import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protocol import decode_message, encode_message


class ProtocolTests(unittest.TestCase):
    def test_encode_decode(self):
        original = {"command": "calculate", "data": {"expression": "2 + 2"}}
        encoded = encode_message(original).decode("utf-8").strip()
        self.assertEqual(decode_message(encoded), original)


if __name__ == "__main__":
    unittest.main()
