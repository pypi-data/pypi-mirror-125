# Macrophage Anlaysis Toolkit (MAT)

*This tool was documented in [our paper](http://doi.org/10.1016/j.mex.2019.11.028) on marcophage and fibrosis quantification*

*Hundlab Website: [hundlab.org](http://hundlab.org/)*

*PyPI: [pypi.org/project/hundlab-MAT](https://pypi.org/project/hundlab-MAT/)*

*Github: [github.com/hundlab/MAT](https://github.com/hundlab/MAT)*

## Setup

### Windows

1. Python 3 will need to be installed prior to setting up MAT, preferably any python
    greater than 3.7. Python 3 can be downloaded from the [python website](http://python.org).
    The x86-64 executable installer is reccommended, as the default install configuration 
    will set python to open .py files by double clicking. If it is installed correctly opening
    cmd or powershell window and typing `py --version` will print the installed python
    version.

2.  Install MAT by opening a cmd or powershell window and running 
    `py -m pip install hundlab-MAT`, this should install MAT and all of its dependancies. 

3.  Once MAT has been installed it can be run via cmd, powershell or the start menu. To run
     type `MacrophageAnalysisToolkit.py`. To create a desktop shortcut type
     `MacrophageAnalysisToolkit.py` into the start menu select `Copy full path`, then on the 
     Desktop `right-click` -> `new` -> `new shortcut` and paste the path when it askes for a
     path.

     If MAT does not run above as described this means that the python scipts directory has
     not been added to the windows path. To find the install location of python type 
     `py -0p` this will give the location of the python executable. In the same directory
     as python.exe is a Scripts directory and the `MacrophageAnalysisToolkit.py` will be in
     there. Once the MAT script has been found, a shortcut can be made to it directly and
     placed on the desktop.

*Note that it may take some time for MAT to start and it may be slow with larger images. 
On some machines the calibration widgets are especially slow*

### Mac/Linux

1. Python 3 will need to be installed prior to setting up MAT. Python 3 can be 
    installed via your package manager in linux. If it is installed correctly
    opening a terminal and typing `python --version` (in some distributions such as Ubuntu
    the command is python3) should print the python version. It may also be necessary
    to install Qt5. On unbuntu the package is `qt5-default`.

2. Install MAT using pip: `python -m pip install hundlab-MAT`

3. To run MAT use the command `MacrophageAnalysisToolkit.py`.

## Usage

TODO!! For now see the paper.

