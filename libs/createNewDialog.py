try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

class CreateNewDialog(QDialog):
    def __init__(self, classes=None, parent=None):
        super(CreateNewDialog, self).__init__(parent)
        self.classes = classes or {}

        self.setWindowTitle("Create New Class")

        self.class_name_edit = QLineEdit(self)
        self.class_name_edit.setPlaceholderText("Enter class name")

        self.composition_combo = QComboBox()
        self.composition_combo.addItems(["Cystic or almost completely cystic", "Spongiform", "Mixed cystic and solid", "Solid or almost completely solid"])

        self.echogenicity_combo = QComboBox()
        self.echogenicity_combo.addItems(["Anechoic", "Hyperechoic or isoechoic", "Hypoechoic", "Very hypoechoic"])

        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Wider-than-tall", "Taller-than-wide"])

        self.margin_combo = QComboBox()
        self.margin_combo.addItems(["Smooth", "Ill-defined", "Lobulated or irregular", "Extra-thyroidal extension"])

        self.echogenic_foci_list = QListWidget()
        self.echogenic_foci_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.echogenic_foci_list.addItems(["None or large comet-tail artifacts", "Macrocalcifications", "Peripheral (rim) calcifications", "Punctate echogenic foci"])

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.finalize_and_save)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Class Name"))
        layout.addWidget(self.class_name_edit)
        layout.addWidget(QLabel("Composition"))
        layout.addWidget(self.composition_combo)
        layout.addWidget(QLabel("Echogenicity"))
        layout.addWidget(self.echogenicity_combo)
        layout.addWidget(QLabel("Shape"))
        layout.addWidget(self.shape_combo)
        layout.addWidget(QLabel("Margin"))
        layout.addWidget(self.margin_combo)
        layout.addWidget(QLabel("Echogenic Foci"))
        layout.addWidget(self.echogenic_foci_list)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def finalize_and_save(self):
        class_name = self.class_name_edit.text().strip()
        if class_name:
            echogenic_foci = [self.echogenic_foci_list.item(i).text() for i in range(self.echogenic_foci_list.count()) if self.echogenic_foci_list.item(i).isSelected()]
            self.classes[class_name] = {
                'composition': self.composition_combo.currentText(),
                'echogenicity': self.echogenicity_combo.currentText(),
                'shape': self.shape_combo.currentText(),
                'margin': self.margin_combo.currentText(),
                'echogenic_foci': echogenic_foci
            }
            self.accept()  # Emit the accepted signal and close the dialog
        else:
            QMessageBox.warning(self, "Input Error", "Class name cannot be empty.")
