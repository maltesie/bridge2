#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$DIR/../python3env/bin/pyside2-uic $DIR/../ui/main_window.ui > $DIR/../main_window.py
$DIR/../python3env/bin/pyside2-uic $DIR/../ui/new_analysis_dialog.ui > $DIR/../new_analysis_dialog.py
$DIR/../python3env/bin/pyside2-uic $DIR/../ui/atom_names.ui > $DIR/../default_atoms_dialog.py
$DIR/../python3env/bin/pyside2-uic $DIR/../ui/computations_results.ui > $DIR/../results_dialog.py
$DIR/../python3env/bin/pyside2-rcc $DIR/../ui/icons.qrc > $DIR/../icons_rc.py

$DIR/../python3env/bin/pyside2-uic $DIR/../ui/md_statistics.ui > $DIR/../ui/plugins/md_statistics.py
$DIR/../python3env/bin/pyside2-uic $DIR/../ui/motif_detection.ui > $DIR/../ui/plugins/motif_detection.py
$DIR/../python3env/bin/pyside2-uic $DIR/../ui/clusters.ui > $DIR/../ui/plugins/clusters.py
$DIR/../python3env/bin/pyside2-uic $DIR/../ui/centrality.ui > $DIR/../ui/plugins/centrality.py

#this is a test
