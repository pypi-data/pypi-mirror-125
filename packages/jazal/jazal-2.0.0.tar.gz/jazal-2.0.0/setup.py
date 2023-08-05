# PyPI references
# https://packaging.python.org/tutorials/packaging-projects/
# https://www.geeksforgeeks.org/how-to-publish-python-package-at-pypi-using-twine-module/

# grayskull references
# https://github.com/conda-incubator/grayskull
# https://githubmemory.com/repo/conda-incubator/grayskull/issues/209?page=2
# https://docs.python.org/3/distutils/sourcedist.html


import setuptools


with open("README.md", "r", encoding="utf-8") as readme_stream:
	long_description = readme_stream.read()

setuptools.setup(
	name = "jazal",
	version = "2.0.0",
	author = "Guyllaume Rousseau",
	description = "Jazal performs certain verifications on filepaths before a function or a script uses them.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/GRV96/jazal",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Utilities"
	],
	packages = setuptools.find_packages(),
	license = "MIT",
	license_files = ("LICENSE",)
)
