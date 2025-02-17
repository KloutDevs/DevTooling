from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.MD").read_text(encoding="utf-8")

setup(
    name="devtooling-cli",
    version="0.2.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rich>=10.0.0',
        'questionary>=1.10.0',
        'pyfiglet>=0.8.post1',
        'colorama>=0.4.4',
    ],
    entry_points={
        'console_scripts': [
            'devtool=src.main:main',
        ],
    },
    author="KloutDevs",
    author_email="schmidtnahuel09@gmail.com",
    description="A CLI tool for project analysis and management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KloutDevs/DevTooling",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)