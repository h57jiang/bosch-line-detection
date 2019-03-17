
from setuptools import find_packages, setup

with open('requirements.txt') as fp:
    install_requires = fp.read()


setup(
    name='bosch-line-detection',
    version='1.0.0',
    description='web application for bosch line detection',
    author='Hai (Wisdom) Jiang',
    author_email='h57jiang@uwaterloo.ca',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
