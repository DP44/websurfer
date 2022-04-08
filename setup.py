from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='websurfer',
    version='0.0.1',
    description='A utility for discovering web servers on a network.',
    long_description='fuck you',
    author='DP44',
    author_email='donkeypounder44@nigge.rs',
    url='https://github.com/DP44/websurfer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)