# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyftype', 'pyftype.modules']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ftype = pyftype.cli:main']}

setup_kwargs = {
    'name': 'pyftype',
    'version': '1.0.1',
    'description': '类型检测',
    'long_description': '\npyftype\n=======\n\n一个类型检测库。\n\n特性\n~~~~\n\n\n#. 类型检测完全模块化，需要检测新的类型，直接参考modules中的检测，编写即可。\n#. 主要面向逆向工程方向的类型检测，也支持一般类型检测。\n\n安装\n~~~~\n\n.. code-block::\n\n   pip install pyftype\n\n用法\n~~~~\n\n具体参考examples目录\n\n参考\n~~~~\n\n\n* https://github.com/h2non/filetype.py\n* https://github.com/kin9-0rz/cigam\n',
    'author': 'kin9-0rz',
    'author_email': 'kin9-0rz@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitee.com/kin9-0rz/pyftype',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
