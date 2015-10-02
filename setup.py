from setuptools import setup

setup(
    name='biomart',
    version='0.8.0',
    url='https://github.com/sebriois/biomart',
    author='Sebastien Briois',
    author_email='sebriois@gmail.com',
    packages=['biomart','biomart.lib','biomart.test'],
    keywords='bioinformatics biomart',
    license='BSD',
    description='Python API that consumes the biomart webservice',
    long_description=open('README.txt').read(),
    install_requires=[ "requests>=2.2" ],
    test_suite = 'biomart.test.suite',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
