from setuptools import setup, find_packages

setup(
	name='EasyDonate_API',
	version='1.0.0+dev001',
	author='Dreae',
	author_email='dreae@easydonate.tk',
	packages=find_packages(),
	url='http://easydonate.tk',
	license='MIT License',
	description='Provides API backend implementation for EasyDonate',
	install_requires=['requests'],
)