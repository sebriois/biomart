from setuptools import setup

setup(
    name='biomart',
    version='0.5.0',
    author='Sebastien Briois',
    author_email='sebriois@gmail.com',
    packages=['biomart','biomart.lib','biomart.test'],
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
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
