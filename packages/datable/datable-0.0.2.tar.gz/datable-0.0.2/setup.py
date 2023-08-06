from setuptools import setup, find_packages
import os
pkgs=list(filter(None, [x[0].replace('{}/src/'.format(os.getcwd()), '').replace('/','.') if '.git' not in x[0] else '' for x in os.walk('{}/src/'.format(os.getcwd()))]))
setup(
    name='datable',
    version='0.0.2',
    license='MIT',
    author="Ziplux LHS",
    author_email='ziplux.so@ziplux.so',
    packages=find_packages(include=pkgs),
    package_dir={'': 'src'},
    url='https://github.com/ZipluxLhs/datable',
    keywords='data',
    install_requires=[
           'pip',
	  'setuptools',
      ],

)