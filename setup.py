from distutils.core import setup

setup(
    name='tkpdb',
    version='0.1',
    author='Gijs Molenaar',
    author_email='gijsmolenaar%(at)sgmail.com' % {'at': '@'},
    packages=['tkpdb'],
    url='https://github.com/gijzelaerr/banana',
    license='BSD licence, see LICENCE',
    description='A webinterface for TKP',
    long_description=open('README.rst').read(),
    zip_safe=False,
)
