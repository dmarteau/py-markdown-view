from setuptools import setup, find_packages, Extension
import os


def parse_requirements( filename ):
    with open( filename ) as fp:
        return list(filter(None, (r.strip('\n ').partition('#')[0] for r in fp.readlines())))

version_tag = "0.1"

kwargs = {}

with open('README.md') as f:
    kwargs['long_description'] = f.read()

# Parse requirement file and transform it to setuptools requirements'''
requirements = 'requirements.txt'
if os.path.exists(requirements):
    kwargs['install_requires']=parse_requirements(requirements)

setup(
    name='markdown-display',
    version=version_tag,
    author='David Marteau',
    maintainer='David Marteau',
    description="Simple markdown server viewer",
    url='',
    packages=find_packages(include=['markdown_display','markdown_display.*']),
    entry_points={
        'console_scripts': [
            'markdown-display = markdown_display.viewer:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    **kwargs
)

