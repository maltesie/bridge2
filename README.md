# Bridge2

This program aims to provide an interactive tool to analyze hydrogen bonds and hydrophobic
interactions in crystal structures and Molecular Dynamics (MD) simulations. It is compatible 
with structures and trajectories that can be accessed with [MDAnalysis](https://userguide.mdanalysis.org/1.0.0/formats/index.html). The corresponding
publication with an examplatory application can be found [here](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.1c00306).

## Installation guide

For Linux and Windows, there are pre-packed binary versions of the program [here](https://github.com/maltesie/bridge2/releases/). 
If you encounter problems with the binaries, you can also download the source code, install 
the dependencies and use the bridge2 script to start the program:

#### IMPORTANT: Deactivate any other virtual environment or conda environment before the installation and before running bridge.

### 1 Install dependencies

#### 1.a Linux

> sudo apt-get install libxcb-xinerama0 build-essential python3-dev python3-venv (Ubuntu/Debian)

> bash rhel8_dependencies (RHEL8)

> sudo dnf install python3-devel (Fedora)

#### 1.b macOS

In order to install the required software for Bridge2 to work, we recommend using the 
Homebrew package manager. The later commands assume it is installed on your system. You can
install Homebrew by running the following command in a terminal:

> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

Then install the prerequisites:

> xcode-select --install

> brew install qt5 python

#### 1.c Windows 10

Install Python3.10 from the Windows App Store.

### 2 Run bridge2

> ./bridge2 (Linux, macOS)

> bridge2.bat (Windows)

This will create a python virtual environment containing all the necessary packages and start 
Bridge2 then. If you have any problems with python packages bridge is depending on, please 
remove the python3env folder to reinstall the virtual environment the next time the bridge 
script is run.

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

#### batch computations

The initial computations can be performed in batches. To run the computations with identical 
parameters for multiple structures and trajectories, create two text files, one listing the
paths to the structure files (one per line), and one listing the corresponding trajectories
(all trajectory file paths per structure in one line, separated by a comma). In the file
dialogs, those text files can be selected and for every structure, a corresponding bridge
analysis file is created.

### Setting the layout

The "Layout" tab allows for graphical settings such as colors or descriptions for nodes and
edges. Here, it is possible to visualize the degree centrality or the betweenness centrality
by coloring the nodes respectively. It is generally possible to move nodes by dragging them
across the canvas to allow for custom positioning.

### Applying filters

In the "Filters" tab several restrictions can be defined to filter for interactions of interest.
If a field requests a node name it is always possible to click into that field and then on the
node of interest. Here, shortest paths or connected components can be computed or the graph
can be reduced to hand-picked nodes of interest.

### Computations and plots

This tab contains additional computational plugins that aim to produce plots on statistical
properties of interactions in MD simulations or to further visualize centrality measures.

### Portable save files

Bridge2 can save and reopen an analysis in a .baf file. Those files contain all initial 
computations results and are independent of the analyzed data files.

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


Malte Siemers, Michalis Lazaratos, Konstantina Karathanou, Federico Guerra, 
Leonid Brown, and Ana-Nicoleta Bondar. Bridge: A graph-based algorithm to 
analyze dynamic H-bond networks in membrane proteins, 
Journal of Chemical Theory and Computation 2019 15 (12) 6781-6798

and

Malte Siemers and Ana-Nicoleta Bondar. Interactive Interface for 
Graph-Based Analyses of Dynamic H-Bond Networks: Application to Spike Protein S, 
Journal of Chemical Information and Modeling 2021 61 (6), 2998-3014 


