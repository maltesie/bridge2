# -*- coding: utf-8 -*-
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Author: Malte Siemers, Freie Universität Berlin 
#   
#    If you use this software or anything it produces for work to be published,
#    please cite:
#    
#    Malte Siemers, Michalis Lazaratos, Konstantina Karathanou, Federico Guerra, 
#    Leonid Brown, and Ana-Nicoleta Bondar. Bridge: A graph-based algorithm to 
#    analyze dynamic H-bond networks in membrane proteins, 
#    Journal of Chemical Theory and Computation 2019 15 (12) 6781-6798
#
#    and
#
#    Malte Siemers and Ana-Nicoleta Bondar. Interactive Interface for 
#    Graph-Based Analyses of Dynamic H-Bond Networks: Application to Spike Protein S, 
#    Journal of Chemical Information and Modeling 2021 61 (6), 2998-3014 

from datetime import datetime
import os, sys, importlib, pickle, shutil, traceback, webbrowser
from os.path import isfile as fc
from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow, QDialog, QButtonGroup
from PySide2.QtCore import Qt, QCoreApplication, QThreadPool
from main_window import Ui_MainWindow
from new_analysis_dialog import Ui_Dialog as Ui_NewAnalysisDialog
from default_atoms_dialog import Ui_Dialog as Ui_DefaultAtomsDialog
from results_dialog import Ui_Dialog as Ui_ResultsDialog
from multithreading import Worker
import numpy as np
from core import HbondAnalysis, WireAnalysis, HydrophobicAnalysis
from interactive import InteractiveMPLGraph as igraph, default_colors
from core.helpfunctions import (Error, Info, ranges_to_numbers, 
                                acceptor_names_global, donor_names_global,
                                water_definition)

all_filter = ['occupancy', 'shortest', 'connected', 'specific', 'between', 'selected_nodes']
filter_description = {'occupancy': 'Occupancy', 
                      'shortest': 'All Shortest Paths', 
                      'connected': 'Connected Component', 
                      'specific': 'Specific Path', 
                      'between': 'Between Sections', 
                      'selected_nodes': 'Selected Nodes',
                      'None': 'none'}

