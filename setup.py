from setuptools import setup, find_packages

setup(
    name='BoxArcade',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.9',
        'Jinja2==2.6',
        'Werkzeug==0.8.3',
        'distribute==0.6.31',
        'itsdangerous==0.17',
        'requests==1.1.0',
        'wsgiref==0.1.2'
    ]
)
