from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup(**generate_distutils_setup(packages=['valve_edge_node'], package_dir={'': 'src'}))
