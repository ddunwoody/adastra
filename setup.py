from setuptools import setup, find_packages
import adastra

setup(
    name='adastra',
    version=adastra.__version__,
    packages=find_packages(),
    install_requires=['cymunk', 'cython', 'kivent_core', 'kivent_cymunk', 'kivy', 'kivy-garden', 'numpy'],
    tests_require=['mock', 'pytest'],
    entry_points={
        'console_scripts': [
            'adastra=adastra.main:main',
        ]
    }
)
