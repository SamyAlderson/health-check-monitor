# src/utils.py

"""
Utility functions for service discovery and health checks.
"""

import logging
import time
from typing import Dict, List
from dnspython import resolver
from requests import get, ConnectionError

# Set up logging with a concise format
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def get_services_from_dns(dns_server: str = '8.8.8.8') -> List[str]:
    """
    Retrieve a list of services from a DNS server using a DNS query.

    Args:
    - dns_server (str): The DNS server IP address to query (default: Google's public DNS server)

    Returns:
    - A list of service names discovered via DNS
    """
    # Not proud of this but it works - we're using a raw DNS query to extract service names
    try:
        resolver = resolver.Resolver()
        resolver.nameservers = [dns_server]
        answers = resolver.query('.', 'NS')
        service_names = [answer.name for answer in answers if answer.type == 2]  # NS records
        return service_names
    except Exception as e:
        logging.error(f"Failed to retrieve services from DNS: {e}")
        return []

def perform_http_probe(service_url: str, timeout: int = 5) -> bool:
    """
    Perform an HTTP probe to a service endpoint to check for responsiveness.

    Args:
    - service_url (str): The URL of the service endpoint to probe
    - timeout (int): The maximum timeout for the HTTP request (default: 5 seconds)

    Returns:
    - True if the service is responsive, False otherwise
    """
    try:
        # This was tricky - we don't want to raise exceptions on failed probes
        get(service_url, timeout=timeout)
        return True
    except ConnectionError:
        # Ignore connection errors and return False for non-responsive services
        return False

def retry_with_backoff(max_attempts: int = 3) -> callable:
    """
    A decorator to implement exponential backoff for retries.

    Args:
    - max_attempts (int): The maximum number of attempts before giving up (default: 3)

    Returns:
    - A decorator function to wrap the target function with retry logic
    """
    def decorator(target_function):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return target_function(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(f"Attempt {attempts} failed with error: {e}")
                    # Exponential backoff with a short initial delay and doubling intervals
                    delay = 2 ** attempts * 0.1
                    time.sleep(delay)
            # Log the final failure and re-raise the exception
            logging.error(f"Max attempts ({max_attempts}) exceeded")
            raise
        return wrapper
    return decorator