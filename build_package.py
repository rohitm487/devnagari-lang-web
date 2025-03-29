import os
import shutil
from setuptools import setup

# Clean previous builds
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("*.egg-info"):
    for f in os.listdir("."):
        if f.endswith(".egg-info"):
            shutil.rmtree(f)

# Build the package
setup(
    name="devnagari-lang",
    version="0.1.0",
    packages=["devnagari_lang"],
    package_data={
        "devnagari_lang": ["*.py"],
    },
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="A programming language using Devanagari script",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/devnagari-lang",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 