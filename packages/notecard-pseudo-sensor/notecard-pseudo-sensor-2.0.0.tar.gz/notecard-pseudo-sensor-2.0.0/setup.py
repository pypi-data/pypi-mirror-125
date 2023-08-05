import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notecard-pseudo-sensor",
    version="2.0.0",
    author="Blues Inc.",
    author_email="support@blues.com",
    description="An API interface to the internal sensors of the Blues Wireless Notecard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blues/notecard-pseudo-sensor-python",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    install_requires=["note-python"],
    python_requires='>=3.6',
)