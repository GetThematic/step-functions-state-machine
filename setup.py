from setuptools import setup, find_packages


setup(
    name="step_functions_state_machine",
    version="1.0.0",
    author="Thematic Ltd",
    author_email="contact@getthematic.com",
    url="http://getthematic.com/",
    description="",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=["jsonschema==2.6.0", "jsonpath-ng==1.5.3"],
)
