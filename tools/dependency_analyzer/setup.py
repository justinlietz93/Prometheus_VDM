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
