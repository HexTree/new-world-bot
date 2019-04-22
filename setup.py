from setuptools import setup, find_packages

setup(
    name='NewWorldBot',
    author='Liam Mencel',
    version='0.1dev',
    description='Discord bots related to the game: New World',
    packages=find_packages(exclude=('tests', 'docs', 'data')),
    license='MIT',
    long_description=open('README.md').read(),
    python_requires='>=3.6.0',
    install_requires=['discord.py'],
)