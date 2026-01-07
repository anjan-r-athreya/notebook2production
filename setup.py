"""Setup configuration for nb2prod."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

setup(
    name="nb2prod",
    version="0.1.0",
    description="Convert messy Jupyter notebooks to production-ready Python code using AI-powered analysis and refactoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anjan Athreya",
    author_email="anjan.athreya@example.com",
    url="https://github.com/anjan-r-athreya/notebook2production",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    install_requires=[
        "nbformat>=5.0.0",
        "click>=8.0.0",
        "rich>=10.0.0",
        "pyyaml>=6.0.0",
        "anthropic>=0.18.0",
        "streamlit>=1.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "nb2prod=nb2prod.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Data Scientists",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    keywords="jupyter notebook production refactoring ai code-generation data-science",
    project_urls={
        "Bug Reports": "https://github.com/anjan-r-athreya/notebook2production/issues",
        "Source": "https://github.com/anjan-r-athreya/notebook2production",
        "Documentation": "https://github.com/anjan-r-athreya/notebook2production/blob/main/README.md",
    },
)
