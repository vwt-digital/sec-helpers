import os

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='sec-helpers',
    packages=find_packages(),
    package_data={'': ['sec-helpers/sec_helpers/no_ssl/ssl3.sh']},
    include_package_data=True,
    version=os.getenv('TAG_NAME', '0.0.0'),
    license='gpl-3.0',
    description='DAST Security Helpers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='VWT Digital',
    author_email='support@vwt.digital',
    url='https://github.com/vwt-digital/sec-helpers/tree/master',
    keywords=['DAST', 'security', 'helpers', 'vwt'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
    install_requires=install_requires,
    python_requires='>=3.6',
)
