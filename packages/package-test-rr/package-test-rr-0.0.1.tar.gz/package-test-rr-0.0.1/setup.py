from setuptools import setup

with open("README.md", "r") as fh:
   long_description = fh.read()

setup (
   name='package-test-rr',
   version='0.0.1',
   description='say hello',
   py_modules=["qsamplehelloram"],
   package_dir={'':'src'},
   classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
   ],
   install_requires = [
        "blessings ~= 1.7",
   ], 
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/ramagopr/sara",
   author="Ramkumar Ramagopalan",
   author_email="kumar.gopalan@gmail.com",
)
