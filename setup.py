from setuptools import find_packages
from setuptools import setup

setup(name='movs',
      version='0.0.1',
      url='https://github.com/ZeeD/movs',
      author='Vito De Tullio',
      author_email='vito.detullio@gmail.com',
      py_modules=find_packages(),
      package_data={
          'movs': ['py.typed'],
      },
      install_requires=[
          'tabula-py',
      ])
