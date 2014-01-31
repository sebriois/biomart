from setuptools import setup

setup(
    name='biomart',
    version='0.1.0',
    author='Sebastien Briois',
    author_email='sebriois@gmail.com',
    packages=['biomart','biomart.test'],
    scripts=['bin/examples.py'],
    license='BSD',
    description='Python API that consumes the biomart webservice',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.2",
    ],
)
