from distutils.core import setup
from setuptools import find_packages

setup(
    name='tkpdb',
    version='0.1',
    author='Gijs Molenaar',
    author_email='gijsmolenaar%(at)sgmail.com' % {'at': '@'},
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/gijzelaerr/banana',
    license='BSD licence, see LICENCE',
    description='A webinterface for TKP',
    long_description=open('README.rst').read(),
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: JavaScript',
    ],
)
