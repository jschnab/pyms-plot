import os
import re
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

version = re.search(
        "^__version__\s*=\s*'(.*)'",
        open('pyms/pyms.py').read(),
        re.M
        ).group(1)

with open(os.path.join(here, 'README.md')) as infile:
    long_description = infile.read()

setup(
        name='pyms-plot',
        packages=['pyms'],
        entry_points={
            'console_scripts': ['pyms=pyms.pyms:main']
            },
        version=version,
        description='PyMS (Python for Mycorrhizal Symbiosis)',
        long_description=long_description,
        url='https://github.com/jschnab/pyms',
        author='Jonathan Schnabel',
        author_email='jonathan.schnabel31@gmail.com',
        license='GNU General Public License v3.0',
        classifiers=[
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering',
            'Programming Language :: Python :: 3.5',
        ],
        python_requires='>=3.5.2',
        keywords='arbuscular mycorrhizal symbiosis data analysis statistics',
        install_requires=['numpy', 'scipy', 'pandas', 'matplotlib', 'statsmodels'],
)
