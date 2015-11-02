from setuptools import setup, find_packages
import adastra

setup(
    name='adastra',
    version=adastra.__version__,
    packages=find_packages(),
    install_requires=['cymunk', 'cython==0.23', 'kivent_core', 'kivent_cymunk', 'kivy', 'numpy'],
    extras_require={'test': ['mock', 'pytest']},
    entry_points={
        'console_scripts': [
            'adastra=adastra.main:main',
            'kivy_example=adastra.kivy.main:main'
        ]
    }
)
