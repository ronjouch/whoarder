from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='whoarder',
    version='0.3.0',
    description="whoarder converts your Kindle's 'My Clippings.txt' file to a more pleasant, sortable, filterable HTML file",
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    keywords='amazon kindle transform notes highlights clippings html',
    author='Ronan Jouchet',
    author_email='ronan@jouchet.fr',
    url='https://github.com/ronjouch/whoarder',
    license='LICENSE.txt',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={'whoarder': ['templates/*.html']},
    test_suite='test',
    scripts=['bin/whoarder'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'jinja2',
        'chardet2',
    ],
)
