# PyDRS - Sirius Power Supplies communication.

![Linting and Static](https://github.com/lnls-sirius/pydrs/actions/workflows/lint.yml/badge.svg)
![Latest tag](https://img.shields.io/github/tag/lnls-sirius/pydrs.svg?style=flat)
[![Latest release](https://img.shields.io/github/release/lnls-sirius/pydrs.svg?style=flat)](https://github.com/lnls-sirius/pydrs/releases)
[![PyPI version fury.io](https://badge.fury.io/py/pydrs.svg)](https://pypi.python.org/pypi/pydrs/)
[![Read the Docs](https://readthedocs.org/projects/spack/badge/?version=latest)](https://lnls-sirius.github.io/pydrs/)

## What is PyDRS?

**PyDRS** is a Python package based on the Basic Small Messages Protocol (**BSMP**). It is used to communicate with and command Sirius Current Power Supplies and its peripherals ran by Digital Regulation System (**DRS**).

Development packages are listed at [requirements-dev.txt](requirements_dev.txt) and runtime dependencies at [requirements.txt](requirements.txt).
## Prerequisites

* [python==3.6](https://www.python.org/downloads/release/python-3612/)  
* pyserial==3.5  
* numpy  
* matplotlib*  

May require Microsoft C++ build tools  [**visualcppbuildtools**](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools).  

**Disclaimer:** Although pydrs is tested up to [**Python 3.10.0**](https://www.python.org/downloads/release/python-3100/) version you may check whether other apps you want to use with it may run Python 3.10 version.

## Conda

As an option, Conda can be used to create a specific environment where PyDRS library can be installed.
Conda can be installed with [**miniconda**](https://docs.conda.io/en/latest/miniconda.html#miniconda) or [**anaconda**](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

```command
conda create --name pydrs python=3.6
conda activate pydrs
```

## Dev Utility scripts

```sh
sh ./scripts/clean.sh
```
## Installation Guide

 **User level:**  
User-level version must be installed from the [**PyPI**](https://pypi.org/project/pydrs/) repository, using the 'pip install pydrs' command, which will install PyDRS onto the current Python path version.  
If you want to install it onto a specific Python version environment, please use Conda to create and activate such environment.  
Once that environment is active, you may proceed the installation with pip command.

```command
pip install pydrs
```
**Developer level:**  
Developer-level version can be installed locally, by cloning the project repository from [**GitHub**](https://github.com/lnls-sirius/pydrs) to a folder on your device via git command: 

```command
 git clone https://github.com/lnls-sirius/pydrs.git
``` 
You can run the pydrs app from **your_local_folder**\pydrs\src\pydrs\pydrs.py

![image](https://user-images.githubusercontent.com/19196344/138936564-32684536-d08d-4e21-ad99-84f8d9ca6e14.png)


## Usage

When all installation is done, python or ipython instance can be called.

![14](https://user-images.githubusercontent.com/19196344/138935751-d90dc9b9-1409-4dc4-98bd-66f480dcd489.png)


Import pydrs  

![image](https://user-images.githubusercontent.com/19196344/138935810-6664c76d-016d-4d63-a315-e42eb9a0c774.png)


Create *drs* object.  

![image](https://user-images.githubusercontent.com/19196344/138935856-a4d7c238-3327-4d4d-8d8e-05f5fc52c103.png)


Establish the connection.  

![image](https://user-images.githubusercontent.com/19196344/138935887-75f0a776-1863-47b6-addf-a1ef9446fb98.png)


Set the device address to communicate.  

![image](https://user-images.githubusercontent.com/19196344/138935909-ef2cbdce-b967-4791-9181-1c5642361f90.png)


Use BSMP commands to control the device.  

![image](https://user-images.githubusercontent.com/19196344/138935930-f6aee517-d734-4466-ae95-c7f5fb4761e3.png)


