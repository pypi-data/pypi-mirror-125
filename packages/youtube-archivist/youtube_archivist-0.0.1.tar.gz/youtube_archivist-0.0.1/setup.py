from setuptools import setup

setup(
    name='youtube_archivist',
    version='0.0.1',
    packages=['youtube_archivist'],
    url='',
    license='apache2',
    install_requires=["json_database>=0.3.0", "tutubo"],
    author='jarbasai',
    author_email='jarbasai@mailfence.com',
    description='youtube indexer - keep track of your favorite channels!'
)
