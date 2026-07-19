# Health Check Monitor
[![Python](https://img.shields.io/badge/language-python-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/samy-alderson/health-check-monitor/workflows/CI/badge.svg)](https://github.com/samy-alderson/health-check-monitor/actions)

**"Monitor your services, ensure their health."**

## Overview

The health-check-monitor is a lightweight Python application designed for detecting service availability and performance issues. It utilizes DNS and HTTP probes for service discovery, allowing for multiple health checks with customizable timeout and retry policies. The application also features alerting and logging mechanisms for detected issues, making it a valuable tool for DevOps teams.

## Features

* Service discovery using DNS and HTTP probes
* Multiple service health checks with customizable timeout and retry policies
* Alerting and logging mechanisms for detected issues

## Prerequisites

* Python 3.8+
* Poetry (for project dependencies)

## Installation

1. Clone the repository: `git clone https://github.com/samy-alderson/health-check-monitor.git`
2. Install project dependencies: `poetry install`
3. Create a configuration file (`config.ini`) with service discovery and health check settings

## Usage

Example usage:
```python
import config
from src.main import HealthCheckMonitor

# Initialize health check monitor
monitor = HealthCheckMonitor(config.config)

# Perform service health checks
monitor.check_services()

# Log detected issues
monitor.log_issues()
```
Example configuration file (`config.ini`):
```ini
[service1]
url = http://example.com/service1
timeout = 5s
retry = 3

[service2]
url = http://example.com/service2
timeout = 10s
retry = 2
```
## Project Architecture

The project structure is organized into the following modules:

* `src/main.py`: Main entry point for running the health check monitor
* `src/utils.py`: Utility functions for service discovery and health checks
* `src/health_check.py`: Module for performing service health checks
* `tests/test_health_check.py`: Unit tests for the health check module
* `tests/test_main.py`: Integration tests for the main entry point
* `setup.py`: Build script for packaging the project
* `pyproject.toml`: Project configuration file for poetry
* `config.ini`: Configuration file for service discovery and health checks

## Building from Source

To build the project from source, run the following command:
```bash
poetry build
```
This will create a wheel package in the `dist` directory.

## Testing

To run unit tests, execute the following command:
```bash
poetry run pytest tests
```
To run integration tests, execute the following command:
```bash
poetry run pytest tests/test_main.py
```
## Contributing

Contributions are welcome! Please submit pull requests with clear descriptions of changes made. Ensure all changes adhere to the project's coding standards.

## License

The health-check-monitor is licensed under the MIT License. See `LICENSE` for details.