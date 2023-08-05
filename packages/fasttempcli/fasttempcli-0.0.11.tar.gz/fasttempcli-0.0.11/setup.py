from setuptools import setup

setup(
    name='fasttempcli',
    version='0.0.11',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author_email = 'luis78270@gmail.com',
    author = 'Luis Ernandes',
    py_modules=['fastcli'],
    keywords = ['fastcli', 'fastapi', 'fascli', 'cli', 'api', 'template', 'heroku'],
    description = 'Template of fastapi to upload to heroku',
    url = 'https://github.com/LErnandes/fastcli',
    install_requires=[
        'click',
        'emoji',
        'fastapi',
        'typing',
        'uvicorn',
    ],
    entry_points={
        'console_scripts': [
            'fastcli = fastcli.main:cli',
        ],
    },
)
