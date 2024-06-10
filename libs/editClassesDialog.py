try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

class EditClassesDialog(QDialog):
    def __init__(self, classes=None, parent=None):
        super(EditClassesDialog, self).__init__(parent)
        self.classes = classes or {}
        self.selected_class = None

        self.setWindowTitle("Edit Classes")

        self.class_list_widget = QListWidget(self)
        self.class_list_widget.addItems(self.classes.keys())
        self.class_list_widget.itemClicked.connect(self.class_item_click)
        self.class_list_widget.itemSelectionChanged.connect(self.class_item_deselected)

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

        self.new_button = QPushButton("Create New")
        self.new_button.clicked.connect(self.new_class)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.finalize_and_save)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_class)
        self.update_button.setEnabled(False)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_class)
        self.delete_button.setEnabled(False)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.new_button)
        button_layout1.addWidget(self.update_button)
        button_layout1.addWidget(self.delete_button)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.save_button)
        button_layout2.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(self.class_list_widget)
        layout.addLayout(button_layout1)
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
        layout.addLayout(button_layout2)

        self.setLayout(layout)

    def class_item_click(self, item):
        self.selected_class = item.text()
        if self.selected_class in self.classes:
            class_criteria = self.classes[self.selected_class]
            self.composition_combo.setCurrentText(class_criteria['composition'])
            self.echogenicity_combo.setCurrentText(class_criteria['echogenicity'])
            self.shape_combo.setCurrentText(class_criteria['shape'])
            self.margin_combo.setCurrentText(class_criteria['margin'])
            selected_foci = class_criteria['echogenic_foci']
            for i in range(self.echogenic_foci_list.count()):
                list_item = self.echogenic_foci_list.item(i)
                list_item.setSelected(list_item.text() in selected_foci)
            self.update_button.setEnabled(True)
            self.delete_button.setEnabled(True)

    def class_item_deselected(self):
        if not self.class_list_widget.selectedItems():
            self.selected_class = None
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def new_class(self):
        class_name, ok = QInputDialog.getText(self, "Class Name", "Enter new class name:")
        if ok and class_name:
            self.classes[class_name] = {
                'composition': self.composition_combo.currentText(),
                'echogenicity': self.echogenicity_combo.currentText(),
                'shape': self.shape_combo.currentText(),
                'margin': self.margin_combo.currentText(),
                'echogenic_foci': [self.echogenic_foci_list.item(i).text() for i in range(self.echogenic_foci_list.count()) if self.echogenic_foci_list.item(i).isSelected()]
            }
            self.class_list_widget.addItem(class_name)
            self.class_list_widget.setCurrentItem(self.class_list_widget.findItems(class_name, Qt.MatchExactly)[0])
            self.selected_class = class_name
            self.class_item_click(self.class_list_widget.currentItem())

    def save_class(self):
        if self.selected_class:
            echogenic_foci = [self.echogenic_foci_list.item(i).text() for i in range(self.echogenic_foci_list.count()) if self.echogenic_foci_list.item(i).isSelected()]
            self.classes[self.selected_class] = {
                'composition': self.composition_combo.currentText(),
                'echogenicity': self.echogenicity_combo.currentText(),
                'shape': self.shape_combo.currentText(),
                'margin': self.margin_combo.currentText(),
                'echogenic_foci': echogenic_foci
            }

    def update_class(self):
        if self.selected_class:
            echogenic_foci = [self.echogenic_foci_list.item(i).text() for i in range(self.echogenic_foci_list.count()) if self.echogenic_foci_list.item(i).isSelected()]
            self.classes[self.selected_class] = {
                'composition': self.composition_combo.currentText(),
                'echogenicity': self.echogenicity_combo.currentText(),
                'shape': self.shape_combo.currentText(),
                'margin': self.margin_combo.currentText(),
                'echogenic_foci': echogenic_foci
            }
            self.class_list_widget.clear()
            self.class_list_widget.addItems(self.classes.keys())

    def delete_class(self):
        if self.selected_class:
            del self.classes[self.selected_class]
            self.class_list_widget.takeItem(self.class_list_widget.currentRow())
            self.selected_class = None
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def finalize_and_save(self):
        self.save_class()
        self.accept()  # Emit the accepted signal and close the dialog
