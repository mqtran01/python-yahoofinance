import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yahoofinance",
    version="0.0.1",
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
        "pandas",
        "beautifulsoup4",
        "requests"
    ]

)