from setuptools import setup, find_packages

setup(
    name="seenons_api",
    version="0.1.0",
    packages=find_packages(),  # Automatically discover all packages
    install_requires=[
        'Flask==2.0.1',
        'Flask-RESTX==0.5.1',
        'Werkzeug==2.0.3',
        'pytest',
        'pytest-mock',
    ],
    entry_points={
        'console_scripts': [
            'run_seenons_api = seenons_api.main:main',  # Optional entry point for CLI usage
        ],
    },
)
