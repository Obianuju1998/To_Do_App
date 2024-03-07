from to_do import MyTasks
import datetime

today = datetime.datetime.now()
time = today.hour
print(time)

new_table = """
CREATE TABLE task_details (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    TaskName VARCHAR(40) NOT NULL,
    TaskDescription VARCHAR(40) NOT NULL,
    Status Boolean
    );
"""

all_columns = "SELECT * FROM task_details"

connection = MyTasks('localhost', 'root', "to_do_app", 'Agnes123.456/789*')

app_on = True

while app_on:
    task = input("Type 1 to add, 2 to update, 3 to delete, 4 to show all tasks, and 5 to close connection: ")
    if task == "1":
        connection.add_task()
    elif task == "2":
        connection.update_task()
    elif task == "3":
        connection.delete_task()
    elif task == "4":
        connection.get_all(all_columns)
    elif task == "5":
        connection.closeTask()
        break
