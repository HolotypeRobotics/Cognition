from setuptools import setup, find_packages

setup(
    name='cognition',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'htm.core'
    ],
    author='Josh Collins',
    author_email='josh@holotyperobotics.com',
    description='Library for cognitive agents',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
