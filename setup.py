from setuptools import setup, find_packages
import re

with open("src/shortly/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]
    
setup(
    name="link-shortly",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
    "aiohttp>=3.12.15",
],
    author="rkndeveloper",
    author_email="vardhacopyrightteam@gmail.com",
    description="Link-Shortly is a simple Python library to shorten links using the Link-Shortly API or compatible services (like Adlinkfy, GPLinks, etc).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RknDeveloper/link-shortly",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
