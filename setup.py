"""setuptools based setup module"""

import codecs
from os import path
from setuptools import find_packages, setup


current_dir = path.abspath(path.dirname(__file__))


with codecs.open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='packingslip',
    version='0.1.0',
    description='Tools to compare files by checksum.',
    long_description=long_description,
    url='https://github.com/dmwilcox/packingslip',
    author='Yuba Solutions LLC',
    author_email='dmw@yubasoluions.com',
    license='GPL',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    keywords='rsync',
    packages = [
        'packingslip',
    ],
    entry_points = {
        'console_scripts': [
            'packingslip = packingslip.packingslip:main',
            'spotcheck = packingslip.spotcheck:dispatch_main',
        ],
    },
    install_requires = ['argparse', 'PyYAML']
)
