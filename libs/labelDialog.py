try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import new_icon, label_validator, trimmed
from libs.editClassesDialog import EditClassesDialog  # Import the new dialog

BB = QDialogButtonBox

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, class_criteria=None):
        super(LabelDialog, self).__init__(parent)

        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(label_validator())
        self.edit.editingFinished.connect(self.post_process)

        model = QStringListModel()
        model.setStringList(list(class_criteria.keys()))
        completer = QCompleter()
        completer.setModel(model)
        self.edit.setCompleter(completer)

        self.button_box = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(new_icon('done'))
        bb.button(BB.Cancel).setIcon(new_icon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)

        self.edit_classes_button = QPushButton("Edit classes")
        self.edit_classes_button.clicked.connect(self.edit_classes)

        layout = QVBoxLayout()
        layout.addWidget(self.edit_classes_button, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.edit)
        layout.addWidget(bb, alignment=Qt.AlignmentFlag.AlignLeft)

        self.list_widget = QListWidget(self)
        if class_criteria is not None and len(class_criteria) > 0:
            for item in class_criteria.keys():
                self.list_widget.addItem(item)
            self.list_widget.itemClicked.connect(self.list_item_click)
            self.list_widget.itemDoubleClicked.connect(self.list_item_double_click)
            layout.addWidget(self.list_widget)

        self.setLayout(layout)
        
        # Initialize classes from class_criteria
        self.classes = class_criteria

    def validate(self):
        if trimmed(self.edit.text()):
            self.accept()

    def post_process(self):
        self.edit.setText(trimmed(self.edit.text()))

    def pop_up(self, text='', move=True):
        """
        Shows the dialog, setting the current text to `text`, and blocks the caller until the user has made a choice.
        If the user entered a label, that label is returned, otherwise (i.e. if the user cancelled the action)
        `None` is returned.
        """
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            cursor_pos = QCursor.pos()

            # move OK button below cursor
            btn = self.button_box.buttons()[0]
            self.adjustSize()
            btn.adjustSize()
            offset = btn.mapToGlobal(btn.pos()) - self.pos()
            offset += QPoint(btn.size().width() // 4, btn.size().height() // 2)
            cursor_pos.setX(max(0, cursor_pos.x() - offset.x()))
            cursor_pos.setY(max(0, cursor_pos.y() - offset.y()))

            parent_bottom_right = self.parentWidget().geometry()
            max_x = parent_bottom_right.x() + parent_bottom_right.width() - self.sizeHint().width()
            max_y = parent_bottom_right.y() + parent_bottom_right.height() - self.sizeHint().height()
            max_global = self.parentWidget().mapToGlobal(QPoint(max_x, max_y))
            if cursor_pos.x() > max_global.x():
                cursor_pos.setX(max_global.x())
            if cursor_pos.y() > max_global.y():
                cursor_pos.setY(max_global.y())
            self.move(cursor_pos)
        return trimmed(self.edit.text()) if self.exec_() else None

    def list_item_click(self, t_qlist_widget_item):
        text = trimmed(t_qlist_widget_item.text())
        self.edit.setText(text)

    def list_item_double_click(self, t_qlist_widget_item):
        self.list_item_click(t_qlist_widget_item)
        self.validate()

    def edit_classes(self):
        dialog = EditClassesDialog(classes=self.classes, parent=self)
        if dialog.exec_():
            new_classes = dialog.classes
            self.classes.update(new_classes)
            self.update_class_list()
            self.debug_classes()  # Add this line to print all classes and their criteria

    def update_class_list(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.classes.keys())

    def debug_classes(self):
        print("Classes and their criteria:")
        for class_name, criteria in self.classes.items():
            print(f"Class: {class_name}")
            print(f"  Composition: {criteria['composition']}")
            print(f"  Echogenicity: {criteria['echogenicity']}")
            print(f"  Shape: {criteria['shape']}")
            print(f"  Margin: {criteria['margin']}")
            print(f"  Echogenic Foci: {criteria['echogenic_foci']}")
