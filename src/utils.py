# src/utils.py

import logging
import os
import json
import requests

# Set up logging with a simple config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(file_path):
    """
    Loads a JSON configuration file.
    
    Args:
    file_path (str): Path to the configuration file.
    
    Returns:
    dict: Configuration data.
    
    Raises:
    FileNotFoundError: If the configuration file does not exist.
    json.JSONDecodeError: If the configuration file is malformed.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Malformed configuration file: {e}")
        raise

def check_service_availability(url):
    """
    Checks the availability of a service at a given URL.
    
    Args:
    url (str): URL to check.
    
    Returns:
    bool: True if the service is available, False otherwise.
    
    Raises:
    requests.RequestException: If there's a problem with the request.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        logger.error(f"Error checking service availability: {e}")
        raise

def get_service_status(url):
    """
    Checks the status of a service at a given URL.
    
    Args:
    url (str): URL to check.
    
    Returns:
    str: Status code of the service.
    
    Raises:
    requests.RequestException: If there's a problem with the request.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.RequestException as e:
        logger.error(f"Error checking service status: {e}")
        raise

def get_environment_variable(var_name):
    """
    Retrieves an environment variable.
    
    Args:
    var_name (str): Name of the environment variable.
    
    Returns:
    str: Value of the environment variable.
    
    Raises:
    KeyError: If the environment variable is not set.
    """
    try:
        return os.environ[var_name]
    except KeyError as e:
        logger.error(f"Environment variable not set: {e}")
        raise