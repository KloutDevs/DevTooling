from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.MD").read_text(encoding="utf-8")

setup(
    name="devtooling-cli",
    version="0.2.7",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'devtooling': ['config/*.json'],
    },
    install_requires=[
        'rich>=10.0.0',
        'questionary>=1.10.0',
        'pyfiglet>=0.8.post1',
        'colorama>=0.4.4',
        'appdirs>=1.4.4',
    ],
    entry_points={
        'console_scripts': [
            'devtool=devtooling.main:main',
        ],
    },
    author="KloutDevs",
    author_email="schmidtnahuel09@gmail.com",
    description="A CLI tool for project analysis and management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KloutDevs/DevTooling",
    project_urls={
        'Bug Reports': 'https://github.com/KloutDevs/DevTooling/issues',
        'Source': 'https://github.com/KloutDevs/DevTooling',
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    keywords='development, cli, project management, utilities',
)