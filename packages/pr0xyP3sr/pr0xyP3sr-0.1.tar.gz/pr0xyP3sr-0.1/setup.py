import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pr0xyP3sr",
    version="0.1",
    author="karthithehacker",
    author_email="contact@karthithehacker.com",
     description="Load any recon data into burp in just Single click",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/karthi-the-hacker/pr0xyP4rs3",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
