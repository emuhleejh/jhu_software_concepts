import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from setuptools import setup

setup(
   name='ehammer',
   version='1.0',
   description='Setup module',
   author='ehammer',
   author_email='ehammer@jh.edu',
   packages=['data_processing', 'llm_hosting', 'templates']  #same as name
)