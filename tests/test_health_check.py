# tests/test_health_check.py

import unittest
from unittest.mock import patch, MagicMock
from src.health_check import HealthCheck

class TestHealthCheck(unittest.TestCase):

    @patch('src.health_check.requests.get')
    def test_service_available(self, mock_get):
        # Arrange
        mock_response = MagicMock(status_code=200)
        mock_get.return_value = mock_response

        # Act
        health_check = HealthCheck('http://example.com')
        result = health_check.check()

        # Assert
        self.assertTrue(result)
        mock_get.assert_called_once()

    @patch('src.health_check.requests.get')
    def test_service_unavailable(self, mock_get):
        # Arrange
        mock_response = MagicMock(status_code=500)
        mock_get.return_value = mock_response

        # Act
        health_check = HealthCheck('http://example.com')
        result = health_check.check()

        # Assert
        self.assertFalse(result)
        mock_get.assert_called_once()

    @patch('src.health_check.requests.get')
    def test_service_timeout(self, mock_get):
        # Arrange
        mock_response = MagicMock(status_code=200)
        mock_get.side_effect = TimeoutError
        mock_get.return_value = mock_response

        # Act
        health_check = HealthCheck('http://example.com')
        result = health_check.check()

        # Assert
        self.assertFalse(result)
        mock_get.assert_called_once()

    def test_service_invalid_url(self):
        # Act and Assert
        with self.assertRaises(ValueError):
            HealthCheck('invalid_url')

if __name__ == '__main__':
    unittest.main()