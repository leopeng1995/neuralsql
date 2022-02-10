import ast
import codecs
import re

from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with codecs.open('neuralsql/__init__.py', 'r', 'utf-8')  as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read()).group(1)))

description = 'NeuralSQL - Make MongoDB More Intelligent'

install_requirements = [
    'ChatterBot==1.0.5',
    # break PyYAML version
    # 'chatterbot-corpus==1.2.0',

    'click==6.7',
    'prompt-toolkit==2.0.9',
    'PyYAML>=5.1,<5.2',
    'pymongo[tls,srv]==3.8.0',
    'pyparsing==2.4.0',
    'Pygments==2.4.0',
    'tensorflow==2.5.3',
    'tqdm>=4.31.1',
    'requests>=2.21.0',
    'scikit-learn>=0.21.0',
    'jieba==0.39',
    'numpy==1.16.3',
    'Flask>=1.0.3',
]

dependency_links = [
    'https://github.com/gunthercox/chatterbot-corpus.git#egg=chatterbot-corpus'
]

setup(
    name='neuralsql',
    author='leopeng1995',
    author_email='pengliu@flowhub.ai',
    version=version,
    url='http://github.com/leopeng1995/neuralsql',
    packages=find_packages(),
    description=description,
    long_description=description,
    install_requires=install_requirements,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': ['neuralsql = neuralsql.main:cli'],
    },
)
