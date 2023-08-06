from setuptools import find_packages, setup


setup(
    name='queensbarry',
    version='0.0.2',
    description='Self use tool.',
    packages=find_packages(exclude=('test*',)),
    author='Queensbarry',
    author_email='queensbarry@foxmail.com',
    url='https://github.com/Queensbarry/qb',
    license='GPL License',
    python_requires='>3.8',
    include_package_data=True,
    install_requires=[
        'numpy>=1.21.0'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
