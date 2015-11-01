from setuptools import setup, find_packages
import adastra

setup(
    name='adastra',
    version=adastra.__version__,
    packages=find_packages(),
    install_requires=['numpy', 'pymunk', 'cocos2d', 'pyglet'],
    # install_requires=['numpy', 'pygame', 'pymunk'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'adastra=adastra.main:main',
            'box2d=adastra.box2d_pyramid:main'
        ]
    }
)
