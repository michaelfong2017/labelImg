from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QWidget, QMessageBox, QScrollArea, QHBoxLayout
from PyQt5.QtCore import Qt
from libs.createNewDialog import CreateNewDialog
from libs.updateClassDialog import UpdateClassDialog

class ClassManagerDock(QDockWidget):
    def __init__(self, classes=None, parent=None):
        super(ClassManagerDock, self).__init__("Class Manager", parent)
        self.classes = classes or {}
        self.main_window = parent
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Create the list widget to display classes
        self.classes_list_widget = QListWidget()
        self.classes_list_widget.itemSelectionChanged.connect(self.on_class_selected)
        self.classes_list_widget.itemClicked.connect(self.on_class_clicked)

        # Create buttons
        self.new_class_button = QPushButton("Create New Class")
        self.new_class_button.clicked.connect(self.create_new_class)

        self.update_class_button = QPushButton("Update Class")
        self.update_class_button.clicked.connect(self.update_class)
        self.update_class_button.setEnabled(False)

        self.delete_class_button = QPushButton("Delete Class")
        self.delete_class_button.clicked.connect(self.delete_class)
        self.delete_class_button.setEnabled(False)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_class_button)
        button_layout.addWidget(self.update_class_button)
        button_layout.addWidget(self.delete_class_button)

        # Vertical layout for the dock widget
        layout = QVBoxLayout()
        layout.addWidget(self.classes_list_widget)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setWidget(container)

        self.load_classes()

        self.last_selected_item = None

    def load_classes(self):
        self.classes_list_widget.clear()
        for class_name in self.classes:
            self.classes_list_widget.addItem(class_name)

    def on_class_selected(self):
        selected_items = self.classes_list_widget.selectedItems()
        self.update_class_button.setEnabled(bool(selected_items))
        self.delete_class_button.setEnabled(bool(selected_items))

    def on_class_clicked(self, item):
        if item == self.last_selected_item:
            self.classes_list_widget.clearSelection()
            self.last_selected_item = None
            self.update_class_button.setEnabled(False)
            self.delete_class_button.setEnabled(False)
        else:
            self.last_selected_item = item

    def create_new_class(self):
        dialog = CreateNewDialog(classes=self.classes, parent=self)
        if dialog.exec_():
            self.classes.update(dialog.classes)
            self.load_classes()
            self.save_classes()

    def update_class(self):
        selected_items = self.classes_list_widget.selectedItems()
        if not selected_items:
            return
        class_name = selected_items[0].text()
        class_data = self.classes[class_name]

        dialog = UpdateClassDialog(class_name=class_name, class_data=class_data, parent=self)
        if dialog.exec_():
            self.classes[class_name] = dialog.class_data
            self.load_classes()
            self.save_classes()

    def delete_class(self):
        selected_items = self.classes_list_widget.selectedItems()
        if not selected_items:
            return
        class_name = selected_items[0].text()
        del self.classes[class_name]
        self.load_classes()
        self.save_classes()

    def save_classes(self):
        self.main_window.update_class_criteria(self.classes)
        self.main_window.save_updated_classes()