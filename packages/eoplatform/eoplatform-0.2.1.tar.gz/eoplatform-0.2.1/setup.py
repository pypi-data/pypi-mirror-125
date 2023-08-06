# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eoplatform',
 'eoplatform.composites',
 'eoplatform.download',
 'eoplatform.info',
 'eoplatform.metadata',
 'eoplatform.platforms',
 'eoplatform.platforms.Landsat8']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.3,<2.0.0', 'rich>=10.12.0,<11.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['eoplatform = eoplatform.cli:app']}

setup_kwargs = {
    'name': 'eoplatform',
    'version': '0.2.1',
    'description': 'Earth Observation made easy.',
    'long_description': '<br/>\n<p align="center">\n  <a href="https://github.com/mtralka/EOPlatform">\n    <img src="images/logo.jpg" alt="EOP Logo" width="300" height="300">\n  </a>\n\n  <h3 align="center">An Earth Observation Platform</h3>\n\n  <p align="center">\n    Earth Observation made easy. \n    <br/>\n    <br/>\n    <a href="https://github.com/mtralka/EOPlatform/issues">Report Bug</a>\n    |\n    <a href="https://github.com/mtralka/EOPlatform/issues">Request Feature</a>\n  </p>\n</p>\n\n![Downloads](https://img.shields.io/github/downloads/mtralka/EOPlatform/total) ![Forks](https://img.shields.io/github/forks/mtralka/EOPlatform?style=social) ![Stargazers](https://img.shields.io/github/stars/mtralka/EOPlatform?style=social) <br/> ![Issues](https://img.shields.io/github/issues/mtralka/EOPlatform) ![License](https://img.shields.io/github/license/mtralka/EOPlatform) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![mypy](https://img.shields.io/badge/mypy-checked-brightgreen)\n\n## About\n\n*eoplatform* is a Python package that aims to simplify Remote Sensing Earth Observation by providing actionable information on a wide swath of RS platforms and provide a simple API for downloading and visualizing RS imagery. Made for scientists, educators, and hobbiests alike.\n\n* Easy to access **information** on RS platforms\n  * Band information\n  * Orbit regimes\n  * Scene statistics\n  * etc\n* `metadata` module for extracting platform metadata\n  * supports `.txt` and `.xml` files\n* `composites` modules for creating and learning about popular RS band composites\n  * Included so far - NDVI, SR, DVI, EVI, EVI2, NDWI, NBR, NDSI, NDBI\n\nComing soon:\n\n* Data downloading\n  * Landsat 8\n  * Sentinel-2\n* Raster tools\n  * Raster IO functions\n\n### Installation\n\n`eoplatform` can be installed by running `pip install eoplatform`. It requires Python 3.7 or above to run. \n\n### Example\n\n<img src="images/eoplatform-info-landsat8.PNG" alt="Landsat8 Info" width="600">\n\n## Usage\n\n*eoplatform* is accessible through the command line (CLI) and as a module import.\n\n### Querying platform info\n\n#### CLI\n\n`PLATFORM` argument is case-insensitive\n\n```sh\nUsage: eoplatform info [OPTIONS] PLATFORM\n\nArguments:\n  PLATFORM  [required]\n\nOptions:\n  -d, --description / -nd, --no-description\n                                  [default: description]     \n  --help                          Show this message and exit.\n```\n\nEX:\n\n```sh\neoplatform info landsat8\n```\n\nshow all info *eoplatform* has on `Landsat8`\n\n```sh\neoplatform info landsat8 -b\n```\n\nshows only `Landsat8`\'s bands\n\n#### Module import\n\nYou can import your desired platform\n\n```python\nfrom eoplatform import landsat8\n\nlandsat8.info()  # OR print(landsat8)\n```\n\nor search from the *eoplatform* module itself\n\n```python\nimport eoplatform as eop\n\neop.info("Landsat8")  # case insensitive\n```\n\n### Downloading platform scenes\n\n#### CLI\n\nin-progress\n\n```sh\nUsage: eoplatform download [OPTIONS] PLATFORM\n\nArguments:\n  PLATFORM  [required]\n\nOptions:\n  --help  Show this message and exit.\n```\n\n#### Module import\n\n in-progress\n\n ```python\nfrom eoplatform import landsat8\n\nlandsat8.download()\n```\n\n```python\nimport eoplatform as eop\n\neop.download("landsat8")\n```\n\nboth methods accept the full range of search keword arguments\n\n### Band composites\n\nImplemented composites:\n\n* Normalized Difference Vegetation Index (NDVI)\n* Simple Ratio (SR)\n* Difference Vegetation Index (DVI)\n* Enhanced Vegetation Index (EVI)\n* Enhanced Vegetation Index 2 (EVI2)\n* Normalized Difference Water Index (NDWI)\n* Normalized Burn Ratio (NBR)\n* Normalized Difference Snow Index (NDSI)\n* Normalized DIfference Built-Up Index (NDBI)\n\n#### Composite information\n\n```python\nfrom eoplatform.composites import NDVI  # DVI, etc\n\nNDVI.info()\n```\n\n#### Creating composite\n\n```python\nfrom eoplatform.composites import NDVI\n\nred_array: np.ndarray = ...\nnir_array: np.ndarray = ...\n\nndvi: np.ndarray = NDVI.create(nir_array, red_array)\n```\n\n### Metadata extraction\n\nSupports `.txt` and `.xml` files through `extract_XML_metadata` and `extract_TXT_metadata`.\n\n```python\nfrom eoplatform.metadata import extract_XML_metadata\n\nfile_path: str = ...\ntarget_attributes: List[str] = ...\n\nvalues: Dict[str, str] = extract_XML_metadata(file_path, target_attributes)\n```\n\n## Roadmap\n\nSee the [open issues](https://github.com/mtralka/EOPlatform/issues) for a list of proposed features (and known issues).\n\n* download support\n\n## Contributing\n\nContributions are welcome. Currently, *eoplatform* is undergoing rapid development and contribution opportunities may be scarce.\n\n* If you have suggestions for adding or removing features, feel free to [open an issue](https://github.com/mtralka/EOPlatform/issues/new) to discuss it, or directly create a pull request with the proposed changes.\n* Create individual PR for each suggestion.\n* Use pre-commit hooks - `pre-commit install`\n* Code style is `black`, `mypy --strict`\n\n## License\n\nDistributed under the GNU GPL-3.0 License. See [LICENSE](https://github.com/mtralka/EOPlatform/blob/main/LICENSE.md) for more information.\n\n## Built With\n\n* [Rich](https://github.com/willmcgugan/rich)\n* [Typer](https://github.com/tiangolo/typer)\n\n## Authors\n\n* [**Matthew Tralka**](https://github.com/mtralka/)\n',
    'author': 'Matthew Tralka',
    'author_email': 'matthew@tralka.xyz',
    'maintainer': 'Matthew Tralka',
    'maintainer_email': 'matthew@tralka.xyz',
    'url': 'https://github.com/mtralka/EOPlatform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
