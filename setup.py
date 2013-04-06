from distutils.core import setup
setup(
    name = 'todoq',
    packages = ['todoqlib', 'todoqlib.test'],
    scripts = ['scripts/todoq'],
    version = '1.0.11',
    description = 'Simplest command-line TODO list',
    author = 'Jeff Jia',
    author_email = 'jeffjia@outlook.com',
    url = 'http://jeffjia.github.com/TODOQ/',
    license = 'LICENSE.txt',
    long_description = open('README.txt').read(),
    classifiers = ['Development Status :: 2 - Pre-Alpha',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'Intended Audience :: System Administrators',
      'Environment :: Console',
      'License :: OSI Approved :: Apache Software License',
      'Topic :: Office/Business :: Scheduling',
      'Topic :: Utilities'
      ],
)
