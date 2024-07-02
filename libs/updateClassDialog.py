from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QAbstractItemView

class UpdateClassDialog(QDialog):
    def __init__(self, class_name, class_data, parent=None):
        super(UpdateClassDialog, self).__init__(parent)

        self.class_name = class_name
        self.class_data = class_data

        self.setWindowTitle("Update Class")

        self.class_name_label = QLabel(self.class_name)
        self.class_name_label.setStyleSheet("background-color: lightgray;")

        self.composition_combo = QComboBox()
        self.composition_combo.addItems(["Cystic or almost completely cystic", "Spongiform", "Mixed cystic and solid", "Solid or almost completely solid"])
        self.composition_combo.setCurrentText(self.class_data['composition'])

        self.echogenicity_combo = QComboBox()
        self.echogenicity_combo.addItems(["Anechoic", "Hyperechoic or isoechoic", "Hypoechoic", "Very hypoechoic"])
        self.echogenicity_combo.setCurrentText(self.class_data['echogenicity'])

        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Wider-than-tall", "Taller-than-wide"])
        self.shape_combo.setCurrentText(self.class_data['shape'])

        self.margin_combo = QComboBox()
        self.margin_combo.addItems(["Smooth", "Ill-defined", "Lobulated or irregular", "Extra-thyroidal extension"])
        self.margin_combo.setCurrentText(self.class_data['margin'])

        self.echogenic_foci_list = QListWidget()
        self.echogenic_foci_list.setSelectionMode(QAbstractItemView.MultiSelection)
        echogenic_foci_options = ["None or large comet-tail artifacts", "Macrocalcifications", "Peripheral (rim) calcifications", "Punctate echogenic foci"]
        self.echogenic_foci_list.addItems(echogenic_foci_options)
        for i in range(self.echogenic_foci_list.count()):
            item = self.echogenic_foci_list.item(i)
            if item.text() in self.class_data['echogenic_foci']:
                item.setSelected(True)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.finalize_and_save)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Class Name"))
        layout.addWidget(self.class_name_label)
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
        echogenic_foci = [self.echogenic_foci_list.item(i).text() for i in range(self.echogenic_foci_list.count()) if self.echogenic_foci_list.item(i).isSelected()]
        self.class_data = {
            'composition': self.composition_combo.currentText(),
            'echogenicity': self.echogenicity_combo.currentText(),
            'shape': self.shape_combo.currentText(),
            'margin': self.margin_combo.currentText(),
            'echogenic_foci': echogenic_foci
        }
        self.accept()  # Emit the accepted signal and close the dialog
