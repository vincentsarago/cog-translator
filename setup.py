"""Setup."""

from setuptools import setup, find_packages

with open("cog_translator/__init__.py") as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break

# Runtime requirements.
inst_reqs = ["click", "rasterio[s3]", "rio-cogeo", "wget"]

extra_reqs = {"test": ["pytest", "pytest-cov", "mock"]}


setup(
    name="cog_translator",
    version=version,
    description=u"Download, convert to COG and upload a file",
    long_description=u"Download, convert to COG and upload a file",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="AWS-Lambda Python",
    author=u"",
    author_email="",
    url="",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points={"console_scripts": ["worker=cog_translator.scripts.cli:main"]},
)
