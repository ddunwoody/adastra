from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name = 'Ad Astra',
    version = __version__,
    packages = find_packages(),
    install_requires=['cocos2d>=0.5.0',],
    tests_require=['nose'],
    test_suite='nose.collector',
)