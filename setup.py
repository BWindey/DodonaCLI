from setuptools import setup, find_packages


setup(
    name='dodona',
    version='0.9',
    packages=find_packages(),
    install_requires=[
        'click',
        'bs4',
        'rich',
        'markdownify'
    ],
    entry_points={
        'console_scripts': [
            'dodona=main:main'
        ],
    },
)
