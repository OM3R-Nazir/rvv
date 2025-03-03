from setuptools import setup, find_packages

setup(
    name="rvv",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18",    
    ],
    author="Omer Nazir",
    description="A library for RISC-V Vector extensions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OM3R-Nazir/rvv.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    license="MIT",
)
