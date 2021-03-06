import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-polar-codes2",
    version="1.3",
    author="Brendon McBain",
    license="MIT",
    author_email="brendon.mcbain9@gmail.com",
    description="A package for polar codes in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/david13pod/polarcodegui",
    download_url="https://github.com/david13pod/polarcodegui/tarball",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
              'numpy',
              'matplotlib',
          ],
)