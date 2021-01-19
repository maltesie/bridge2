#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pyside2-uic $DIR/../ui/main_window.ui > $DIR/../main_window.py
pyside2-uic $DIR/../ui/new_analysis_dialog.ui > $DIR/../new_analysis_dialog.py
pyside2-uic $DIR/../ui/atom_names.ui > $DIR/../default_atoms_dialog.py
pyside2-uic $DIR/../ui/computations_results.ui > $DIR/../results_dialog.py
pyside2-rcc $DIR/../ui/icons.qrc > $DIR/../icons_rc.py

pyside2-uic $DIR/../ui/md_statistics.ui > $DIR/../ui/plugins/md_statistics.py
pyside2-uic $DIR/../ui/motif_detection.ui > $DIR/../ui/plugins/motif_detection.py
pyside2-uic $DIR/../ui/clusters.ui > $DIR/../ui/plugins/clusters.py
pyside2-uic $DIR/../ui/centrality.ui > $DIR/../ui/plugins/centrality.py

#this is a test
