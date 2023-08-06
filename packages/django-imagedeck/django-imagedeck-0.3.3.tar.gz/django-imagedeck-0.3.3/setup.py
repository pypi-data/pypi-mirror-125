# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imagedeck',
 'imagedeck.management.commands',
 'imagedeck.migrations',
 'imagedeck.templatetags']

package_data = \
{'': ['*'],
 'imagedeck': ['static/imagedeck/vendor/jquery-file-upload/jquery.fileupload.js',
               'static/imagedeck/vendor/jquery-file-upload/jquery.fileupload.js',
               'static/imagedeck/vendor/jquery-file-upload/jquery.iframe-transport.js',
               'static/imagedeck/vendor/jquery-file-upload/jquery.iframe-transport.js',
               'static/imagedeck/vendor/jquery.ui.widget.js']}

install_requires = \
['Django>=3.2.6,<4.0.0',
 'django-filer>=2.0.2,<3.0.0',
 'django-imagekit>=4.0.2,<5.0.0',
 'django-polymorphic>=3.0.0,<4.0.0',
 'easy-thumbnails>=2.7.1,<3.0.0',
 'iiif-prezi>=0.3.0,<0.4.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'django-imagedeck',
    'version': '0.3.3',
    'description': 'A package to seamlessly group different sorts of images into groups.',
    'long_description': '# django-imagedeck\n\nA package to seamlessly group different sorts of images into groups.\n\n',
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.unimelb.edu.au/rturnbull/django-imagedeck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
