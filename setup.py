# setup.py

from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the contents of README.md for the long description
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="mtmpl",  # Replace with your desired package name
    py_modules=["mtmpl"],
    version="0.1.0",  # Start with a small version and increase it with each release
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    description="A simple template engine inspired by Jinja, supporting variables, conditions, and loops.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/07h/mtmpl",
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify your Python version requirements
    keywords="template engine jinja simple",  # Add relevant keywords
    project_urls={  # Optional
        "Bug Reports": "https://github.com/07h/mtmpl/issues",
        "Source": "https://github.com/07h/mtmpl",
    },
    # install_requires=[],  # Add any dependencies if necessary
    # entry_points={},  # Define entry points if you have any CLI tools
)
