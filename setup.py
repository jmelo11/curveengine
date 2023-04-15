from setuptools import setup, find_packages


setup(
    name='curvemanager',
    version='1.0.0',
    description='A simple curve manager for ORE/QuantLib',
    author='Jose Melo',
    packages=find_packages(where='src'),
    py_modules=["curvemanager"],
    package_dir={'': 'src'},
    package_data={
        "": ["*.py"]
    },
    author_email='jmelo@live.cl',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
    install_requires=[
        'open-source-risk-engine']
)