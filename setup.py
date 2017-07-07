import re
from setuptools import setup


with open('outcast/__init__.py') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                                    fd.read(), re.MULTILINE).group(1)

requirements = []
test_requirements = ['colorama>=0.3.6', 'python-termstyle>=0.1.10', 'rednose>=0.4.3']
setup(
    name='outcast',
    version=version,
    install_requires=requirements,
    tests_require=test_requirements,
)
