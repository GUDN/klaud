from pkg_resources import parse_requirements
from setuptools import find_packages, setup


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name='klaud',
    version='0.0.1',
    description='Base cloud storage with REST-API',
    license='MIT',
    author='GUDN',
    author_email='gudnmail@gmail.com',
    url='https://github.com/gudn/klaud',
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    entry_points={
        'console_scripts': [
            'klaud-server = klaud.__main__:main'
        ]
    },
    include_package_data=True
)
