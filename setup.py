from setuptools import setup

setup(
    name='ceaos_reservoir',
    version='0.0.1',
    packages=['ceaos_reservoir'],
    install_requires=[
        'pigpio',
        'zmq'
    ],
)