class DefaultAtomsDialog(QDialog, Ui_DefaultAtomsDialog):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.default_donors = None
        self.default_acceptors = None
        self.load_atom_names()
        self.connect_actions()
        
    def connect_actions(self):
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_reset.clicked.connect(self.reset)
        self.pushButton_cancel.clicked.connect(self.cancel)
        
    def load_atom_names(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ini_file = dir_path + '/settings.ini'
        if fc(ini_file):
            with open(ini_file, 'r') as f:
                donors = f.readline()
                acceptors = f.readline()
                water_def = f.readline().strip()
        else:
            donors = ', '.join(donor_names_global)
            acceptors = ', '.join(acceptor_names_global)
            water_def = water_definition
            self.plainTextEdit_donors.setPlainText(donors)
            self.plainTextEdit_acceptors.setPlainText(acceptors)
            self.lineEdit_water.setText(water_def)
            self.save()
        self.plainTextEdit_donors.clear()
        self.plainTextEdit_acceptors.clear()
        self.plainTextEdit_donors.setPlainText(donors)
        self.plainTextEdit_acceptors.setPlainText(acceptors)
        self.lineEdit_water.clear()
        self.lineEdit_water.setText(water_def)
        self.default_donors = {donor.strip() for donor in donors.split(',')}
        self.default_acceptors = {acceptor.strip() for acceptor in acceptors.split(',')}
        self.default_water = water_def

    def save(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ini_file = dir_path + '/settings.ini'
        donors = self.plainTextEdit_donors.toPlainText().strip().replace('\n', ' ')
        acceptors = self.plainTextEdit_acceptors.toPlainText().replace('\n', ' ')
        water_def = self.lineEdit_water.text()
        self.default_donors = {donor.strip() for donor in donors.split(',')}
        self.default_acceptors = {acceptor.strip() for acceptor in acceptors.split(',')}
        self.default_water = water_def
        with open(ini_file, 'w') as f:
            f.write(donors + '\n' + acceptors + '\n' + water_def)
        self.close()
            
    def cancel(self):
        self.close()
    
    def reset(self):
        donors = donor_names_global
        acceptors = acceptor_names_global
        water_def = water_definition
        self.plainTextEdit_donors.setPlainText(', '.join(sorted(list(donors))))
        self.plainTextEdit_acceptors.setPlainText(', '.join(sorted(list(acceptors))))
        self.lineEdit_water.setText(water_def)

class NewAnalysisDialog(QDialog, Ui_NewAnalysisDialog):
    
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.connect_actions()
        self.main_window = parent
        
    def connect_actions(self):
        self.button_structure.clicked.connect(self.browse_filename_structure)
        self.button_trajectories.clicked.connect(self.browse_filename_trajectories)
        self.button_cancel.clicked.connect(self.close)
        self.button_load.clicked.connect(self.init_new_analysis)
    
    def browse_filename_structure(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Structure File', filter='All Files (*.*);;Structure File (*.psf *.pdb);;Batch File List (*.txt)')[0]
        if filename:
            self.line_bonds_structure.setText(filename)
    
    def browse_filename_trajectories(self):
        filenames = QFileDialog.getOpenFileNames(self, 'Open Trajectory File(s)', filter='All Files (*.*);;DCD File (*.dcd);;Batch File List (*.txt)')[0]
        if filenames:
            fnames = ', '.join(filenames)
            self.line_bonds_trajectories.setText(fnames)
            
    def clear_all(self):
        #Files
        self.line_bonds_structure.setText('')
        self.line_bonds_trajectories.setText('')
        self.checkBox_bonds_donors_without_hydrogen.setChecked(False)
        #Search
        self.line_bonds_selection.setText('protein')
        self.checkBox_residuewise.setChecked(True)
        self.checkBox_all_oxygen.setChecked(False)
        self.checkBox_all_nitrogen.setChecked(False)
        self.checkBox_all_sulphur.setChecked(False)
        self.checkBox_consider_backbone.setChecked(False)
        #self.checkBox_disulphide_bridges.setChecked(False)
        #self.lineEdit_disulphide_distance.setText('2.05')
        self.line_bonds_start.setText('1')
        self.line_bonds_step.setText('1')
        self.line_bonds_stop.setText('-1')
        self.line_bonds_distance.setText('3.5')
        self.line_bonds_angle.setText('60')
        self.checkBox_angle.setChecked(True)
        #Algorithm
        self.radio_in_selection.setChecked(True)
        self.line_around_value.setText('3.5')
        self.checkBox_not_water_water.setChecked(True)
        self.line_wire_max_water.setText('5')
        self.checkBox_wires_allow_direct_bonds.setChecked(False)
        self.checkBo_wires_convex.setChecked(False)
        self.checkBox_partially_hydrophobic.setChecked(False)
        #Additional
        self.checkBox_frame_time.setChecked(False)
        self.comboBox_frame_time_unit.setCurrentIndex(1)
        self.lineEdit_frame_time.setText('')
        self.lineEdit_add_residue.setText('0')

    def init_new_analysis(self):
        structure = self.line_bonds_structure.text()
        trajectories = self.line_bonds_trajectories.text()
        selection = self.line_bonds_selection.text()
        start = self.line_bonds_start.text()
        step = self.line_bonds_step.text()
        stop = self.line_bonds_stop.text()
        distance = self.line_bonds_distance.text()
        angle = self.line_bonds_angle.text()
        around = self.line_around_value.text()
        hydrophobic_distance = self.lineEdit_hydrophobic_distance.text()
        partially_hydrophobic_residues = self.checkBox_partially_hydrophobic.isChecked()
        #ss_distance = self.lineEdit_disulphide_distance.text()
        max_water = self.line_wire_max_water.text()
        crytal_structure = self.checkBox_bonds_donors_without_hydrogen.isChecked()
        consider_backbone = self.checkBox_consider_backbone.isChecked()
        if crytal_structure: self.checkBox_angle.setChecked(False)
        residuewise = self.checkBox_residuewise.isChecked()
        add_all_donor_acceptor = []
        if self.checkBox_all_oxygen.isChecked(): add_all_donor_acceptor.append('O')
        if self.checkBox_all_nitrogen.isChecked(): add_all_donor_acceptor.append('N')
        if self.checkBox_all_sulphur.isChecked(): add_all_donor_acceptor.append('S')
        check_angle = self.checkBox_angle.isChecked()
        #compute_ss = self.checkBox_disulphide_bridges.isChecked()
        allow_direct_bonds = self.checkBox_wires_allow_direct_bonds.isChecked()
        ww_in_hull = self.checkBo_wires_convex.isChecked()
        not_water_water = self.checkBox_not_water_water.isChecked()
        
        if not fc(structure): 
            Error('File not found!', 'Could not find a structure file at the specified location.')
            return
        
        if trajectories != '':
            trajectories = [t.strip(' ') for t in trajectories.split(',')]
            if not all([fc(path) for path in trajectories]): 
                Error('File not found!', 'Could not find trajectory file(s) at the specified location.')
                return
        else:
            trajectories = None
            
        batch_mode = False
        if structure.endswith(".txt"):
            batch_mode = True
            with open(structure) as f:
                structure = [s.strip() for s in f.readlines()]
            if trajectories == None:
                trajectories = [None for i in range(len(structure))]
            elif len(trajectories)==1 and trajectories[0].endswith(".txt"):
                with open(trajectories[0]) as f:
                    trajectories = [[ss.strip() for ss in s.strip().split(',')] if len(s.strip())>0 else None for s in f.readlines()]
        else:
            structure = [structure]
            trajectories = [trajectories]
        
        add_donors = set(self.main_window.default_atoms_dialog.default_donors)
        add_acceptors = set(self.main_window.default_atoms_dialog.default_acceptors)
        water_def = self.main_window.default_atoms_dialog.default_water
        if consider_backbone:
            add_donors |= {'N'}
            add_acceptors |= {'O'}
        
        if selection == '': selection = 'protein'
        
        try:
            if step == '': step=1
            else: step = int(step)
            if (stop == '') or (stop=='-1'): stop=None
            else: stop = int(stop)
            if start == '': start=None
            else: start = int(start)-1
        except:
            Error('Datatype not understood!', 'Please use integers to define the frames used in the analysis.')
            return
        
        try:
            distance = float(distance)
            angle = float(angle)
        except:
            Error('Datatype not understood!', 'Please use floats to define the geometric criterion.')
            return
        
        search_args = {'around':None, 
                       'max_water':None, 
                       'allow_direct_bonds':None, 
                       'algorithm':None, 
                       'not_water_water':None, 
                       'ww_in_hull':None,
                       'hydrophobic_distance':None,
                       'partially_hydrophobic_residues':None,
                       'ss_distance':None,
                       #'compute_ss':compute_ss,
                       'consider_backbone':consider_backbone,
                       'frame_time':(None, None),
                       'add_residues':0}
        
        hb_selection = self.radio_in_selection.isChecked()
        hb_around = self.radio_around.isChecked()
        ww_dict = self.radio_wire_dict.isChecked()
        hydrophobic = self.radioButton_hydrophobic_contacts.isChecked()
        
        if hb_selection: search_args['algorithm'] = 'hb_selection'
        if hb_around: search_args['algorithm'] = 'hb_around'
        if ww_dict: search_args['algorithm'] = 'ww_dict'
        if hydrophobic: search_args['algorithm'] = 'hydrophobic'
        
        if hydrophobic: 
            try:
                search_args['hydrophobic_distance'] = float(hydrophobic_distance)
                search_args['partially_hydrophobic_residues'] = partially_hydrophobic_residues
            except:
                Error('Datatype not understood!', 'Please specify the hydrophobic distance as a float.')
                return
        
        if hb_around:
            try:
                search_args['around'] = float(around)
                search_args['not_water_water'] = not_water_water
            except:
                Error('Datatype not understood!', 'Please specify the radius parameter as a float.')
                return
            
        if ww_dict:
            try:
                search_args['max_water'] = int(max_water)
                search_args['allow_direct_bonds'] = allow_direct_bonds
                search_args['ww_in_hull'] = ww_in_hull
            except:
                Error('Datatype not understood!', 'Please specify the maximum number of waters as an integer.')
                return
        
        if self.checkBox_frame_time.isChecked():
            frame_time = self.lineEdit_frame_time.text()
            try:
                frame_time = float(frame_time)
                frame_time_unit = self.comboBox_frame_time_unit.currentText()
            except:
                Error('Datatype not understood!', 'Please specify the frame time as a floating point number.')
                return
            search_args['frame_time'] = (frame_time*step, frame_time_unit)
            
        try:
            add_residues = int(self.lineEdit_add_residue.text())
            search_args['add_residues'] = add_residues
        except:
            Error('Datatype not understood!', 'Please specify the beginning n-terminal residue as an integer.')
            return
        
        #if compute_ss:
        #    try:
        #        search_args['ss_distance'] = float(ss_distance)
        #    except:
        #        Error('Datatype not understood!', 'Please specify the sulphur-sulphur distance as a floating point number.')
        
        self.main_window._search_parameter = search_args 
        
        kwargs = {
            'batch_mode':batch_mode,
            'structure':structure,
            'trajectories':trajectories,
            'selection':selection,
            'check_angle':check_angle,
            'cut_angle':angle,
            'distance':distance,
            'start':start,
            'stop':stop,
            'step':step,
            'residuewise':residuewise,
            'additional_donors':add_donors, 
            'additional_acceptors':add_acceptors,
            'water_definition':water_def,
            'add_all_donor_acceptor':add_all_donor_acceptor,
            'add_donors_without_hydrogen':crytal_structure
            }
        
        self.main_window._analysis_parameter = kwargs
        if self.main_window.working:
            Error('Multi-Threading Error!', 'There is another computation running. If this keeps happening, please restart Bridge.')
            return
        worker = Worker(self.compute_initial_state, **kwargs) 
        worker.signals.finished.connect(self.main_window.init_interactive_graph)
        worker.signals.progress.connect(self.main_window.update_status_bar)
        worker.signals.error.connect(self.error_in_worker)
        self.main_window.statusbar.showMessage('Started initialization...')
        self.main_window.statusbar.repaint()
        self.main_window.working = True
        self.main_window.threadpool.start(worker)
        
        self.close()
    
    def error_in_worker(self, error_tuple):
        message = str(error_tuple[1]) +'\n'+ str(error_tuple[2])
        Error(message)
        self.main_window.statusbar.showMessage('Failed Initialization!')
        self.main_window.working = False
        self.show()
    
    def compute_initial_state(self, **kwargs):
        all_structure, all_trajectories = kwargs["structure"].copy(), kwargs["trajectories"].copy()
        batch_mode = kwargs["batch_mode"]
        del kwargs["batch_mode"]
        for i, (structure, trajectories) in enumerate(zip(all_structure, all_trajectories)):
            kwargs["structure"] = structure
            kwargs["trajectories"] = trajectories
            hb_selection = self.radio_in_selection.isChecked()
            hb_around = self.radio_around.isChecked()
            ww_dict = self.radio_wire_dict.isChecked()
            hydrophobic = self.radioButton_hydrophobic_contacts.isChecked()
            
            search_args = self.main_window._search_parameter
            
            if ww_dict: 
                self.main_window.analysis = WireAnalysis(**kwargs)
                self.main_window._analysis_type = 'ww'
            elif hydrophobic: 
                kwargs_hydrophobic = {'selection':kwargs['selection'], 'structure':kwargs['structure'], 
                          'trajectories':kwargs['trajectories'], 'distance':search_args['hydrophobic_distance'], 
                          'partially_hydrophobic_residues':search_args['partially_hydrophobic_residues'], 
                          'start':kwargs['start'], 'stop':kwargs['stop'], 'step':kwargs['step'], 
                          'residuewise':kwargs['residuewise'], 'progress_callback':kwargs['progress_callback']}
                self.main_window.analysis = HydrophobicAnalysis(**kwargs_hydrophobic)
                self.main_window._analysis_type = 'hy'
            elif (hb_selection | hb_around):
                self.main_window.analysis = HbondAnalysis(**kwargs)
                self.main_window._analysis_type = 'hb'
                
            do_not_use_water_algorithm = (self.main_window.analysis.nb_frames > 100) and not (hb_around and self.main_window._search_parameter['not_water_water'])
            include_water = hb_around
            if do_not_use_water_algorithm and include_water: 
                self.show()
                raise AssertionError('Algorithm not supported! Including water in the search consumes too much memory for your trajectory length (> 100) or the number of water molecules (>1000)!')
            
            if hb_selection: self.main_window.analysis.set_hbonds_in_selection()
            elif hb_around: self.main_window.analysis.set_hbonds_in_selection_and_water_around(around_radius=search_args['around'], not_water_water=search_args['not_water_water'])
            elif ww_dict: self.main_window.analysis.set_water_wires(max_water=search_args['max_water'], allow_direct_bonds=search_args['allow_direct_bonds'], water_in_convex_hull=search_args['ww_in_hull'])
            elif hydrophobic: self.main_window.analysis.set_hydrophobic_contacts_in_selection()
            

            self.main_window.analysis.add_missing_residues = int(self.lineEdit_add_residue.text())
            self.main_window.analysis.set_node_positions_3d(include_water=include_water)
            self.main_window.analysis.set_centralities()
            self.main_window._active_filters = {}
            self.main_window.current_filter = None
            self.main_window.apply_filters()
            
            if batch_mode:
                self.main_window._save_analysis(structure + ".batch{}.baf".format(i))
        
 
class ResultsDialog(QDialog, Ui_ResultsDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_actions()
        
    def connect_actions(self):
        self.pushButton_save.clicked.connect(self.save_to_file)
        self.pushButton_close.clicked.connect(self.close)
        
    def save_to_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Save ASCII', filter='ASCII text file (*.txt);;All Files (*.*)')[0]
        if not filename: return
        with open(filename, 'w') as af:
            af.write(self.textEdit_results.toPlainText())
        
    def show_results(self, result_string):
        self.textEdit_results.clear()
        self.textEdit_results.setText(result_string)
        self.show()

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.new_analysis_dialog = NewAnalysisDialog(self)
        self.working = False
        self.default_atoms_dialog = DefaultAtomsDialog()
        self.results_dialog = ResultsDialog()
        self.interactive_graph = None
        self.threadpool = QThreadPool()
        self.analysis = None
        self._analysis_type = None
        self.compare_analysis = None
        self._segname_colors = {}
        self._active_filters = {}
        self._current_filter = None
        self._analysis_parameter = None
        self._current_save_filename = None
        self._search_parameter = {}
        self._plugins = {}
        self._connect_actions()
        self._load_plugins()
        self.buttonGroup_coloring = QButtonGroup(self)
        self.buttonGroup_coloring.addButton(self.radioButton_color)
        self.buttonGroup_coloring.addButton(self.radioButton_colors)
        self.buttonGroup_coloring.addButton(self.radioButton_degree)
        self.buttonGroup_coloring.addButton(self.radioButton_betweenness)
        self.buttonGroup_rotation = QButtonGroup(self)
        self.buttonGroup_rotation.addButton(self.radioButton_rotation_zy)
        self.buttonGroup_rotation.addButton(self.radioButton_rotation_pca)
        self.buttonGroup_rotation.addButton(self.radioButton_rotation_xy)
        
    def _connect_actions(self):
        self.actionNew.triggered.connect(self.new_analysis)
        self.actionSave.triggered.connect(self.save_analysis)
        self.actionSaveAs.triggered.connect(self.save_as_analysis)
        self.actionOpen.triggered.connect(self.restore_analysis)
        self.actionQuit.triggered.connect(QCoreApplication.quit)
        self.actionEditParameter.triggered.connect(self.edit_analysis)
        self.actionDefaultAtomNames.triggered.connect(self.edit_default_atom_names)
        self.actionShowAtoms.triggered.connect(self.show_atoms)
        self.actionAddComputationPlugin.triggered.connect(self.add_computation_plugin)
        self.actionAbout.triggered.connect(self.goto_github)
        self.actionExport_Analysis_Summary.triggered.connect(self.export_analysis_summary)
        
        self._connect_between_comboboxes()
        self.line_bonds_filter_resida.returnPressed.connect(self.process_between_segments)
        self.line_bonds_filter_residb.returnPressed.connect(self.process_between_segments)
        self.checkBox_selected_nodes.clicked.connect(self.process_selection)
        
        self.groupBox_occupancy.clicked.connect(self.process_occupancy)
        self.line_bonds_occupancy.returnPressed.connect(self.process_occupancy)
        self.groupBox_connected.clicked.connect(self.process_connected_component)
        self.line_bonds_connected_root.returnPressed.connect(self.process_connected_component)
        self.groupBox_shortest_paths.clicked.connect(self.process_shortest_paths)
        self.line_bonds_path_root.returnPressed.connect(self.line_bonds_path_goal.setFocus)
        self.line_bonds_path_goal.returnPressed.connect(self.process_shortest_paths)
        self.groupBox_specific_path.clicked.connect(self.process_specific_path)
        self.lineEdit_specific_path.returnPressed.connect(self.process_specific_path)
        self.groupBox_between_segments.clicked.connect(self.process_between_segments)
        self.pushButton_apply_filter.clicked.connect(self.apply_current)
        self.pushButton_remove_filter.clicked.connect(self.remove_current)
        
        self.comboBox_segnames.activated.connect(self.switch_segname_color)
        self.comboBox_single_color.activated.connect(self.single_color_changed)
        self.comboBox_colors.activated.connect(self.color_per_segment_changed)
        
        self.horizontalSlider_frame.valueChanged.connect(self.update_frame)
        
    
    def _connect_between_comboboxes(self):
        self.comboBox_filter_segna.currentTextChanged.connect(self.process_between_segments)
        self.comboBox_filter_segnb.currentTextChanged.connect(self.process_between_segments)
        self.comboBox_filter_resna.currentTextChanged.connect(self.process_between_segments)
        self.comboBox_filter_resnb.currentTextChanged.connect(self.process_between_segments)
        
    def _disconnect_between_comboboxes(self):
        self.comboBox_filter_segna.currentTextChanged.disconnect(self.process_between_segments)
        self.comboBox_filter_segnb.currentTextChanged.disconnect(self.process_between_segments)
        self.comboBox_filter_resna.currentTextChanged.disconnect(self.process_between_segments)
        self.comboBox_filter_resnb.currentTextChanged.disconnect(self.process_between_segments)
    
    def _set_enabled(self):
        self.checkBox_nb_water.setEnabled(self._search_parameter['algorithm'] == 'ww_dict')

    def export_analysis_summary(self):
        yes_no = {True:'Yes', False:'No'}
        result_string = "Bridge2 analysis summary from " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n\n"
        if self._search_parameter['algorithm'] == 'hb_selection': algorithm_string = "H bonds in selection"
        elif self._search_parameter['algorithm'] == 'hb_around': algorithm_string = "H bonds in selection and water within {}A of the selection".format(self._search_parameter['around'])
        elif self._search_parameter['algorithm'] == 'ww_dict': algorithm_string = "Water wires in selection with maximum {} waters per wire.\nSearch confined to convex hull around selection: {}\nDirect H bonds allowed in search: {}".format(self._search_parameter['max_water'], yes_no[self._search_parameter['ww_in_hull']], yes_no[self._search_parameter['allow_direct_bonds']])
        elif self._search_parameter['algorithm'] == 'hydrophobic': algorithm_string = "Hydrophobic contacts in selection within a distance of {}A\nAdded partially hydrophobic residues: {}".format(self._search_parameter['hydrophobic_distance'], yes_no[self._search_parameter['partially_hydrophobic']])
        
        between_filter_string = ""
        if 'between' in self._active_filters:
            sega, segb, resa, resb, ida, idb = self._active_filters['between']
            all_strings = []
            if sega is not None: 
                if segb is not None: all_strings.append("Between segments {} and {}".format(sega, segb))
                else: all_strings.append("Within segment {}".format(sega))
            if resa is not None:
                if resb is not None: all_strings.append("Between residue types {} and {}".format(resa, resb))
                else: all_strings.append("Only pairs involving at least one {}".format(resa))
            if ida is not None:
                if idb is not None: all_strings.append("Between two groups fedined by ids {} and ids {}".format(str(ida), str(idb)))
                else: all_strings.append("Only pairs involving at least one residue with an id in {}".format(str(ida)))
            between_filter_string = "Between Regions:\n{}".format('\n'.join(all_strings))
        filter_dict = {}
        if self.groupBox_specific_path.isChecked() and ('specific' in self._active_filters): filter_dict['specific'] = "Specific Path: {}".format(' ,'.join(self._active_filters['specific']))
        if self.groupBox_shortest_paths.isChecked() and ('shortest' in self._active_filters): filter_dict['shortest'] = "Shortest Paths: Between node {} and node {}.".format(*self._active_filters['shortest'])
        if self.groupBox_between_segments.isChecked() and ('between' in self._active_filters): filter_dict['between'] = between_filter_string
        if self.groupBox_occupancy.isChecked() and ('occupancy' in self._active_filters): filter_dict['occupancy'] = "Occupancy: Set threshold of occupancy of {}%".format(self._active_filters['occupancy'])
        if self.checkBox_selected_nodes.isChecked() and ('selected_nodes' in self._active_filters): filter_dict['selected_nodes'] = "Selection: Graph was reduced by hand"
        if self.groupBox_connected.isChecked() and ('connected' in self._active_filters): filter_dict['connected'] = "Connected Component: Connected component that contains root node {}".format(self._active_filters['connected'])
        if len(self._active_filters) == 0: filter_string = 'No filters applied.'
        else: filter_string = '\n'.join([filter_dict[active_filter] for active_filter in self._active_filters])
        
        end_times = self.analysis.get_endurance_times()
        if self._analysis_type == 'ww':
            average_water = {key: res[res!=np.inf].mean() for key, res in self.analysis.wire_lengths.items()}
            sd_water = {key: res[res!=np.inf].std() for key, res in self.analysis.wire_lengths.items()}
            edges_string = "partner1:partner2\toccupancy\tendurance_time\tavg_nb_water\n\n"
            edges_string += "\n".join(['{}\t{:.1f}\t{}\t{:.1f}+-{:.1f}'.format(key, 
                                      res.mean()*100, 
                                      end_times[key],
                                      average_water[key],
                                      sd_water[key]) for key, res in self.analysis.filtered_results.items()])
        else:
            edges_string = "partner1:partner2\toccupancy\tendurance_time\n\n"
            edges_string += "\n".join(['{}\t{:.1f}\t{}'.format(key, 
                                      res.mean()*100, 
                                      end_times[key]) for key, res in self.analysis.filtered_results.items()])
    
        if self._analysis_parameter['check_angle']: angle_string = "{}".format(self._analysis_parameter['cut_angle'])
        else: angle_string = "No"
        donor_string = ", ".join(self.default_atoms_dialog.default_donors)
        acceptor_string = ", ".join(self.default_atoms_dialog.default_acceptors)
        #if self._search_parameter['ss_distance'] is not None: disulphide_string = "Yes, with a maximum Sulphur-Sulphur distance of {}A".format(self._search_parameter['ss_distance'])
        disulphide_string = "No disulphide bridges included in the search"
        if self._search_parameter['frame_time'] == (None,None): time_string = "No time specified"
        else: time_string = "{}{}".format(*self._search_parameter['frame_time'])
        stop = self._analysis_parameter['stop']
        if stop is None: stop = -1
        
        result_string +=   "--- ANALYSIS PARAMETER ---\n\n\
- Files -\n\n\
structure: {}\n\
trajectories: {}\n\
crystal structure: {}\n\n\
- Search -\n\n\
static selection: {}\n\
residuewise: {}\n\
included donor atom names: {}\n\
included acceptor atom names: {}\n\
included all oxygen: {}\n\
included all nitrogen: {}\n\
included all sulphur: {}\n\
backbone atoms: {}\n\
disulphide bridges: {}\n\
frames: from {} to {} with step {}, resulting in {} frames\n\
H bond distance: {}\n\
H bond angle: {}\n\n\
- Algorithm -\n\n\
{}\n\n\
- Additional Options -\n\n\
time between frames: {}\n\
starting n-terminal residue: {}\n\n\
--- FILTER ---\n\n\
{}\n\n\
--- RESULTS ---\n\n\
{}\n".format(self._analysis_parameter['structure'][-1],
                                            ', '.join([t if t is not None else ['no trajectory'] for t in self._analysis_parameter['trajectories']][-1]),
                                            yes_no[self._analysis_parameter['add_donors_without_hydrogen']],
                                            self._analysis_parameter['selection'],
                                            yes_no[self._analysis_parameter['residuewise']],
                                            donor_string,
                                            acceptor_string,
                                            yes_no['O' in self._analysis_parameter['add_all_donor_acceptor']],
                                            yes_no['N' in self._analysis_parameter['add_all_donor_acceptor']],
                                            yes_no['S' in self._analysis_parameter['add_all_donor_acceptor']],
                                            yes_no[self.new_analysis_dialog.checkBox_consider_backbone.isChecked()],
                                            disulphide_string,
                                            self._analysis_parameter['start'],
                                            stop,
                                            self._analysis_parameter['step'],
                                            self.analysis.nb_frames,
                                            self._analysis_parameter['distance'],
                                            angle_string,
                                            algorithm_string,
                                            time_string,
                                            self._search_parameter['add_residues'],
                                            filter_string,
                                            edges_string)
                            
        self.results_dialog.show_results(result_string)
    
    def update_frame(self):
        if self.interactive_graph is None: return
        nb_samples = min(100, self.analysis.nb_frames)
        self.label_frame.setText(str(np.linspace(1, self.analysis.nb_frames, nb_samples, dtype=int)[self.horizontalSlider_frame.value()]))
    
    def goto_github(self):
        webbrowser.open('https://github.com/maltesie/bridge')
    
    def add_computation_plugin(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = QFileDialog.getOpenFileName(self, 'Open Computation Plugin', filter='Python File (*.py)')[0]
        if filepath:
            filename = os.path.basename(filepath)
            try:
                shutil.copyfile(filepath, dir_path+'/plugins/'+filename)
            except:
                Error(traceback.format_exc())
        
        for plugin in self._plugins:
            widget = self._plugins[plugin].plugin_widget
            widget.setParent(None)
        self._plugins = {}
        self.comboBox_plugins.currentTextChanged.disconnect(self.activate_plugin)
        self.comboBox_plugins.clear()
        self._load_plugins()
        
    def show_atoms(self):
        if self.analysis is not None:
            donor_string = ', '.join(self._analysis_parameter['additional_donors'])
            acceptor_string = ', '.join(self._analysis_parameter['additional_acceptors'])
            message = 'Atom names used in this analysis:\n\n' + 'donors: ' + donor_string + '\n\nacceptors: ' + acceptor_string
            Info(message=message, title='Donor/Acceptor names')
    
    def edit_default_atom_names(self):
        self.default_atoms_dialog.load_atom_names()
        self.default_atoms_dialog.show()
    
    def _load_plugins(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        for file in sorted(os.listdir(dir_path+'/plugins')):
            if file.endswith(".py"):
                plugin_name = file[:-3]
                try:
                    plugin = importlib.import_module('plugins.'+plugin_name)
                    title = plugin.title
                    plugin.load(self)
                    self._plugins[title] = plugin
                    self.comboBox_plugins.addItem(title)
                except:
                    exctype, value = sys.exc_info()[:2]
                    print('Could not load a plugin from file {} in the plugin folder.'.format(file), value)
        self.activate_plugin()
        self.comboBox_plugins.currentTextChanged.connect(self.activate_plugin)
        self.toolBox.currentChanged.connect(self.tool_changed)
    
    def tool_changed(self):
        if self.toolBox.currentIndex() == 2:
            self.activate_plugin()
    
    def prepare_filters(self):    
        if 'between' in self._active_filters: self.groupBox_between_segments.setChecked(True)
        if 'specific' in self._active_filters: self.groupBox_specific_path.setChecked(True)
        if 'connected' in self._active_filters: self.groupBox_connected.setChecked(True)
        if 'shortest' in self._active_filters: self.groupBox_shortest_paths.setChecked(True)
        if 'occupancy' in self._active_filters: self.groupBox_occupancy.setChecked(True)
        if 'selected_nodes' in self._active_filters: self.groupBox_occupancy.setChecked(True)
        if len(self._active_filters) > 0:
            for key in self._active_filters.keys(): self._current_filter = key
        else:
            self._current_filter = None
        self.check_filters()
    
    def activate_plugin(self):
        current_plugin = self.comboBox_plugins.currentText()
        self._plugins[current_plugin].update(self)
        for plugin in self._plugins:
            widget = self._plugins[plugin].plugin_widget
            widget.setParent(None)
        self.verticalLayout_plugin.addWidget(self._plugins[current_plugin].plugin_widget)
    
    def set_analysis_parameter(self):
        if self._analysis_parameter is not None:
            structure = self._analysis_parameter['structure']
            trajectories = self._analysis_parameter['trajectories']
            if trajectories is None: trajectories = ['']
            selection = self._analysis_parameter['selection']
            start = self._analysis_parameter['start'] + 1
            step = self._analysis_parameter['step']
            stop = self._analysis_parameter['stop']
            if stop is None: stop = -1
            distance = self._analysis_parameter['distance']
            angle = self._analysis_parameter['cut_angle']
            crystal_structure = self._analysis_parameter['add_donors_without_hydrogen']
            add_all_donor_acceptor = self._analysis_parameter['add_all_donor_acceptor']
            check_angle = self._analysis_parameter['check_angle']
            residuewise = self._analysis_parameter['residuewise']

            hydrophobic_distance = self._search_parameter['hydrophobic_distance']
            if hydrophobic_distance is None: hydrophobic_distance = '5.0'
            ss_distance = self._search_parameter['ss_distance']
            if ss_distance is None: ss_distance = '2.05'
            #compute_ss = self._search_parameter['compute_ss']
            #if compute_ss is None: compute_ss = False
            ww_in_hull = self._search_parameter['ww_in_hull']
            if ww_in_hull is None: ww_in_hull = False
            partially_hydrophobic_residues = self._search_parameter['partially_hydrophobic_residues']
            if partially_hydrophobic_residues is None: partially_hydrophobic_residues = False
            allow_direct_bonds = self._search_parameter['allow_direct_bonds']
            if allow_direct_bonds is None: allow_direct_bonds = False
            around = self._search_parameter['around']
            if around is None: around = '3.5'
            max_water = self._search_parameter['max_water']
            if max_water is None: max_water = '5'
            not_water_water = self._search_parameter['not_water_water']
            if not_water_water is None: not_water_water = False
            consider_backbone = self._search_parameter['consider_backbone']
            add_residues = self._search_parameter['add_residues']
            
            frame_time, frame_time_unit = self._search_parameter['frame_time']
            if frame_time is not None:
                self.new_analysis_dialog.lineEdit_frame_time.setText(str(frame_time))
                self.new_analysis_dialog.comboBox_frame_time_unit.setCurrentText(frame_time_unit)
                self.new_analysis_dialog.checkBox_frame_time.setChecked(True)
            
            self.new_analysis_dialog.lineEdit_add_residue.setText(str(add_residues))
            self.new_analysis_dialog.line_bonds_structure.setText(structure[-1])
            self.new_analysis_dialog.line_bonds_trajectories.setText(', '.join(trajectories[-1]))
            self.new_analysis_dialog.line_bonds_selection.setText(selection)
            self.new_analysis_dialog.line_bonds_start.setText(str(start))
            self.new_analysis_dialog.line_bonds_step.setText(str(step))
            self.new_analysis_dialog.line_bonds_stop.setText(str(stop))
            self.new_analysis_dialog.line_bonds_distance.setText(str(distance))
            self.new_analysis_dialog.line_bonds_angle.setText(str(angle))
            self.new_analysis_dialog.line_around_value.setText(str(around))
            self.new_analysis_dialog.line_wire_max_water.setText(str(max_water))
            #self.new_analysis_dialog.lineEdit_disulphide_distance.setText(str(ss_distance))
            self.new_analysis_dialog.lineEdit_hydrophobic_distance.setText(str(hydrophobic_distance))
            
            if not crystal_structure: self.new_analysis_dialog.checkBox_angle.setChecked(check_angle)
            self.new_analysis_dialog.checkBox_residuewise.setChecked(residuewise)
            self.new_analysis_dialog.checkBox_partially_hydrophobic.setChecked(partially_hydrophobic_residues)
            self.new_analysis_dialog.checkBo_wires_convex.setChecked(ww_in_hull)
            #self.new_analysis_dialog.checkBox_disulphide_bridges.setChecked(compute_ss)
            self.new_analysis_dialog.checkBox_bonds_donors_without_hydrogen.setChecked(crystal_structure)
            self.new_analysis_dialog.checkBox_all_oxygen.setChecked('O' in add_all_donor_acceptor)
            self.new_analysis_dialog.checkBox_all_nitrogen.setChecked('N' in add_all_donor_acceptor)
            self.new_analysis_dialog.checkBox_all_sulphur.setChecked('S' in add_all_donor_acceptor)
            self.new_analysis_dialog.checkBox_wires_allow_direct_bonds.setChecked(allow_direct_bonds)
            self.new_analysis_dialog.checkBox_not_water_water.setChecked(not_water_water)
            self.new_analysis_dialog.checkBox_consider_backbone.setChecked(consider_backbone)
            
            hb_selection = self._search_parameter['algorithm'] == 'hb_selection'
            hb_around =  self._search_parameter['algorithm'] =='hb_around'
            ww_dict = self._search_parameter['algorithm'] == 'ww_dict'
            hydrophobic = self._search_parameter['algorithm'] == 'hydrophobic'
            
            if hb_selection: self.new_analysis_dialog.radio_in_selection.setChecked(True)
            if hb_around: self.new_analysis_dialog.radio_around.setChecked(True)
            if ww_dict: self.new_analysis_dialog.radio_wire_dict.setChecked(True)
            if hydrophobic: self.new_analysis_dialog.radioButton_hydrophobic_contacts.setChecked(True)
    
    def edit_analysis(self):
        self.set_analysis_parameter()
        self.new_analysis_dialog.setWindowTitle('Edit Analysis')
        self.new_analysis_dialog.button_load.setText('Rerun')
        self.new_analysis_dialog.show()
        
    def new_analysis(self):
        self.new_analysis_dialog.setWindowTitle('New Analysis')
        self.new_analysis_dialog.button_load.setText('Load')
        self.deactivate_all_filters()
        self.new_analysis_dialog.clear_all()
        self.new_analysis_dialog.show()
        
    def update_status_bar(self, message):
        self.statusbar.showMessage(message)
        self.statusbar.repaint()
    
    def init_interactive_graph(self):
        self.statusbar.showMessage('Done!')
        self.statusbar.repaint()
        self.working = False
        if self.interactive_graph is not None:
            self.buttonGroup_coloring.buttonClicked.disconnect(self.interactive_graph.set_colors)
            self.checkBox_centralities_norm.clicked.disconnect(self.interactive_graph.set_colors)
            self.checkBox_white.clicked.disconnect(self.interactive_graph.set_colors)
            self.horizontalSlider_nodes.sliderReleased.disconnect(self.interactive_graph.set_nodesize)
            self.horizontalSlider_edges.sliderReleased.disconnect(self.interactive_graph.set_edgesize)
            self.horizontalSlider_labels.sliderReleased.disconnect(self.interactive_graph.set_labelsize)
            self.checkBox_segnames_legend.clicked.disconnect(self.interactive_graph.set_colors)
            self.checkBox_bonds_graph_labels.clicked.disconnect(self.interactive_graph.set_node_labels)
            self.checkBox_color_legend.clicked.disconnect(self.interactive_graph.set_colors)
            self.checkBox_bonds_occupancy.clicked.disconnect(self.edge_labels_occupancy)
            self.checkBox_bonds_endurance.clicked.disconnect(self.edge_labels_endurance)
            self.checkBox_nb_water.clicked.disconnect(self.edge_labels_nb_waters)
            self.buttonGroup_rotation.buttonClicked.disconnect(self.interactive_graph.set_node_positions)
            self.horizontalSlider_frame.valueChanged.disconnect(self.interactive_graph.set_node_positions)
            
            self.interactive_graph.canvas.setParent(None)
            del self.interactive_graph.canvas
            self.interactive_graph.remove_toolbar()
            self.comboBox_segnames.clear() 
        self.interactive_graph = igraph(self)
        
        self.buttonGroup_coloring.buttonClicked.connect(self.interactive_graph.set_colors)
        self.checkBox_centralities_norm.clicked.connect(self.interactive_graph.set_colors)
        self.checkBox_white.clicked.connect(self.interactive_graph.set_colors)
        self.horizontalSlider_nodes.sliderReleased.connect(self.interactive_graph.set_nodesize)
        self.horizontalSlider_edges.sliderReleased.connect(self.interactive_graph.set_edgesize)
        self.horizontalSlider_labels.sliderReleased.connect(self.interactive_graph.set_labelsize)
        self.checkBox_segnames_legend.clicked.connect(self.interactive_graph.set_colors)
        self.checkBox_bonds_graph_labels.clicked.connect(self.interactive_graph.set_node_labels)
        self.checkBox_color_legend.clicked.connect(self.interactive_graph.set_colors)
        self.checkBox_bonds_occupancy.clicked.connect(self.edge_labels_occupancy)
        self.checkBox_bonds_endurance.clicked.connect(self.edge_labels_endurance)
        self.checkBox_nb_water.clicked.connect(self.edge_labels_nb_waters)
        self.buttonGroup_rotation.buttonClicked.connect(self.interactive_graph.set_node_positions)
        self.horizontalSlider_frame.valueChanged.connect(self.interactive_graph.set_node_positions)
        
        self.layout_interactive.addWidget(self.interactive_graph.canvas)
        self.interactive_graph.add_toolbar()
        
        self.horizontalSlider_frame.setMaximum(min(99, self.analysis.nb_frames-1))
        self.horizontalSlider_frame.setMinimum(0)
        
        segnames, resnames = self.analysis.get_segnames_and_resnames()
        self.comboBox_segnames.addItems(sorted(segnames))
        self._segname_colors = {}
        for i in range(self.comboBox_segnames.count()):
            segname = self.comboBox_segnames.itemText(i)
            if segname not in self._segname_colors: self._segname_colors[self.comboBox_segnames.itemText(i)] = default_colors[i]
        
        try: 
            self.comboBox_colors.setCurrentText(self._segname_colors[self.comboBox_segnames.currentText()])
        except:
            if len(self.analysis.initial_results) == 0: Error("Empty results!")

        self.radioButton_colors.setChecked(True)
        self.checkBox_bonds_occupancy.setChecked(False)
        self.checkBox_bonds_graph_labels.setChecked(True)
        self.checkBox_color_legend.setChecked(True)
        
        self.comboBox_filter_segna.clear()
        self.comboBox_filter_segnb.clear()
        self.comboBox_filter_resna.clear()
        self.comboBox_filter_resnb.clear()
        self.comboBox_filter_segna.addItems(['all']+sorted(segnames))
        self.comboBox_filter_segnb.addItems(['all']+sorted(segnames))
        self.comboBox_filter_resna.addItems(['all']+sorted(resnames))
        self.comboBox_filter_resnb.addItems(['all']+sorted(resnames))
        
        self.activate_plugin()
        self.interactive_graph.set_colors()
        self._set_enabled()
        self.repaint()
        
        
    
    def edge_labels_occupancy(self):
        self.checkBox_bonds_endurance.setChecked(False)
        self.checkBox_nb_water.setChecked(False)
        self.interactive_graph.set_edge_labels()
        
    def edge_labels_endurance(self):
        self.checkBox_bonds_occupancy.setChecked(False)
        self.checkBox_nb_water.setChecked(False)
        self.interactive_graph.set_edge_labels()
        
    def edge_labels_nb_waters(self):
        self.checkBox_bonds_occupancy.setChecked(False)
        self.checkBox_bonds_endurance.setChecked(False)
        self.interactive_graph.set_edge_labels()
    
    def error_in_worker(self, error_tuple):
        message = str(error_tuple[1])
        Error(message)
        self.statusbar.showMessage('Failed Centrality Computations!')
    
    def enable_centrality_coloring(self):
        self.statusbar.showMessage('Done!')
        self.statusbar.repaint()
    
    def deactivate_all_filters(self):
        self.line_bonds_occupancy.setText('')
        self.groupBox_occupancy.setChecked(False)
        self.line_bonds_path_root.setText('')
        self.line_bonds_path_goal.setText('')
        self.groupBox_shortest_paths.setChecked(False)
        self.line_bonds_connected_root.setText('')
        self.groupBox_connected.setChecked(False)
        self.lineEdit_specific_path.setText('')
        self.groupBox_specific_path.setChecked(False)
        self.line_bonds_filter_resida.setText('')
        self.line_bonds_filter_residb.setText('')
        self._disconnect_between_comboboxes()
        self.comboBox_filter_resnb.setCurrentIndex(0)
        self.comboBox_filter_resna.setCurrentIndex(0)
        self.comboBox_filter_segnb.setCurrentIndex(0)
        self._connect_between_comboboxes()
        self.comboBox_filter_segna.setCurrentIndex(0)
        self.groupBox_between_segments.setChecked(False)
        for f in list(self._active_filters.keys()): del self._active_filters[f]
        
    def close_open_filters(self):
        if self.groupBox_occupancy.isChecked() and (self._current_filter != 'occupancy') and ('occupancy' not in self._active_filters): 
            self.groupBox_occupancy.setChecked(False)
        elif not self.groupBox_occupancy.isChecked() and ('occupancy' not in self._active_filters):
            self.line_bonds_occupancy.setText('')
        elif self.groupBox_occupancy.isChecked() and (self._current_filter != 'occupancy') and ('occupancy' in self._active_filters):
            self.groupBox_occupancy.setEnabled(False)
        elif self.groupBox_occupancy.isChecked() and (self._current_filter == 'occupancy') and ('occupancy' in self._active_filters):
            self.groupBox_occupancy.setEnabled(True)
        
        if self.groupBox_shortest_paths.isChecked() and (self._current_filter != 'shortest') and ('shortest' not in self._active_filters): 
            self.line_bonds_path_root.setText('')
            self.line_bonds_path_goal.setText('')
            self.groupBox_shortest_paths.setChecked(False)
        elif not self.groupBox_shortest_paths.isChecked() and ('shortest' not in self._active_filters):
            self.line_bonds_path_root.setText('')
            self.line_bonds_path_goal.setText('')
        elif self.groupBox_shortest_paths.isChecked() and (self._current_filter != 'shortest') and ('shortest' in self._active_filters):
            self.groupBox_shortest_paths.setEnabled(False)
        elif self.groupBox_shortest_paths.isChecked() and (self._current_filter == 'shortest') and ('shortest' in self._active_filters):
            self.groupBox_shortest_paths.setEnabled(True)
        
        if self.groupBox_connected.isChecked() and (self._current_filter != 'connected') and ('connected' not in self._active_filters): 
            self.line_bonds_connected_root.setText('')
            self.groupBox_connected.setChecked(False)
        elif not self.groupBox_connected.isChecked() and ('connected' not in self._active_filters):
            self.line_bonds_connected_root.setText('')
        elif self.groupBox_connected.isChecked() and (self._current_filter != 'connected') and ('connected' in self._active_filters):
            self.groupBox_connected.setEnabled(False)
        elif self.groupBox_connected.isChecked() and (self._current_filter == 'connected') and ('connected' in self._active_filters):
            self.groupBox_connected.setEnabled(True)
        
        if self.groupBox_specific_path.isChecked() and (self._current_filter != 'specific') and ('specific' not in self._active_filters): 
            self.lineEdit_specific_path.setText('')
            self.groupBox_specific_path.setChecked(False)
        elif not self.groupBox_specific_path.isChecked() and ('specific' not in self._active_filters): 
            self.lineEdit_specific_path.setText('')
        elif self.groupBox_specific_path.isChecked() and (self._current_filter != 'specific') and ('specific' in self._active_filters):
            self.groupBox_specific_path.setEnabled(False)
        elif self.groupBox_specific_path.isChecked() and (self._current_filter == 'specific') and ('specific' in self._active_filters):
            self.groupBox_specific_path.setEnabled(True)
        
        if self.groupBox_between_segments.isChecked() and (self._current_filter != 'between') and ('between' not in self._active_filters): 
            self.line_bonds_filter_resida.setText('')
            self.line_bonds_filter_residb.setText('')
            self._disconnect_between_comboboxes()
            self.comboBox_filter_resnb.setCurrentIndex(0)
            self.comboBox_filter_resna.setCurrentIndex(0)
            self.comboBox_filter_segnb.setCurrentIndex(0)
            self.comboBox_filter_segna.setCurrentIndex(0)
            self._connect_between_comboboxes()
            self.groupBox_between_segments.setChecked(False)
        elif ('between' not in self._active_filters): 
            self.line_bonds_filter_resida.setText('')
            self.line_bonds_filter_residb.setText('')
            self._disconnect_between_comboboxes()
            self.comboBox_filter_resnb.setCurrentIndex(0)
            self.comboBox_filter_resna.setCurrentIndex(0)
            self.comboBox_filter_segnb.setCurrentIndex(0)
            self.comboBox_filter_segna.setCurrentIndex(0)
            self._connect_between_comboboxes()
        elif self.groupBox_between_segments.isChecked() and (self._current_filter != 'between') and ('between' in self._active_filters):
            self.groupBox_between_segments.setEnabled(False)
        elif self.groupBox_between_segments.isChecked() and (self._current_filter == 'between') and ('between' in self._active_filters):
            self.groupBox_between_segments.setEnabled(True)
        
        if self.checkBox_selected_nodes.isChecked() and (self._current_filter != 'selected_nodes') and ('selected_nodes' not in self._active_filters): 
            self.checkBox_selected_nodes.setChecked(False)
        elif self.checkBox_selected_nodes.isChecked() and (self._current_filter != 'selected_nodes') and ('selected_nodes' in self._active_filters):
            self.checkBox_selected_nodes.setEnabled(False)
        elif self.checkBox_selected_nodes.isChecked() and (self._current_filter == 'selected_nodes') and ('selected_nodes' in self._active_filters):
            self.checkBox_selected_nodes.setEnabled(True)
        
    def check_filters(self):
        if 'occupancy' in self._active_filters:
            self.line_bonds_occupancy.setText(str(self._active_filters['occupancy']))
        if 'shortest' in self._active_filters:
            self.line_bonds_path_root.setText(str(self._active_filters['shortest'][0]))
            self.line_bonds_path_goal.setText(str(self._active_filters['shortest'][1]))
        if 'connected' in self._active_filters:
            self.line_bonds_connected_root.setText(str(self._active_filters['connected']))
        if 'specific' in self._active_filters:
            self.lineEdit_specific_path.setText(', '.join(self._active_filters['specific']))
        if 'between' in self._active_filters:
            self.comboBox_filter_segna.setCurrentText(str(self._active_filters['between'][0]))
            self.comboBox_filter_segnb.setCurrentText(str(self._active_filters['between'][1]))
            self.comboBox_filter_resna.setCurrentText(str(self._active_filters['between'][2]))
            self.comboBox_filter_resnb.setCurrentText(str(self._active_filters['between'][3]))
            resida, residb = self._active_filters['between'][4:6]
            if resida is None: resida = ''
            if residb is None: residb = ''
            self.line_bonds_filter_resida.setText(str(resida))
            self.line_bonds_filter_residb.setText(str(residb))
        if 'selected_nodes' in self._active_filters:
            self.checkBox_selected_nodes.setChecked(True)
        
        self.close_open_filters()
        if self.interactive_graph is not None: self.interactive_graph.reset_selected_nodes()
        self.label_current_filter.setText('current filter: ' + filter_description[str(self._current_filter)])
        if self.analysis is not None:
            self.apply_filters()
    
    def enable_current(self):
        if self._current_filter == 'occupancy': self.groupBox_occupancy.setEnabled(True)
        elif self._current_filter == 'shortest': self.groupBox_shortest_paths.setEnabled(True)
        elif self._current_filter == 'connected': self.groupBox_connected.setEnabled(True)
        elif self._current_filter == 'specific': self.groupBox_specific_path.setEnabled(True)
        elif self._current_filter == 'between': self.groupBox_between_segments.setEnabled(True)
        elif self._current_filter == 'selected_nodes': self.checkBox_selected_nodes.setEnabled(True)
    
    def apply_current(self):
        if self._current_filter is None:
            Error('Cannot apply!','No filter selected.')
            return
        if self._current_filter == 'occupancy':
            self.process_occupancy()
        elif self._current_filter == 'shortest':
            self.process_shortest_paths()
        elif self._current_filter == 'specific':
            self.process_specific_path()
        elif self._current_filter == 'connected':
            self.process_connected_component()
        elif self._current_filter == 'between':
            self.process_between_segments()
        elif self._current_filter == 'selected_nodes':
            self.process_selection()
    
    def remove_current(self):
        if len(self._active_filters) > 0:
            try:
                del self._active_filters[self._current_filter]
            except:
                Error('Cannot Remove!', 'The currently selected filter was not applied yet.')
                return
            if len(self._active_filters) > 0:
                for key in self._active_filters.keys(): self._current_filter = key
                #print('after check', self._active_filters, self._current_filter)
            else:
                self._current_filter = None
                self.deactivate_all_filters()
        self.check_filters()
        
    
    def process_occupancy(self):
        if self.groupBox_occupancy.isChecked(): 
            occupancy = self.line_bonds_occupancy.text()
            if occupancy != '':
                try: 
                    occupancy = float(occupancy)
                except: 
                    Error('Type Error!', "Could not convert '{}' into a floating point number.".format(self.line_bonds_occupancy.text()))
                    if ('occupancy' in self._active_filters): del self._active_filters['occupancy']
                    return
                if not (0.0<=occupancy<=100.0):
                    Error('Value Error!', "The occupancy has to be a floating point number in [0.0, 100.0].")
                    if ('occupancy' in self._active_filters): del self._active_filters['occupancy']
                    return
                self._active_filters['occupancy'] = occupancy
            elif ('occupancy' in self._active_filters):
                del self._active_filters['occupancy']
        
            self._current_filter = 'occupancy'
            self.line_bonds_occupancy.setFocus()
        else: 
            self._current_filter = None
            if len(self._active_filters) > 0: 
                for key in self._active_filters.keys(): self._current_filter = key
            
        self.check_filters()
        
    
    def process_shortest_paths(self):
        if self.groupBox_shortest_paths.isChecked(): 
            root = self.line_bonds_path_root.text()
            goal = self.line_bonds_path_goal.text()
            if root != '':
                if root not in self.interactive_graph._node:
                    Error('Node not found!', 'The specified root node was not found in the initial graph!')
                    if ('shortest' in self._active_filters): del self._active_filters['shortest']
                    return
                if root not in self.interactive_graph.get_active_nodes():
                    Error('Node not found!', 'The specified root node was not found in the currently displayed graph!')
                    if ('shortest' in self._active_filters): del self._active_filters['shortest']
                    return
            if goal != '':
                if goal not in self.interactive_graph._node:
                    Error('Node not found!', 'The specified target node was not found in the initial graph!')
                    if ('shortest' in self._active_filters): del self._active_filters['shortest']
                    return
                if goal not in self.interactive_graph.get_active_nodes():
                    Error('Node not found!', 'The specified goal node was not found in the currently displayed graph!')
                    if ('shortest' in self._active_filters): del self._active_filters['shortest']
                    return
            if ((root != '') and (goal == '')) or ((root == '') and (goal != '')):
                Error('Node not specified!','Please specify a root and a target node.')
                if ('shortest' in self._active_filters): del self._active_filters['shortest']
                return
            if not ((root == '') and (goal == '')):
                self._active_filters['shortest'] = (root, goal)
            elif ('shortest' in self._active_filters):
                del self._active_filters['shortest']
            else:
                self.interactive_graph.reset_selected_nodes()
        
            self._current_filter = 'shortest'
            if self.focusWidget() is not self.line_bonds_path_goal: self.line_bonds_path_root.setFocus()
        else: 
            self._current_filter = None
            if len(self._active_filters) > 0: 
                for key in self._active_filters.keys(): self._current_filter = key
        self.check_filters()
        
    
    def process_connected_component(self):
        root = self.line_bonds_connected_root.text()
        if self.groupBox_connected.isChecked(): 
            if root != '':
                if root not in self.interactive_graph._node:
                    Error('Node not found!', 'The specified root node was not found in the initial graph!')
                    if ('connected' in self._active_filters): del self._active_filters['connected']
                    return
                if root not in self.interactive_graph.get_active_nodes():
                    Error('Node not found!', 'The specified root node was not found in the currently displayed graph!')
                    if ('connected' in self._active_filters): del self._active_filters['connected']
                    return
                self._active_filters['connected'] = root
            elif ('connected' in self._active_filters): 
                del self._active_filters['connected']
            else:
                self.interactive_graph.reset_selected_nodes()
            
            self._current_filter = 'connected'
            self.line_bonds_connected_root.setFocus()
        else:
            self._current_filter = None
            if len(self._active_filters) > 0: 
                for key in self._active_filters.keys(): self._current_filter = key
        self.check_filters()
        
        
    def process_specific_path(self):
        if self.groupBox_specific_path.isChecked(): 
            nodes = [node.strip(' ') for node in self.lineEdit_specific_path.text().split(',')]
            for node in nodes:
                if node != '':
                    if node not in self.interactive_graph._node:
                        Error('Node not found!', "The specified node '{}' was not found in the initial graph!".format(node))
                        if ('specific' in self._active_filters): del self._active_filters['specific']
                        return
                    if node not in self.interactive_graph.get_active_nodes():
                        Error('Node not found!', "The specified node '{}' was not found in the currently displayed graph!".format(node))
                        if ('specific' in self._active_filters): del self._active_filters['specific']
                        return
            if all([node != '' for node in nodes]):
                self._active_filters['specific'] = nodes
            
            if ('specific' in self._active_filters) and (nodes == ['']): 
                del self._active_filters['specific']
            elif nodes == ['']:
                self.interactive_graph.reset_selected_nodes()
        
            self._current_filter = 'specific'
            self.lineEdit_specific_path.setFocus()
        else:
            self._current_filter = None
            if len(self._active_filters) > 0: 
                for key in self._active_filters.keys(): self._current_filter = key
        self.check_filters()
        
        
    def process_between_segments(self):
        if self.groupBox_between_segments.isChecked(): 
            sega = self.comboBox_filter_segna.currentText()
            if sega == 'all': sega = None
            segb = self.comboBox_filter_segnb.currentText()
            if segb == 'all': segb = None
            
            resa = self.comboBox_filter_resna.currentText()
            if resa == 'all': resa = None
            resb = self.comboBox_filter_resnb.currentText()
            if resb == 'all': resb = None
            
            ida = self.line_bonds_filter_resida.text()
            if ida == '': ida = None
            idb = self.line_bonds_filter_residb.text()
            if idb == '': idb = None
                
            numbers_a = None
            numbers_b = None
            if ida is not None:
                numbers_a = ranges_to_numbers(ida)
                if numbers_a == []: 
                    Error('Format Error!', 'Could not understand the input for residue ids of segment 1. Please define ranges like 10-20 and single numbers and separate them with commas.')
                    if ('between' in self._active_filters): del self._active_filters['between']
                    return
            if idb is not None:
                numbers_b = ranges_to_numbers(idb)
                if numbers_b == []: 
                    Error('Format Error!', 'Could not understand the input for residue ids of segment 2. Please define ranges like 10-20 and single numbers and separate them with commas.')
                    if ('between' in self._active_filters): del self._active_filters['between']
                    return
            
            #if ida is None and idb is not None: 
                #Error('Format Error!', 'Please specify residue ids for segment 1.')
                #if ('between' in self._active_filters): 
                #    del self._active_filters['between']
                #    self.check_filters()
                #return
                    
            #if resa is None and resb is not None: 
                #Error('Format Error!', 'Please specify resnames for segment 1.')
                #if ('between' in self._active_filters): 
                #    del self._active_filters['between']
                #    self.check_filters()
                #return
                    
            #if sega is None and segb is not None: 
                #Error('Format Error!', 'Please specify segnames for segment 1.')
                #if ('between' in self._active_filters): 
                #    del self._active_filters['between']
                #    self.check_filters()
                #return
            
            self._active_filters['between'] = (sega, segb, resa, resb, ida, idb)
            
            if ('between' in self._active_filters) and (sega is None) and (segb is None) and (resa is None) and (resb is None) and (numbers_a is None) and (numbers_b is None): 
                del self._active_filters['between']
        
            self._current_filter = 'between'
        else:
            self._current_filter = None
            if len(self._active_filters) > 0: 
                for key in self._active_filters.keys(): self._current_filter = key
        self.check_filters()
        
        
    def process_selection(self):
        if self.checkBox_selected_nodes.isChecked(): 
            if self.interactive_graph.selected_nodes == []:    
                Error('Selection Error!', "No nodes are selected currently.")
                self.checkBox_selected_nodes.setChecked(False)
                return
            else: 
                self._active_filters['selected_nodes'] = self.interactive_graph.selected_nodes
            
            self._current_filter = 'selected_nodes'
        else: 
            self._current_filter = None
            del self._active_filters['selected_nodes']
            if len(self._active_filters) > 0: 
                for key in self._active_filters.keys(): self._current_filter = key
        self.check_filters()

    
    def apply_filters(self):
        use_filtered = False
        if self.analysis is None: return
        edges_before = {edge for edge in self.analysis.filtered_graph.edges()}
        for active_filter in self._active_filters: 
            if self.groupBox_specific_path.isChecked() and active_filter=='specific':
                try:
                    nodes = self._active_filters['specific']
                    self.analysis.filter_single_path(nodes, use_filtered)
                    use_filtered = True
                except: 
                    Error('Path not found!', 'The nodes do not form a path in that order.')
            
            if self.groupBox_occupancy.isChecked() and active_filter=='occupancy':
                occupancy_cut = self._active_filters['occupancy']
                self.analysis.filter_occupancy(occupancy_cut, use_filtered)
                use_filtered = True
            
            if self.groupBox_connected.isChecked() and active_filter=='connected':
                root = self._active_filters['connected']
                try:
                    self.analysis.filter_connected_component(root, use_filtered=use_filtered)
                except:
                    Error('Node not found!', 'The selected node is not in the current graph!')
                use_filtered = True
            
            if self.groupBox_shortest_paths.isChecked() and active_filter=='shortest':
                root, goal = self._active_filters['shortest']
                try:
                    self.analysis.filter_all_paths(root, goal, use_filtered)
                except AssertionError:
                    Error('Not connected!', 'The selected nodes are not connected!')
                use_filtered = True
            
            if self.groupBox_between_segments.isChecked() and active_filter=='between':
                sega, segb, resa, resb, numbersa, numbersb = self._active_filters['between']
                if sega is not None or segb is not None:
                    self.analysis.filter_between_segnames(sega, segb, use_filtered)
                    use_filtered = True
                if resa is not None or resb is not None:
                    self.analysis.filter_between_resnames(resa, resb, use_filtered)
                    use_filtered = True
                if numbersa is not None or numbersb is not None:
                    numbersa = ranges_to_numbers(numbersa)
                    if numbersb is not None: numbersb = ranges_to_numbers(numbersb)
                    self.analysis.filter_between_resids(numbersa, numbersb, use_filtered)
                    use_filtered = True
            
            if self.checkBox_selected_nodes.isChecked() and active_filter=='selected_nodes':
                nodes = self._active_filters['selected_nodes']
                self.analysis.filter_set_nodes(nodes, use_filtered)
                use_filtered = True
            
            if self.analysis.filtered_graph.number_of_nodes() == 0:
                Error('Empty graph!', 'Adding this filter leads to an empty graph!')
                del self._active_filters[active_filter]
                self.check_filters()
                return
        
        if not use_filtered: 
            self.analysis.filtered_graph = self.analysis.initial_graph
            self.analysis.filtered_results = self.analysis.initial_results
        
        if edges_before != {edge for edge in self.analysis.filtered_graph.edges()}:
            self.interactive_graph.set_subgraph()
            
    def switch_segname_color(self):
        current_segname = self.comboBox_segnames.currentText()
        self.comboBox_colors.setCurrentText(self._segname_colors[current_segname])
        
    def color_per_segment_changed(self):
        color = self.comboBox_colors.currentText()
        self._segname_colors[self.comboBox_segnames.currentText()] = color
        self.interactive_graph.set_colors()
        
    def single_color_changed(self):
        self.interactive_graph.set_colors()
        
    def save_analysis(self):
        if self._current_save_filename is not None:
            filename = self._current_save_filename
        else:
            filename = QFileDialog.getSaveFileName(self, 'Save Analysis', filter='Bridge Analysis File (*.baf);;All Files (*.*)')[0]
            if not filename: return
        self._save_analysis(filename)
        
    def save_as_analysis(self):
        filename = QFileDialog.getSaveFileName(self, 'Save Analysis', filter='Bridge Analysis File (*.baf);;All Files (*.*)')[0]
        if not filename: return
        self._save_analysis(filename)
            
    def _save_analysis(self, filename):
        self._current_save_filename = filename
        self.analysis.prepare_for_pickling()
        if self.interactive_graph is not None: self.interactive_graph.set_current_pos()
        self._analysis_parameter['progress_callback'] = None
        self.close_open_filters()
        save_dict = {'analysis': self.analysis,
                     '_analysis_parameter': self._analysis_parameter,
                     '_search_parameter': self._search_parameter,
                     '_analysis_type': self._analysis_type,
                     '_active_filters': self._active_filters,
                     '_segname_colors': self._segname_colors}
        
        with open(filename, 'wb') as af:
            af.write(pickle.dumps(save_dict))
        self.analysis.restore_after_pickle()
    
    def restore_analysis(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Analysis', filter='Bridge Analysis File (*.baf);;All Files (*.*)')[0]
        if not filename: return
        with open(filename, 'rb') as af:
            save_dict = pickle.loads(af.read())
        
        self._current_save_filename = filename
        
        self.analysis = None
        self._analysis_type = None
        self._analysis_parameter = None
        self._search_parameter = None
        self._segname_colors = None
        
        self.deactivate_all_filters()
        self.__dict__.update(save_dict)
        self.analysis.restore_after_pickle()
        self.radioButton_rotation_pca.setChecked(True)
        self.horizontalSlider_frame.setValue(0)
        self.init_interactive_graph()
        self.prepare_filters()
        self._set_enabled()
        
        
if __name__ == "__main__":
    
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
