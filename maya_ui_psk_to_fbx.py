import os
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets

import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    '''Return the Maya main window widget as a Python object'''
    main_window_ptr = omui.MQtUtil.mainWindow()
    if not main_window_ptr:
        return None
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ConvertPSKToFBX(QtWidgets.QDialog):
    def __init__(self,
				 fix_fbx=True,
				 parent=maya_main_window()):
        super(ConvertPSKToFBX, self).__init__(parent)

        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        # Set main QDialog size/style.
        style_file = QtCore.QFile(cmds.internalVar(userAppDir=True) + "scripts/btom_psk/btom_style.qss")
        style_file.open(QtCore.QFile.ReadOnly)
        stylesheet = str(style_file.readAll())
        self.setStyleSheet(stylesheet)
        self.setMinimumWidth(400)

        self.max_progress = 100
        self.setWindowTitle("Blender PSK to FBX")
        self.process = QtCore.QProcess(self)
        self.errors_list = []
        self.input_path = ""
        self.output_path = ""
        self.blender_exe_path = ""
        self.blender_args = ["-b",
                             "--python",
                             cmds.internalVar(userAppDir=True) + "scripts/btom_psk/blender_convert_psk_to_fbx.py"]
        self.user_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        if os.path.exists("C:/Program Files/Blender Foundation/"):
            self.blender_exe = "C:/Program Files/Blender Foundation/"
        else:
            self.blender_exe = self.user_desktop

        self.fix_fbx = fix_fbx

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.blender_path_lbl = QtWidgets.QLabel("Blender.exe path:")
        self.blender_path_line = QtWidgets.QLineEdit()
        self.blender_path_line.setReadOnly(True)
        self.blender_dialog_btn = QtWidgets.QPushButton("...")

        self.blender_dialog = QtWidgets.QFileDialog()
        self.blender_dialog.setWindowTitle("Select Blender.exe")
        self.blender_dialog.setDirectory(self.blender_exe)
        self.blender_dialog.setDefaultSuffix("exe")
        self.blender_dialog.setNameFilter(("exe (*.exe)"))
        self.blender_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

        self.input_path_lbl = QtWidgets.QLabel("Skeleton mesh path:")
        self.input_path_line = QtWidgets.QLineEdit()
        self.input_path_line.setReadOnly(True)
        self.input_dialog_btn = QtWidgets.QPushButton("...")

        self.input_dialog = QtWidgets.QFileDialog()
        self.input_dialog.setWindowTitle("Select Skeleton Mesh")
        self.input_dialog.setDirectory(self.user_desktop)
        self.input_dialog.setDefaultSuffix("psk")
        self.input_dialog.setNameFilter(("psk (*.psk *.pskx)"))
        self.input_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

        self.output_path_lbl = QtWidgets.QLabel("Save/Output fbx path:")
        self.output_path_line = QtWidgets.QLineEdit()
        self.output_path_line.setReadOnly(True)
        self.output_dialog_btn = QtWidgets.QPushButton("...")

        self.output_dialog = QtWidgets.QFileDialog()
        self.output_dialog.setWindowTitle("Select save location of blender FBX")
        self.output_dialog.setDirectory(self.user_desktop)
        self.output_dialog.setDefaultSuffix("fbx")
        self.output_dialog.setNameFilter("Fbx (*.fbx)")
        self.output_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        self.progress_lbl = QtWidgets.QLabel("Converting SPK in Blender...")
        self.progress_lbl.setVisible(False)
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setVisible(False)

        self.import_fbx_btn = QtWidgets.QPushButton("Import FBX")
        self.import_fbx_btn.setVisible(False)

        self.error_title_lbl = QtWidgets.QLabel("Errors:")
        self.error_txted = QtWidgets.QTextEdit()
        self.error_txted.setReadOnly(True)
        self.error_field = QtWidgets.QScrollArea()

        self.convert_btn = QtWidgets.QPushButton("Convert!")


    def create_layouts(self):
        self.blender_dialog_lay = QtWidgets.QHBoxLayout()
        self.blender_dialog_lay.setContentsMargins(2, 2, 2, 2)
        self.blender_dialog_lay.addWidget(self.blender_path_line)
        self.blender_dialog_lay.addWidget(self.blender_dialog_btn)

        self.input_dialog_lay = QtWidgets.QHBoxLayout()
        self.input_dialog_lay.setContentsMargins(2, 2, 2, 2)
        self.input_dialog_lay.addWidget(self.input_path_line)
        self.input_dialog_lay.addWidget(self.input_dialog_btn)

        self.output_dialog_lay = QtWidgets.QHBoxLayout()
        self.output_dialog_lay.setContentsMargins(2, 2, 2, 2)
        self.output_dialog_lay.addWidget(self.output_path_line)
        self.output_dialog_lay.addWidget(self.output_dialog_btn)

        self.error_field_lay = QtWidgets.QVBoxLayout()
        self.error_field_lay.setContentsMargins(0, 0, 0, 0)
        self.error_field_lay.setSpacing(2)
        self.error_field_lay.addWidget(self.error_txted)
        self.error_field.setLayout(self.error_field_lay)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.blender_path_lbl)
        self.main_layout.addLayout(self.blender_dialog_lay)
        self.main_layout.addWidget(self.input_path_lbl)
        self.main_layout.addLayout(self.input_dialog_lay)
        self.main_layout.addWidget(self.output_path_lbl)
        self.main_layout.addLayout(self.output_dialog_lay)
        self.main_layout.addWidget(self.progress_lbl)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.error_title_lbl)
        self.main_layout.addWidget(self.error_field)
        self.main_layout.addWidget(self.convert_btn)
        self.main_layout.addWidget(self.import_fbx_btn)


    def create_connections(self):
        self.blender_dialog_btn.clicked.connect(self.get_blender_path)
        self.input_dialog_btn.clicked.connect(self.get_input_path)
        self.output_dialog_btn.clicked.connect(self.get_output_path)
        self.convert_btn.clicked.connect(self.convert_in_blender)
        self.process.stateChanged.connect(self.proc_state_changed)
        self.process.readyReadStandardOutput.connect(self.update_progressbar)
        self.process.readyReadStandardError.connect(self.handle_errors)
        self.import_fbx_btn.clicked.connect(self.import_fbx)


    def popup_win(self, message):
        popup = QtWidgets.QMessageBox()
        popup.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        popup.setText(message)
        popup.exec_()


    def get_blender_path(self):
        self.blender_dialog.exec_()
        if self.blender_dialog.selectedFiles and self.blender_dialog.selectedFiles():
            self.blender_exe_path = self.blender_dialog.selectedFiles()[0]
            self.blender_path_line.setText(self.blender_exe_path)
            self.blender_dialog.setDirectory(self.blender_exe_path)


    def get_input_path(self):
        self.input_dialog.exec_()
        if self.input_dialog.selectedFiles and self.input_dialog.selectedFiles():
            self.input_path = self.input_dialog.selectedFiles()[0]
            self.input_path_line.setText(self.input_path)
            self.input_dialog.setDirectory(self.input_path)
            self.output_dialog.setDirectory(self.input_path)


    def get_output_path(self):
        self.output_dialog.exec_()
        if self.output_dialog.selectedFiles and self.output_dialog.selectedFiles():
            self.output_path = self.output_dialog.selectedFiles()[0]
            self.output_path_line.setText(self.output_path)
            self.output_dialog.setDirectory(self.output_path)


    def convert_in_blender(self):

        if any(self.input_path and self.output_path and self.blender_exe_path) is False:
            self.popup_win("Ensure each field has a path.")
            return
        else:
            # Start the Proc
            self.progress_lbl.setVisible(True)
            self.progress_bar.setVisible(True)
            self.repaint()
            self.convert_proc()


    def convert_proc(self):
        """
        Starts the QProcess
        """

        self.convert_btn.setEnabled(False)

        # Add paths as arguments
        self.blender_args.append(self.input_path)
        self.blender_args.append(self.output_path)
        self.process.start(self.blender_exe_path, self.blender_args)


    def update_progressbar(self):
        """
        Updates the progressbar value by looking for a string printed from the
        executed process.
        Reads the stdout and string manipulates to get only the integers in the line.
        """
        self.process.setReadChannel(QtCore.QProcess.StandardOutput)

        while self.process.canReadLine():
            line_stdout = str(self.process.readLine())
            # Set line to be a list of only digits found.
            line_stdout_digits = [int(i) for i in line_stdout.split() if i.isdigit()]

            # Check if the line isn't empty
            if len(line_stdout_digits) == 1:
                # Set the max progress for progress bar
                if "~PROGRESSBAR~ set_length: " in line_stdout:
                    # Adding 1 extra progress step for showing completed status
                    self.max_progress = line_stdout_digits[0] + 1
                    self.progress_bar.setMaximum(self.max_progress)
                # Increase the progress bar
                if "~PROGRESSBAR~ set_value: " in line_stdout:
                    self.progress_bar.setValue(line_stdout_digits[0])


    def proc_state_changed(self):
        """
        Sets the final completed status bar % if a NormalExit.
        """
        if self.process.state() == QtCore.QProcess.ProcessState.NotRunning:
            if self.process.exitStatus() == QtCore.QProcess.ExitStatus.NormalExit:
                self.progress_bar.setValue(self.max_progress)
                self.progress_bar.setDisabled(True)
                self.convert_btn.setVisible(False)
                self.import_fbx_btn.setVisible(True)

            if self.process.exitStatus() == QtCore.QProcess.ExitStatus.CrashExit:
                self.progress_bar.setDisabled(True)


    def import_fbx(self):
        if os.path.exists(self.output_path):
            output_path_name = self.output_path.split("/")[-1].split(".")[0]
            if cmds.namespace(exists=output_path_name):
                self.popup_win(("Namespace with name: %s already exists,"
							   "please remove/rename it." % output_path_name))
                return

            cmds.file(self.output_path,
                      namespace=output_path_name,
                      reference=True,
                      ignoreVersion=True,
                      mergeNamespacesOnClash=False)
            cmds.file(self.output_path, importReference=True)
            cmds.namespace(removeNamespace=output_path_name,
						   mergeNamespaceWithRoot=True)

            # Fix the imported fbx if requested
            if self.fix_fbx:
                self.fix_imported_fbx()

            self.close()
        else:
            self.import_fbx_btn.setText("FBX UNAVAILABLE")
            self.import_fbx_btn.setDisabled(True)


    def fix_imported_fbx(self):
        joints = cmds.ls(type='joint')
        fbx_period = "FBXASC046"
        to_delete = []

        # # Set joint size in viewport
        for joint in joints:
            cmds.setAttr(joint + ".radius", 1)

        # Remove the FBX period from blenders export
        for node in cmds.ls(type="transform"):
            if fbx_period in node.split("|")[-1]:
                cmds.rename(node, node.replace(fbx_period, "_"))

        # Remove locator
        locators = cmds.ls("*_ao", type="transform", long=True)

        for node in locators:
            if "joint" != cmds.objectType(node):
                to_delete.append(node)
                root_joint = cmds.listRelatives(node,
                                                fullPath=True,
                                                children=True,
                                                type="joint")[0]

        # Unparent root joint to world and remove the old locator
        cmds.parent(root_joint, world=True)
        cmds.delete(to_delete)


    def handle_errors(self):
        error_msg = str(self.process.readAllStandardError())
        self.error_txted.setText(self.error_txted.toPlainText() + error_msg)


# test = ConvertPSKToFBX()
# test.show()
