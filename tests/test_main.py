# tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from main import main
from utils import load_config

class TestMain(unittest.TestCase):
    def test_main_success(self):
        # Mock the load_config function to return a valid config
        with patch('utils.load_config') as mock_load_config:
            mock_load_config.return_value = {
                'services': [
                    {'name': 'service1', 'url': 'http://service1.example.com'},
                    {'name': 'service2', 'url': 'http://service2.example.com'}
                ],
                'timeout': 5,
                'retry': 3
            }

            # Mock the health_check function to return a list of healthy services
            with patch('health_check.health_check') as mock_health_check:
                mock_health_check.return_value = [
                    {'name': 'service1', 'status': 'UP'},
                    {'name': 'service2', 'status': 'UP'}
                ]

                with patch('logging.info') as mock_logging_info:
                    main()

                    # Check that the logging.info function was called with the expected message
                    mock_logging_info.assert_called_once_with('All services are healthy.')

    def test_main_service_down(self):
        # Mock the load_config function to return a valid config
        with patch('utils.load_config') as mock_load_config:
            mock_load_config.return_value = {
                'services': [
                    {'name': 'service1', 'url': 'http://service1.example.com'},
                    {'name': 'service2', 'url': 'http://service2.example.com'}
                ],
                'timeout': 5,
                'retry': 3
            }

            # Mock the health_check function to return a list of services with one down
            with patch('health_check.health_check') as mock_health_check:
                mock_health_check.return_value = [
                    {'name': 'service1', 'status': 'UP'},
                    {'name': 'service2', 'status': 'DOWN'}
                ]

                with patch('logging.error') as mock_logging_error:
                    main()

                    # Check that the logging.error function was called with the expected message
                    mock_logging_error.assert_called_once_with('service2 is DOWN.')

if __name__ == '__main__':
    unittest.main()