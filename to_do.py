import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime


class MyTasks:
    def __init__(self, hostName, userName, dataBase, passWord):
        self.hostName = hostName
        self.userName = userName
        self.dataBase = dataBase
        self.passWord = passWord

        self.mydb = mysql.connector.connect(
            host=self.hostName,
            user=self.userName,
            database=self.dataBase,
            password=self.passWord
        )
        self.cursor = self.mydb.cursor()

        self.delete_row = None
        self.column_description = None
        self.request = None
        self.update = None
        self.old_value = None
        self.new_value = None
        self.deleteDescription = None
        self.deleteTask = None
        self.delete = None
        self.add = None
        self.task = None
        self.description = None
        self.status = None
        self.data = None
        self.deleteRow = None
        self.id = None
        self.id_details = None
        self.option = None
        self.status_details = None

    def add_task(self):
        self.task = input("Enter task: ")
        self.description = input("Enter description: ")
        self.status = False
        self.add = """INSERT INTO task_details (TaskName, TaskDescription, Status) Value (%s, %s, %s)"""
        self.data = (self.task, self.description, self.status)
        self.cursor.execute(self.add, self.data)
        self.mydb.commit()
        print("Your task has been added successfully.")

    def get_all(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        data = []
        for row in rows:
            data.append(row)
        df = pd.DataFrame(data)

        today = datetime.datetime.now()
        time = today.hour

        if time == 12:
            with open("undone_tasks.csv", "a") as file:
                for index, row in df.iterrows():
                    if row[3] == 0:
                        file.write(row[1])
                        file.write("\n")
                        self.deleteRow = f"""DELETE FROM task_details WHERE TaskName = "{row[1]}" and TaskDescription ="{row[2]}" """
                        self.cursor.execute(self.deleteRow)
        print(df)
        print("A file of undone tasks has been created successfully.")

    def delete_task(self):
        self.deleteTask = input("Enter task to be deleted: ")
        self.deleteDescription = input("Enter the description of the task to be deleted: ")
        self.delete = f"""DELETE FROM task_details WHERE TaskName = "{self.deleteTask}" and TaskDescription ="{self.deleteDescription}" """
        self.cursor.execute(self.delete)
        self.mydb.commit()
        print("Your task has been deleted successfully.")

    def update_task(self):
        self.request = input("Enter task ID: ")
        self.id = f"""SELECT TaskName, TaskDescription, Status FROM task_details WHERE ID={self.request}"""
        self.cursor.execute(self.id)
        self.id_details = self.cursor.fetchone()
        print(self.id_details)
        self.option = input("""What do you want to change? Type in the corresponding number.
        1. Task Name
        2. Task Description
        3. Status
        """)
        if self.option == "1":
            self.new_value = input("Enter new value: ")
            self.old_value = self.id_details[0]
            print(f"Old Task Name Value: {self.old_value}")
            print(f"New Task Name Value: {self.new_value}")
            self.update = f"""UPDATE task_details SET TaskName = "{self.new_value}" WHERE TaskName = "{self.old_value}" """
            self.cursor.execute(self.update)
            self.mydb.commit()
        elif self.option == "2":
            self.new_value = input("Enter new value: ")
            self.old_value = self.id_details[1]
            print(f"Old Task Description Value: {self.old_value}")
            print(f"New Task Description Value: {self.new_value}")
            self.update = f"""UPDATE task_details SET TaskDescription = "{self.new_value}" WHERE TaskDescription = "{self.old_value}" """
            self.cursor.execute(self.update)
            self.mydb.commit()
        elif self.option == "3":
            self.column_description = self.id_details[0]
            print(f"Old Task Status: {self.id_details[2]} - Undone")
            self.update = f"""UPDATE task_details SET Status = true  WHERE Status = false AND TaskName = "{self.column_description}" """
            self.cursor.execute(self.update)
            print("New Task Status: 1 - Done")
            self.mydb.commit()
        print("Your task has been updated successfully.")

    def closeTask(self):
        self.cursor.close()
        self.mydb.close()
        print("Your task has been successfully closed.")
