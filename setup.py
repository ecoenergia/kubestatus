from setuptools import setup, find_packages

setup(
    name='kubestatus',
    version='0.1.0',
    author='Stephen Dictor',
    author_email='sdictor@renew-ap.com',
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
