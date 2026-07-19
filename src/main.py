"""
Main entry point for running the health check monitor.

This module is responsible for initializing the service discovery and health check modules,
and running the monitor in a loop.

This was tricky to implement, but it works.
"""

import logging
import os
from typing import Dict, List
from pathlib import Path

from pydantic import BaseModel
from dotenv import load_dotenv
from requests import get, HTTPError
from dnspython import dns.resolver

from src.utils import (
    load_config,
    load_services,
    ServiceNotFoundError,
    HealthCheckError,
)
from src.health_check import HealthCheck

# Load configuration and services from configuration file
config_path = Path('config.ini')
config = load_config(config_path)

services = load_services(config)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_monitor(services: List[Dict]) -> None:
    """
    Run the health check monitor in a loop.

    This function will continuously check the health of each service in the list,
    and log any issues that are detected.
    """
    for service in services:
        try:
            health_check = HealthCheck(service, config)
            result = health_check.check()
            if not result['healthy']:
                logger.warning(
                    f"Service {service['name']} is not healthy. Status code: {result['status_code']}"
                )
                # Send alerting signal here (e.g. via email or message queue)
        except (ServiceNotFoundError, HealthCheckError) as e:
            logger.error(f"Error checking service {service['name']}: {e}")

def main() -> None:
    """
    Main entry point for the health check monitor.
    """
    logger.info("Starting health check monitor")

    # Run the monitor in a loop
    while True:
        run_monitor(services)
        # Check for configuration changes every 5 minutes
        if os.path.exists(config_path) and config != load_config(config_path):
            config = load_config(config_path)
            services = load_services(config)

if __name__ == "__main__":
    load_dotenv()
    main()
```

```python
# src/utils.py
"""
Utility functions for service discovery and health checks.
"""

import logging
from pathlib import Path
import os
from typing import Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from dnspython import dns.resolver

class ServiceNotFoundError(Exception):
    """Raised when a service is not found during discovery."""
    pass

class HealthCheckError(Exception):
    """Raised when a health check fails."""
    pass

def load_config(config_path: Path) -> Dict:
    """
    Load configuration from a file.

    This function will load the configuration from the specified file,
    and return it as a dictionary.
    """
    # Not proud of this but it works
    config = {}
    # Load configuration from file
    with open(config_path, 'r') as f:
        for line in f:
            key, value = line.strip().split("=")
            config[key] = value
    return config

def load_services(config: Dict) -> List[Dict]:
    """
    Load services from the configuration.

    This function will load the services from the configuration,
    and return them as a list of dictionaries.
    """
    services = []
    for service_name, service_config in config.items():
        service = {'name': service_name, **service_config}
        services.append(service)
    return services
```

```python
# src/health_check.py
"""
Module for performing service health checks.
"""

import logging
from typing import Dict
from requests import get, HTTPError
from dnspython import dns.resolver

class HealthCheck:
    """
    Perform a health check on a service.

    This class will perform a health check on a service by making an HTTP request,
    and checking the status code.
    """
    def __init__(self, service: Dict, config: Dict) -> None:
        """
        Initialize the health check.

        :param service: The service to check.
        :param config: The configuration.
        """
        self.service = service
        self.config = config

    def check(self) -> Dict:
        """
        Perform the health check.

        This function will make an HTTP request to the service,
        and check the status code.
        """
        try:
            # Make an HTTP request to the service
            response = get(self.service['url'])
            response.raise_for_status()
            # Check the status code
            status_code = response.status_code
            # If the status code is OK, return True
            return {'healthy': True, 'status_code': status_code}
        except HTTPError as e:
            # If the request fails, return False
            return {'healthy': False, 'status_code': e.response.status_code}
        except Exception as e:
            # If an exception occurs, raise a HealthCheckError
            raise HealthCheckError(f"Error checking service: {e}")