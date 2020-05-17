import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speedmath",
    version="0.0.1",
    author="Marco Herrera-Rendon",
    author_email="mherrerarendon@gmail.com",
    description="Use this package for all your speed/pace conversion needs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mherrerarendon/mhPacer/lib/speedmath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
