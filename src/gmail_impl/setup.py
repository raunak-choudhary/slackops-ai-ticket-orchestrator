from setuptools import find_packages, setup

setup(
    name="gmail_impl",
    version="0.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.11",
)
