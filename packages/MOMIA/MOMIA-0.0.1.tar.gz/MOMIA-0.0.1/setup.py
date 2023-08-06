import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MOMIA",
    version="0.0.1",
    author="jz-rolling",
    author_email="juzhu@hsph.harvard.edu",
    description="Mycobacteria-Optimized Microscopy Image Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jzrolling/MOMIA',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)