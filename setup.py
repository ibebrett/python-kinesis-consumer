from setuptools import setup, find_packages

setup(
    name='Python Kinesis Consumer',
    version='0.3',
    description='System for processing kinesis streams for python',
    author='Brett Jurman',
    author_email='i.be.brett@gmail.com',
    packages=find_packages(),

    install_requires = [
        'boto>=2.33.0',
        'sqlalchemy>=0.9.8'
    ]
)
