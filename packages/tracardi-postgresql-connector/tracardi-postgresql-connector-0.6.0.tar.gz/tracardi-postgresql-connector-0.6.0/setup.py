from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-postgresql-connector',
    version='0.6.0',
    description='The purpose of this plugin is to connect with postresql',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Risto Kowaczewski`',
    author_email='risto.kowaczewski@gmail.com',
    packages=['tracardi_postgresql_connector'],
    install_requires=[
        'pydantic',
        'asyncio',
        'tracardi',
        'tracardi-plugin-sdk>0.6.22',
        'asyncpg'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['tracardi', 'plugin'],
    python_requires=">=3.8",
    include_package_data=True
)