import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Play-Store-Scraper",
    version = "0.0.1",
    author = "Saurabh AV",
    author_email = "saurabhav.torres@gmail.com",
    description = ("Scrapes images and description of apps in google play store"),
    license = "MIT",
    keywords = "play store scraper",    
    packages=find_packages(),
    install_requires= [
        "beautifulsoup4"
    ],
    py_modules=[
        'main',
        'scraper'
    ],
    long_description=read('README.md'),    
    entry_points={
        'console_scripts': ['play-store-scraper=main:console_entry'],
    },
    zip_safe=True,
)
