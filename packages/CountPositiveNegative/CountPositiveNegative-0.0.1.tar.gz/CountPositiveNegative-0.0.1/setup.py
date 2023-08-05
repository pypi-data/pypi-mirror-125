from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup (
    name = 'CountPositiveNegative',
    version = '0.0.1',
    description = 'Count the positive and negative number in the list.',
    url = '',
    author = 'UMESHA RAMESHA HUGGER',
    author_email = 'uumesharameshahugger@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = 'CountPosiveNegative',
    packages = find_packages(),
    install_requires = ['']
)