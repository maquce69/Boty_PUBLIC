from setuptools import setup

requirements = list()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

readme = str()
with open('README.md') as f:
    readme = f.read()

setup(name='Telegram bot in OpenShift',

      # PEP 440 -- Version Identification and Dependency Specification
      version='0.0.1',

      # Project description
      description='A really small and simple Telegram bot',
      long_description=readme,

      # Author details
      author='Miguel Quiros',


      # Project details
      url='https://github.com/maquce69/Boty_PUBLIC',

      # Project dependencies
      install_requires=requirements,
      )
