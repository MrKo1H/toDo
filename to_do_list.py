import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from create_new_db import *
from tab_widget import *
from login_widget import *
from manage_acount_widget import *

class ToDoWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("To Do List")
        self.setMinimumHeight(300)

        self.central_widget = TaskProjectTabs()
        self.setCentralWidget(self.central_widget)

        self.central_widget.task_exit_button.clicked.connect(self.return_login)
        self.central_widget.project_exit_button.clicked.connect(self.return_login)

        self.manage_account = ManageAccountWidget()
        self.manage_account.exit_button.clicked.connect(self.return_login)

        self.form = Form()
        self.form.ui.pushButton.clicked.connect(self.check_user)
        self.form.ui.pushButton_2.clicked.connect(self.exit)

    def return_login(self):
        self.manage_account.hide()
        self.hide()
        self.form.show()

    def exit(self):
        self.manage_account.close()
        self.form.close()
        self.close()

    def check_user(self):
        username = self.form.ui.lineEdit.text()
        password = self.form.ui.lineEdit_2.text()
        if len(username) > 0 and len(password) > 0:
            with sqlite3.connect("to_do.db") as db:
                cursor = db.cursor()
                sql_query = "SELECT UserID, Password From Users Where Username = ?"
                cursor.execute(sql_query, (username,))
                user_info = cursor.fetchone()
                if user_info is not None:
                    userID = user_info[0]
                    userPassword = user_info[1]
                    if str(userPassword) == password:
                        if username == "localhost":
                            self.manage_account.show()
                            self.form.hide()
                            self.hide()
                        else:
                            self.central_widget.set_userID(userID)
                            self.manage_account.hide()
                            self.form.hide()
                            self.show()
                            self.raise_()

                    else:
                        self.form.ui.label_5.setText("Wrong Password!")
                else:
                    self.form.ui.label_5.setText("Invalid Account!")
        else:
            self.form.ui.label_5.setText("Missing Username or Password!")
        pass

if __name__ == "__main__":
    #creates new database when run for the first time
    if not os.path.exists("to_do.db"):
        create_new_db("to_do.db")
        new_db = QMessageBox()
        new_db.setWindowTitle("New Database")
        new_db.setText("New database created")
        new_db.exec_()
    to_do = QApplication(sys.argv)


    main_window = ToDoWindow()
    main_window.raise_()
    main_window.form.show()

    to_do.exec_()
