from setuptools import setup, find_namespace_packages

setup(
    name='addressbook_bot',
    version='1.0.0',
    description='Console helper to store and handle contacts and notes. Also it helps to sort files in any directory.',
    url='https://github.com/TT1410/Team-8-command-project',
    author='Team-8',
    author_email='team8@example.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=[
        'greenlet==2.0.1',
        'SQLAlchemy==1.4.43'
    ],
    entry_points={'console_scripts': ['hello-bot = addressbook_bot.main:main']}
)
