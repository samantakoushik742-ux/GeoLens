import os
import unittest
from unittest.mock import patch

from database_ingestion import create_table


class ConnectMysqlTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "MYSQL_HOST": "db.example.com",
            "MYSQL_USER": "user",
            "MYSQL_PASSWORD": "",
            "MYSQL_DATABASE": "defaultdb",
            "MYSQL_SSL_CA": "ca.pem",
        },
        clear=True,
    )
    @patch("database_ingestion.create_table.mysql.connector.connect")
    def test_connect_mysql_allows_blank_password(self, mock_connect):
        create_table.connect_mysql()

        config = mock_connect.call_args.kwargs
        self.assertEqual(config["host"], "db.example.com")
        self.assertEqual(config["user"], "user")
        self.assertEqual(config["password"], "")
        self.assertEqual(config["database"], "defaultdb")
        self.assertEqual(config["port"], 3306)
        self.assertEqual(config["ssl_ca"], "ca.pem")
        self.assertTrue(config["ssl_verify_cert"])
        self.assertTrue(config["ssl_verify_identity"])

    @patch.dict(
        os.environ,
        {
            "MYSQL_HOST": "db.example.com",
            "MYSQL_USER": "user",
            "MYSQL_PASSWORD": "secret",
            "MYSQL_DATABASE": "defaultdb",
            "MYSQL_PORT": "not-a-number",
            "MYSQL_SSL_CA": "ca.pem",
        },
        clear=True,
    )
    @patch("database_ingestion.create_table.mysql.connector.connect")
    def test_connect_mysql_rejects_invalid_port(self, _mock_connect):
        with self.assertRaisesRegex(RuntimeError, "Invalid MYSQL_PORT"):
            create_table.connect_mysql()

    @patch.dict(
        os.environ,
        {
            "MYSQL_HOST": "db.example.com",
            "MYSQL_USER": "user",
            "MYSQL_PASSWORD": "",
            "MYSQL_DATABASE": "defaultdb",
        },
        clear=True,
    )
    @patch("database_ingestion.create_table.mysql.connector.connect")
    def test_connect_mysql_requires_ca_certificate(self, mock_connect):
        with self.assertRaisesRegex(RuntimeError, "MYSQL_SSL_CA"):
            create_table.connect_mysql()
        mock_connect.assert_not_called()


if __name__ == "__main__":
    unittest.main()
