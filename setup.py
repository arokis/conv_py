from setuptools import setup, find_packages

setup(
    name='ConvPY',
    version='0.8.1',
    description='Conversion TOOL for XML-Data using SAXON and custom workflows',
    download_url = 'https://github.com/arokis/conv_py.git'
    author="Uwe Sikora",
    author_email="arokis.u@gmail.com",
    license = 'MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],
    keywords = 'xslt xsl xml saxon conversion converter xquery'
    # packages=find_packages(exclude=[]),
    install_requires=[],
    # pip install -e .[]
    )