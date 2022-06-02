from setuptools import setup,find_packages

setup(      
    name='main',
    version='0.1.0',    
    description='Main package for this repository',
    install_requires=['flask','flask_cors','joblib','numpy',],
    packages=find_packages(),
    license="MIT"
    )
