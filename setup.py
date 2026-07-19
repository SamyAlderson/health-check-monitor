from setuptools import setup, find_packages

# This was tricky, but we need to specify the package structure for pyproject.toml
# to work correctly with poetry
packages = find_packages(include=['health_check_monitor', 'health_check_monitor.*'])

with open('pyproject.toml', 'r') as f:
    pyproject_toml = f.read()

# Parse the pyproject.toml file to get the project metadata
import tomli
pyproject_data = tomli.loads(pyproject_toml)
project_name = pyproject_data['tool']['poetry']['name']
project_description = pyproject_data['tool']['poetry']['description']

# Not proud of this but it works, we're gonna parse the config.ini file to get
# the dependencies and requirements
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
dependencies = config['dependencies']['packages'].split(',')
requirements = [dep.strip() for dep in config['requirements']['dependencies'].split(',')]

setup(
    name=project_name,
    version='1.0.0',
    description=project_description,
    long_description='A simple health check monitor for detecting service availability and performance issues.',
    long_description_content_type='text/markdown',
    packages=packages,
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='health check monitor service discovery',
    project_urls={
        'Documentation': 'https://health-check-monitor.readthedocs.io/en/latest/',
        'Source Code': 'https://github.com/yourusername/health-check-monitor',
        'Issue Tracker': 'https://github.com/yourusername/health-check-monitor/issues',
    },
    license='MIT',
)