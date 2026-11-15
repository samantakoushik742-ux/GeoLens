import os
import unittest
from unittest.mock import patch

from config import _read_port


class BackendConfigTests(unittest.TestCase):
    @patch.dict(os.environ, {"PORT": "8123"})
    def test_reads_port_from_environment(self):
        self.assertEqual(_read_port(), 8123)

    @patch.dict(os.environ, {"PORT": "not-a-number"})
    def test_rejects_non_integer_port(self):
        with self.assertRaisesRegex(ValueError, "Invalid PORT"):
            _read_port()

    @patch.dict(os.environ, {"PORT": "65536"})
    def test_rejects_out_of_range_port(self):
        with self.assertRaisesRegex(ValueError, "1 and 65535"):
            _read_port()


if __name__ == "__main__":
    unittest.main()
