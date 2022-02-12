import sys

from PyQt5.QtWidgets import  *
from PyQt5.QtWidgets import *
from table_widget import *

class ManageAccountWidget(QWidget):
    def __init__(self):
        super(ManageAccountWidget, self).__init__()
        self.setWindowTitle("Mange Account")
        self.setMinimumHeight(300)
        self.controller = DbController("to_do.db")

        self.add_user_button = QPushButton("Add")
        self.delete_user_button = QPushButton("Delete")
        self.delete_user_button.setEnabled(False)
        self.exit_button = QPushButton("Exit")

        self.user_table = UserTable()
        self.load_user()

        self.user_button_layout = QHBoxLayout()
        self.user_button_layout.addWidget(self.add_user_button)
        self.user_button_layout.addWidget(self.delete_user_button)
        self.user_button_layout.addWidget(self.exit_button)

        self.user_layout = QVBoxLayout()
        self.user_layout.addWidget(self.user_table)
        self.user_layout.addLayout(self.user_button_layout)

        self.setLayout(self.user_layout)

        self.add_user_button.clicked.connect(self.open_new_user_dialog)

        self.user_table.clicked.connect(self.enable_delete_button)
        self.delete_user_button.clicked.connect(self.delete_user)

    def delete_user(self):
        userID = self.user_table.get_id()
        if userID != -1:
            self.controller.delete_task_userID(userID)
            self.controller.delete_project_userID(userID)
            self.controller.delete_user(userID)
            self.load_user()

    def enable_delete_button(self):
        self.delete_user_button.setEnabled(True)

    def load_user(self):
        user_items = self.user_table.get_users()
        self.user_table.show_items(user_items)

    def open_new_user_dialog(self):
        new_user_dialog = NewUserDialog()
        new_user_dialog.exec_()
        self.load_user()

class NewUserDialog(QDialog):
    def __init__(self):
        super(NewUserDialog, self).__init__()

        self.controller = DbController("to_do.db")
        self.setWindowTitle("Add New User")
        self.username_label = QLabel("Username")
        self.password_label = QLabel("Password")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.message = QLabel()

        self.password.setEchoMode(QLineEdit.Password)

        self.add_button = QPushButton("Add")

        self.new_user_layout = QVBoxLayout()
        self.new_user_layout.addWidget(self.username_label)
        self.new_user_layout.addWidget(self.username)
        self.new_user_layout.addWidget(self.password_label)
        self.new_user_layout.addWidget(self.password)
        self.new_user_layout.addWidget(self.message)
        self.new_user_layout.addWidget(self.add_button)

        self.setLayout(self.new_user_layout)
        self.add_button.clicked.connect(self.add_new_user)

    def add_new_user(self):
        username = self.username.text()
        password = self.password.text()
        if len(username) == 0 or len(password) == 0:
            self.message.setText("Invalid Username and Password!")
        else:
            exit_code = self.controller.add_user(username, password)
            if exit_code == 0:
                self.close()
            else:
                self.message.setText("Account exist!")

