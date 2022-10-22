from setuptools import find_packages
from setuptools import setup

setup(name='movs',
      version='0.0.0',
      url='http://www.example.com',
      author='Vito De Tullio',
      author_email='vito.detullio@gmail.com',
      py_modules=find_packages(),
      extra_require={
          'dev': [
              'distutil'
          ]
      },
      package_dir={'': 'src'},
      package_data={
          'movs': ['py.typed'],
      })
