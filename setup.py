import setuptools

make_package=setuptools.setup(
    name="consignement-pricing",
    version="0.1",
    author=["rohan"],
    description=("Consignment Pricing Prediction"),
    license="MIT",
   packages = setuptools.find_packages(where="src"), python_requires='>=3.6',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    
    )
    