# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rafm']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'numpy',
 'pandas>=1.3.4,<2.0.0',
 'statsdict>=0.1.3,<0.2.0',
 'typer']

entry_points = \
{'console_scripts': ['rafm = rafm.__main__:main']}

setup_kwargs = {
    'name': 'rafm',
    'version': '0.3.0',
    'description': 'rafm',
    'long_description': '================================\nrafm Reliable AlphaFold Measures\n================================\n\n.. image:: https://raw.githubusercontent.com/unmtransinfo/rafm/master/docs/_static/calmodulin.png\n   :target: https://raw.githubusercontent.com/unmtransinfo/rafm/master/docs/_static/calmodulin.png\n   :alt: AlphaFold model and two crystal structures of calmodulin\n\n*rafm* computes per-model measures associated with atomic-level accuracy for\nAlphaFold models from *pLDDT* confidence scores.  Outputs are to a\ntab-separated file.\n\n\nInstallation\n------------\n\nYou can install *rafm* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install rafm\n\n\nUsage\n-----\n*rafm --help* lists all commands. Current commands are:\n\n* *plddt-stats*\n    Calculate stats on bounded pLDDTs from list of AlphaFold model files.\n    in PDB format.\n\n    Options:\n\n        * *--criterion FLOAT*\n            The cutoff value on truncated pLDDT for possible utility. [default: 91.2]\n        * *--min-length INTEGER*\n            The minimum sequence length for which to calculate truncated stats.\n            [default: 20]\n        * *--min-count INTEGER*\n            The minimum number of truncated *pLDDT* values for which to calculate stats.\n            [default: 20]\n        * *--lower-bound INTEGER*\n            The *pLDDT* value below which stats will not be calculated. [default: 80]\n        * *--upper-bound INTEGER*\n            The *pLDDT* value above which stats will not be calculated. [default: 100]\n        * *--file-stem TEXT*\n            Output file name stem. [default: rafm]\n\n    Output columns (where *NN* is the bounds specifier, default: 80):\n\n        * *residues_in_pLDDT*\n            The number of residues in the AlphaFold model.\n        * *pLDDT_mean*\n            The mean value of pLDDT over all residues.\n        * *pLDDT_median*\n            The median value of pLDDT over all residues.\n        * *pLDDTNN_count*\n            The number of residues within bounds.\n        * *pLDDTNN_frac*\n            The fraction of pLDDT values within bounds, if the\n            count is greater than the minimum.\n        * *pLDDTNNN_mean*\n            The mean of pLDDT values within bounds, if the\n            count is greater than the minimum.\n        * *pLDDTNN_median*\n            The median of pLDDT values within bounds, if the\n            count is greater than the minimum.\n        * *LDDT_expect*\n            The expectation value of global *LDDT* over the\n            residues with *LDDT* within bounds.  Only\n            produced if default bounds are used.\n        * *passing*\n            True if the model passed the criterion, False\n            otherwise.  Only produced if default bounds are\n            used.\n        * *file*\n            The path to the model file.\n\n* *plddt-select-residues*\n    Writes a tab-separated file of residues from passing models,\n    using an input file of values selected by *plddt-stats*.\n    Input options are the same as *plddt-stats*.\n\n    Output columns:\n\n        * *file*\n            Path to the model file.\n        * *residue*\n            Residue number, starting from 0 and numbered\n            sequentially.  Note that *all* residues will be\n            written, regardless of bounds set.\n        * *pLDDT*\n            pLDDT value for that residue.\n\nStatistical Basis\n-----------------\nThe default parameters were chosen to select for *LDDT* values of greater\nthan 80 on a set of crystal structures obtained since AlphaFold was trained.  The\ndistributions of *LDDT* scores for the passing and non-passing sets, along\nwith an (overlapping) set of PDB files at 100% sequence identity over\nat least 80% of the sequence looks like this:\n\n.. image:: https://raw.githubusercontent.com/unmtransinfo/rafm/master/docs/_static/lddt_dist.png\n   :target: https://raw.githubusercontent.com/unmtransinfo/rafm/master/docs/_static/lddt_dist.png\n   :alt: Distribution of high-scoring, low-scoring, and high-similarity structures\n\nThe markers on the *x*-axis refer to the size of conformational changes observed in\nconformational changes in various protein crystal structures:\n\n* *CALM*\n    Between calcum-bound and calcium-free calmodulin (depicted in the logo image above).\n* *ERK2*\n    Between unphosphorylated and doubly-phosphorylated ERK2 kinase.\n* *HB*\n    Between R- and T-state hemoglobin\n* *MB*\n    Between carbonmonoxy- and deoxy-myoglobin\n\nWhen applied to set of "dark" genomes with no previous PDB entries, the distributions of\nmedian *pLDDT* scores with a lower bound of 80 and per-residue *pLDDT* scores looks like\nthis:\n\n.. image:: https://raw.githubusercontent.com/unmtransinfo/rafm/master/docs/_static/tdark_dist.png\n   :target: https://raw.githubusercontent.com/unmtransinfo/rafm/master/docs/_static/tdark_dist.png\n   :alt: Distribution of *pLDDT80* scores and per-residue *pLDDT* scores\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*rafm* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from the `UNM Translational Informatics Python Cookiecutter`_ template.\n\n*rafm* was written by Joel Berendzen and Jessica Binder.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _UNM Translational Informatics Python Cookiecutter: https://github.com/unmtransinfo/cookiecutter-unmtransinfo-python\n.. _file an issue: https://github.com/unmtransinfo/rafm/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://rafm.readthedocs.io/en/latest/usage.html\n',
    'author': 'UNM Translational Informatics Team',
    'author_email': 'datascience.software@salud.unm.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unmtransinfo/rafm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
