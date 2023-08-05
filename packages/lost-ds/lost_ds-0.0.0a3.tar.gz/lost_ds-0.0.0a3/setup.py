import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lost_ds", # Replace with your own username
    version="0.0.0-alpha.3",
    author="L3bm GmbH",
    author_email="info@l3bm.com",
    description="Lost Dataset library",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l3p-cv/lost_ds",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)