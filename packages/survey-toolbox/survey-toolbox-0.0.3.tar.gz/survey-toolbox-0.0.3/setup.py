import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="survey-toolbox",
    version="0.0.3",
    description="Add surveyor mathematics easily to your projects.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JayArghArgh/surveytoolbox",
    author="Justin Reid",
    author_email="jayarghargh@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["surveytoolbox"],
    include_package_data=True,
    # install_requires=["python-math"],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)
