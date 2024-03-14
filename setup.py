from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in toehold/__init__.py
from toehold import __version__ as version

setup(
	name="toehold",
	version=version,
	description="toehold",
	author="Helloapps",
	author_email="sagar@helloapps.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
