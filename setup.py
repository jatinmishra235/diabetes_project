from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name= 'src',
    version= '0.0.1',
    author= 'jatin_mishra',
    packages= find_packages(),
    author_email='jatinmishra235@gmail.com',
    install_requires = requirements
)