from setuptools import setup, find_packages


setup(
    name="deepwoken-spider",
    version="0.1.0",
    description="Web scraper for Deepwoken Fandom Wiki using Scrapy",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="sirzechs423-stack",
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    install_requires=[
        "scrapy>=2.6.0",
        "scrapy-splash>=0.8.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: Scrapy",
    ],
)
