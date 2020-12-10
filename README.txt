## Copyright Notice and Disclaimer

This program is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this
program. If not, see https://www.gnu.org/licenses/.

Author: Malte Siemers, Freie Universität Berlin

If you use this software or anything it produces for work to be published, please cite:

Malte Siemers, Michalis Lazaratos, Konstantina Karathanou, Federico Guerra, Leonid
Brown, and Ana-Nicoleta Bondar. Bridge: A graph-based algorithm to analyze dynamic H-
bond networks in membrane proteins, Journal of Chemical Theory and Computation 2019,
15 (12) 6781-6798

and

Federico Guerra, Malte Siemers, Christopher Mielack, and Ana-Nicoleta Bondar Dynamics of
Long-Distance Hydrogen-Bond Networks in Photosystem II The Journal of Physical
Chemistry B 2018 122 (17), 4625-4641

## Installation Guide

This is a standalone version of Bridge. It is written in Python3 and Qt5 and depends on Qt5
(5.14.1+) and the python packages MDAnalysis (0.19.2+) and PySide2 (5.14.1+).


### Ubuntu Linux

To set up a virtual python environment with those packages installed, open up a terminal
and cd into the directory you want to have the environment installed in. Then install the
prerequisites:

> sudo apt-get install qt5-default build-essential python3-dev python3-venv

Then run (name_of_your_env will be the name of the folder of the virtual environment):

> python3 -m venv name_of_your_env

You can now activate your environment by typing

> source path_to_your_env/bin/activate

The environment has to be activated every time you open a new terminal. It is possible to
automatically activate the environment by editing your ~/.bashrc file. Just add the line
above at the end of it. After activating the environment (the name of the environment is
displayed in front of your terminals input line), install the required python packages:

> pip install wheel mdanalysis pyside2

Now unzip the archive containing bridge and cd into the extracted directory. Run bridge with
./bridge


### macOS

In order to install the required software for Bridge2 to work, we recommend using the 
Homebrew package manager. The later commands assume it is installed on your system. You can
install Homebrew by running the following command in a terminal:

> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

To set up a virtual python environment with the necessary packages installed, cd into the directory 
you want to have the environment installed in. Then install the prerequisites:

> xcode-select --install
> brew install qt5 python

Then run (name_of_your_env will be the name of the folder of the virtual environment):

> python3 -m venv name_of_your_env

You can now activate your environment by typing

> source path_to_your_env/bin/activate

The environment has to be activated every time you open a new terminal. It is possible to
automatically activate the environment by editing your ~/.bashrc file. Just add the line
above at the end of it. After activating the environment, install the required python
packages

> pip3 install wheel mdanalysis pyside2

Now unzip the archive containing bridge and cd into the extracted directory. Run bridge with

> ./bridge
