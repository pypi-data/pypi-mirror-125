# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuat_feed']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'tuat-feed',
    'version': '0.1.3',
    'description': 'Unofficial library for fetching the feed for TUAT',
    'long_description': '# (非公式)TUAT掲示板ライブラリ\n\n## インストール\n* `python` >= 3.7\n\n```sh\n$ pip install tuat-feed\n```\n\n## 使い方\n```python\n>>> import tuat_feed\n>>> feed = tuat_feed.fetch()\n>>> len(feed)\n40\n>>> feed[0]\nPost(...)\n```\n\n`Post`の定義は',
    'author': 'Shogo Takata',
    'author_email': 's196643z@st.go.tuat.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
