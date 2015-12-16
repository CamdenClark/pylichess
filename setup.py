from setuptools import setup, find_packages

setup(
		name="pylichess",
		version="0.1",
		author="Camden Clark <camdenclark2012@gmail.com>",
		install_requires=['simplejson'],
		description=("Python wrapper for the lichess.com api."),
		author_email="camdenclark2012@gmail.com",
		keywords=["lichess","chess"],
		license='MIT',
		packages=find_packages(exclude=('tests*',)),
)
