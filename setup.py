from setuptools import setup 

with open('README.txt') as file:
    long_description = file.read()
#^

with open('requirements.txt') as fp:
    install_requires = fp.read()
#^

setup(
    name ='broja2pid',
    version='1.0.1',
    description='A robust estimator for the bivariate partial information decomposition measure BROJA',
    url='https://github.com/Abzinger/BROJA_2PID',
    author='Abdullah Makkeh and Dirk Oliver Theis',
    author_email='abdullah.makkeh@gmail.com',
    license=['Apache License 2.0'],
    packages=['broja2pid'],
    install_requires=install_requires,
    classifiers=[
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Development Status :: 5 - Production/Stable",
    "Operating System :: POSIX :: Linux",
    "Intended Audience :: Science/Research",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
