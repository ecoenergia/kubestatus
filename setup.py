from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='kubestatus',
    version='0.1.3',
    author='Stephen Dictor',
    author_email='sdictor@renew-ap.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ecoenergia/kubestatus.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'kubestatus=kubestatus.viewer:main',
        ],
    },
)
