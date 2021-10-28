# Bridge2

This program aims to provide an interactive tool to analyze haydrogen bonds and hydrophobic
interactions in crystal structures and Molecular Dynamics (MD) simulations. It is compatible 
with structures and trajectories that can be accessed with [MDAnalysis](https://userguide.mdanalysis.org/1.0.0/formats/index.html). The corresponding
publication with an examplatory application can be found [here](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.1c00306).


## Installation guide

This is a standalone version of Bridge2. It is written in Python3 and Qt5 and depends on Qt5
(5.14.1+) and the python packages MDAnalysis (0.19.2+) and PySide2 (5.14.1+). After installing 
the dependencies you can use the setup script to create a virtual environment with the 
necessary python packages in your bridge folder. IMPORTANT: Remember to deactivate any other
virtual environment or conda environment before the installation.


### 1 Install dependencies

#### 1.a Linux (Ubuntu/Debian)

> sudo apt-get install qt5-default build-essential python3-dev python3-venv

#### 1.b macOS

In order to install the required software for Bridge2 to work, we recommend using the 
Homebrew package manager. The later commands assume it is installed on your system. You can
install Homebrew by running the following command in a terminal:

> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

Then install the prerequisites:

> xcode-select --install

> brew install qt5 python


### 2 Setup and run Bridge2

Then run the setup script that comes with bridge:

> ./setup

This will create a python virtual environment containing all the necessary packages.
You can now run Bridge2 using the following command:

> ./bridge

### 3 Reinstall or update Bridge2

If you install a new version of Bridge2, delete your old installation folder, unpack the new archive, cd into the new bridge2 folder and follow the instructions under step 2.


## Usage

The usual analysis is split into 4 steps:

### Initializing the analysis

After clicking the "New Analysis" icon in the top left menu, the "New Analysis" dialog opens
and all parameters for the new analysis, such as the input files and the algorithm of interest,
can be set. Bridge2 then computes a portable set of information from the input files that can
be saved and opened without the necessity of having the trajectory or structure files. This step
is computationally costly and can take a long time for long trajectories. The progress is
indicated in the lower left corner. When done, an analysis summary can be saved under the
"File" menu. After the graph of interactions (H-bonds, water wires or hydrophobic interactions) 
becomes visible in the main window, the three tool tabs on the right can be used. They are 
titled "Layout", "Filters" and "Computations and Plots". 

### Setting the layout

The "Layout" tab allows for graphical settings such as colors or descriptions for nodes and
edges. Here, it is possible to visualize the degree centrality or the betweenness centrality
by coloring the nodes respectively.

### Applying filters

In the "Filters" tab several restrictions can be defined to filter for interactions of interest.
If a field requests a node name it is always possible to click into that field and then on the
node of interest. Here, shortest paths or connected components can be computed or the graph
can be reduced to hand-picked nodes of interest.

### Computations and Plots

This tab contains additional computational plugins that aim to produce plots on statistical
properties of interactions in MD simulations or to further visualize centrality measures.


## Copyright notice and disclaimer

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


Malte Siemers and Ana-Nicoleta Bondar. Interactive Interface for Graph-Based Analyses 
of Dynamic H-Bond Networks: Application to Spike Protein S, Journal of Chemical Information 
and Modeling 2021 61 (6), 2998-3014, DOI: 10.1021/acs.jcim.1c00306 


