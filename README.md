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

Then run the setup script that comes with bridge:

> ./setup

This will create a python virtual environment containing all the necessary packages.
You can now run bridge using the following command:

> ./bridge

If you install a new version of Bridge, delete your old installation folder, unpack the new
archive and run ./setup once again to set the new version up. After that start Bridge with 
./bridge

### macOS

In order to install the required software for Bridge2 to work, we recommend using the 
Homebrew package manager. The later commands assume it is installed on your system. You can
install Homebrew by running the following command in a terminal:

> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

To set up a virtual python environment with the necessary packages installed, cd into the directory 
you want to have the environment installed in. Then install the prerequisites:

'''
xcode-select --install
brew install qt5 python
'''

Then run the setup script that comes with bridge:

> ./setup

This will create a python virtual environment containing all the necessary packages.
You can now run bridge using the following command:

> ./bridge

If you install a new version of Bridge, delete your old installation folder, unpack the new
archive and run ./setup once again to set the new version up. After that start Bridge with 
./bridge
