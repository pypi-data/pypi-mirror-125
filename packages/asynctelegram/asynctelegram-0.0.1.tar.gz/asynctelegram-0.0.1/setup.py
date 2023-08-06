from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='asynctelegram',
    version='0.0.1',    
    description='A simple library to create telegram bot',
    url='https://github.com/5IGI0/asynctelegram',
    author='5IGI0',
    author_email='5IGI0@protonmail.com',
    license='LGPL-3',
    packages=['asynctelegram'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)