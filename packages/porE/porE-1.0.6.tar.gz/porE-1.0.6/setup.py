import setuptools
from numpy.distutils.core import Extension, setup

with open("porE/version.py", "r") as fh:
    version = {}
    exec(fh.read(), version)

with open("README.md", "r") as fh:
     name="porE",
     long_description = fh.read()

setup(
   name="porE",
   version=version["__version__"],
   author="Kai Trepte",
   author_email="kai.trepte1987@gmail.com",
   description="Porosity Evaluation tool",
   url="https://gitlab.com/openmof/porE", 
   license='APACHE2.0',
   long_description=long_description,
   long_description_content_type="text/markdown",
   include_package_data=True,
   packages = ['porE','porE/lib','porE/gui','porE/io','porE/hea'],
   install_requires=['ase'],
   zip_safe=False,
   ext_modules=[Extension(name='pore', sources=['porE/lib/porE.f90'], f2py_options=['--quiet'])]
)
