import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="openvpn3_handler",
    version="0.0.2",
    author="Juan Barbosa",
    author_email="js.barbosa10@uniandes.edu.co",
    maintainer="Juan Barbosa",
    maintainer_email="js.barbosa10@uniandes.edu.co",
    description=(
        "Tool develop to easily handle connections with OpenVPN3 in Linux."
    ),
    license="GPL",
    keywords="example documentation tutorial",
    url="https://github.com/jsbarbosa/openvpn3_handler",
    packages=['openvpn3_handler'],
    install_requires=['littlenv>=0.1.7', 'pexpect>=4.8.0'],
    long_description="",
    entry_points={
        'console_scripts': [
            'openvpn3_handler = openvpn3_handler.main:run',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)
