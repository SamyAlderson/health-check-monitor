# src/health_check.py
"""
Health check module for detecting service availability and performance issues.

This module provides a set of functions for performing health checks on services.
It uses DNS and HTTP probes for service discovery and supports customizable timeout
and retry policies.
"""

import logging
import time
from typing import Dict, List
import requests
import dns.resolver
from urllib.parse import urlparse

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_service_url(service_name: str, config: Dict) -> str:
    """
    Resolve the service URL using DNS and configuration.

    This function uses DNS to resolve the service name to an IP address and then
    uses the configuration to construct the full service URL.

    Args:
    - service_name (str): The name of the service to resolve.
    - config (Dict): The configuration dictionary containing the DNS and URL settings.

    Returns:
    - str: The resolved service URL.
    """
    # Get the DNS server and search domains from the configuration
    dns_server = config['dns']['server']
    search_domains = config['dns']['search_domains']

    # Perform DNS lookup
    try:
        answers = dns.resolver.resolve(service_name, 'A')
        for answer in answers:
            logger.info(f"Resolved {service_name} to {answer}")
            return f"http://{answer}"
    except dns.resolver.NoAnswer:
        logger.warning(f"No A record found for {service_name}")
    except dns.resolver.NXDOMAIN:
        logger.warning(f"No DNS record found for {service_name}")

    # If DNS lookup fails, return None
    return None

def perform_http_probe(url: str, timeout: int, retries: int) -> bool:
    """
    Perform an HTTP probe on the given URL.

    This function sends an HTTP GET request to the given URL and checks the response
    status code. If the status code is 200, it returns True; otherwise, it returns
    False.

    Args:
    - url (str): The URL to probe.
    - timeout (int): The timeout in seconds.
    - retries (int): The number of retries.

    Returns:
    - bool: Whether the HTTP probe was successful.
    """
    # Set up the HTTP request
    headers = {'User-Agent': 'health-check-monitor'}
    params = {'timeout': timeout, 'retries': retries}

    # Perform the HTTP probe
    while retries > 0:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            if response.status_code == 200:
                logger.info(f"HTTP probe successful for {url}")
                return True
            else:
                logger.warning(f"HTTP probe failed for {url} with status code {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"HTTP probe failed for {url} with error {e}")

        # Decrement the number of retries
        retries -= 1

    # If all retries fail, return False
    logger.error(f"All retries failed for {url}")
    return False

def health_check(service_name: str, config: Dict) -> bool:
    """
    Perform a health check on the given service.

    This function resolves the service URL using DNS and configuration, performs an
    HTTP probe on the URL, and returns True if the probe is successful; otherwise,
    it returns False.

    Args:
    - service_name (str): The name of the service to check.
    - config (Dict): The configuration dictionary containing the DNS and URL settings.

    Returns:
    - bool: Whether the health check was successful.
    """
    # Resolve the service URL
    url = get_service_url(service_name, config)

    # If the URL is None, return False
    if url is None:
        logger.info(f"No URL found for {service_name}")
        return False

    # Perform the HTTP probe
    return perform_http_probe(url, config['http_probe']['timeout'], config['http_probe']['retries'])
```
```python
# tests/test_health_check.py
"""
Unit tests for the health check module.
"""

import unittest
from unittest.mock import patch
from src.health_check import health_check, get_service_url, perform_http_probe

class TestHealthCheck(unittest.TestCase):
    def test_get_service_url(self):
        config = {
            'dns': {
                'server': '8.8.8.8',
                'search_domains': ['example.com']
            },
            'http_probe': {
                'timeout': 5,
                'retries': 3
            }
        }
        service_name = 'example-service'
        with patch('dns.resolver.resolve') as mock_resolve:
            mock_resolve.return_value = ['192.0.2.1']
            url = get_service_url(service_name, config)
            self.assertEqual(url, 'http://192.0.2.1')

    def test_perform_http_probe(self):
        config = {
            'http_probe': {
                'timeout': 5,
                'retries': 3
            }
        }
        url = 'http://example.com'
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            result = perform_http_probe(url, config['http_probe']['timeout'], config['http_probe']['retries'])
            self.assertTrue(result)

    def test_health_check(self):
        config = {
            'dns': {
                'server': '8.8.8.8',
                'search_domains': ['example.com']
            },
            'http_probe': {
                'timeout': 5,
                'retries': 3
            }
        }
        service_name = 'example-service'
        with patch('src.health_check.get_service_url') as mock_get_url:
            mock_get_url.return_value = 'http://example.com'
            with patch('src.health_check.perform_http_probe') as mock_probe:
                mock_probe.return_value = True
                result = health_check(service_name, config)
                self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()