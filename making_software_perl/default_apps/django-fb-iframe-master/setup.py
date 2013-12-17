from setuptools import setup, find_packages

setup(
    name='django-fb-iframe',
    version='0.1.1',
    description='A small Django app to prevent CSRF request errors by a Facebook iframe.',
    long_description=open('README.rst').read(),
    author='Janneke Janssen',
    author_email='j.janssen@lukkien.com',
    url='http://github.com/jjanssen/django-fb-iframe',
    packages=find_packages(exclude=['example_fb_iframe']),
    include_package_data=True
)