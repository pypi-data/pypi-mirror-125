#!/usr/bin/env python
import setuptools
from setuptools import find_packages
from os import path

README_FILE = path.join(path.dirname(__file__), 'README.pypi')
LONG_DESCRIPTION = open(README_FILE).read()

ENTRY_POINTS = {
    'orange3.addon': ('bioinformatics = orangecontrib.bioinformatics', ),
    'orange.widgets': ('Bioinformatics = orangecontrib.bioinformatics.widgets', ),
    'orange.canvas.help': ('html-index = orangecontrib.bioinformatics.widgets:WIDGET_HELP_PATH', )
}

if __name__ == '__main__':
    setuptools.setup(
        # use_scm_version=True,
        # setup_requires=['setuptools-scm', 'setuptools>=40.0'],
        name='BlueWhale3-Bioinformatics',
        version='4.1.3',
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        license='GPL3+',
        package_data={'orangecontrib.bioinformatics': ['locale/*.yml']},
        packages=find_packages(),
        include_package_data=True,
        entry_points=ENTRY_POINTS,
        install_requires=[
            'BlueWhale3>=3.28.0',
            'bluewhale-widget-base>=4.14.1',
            'scipy>=1.5.0',
            'setuptools-scm',
            'pyclipper>=1.2.0',
            'point-annotator~=2.0',
            'requests',
            'requests-cache>=0.8.0',
            'serverfiles',
            'resdk>=13.3.0',
            'genesis-pyapi',
            # Versions are determined by Orange
            'numpy',
        ],
        extras_require={
            # docutils changed html in 0.17; fixing to 0.16 until parser fixed
            # todo: remove docutils when parser fixed in widget-base and released
            'doc': ['sphinx', 'recommonmark', 'sphinx_rtd_theme', 'docutils<0.17'],
            'test': [
                'flake8',
                'flake8-comprehensions',
                'flake8-black',
                'pep8-naming',
                'isort',
                'pre-commit',
                'pytest',
                'coverage',
                'codecov',
            ],
        },
        keywords=('orange3 add-on', ),
        namespace_packages=["orangecontrib"],
        test_suite="setup._discover_tests",
        zip_safe=False,
        author='大圣实验楼',
        author_email='dashenglab@163.com',
        url="https://github.com/biolab/orange3-bioinformatics",
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'Development Status :: 1 - Planning',
            'Programming Language :: Python :: 3 :: Only',
            'Operating System :: OS Independent',
        ],
    )