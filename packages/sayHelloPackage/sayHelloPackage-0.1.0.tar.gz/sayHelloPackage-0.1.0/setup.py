from setuptools import setup

setup(
    name='sayHelloPackage',
    author='Veronika Anikina',
    author_email='lalala@gmail.com',
    url='https://github.com/lalala/example-package-repo',
    version='0.1.0',
    description='just an example package',
    packages=['sayHelloPackage'],
    install_requires=[
        'numpy<=1.17.2',
        'pandas==1.3.4',
    ],
)