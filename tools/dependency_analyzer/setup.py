"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from setuptools import setup, find_packages

setup(
    name="dependency-analyzer",
    version="0.1.0",
    description="A comprehensive dependency analyzer with live updates",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "dependency_analyzer": ["scripts/parse_js.js", "nodejs/*"]
    },
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
        "watchdog"
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "dependency-analyzer = dependency_analyzer.cli:main"
        ]
    }
)
