from setuptools import setup, find_packages

setup(
    name="topsis-daksh-102497020",
    version="1.0.0",
    author="Daksh",
    description="TOPSIS implementation using Python",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_daksh_102497020.cli:main"
        ]
    },
)
