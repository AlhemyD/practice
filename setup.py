from setuptools import setup, find_packages

setup(
    name='practice',
    version='0.4.0',
    description='Что-то на тесте',
    author='Deppkepa, mgwoorl, AlhemyD',
    author_email='dasha.sisimirova@bk.ru',
    url='https://github.com/AlhemyD/practice.git',
    packages=['src'],
    install_requires=[
        'requests',
        'apscheduler',
        'fastapi',
        'pydantic==1.10.2',
        'paho-mqtt'
    ],
    python_requires='>=0'
)
