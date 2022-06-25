from setuptools import setup,find_packages

setup(name="source/train_evaluate",version="1.0.0",description="Creating package for my machine learning project",url="https://consignmentpricing.herokuapp.com/",author="Rohan Patankar",license="MIT",packages=find_packages(include=["numpy","scikit-learn","pandas","joblib"]),python_requires='>=3')