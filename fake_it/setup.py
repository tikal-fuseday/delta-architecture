#!/usr/bin/env python
from setuptools import find_packages, setup


project = "fake_it"

setup(
    name=project,
    version="0.0.1",
    description="Election faker",
    author="Tom Caspy",
    author_email="tom@tikalk.com",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "alembic==1.4.0",
        "faker==4.0.0",
        "flask>=1.1.1",
        "psycopg2>=2.8.4",
        "werkzeug==0.16.1",
    ],
)