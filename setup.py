from setuptools import setup

setup(
    name='sifr',
    version='0.4.0',
    description='Package to calculate numbers to arbitrarily large ' +
    'significant figures (any base numbering system possible using list of ' +
    'characters representing digits in order and customizable punctuation ' +
    'symbol)',
    # readme="README.md",
    url='https://github.com/AlexanderERoss/Sifr',
    author='Alexander Ross',
    author_email='alex@ross.vip',
    license='GPL v3',
    packages=['sifr'],
    python_requires=">=3.7",  # Need to verify with earlier versions
    install_requires=['logging',
                      ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: " +
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
