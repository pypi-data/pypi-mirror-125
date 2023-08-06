from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages

def _get_requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="ExtensionConvertor",
    version="1.0.4",
    license="MIT",
    author="Akagawa Daisuke",
    url="http://github.com/Akasan/ExtensionConvertor",
    packages=["ExtensionConvertor"],
    include_package_data=True,
    zip_safe=False,
)
