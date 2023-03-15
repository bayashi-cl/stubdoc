from pathlib import Path

from setuptools import setup

readme = Path(__file__).parent / "README.md"
long_description = readme.read_text()

setup(
    name="stubdoc",
    author="Masaki Kobayashi",
    version="0.1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">= 3.8",
    install_requires=["sphinx"],
    packages=["stubdoc"],
)
