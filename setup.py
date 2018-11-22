import os
import sys
import setuptools

if sys.argv[-1] == 'build':
    os.system('python setup.py sdist bdist_wheel')
    sys.exit()
elif sys.argv[-1] == 'test':
    os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
    sys.exit()
elif sys.argv[-1] == 'deploy':
    os.system('twine upload dist/*')
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yahoofinance",
    version="0.0.2",
    author="Michael Tran",
    author_email="example@example.com",
    description="A library to retrieve data from Yahoo Finance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mqtran01/python-yahoo-finance",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    install_requires=[
        "pandas>=0.23.4",
        "beautifulsoup4>=4.6.3",
        "requests>=2.20.1"
    ]

)