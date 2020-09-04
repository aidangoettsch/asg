import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asg",
    version="1.0.0",
    author="Aidan Goettsch",
    description="A tool to automatically generate schematics from SPICE netlists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aidangoettsch/asg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requirements=["numpy", "lark-parser", "bentley_ottmann",],
    entry_points={"console_scripts": ["asg=asg.__init__:main"],},
    include_package_data=True,
    python_requires=">=3.6",
)
