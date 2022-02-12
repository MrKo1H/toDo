import sqlite3
from datetime import datetime

class DbController:
    """Allows user to update task and projects in database"""
    def __init__(self, db_name):
        self.db_name = db_name
    def set_userID(self, userID):
        self.userID = userID

    def query(self, sql, data):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA Foreign_Keys = ON")
            cursor.execute(sql, data)
            db.commit()

    def select_query(self,sql,data=None):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if data:
                cursor.execute(sql,data)
            else:
                cursor.execute(sql)
            results = cursor.fetchall()
        return results

    def add_task(self, description, deadline, project_id):
        created = datetime.now()
        sql_add_task =  "INSERT INTO Tasks (Description, Deadline, Created, ProjectID, UserID) VALUES (?,?,?,?,?)"
        self.query(sql_add_task, (description, deadline, created, project_id, self.userID))

    def add_project(self, description, deadline):
        created = datetime.now()
        sql_add_project =  "INSERT INTO Projects (Description, Deadline, Created, UserID) VALUES (?,?,?,?)"
        self.query(sql_add_project, (description, deadline, created, self.userID))

    def delete_task(self, task_id):
        self.query("DELETE FROM Tasks WHERE TaskID = ? AND UserID = ?", (task_id,self.userID))

    def delete_task_userID(self, userID):
        self.query("DELETE FROM Tasks WHERE UserID = ?", (userID,))

    def delete_project_only(self, project_id):
        self.query("UPDATE Tasks SET ProjectID = NULL WHERE ProjectID = ? AND UserID = ?", (project_id,self.userID))
        self.query("DELETE FROM Projects WHERE ProjectID = ? AND UserID = ? ", (project_id,self.userID))

    def delete_project_and_tasks(self, project_id):
        self.query("DELETE FROM Tasks WHERE ProjectID = ? AND UserID = ? ", (project_id,self.userID))
        self.query("DELETE FROM Projects WHERE ProjectID = ? AND UserID = ? ", (project_id,self.userID))

    def delete_project_userID(self, userID):
        self.query("DELETE FROM Projects WHERE UserID = ? ", (userID,))

    def mark_task_completed(self, task_id):
        completed = datetime.now()
        sql_mark_completed =  "UPDATE Tasks SET Completed = ? WHERE TaskID = ? AND UserID = ?"
        self.query(sql_mark_completed, (completed, task_id, self.userID))

    def mark_project_completed(self, project_id):
        completed = datetime.now()
        sql_mark_completed =  "UPDATE Projects SET Completed = ? WHERE ProjectID = ? AND UserID = ?"
        self.query(sql_mark_completed, (completed, project_id, self.userID))

    def mark_project_tasks_completed(self, project_id):
        completed = datetime.now()
        sql_mark_completed =  "UPDATE Tasks SET Completed = ? WHERE ProjectID = ? AND UserID = ?"
        self.query(sql_mark_completed, (completed, project_id, self.userID))

    def get_task_project_id(self, task_id):
        sql_get_project_id = "SELECT ProjectID FROM Tasks WHERE TaskID = ? AND UserID = ?"
        results = self.select_query(sql_get_project_id, (task_id, self.userID))
        return results[0][0]

    def check_project_tasks_completed(self, project_id):
        sql_check_project = "SELECT TaskID FROM Tasks WHERE ProjectID = ? AND Completed IS NULL AND UserID = ?"
        results = self.select_query(sql_check_project, (project_id, self.userID))
        if not results:
            return True
        return False
        
    def edit_task_description(self, task_id, description):
        sql_edit_descr = "UPDATE Tasks SET Description = ? WHERE TaskID = ? AND UserID = ?"
        self.query(sql_edit_descr, (description, task_id, self.userID))

    def set_task_deadline(self, task_id, deadline):
        sql_set_deadline = "UPDATE Tasks SET Deadline = ? WHERE TaskID = ? AND UserID = ?"
        self.query(sql_set_deadline, (deadline, task_id, self.userID))

    def assign_task_to_project(self, task_id, project_id):
        sql_assign_task = "UPDATE Tasks SET ProjectID = ? WHERE TaskID = ? AND UserID = ?"
        self.query(sql_assign_task, (project_id, task_id, self.userID))

    def set_project_deadline(self, project_id, deadline):
        sql_set_deadline = "UPDATE Projects SET Deadline = ? WHERE ProjectID = ? AND UserID = ?"
        self.query(sql_set_deadline, (deadline, project_id, self.userID))

    def edit_project_description(self, project_id, description):
        sql_edit_descr = "UPDATE Projects SET Description = ? WHERE ProjectID = ? AND UserID = ?"
        self.query(sql_edit_descr, (description, project_id, self.userID))

    def get_all_tasks(self):
        results = self.select_query("SELECT * FROM Tasks WHERE UserID = ?", (self.userID,))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_active_tasks(self):
        results = self.select_query("SELECT * FROM Tasks WHERE Completed IS NULL AND UserID = ? ", (self.userID,))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_completed_tasks(self):
        results = self.select_query("SELECT * FROM Tasks WHERE Completed IS NOT NULL AND UserID = ?", (self.userID, ))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_single_task(self, task_id):
        results = self.select_query("SELECT * FROM Tasks WHERE TaskID = ? AND UserID = ?", (task_id,self.userID))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_all_projects(self):
        results = self.select_query("SELECT * FROM Projects WHERE UserID = ?", (self.userID,))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_active_projects(self):
        results = self.select_query("SELECT * FROM Projects WHERE Completed IS NULL AND UserID = ?", (self.userID,))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_completed_projects(self):
        results = self.select_query("SELECT * FROM Projects WHERE Completed IS NOT NULL AND UserID = ?", (self.userID,))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_single_project(self, project_id):
        results = self.select_query("SELECT * FROM Projects WHERE ProjectID = ? AND UserID = ?", (project_id,self.userID))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def get_project_tasks(self, project_id):
        results = self.select_query("SELECT * FROM Tasks WHERE ProjectID = ? AND UserID = ?", (project_id,self.userID))
        for i in range(len(results)):
            results[i] = results[i][:-1]
        return results

    def check_username(self, username):
        sql_query = "SELECT *  FROM Users WHERE Username = ?"
        result = self.select_query(sql_query, (username,))
        return 0 if len(result) == 0 else 1

    def add_user(self, username, password):
        if self.check_username(username) == 1:
            return 1
        sql_query_userID = self.select_query("SELECT MAX(UserID) FROM Users")
        userID = 1 if len(sql_query_userID) == 0 else sql_query_userID[0][0] + 1
        sql_query = "INSERT INTO Users(UserID, Username, Password, Created) VALUES (?,?,?,?)"
        self.query(sql_query, (userID, username, password, datetime.now()))
        return 0

    def delete_user(self, userID):
        sql_query = "DELETE FROM Users WHERE userID = ?"
        self.query(sql_query, (userID,))

    def get_users(self):
        sql_query = "SELECT * FROM Users"
        return self.select_query(sql_query)





