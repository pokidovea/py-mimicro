#!/usr/bin/env python

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='mimicro',
    version='1.0.0',
    description='A simply configurable mock-server written in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Eugene Pokidov',
    author_email='pokidovea@gmail.com',
    url='https://github.com/pokidovea/py-mimicro',
    packages=['mimicro'],
    entry_points={
        'console_scripts': ['mimicro=mimicro.app:main'],
    },
    install_requires=requirements,
    include_package_data=True,
    license='Apache 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
)
