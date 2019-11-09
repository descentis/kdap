import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='kdap',  
     version='0.1',
     author="Amit Kumar Verma",
     author_email="mt4descentis@gmail.com",
     description="KDAP is a package to analyze knowledge data",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://kdap.github.io/",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: 3-Clause BSD",
         "Operating System :: OS Independent",
     ],
 )