#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

version = "0.1.0"

if __name__ == "__main__":
    setuptools.setup(
        name="EnactiveAgents",
        version=version,
        description="An implementation of the Enactivist Cognitive Architecture in Python",
        author="Thomas Churchman",
        author_email="thomas@churchman.nl",
        url="https://github.com/beskhue/enactive-agents",
        packages=setuptools.find_packages(),
        install_requires=[
            "pygame>=1.9.1"
        ],
        dependency_links=['https://bitbucket.org/pygame/pygame/get/release_1_9_1release.zip#egg=pygame-1.9.1']
    )
