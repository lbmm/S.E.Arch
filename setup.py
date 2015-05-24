try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import pubblicazioniASI 

config = {
    'description': 'ASI Publication portal',
    'author': 'fmoscato',
    'url': '',
    'version': pubblicazioniASI.__version__,
    'download_url': 'Where to download it.',
    'author_email': 'fmoscato@asdc.asi.it',
    'install_requires': ['nose', 'pymongo', 'reportlab', 'bibtexparser', 'bottle'],
    'packages': ['pubblicazioniASI'],
    'scripts': [],
    'name': 'PubblicazioniASI',
    'long_description': open('README.md').read(),
    'entry_points': {
        'console_scripts': [
            'serve = pubblicazioniASI.publication:run_server',
                           ]
                    },
    'package_data': {
        'pubblicazioniASI': ['static/*', 'js/*.js','js/library/*.js', 'views/*.tpl'],
       },
        'include_package_data': True
}

setup(**config)
