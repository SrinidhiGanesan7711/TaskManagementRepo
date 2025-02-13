# db.py
import sqlite3
from datetime import datetime, timedelta

class Task:
    def __init__(self, id, description, deadline, status, priority):
        self.id = id
        self.description = description
        self.deadline = deadline
        self.status = status
        self.priority = priority


    def __str__(self):
        return f"ID: {self.id} | Description: {self.description} | Deadline: {self.deadline} | Status: {self.status} | Priority: {self.priority}"

class TaskManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create the tasks table 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                deadline TEXT,
                status TEXT CHECK(status IN ('pending', 'completed')) NOT NULL DEFAULT 'pending',
                priority TEXT CHECK(priority IN ('high', 'medium', 'low')) NOT NULL DEFAULT 'medium'
            )
        ''')
        self.conn.commit()

    def add_task(self, description, deadline=None, status="pending", priority="medium"):
        # Add a new task to the database
        self.cursor.execute('''
            INSERT INTO tasks (description, deadline, status, priority) 
            VALUES (?, ?, ?, ?)
        ''', (description, deadline, status, priority))
        self.conn.commit()

    def get_all_tasks(self):
        # Fetch all tasks from the database
        self.cursor.execute('SELECT * FROM tasks')
        return [Task(*row) for row in self.cursor.fetchall()]

    def get_pending_tasks(self):
        # Fetch all pending tasks from the database
        self.cursor.execute('SELECT * FROM tasks WHERE status = "pending"')
        return [Task(*row) for row in self.cursor.fetchall()]

    def get_completed_tasks(self):
        # Fetch all completed tasks from the database
        self.cursor.execute('SELECT * FROM tasks WHERE status = "completed"')
        return [Task(*row) for row in self.cursor.fetchall()]

    def update_task(self, task_id, description=None, deadline=None, status=None, priority=None):
        # Update an existing task in the database
        task = self.get_task_by_id(task_id)
        if task:
            new_description = description if description else task.description
            new_deadline = deadline if deadline else task.deadline
            new_status = status if status else task.status
            new_priority = priority if priority else task.priority

            self.cursor.execute('''
                UPDATE tasks SET description = ?, deadline = ?, status = ?, priority = ? WHERE id = ?
            ''', (new_description, new_deadline, new_status, new_priority, task_id))
            self.conn.commit()
            return True
        return False

    def delete_task(self, task_id):
        # Delete a task from the database
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def get_task_by_id(self, task_id):
        # Fetch a task by its ID
        self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = self.cursor.fetchone()
        return Task(*row) if row else None

    def search_tasks_by_description(self, keyword):
        # Search for tasks that contain the given keyword in their description
        self.cursor.execute('SELECT * FROM tasks WHERE description LIKE ?', ('%' + keyword + '%',))
        return [Task(*row) for row in self.cursor.fetchall()]

    def sort_tasks(self, by="deadline"):
        # Sort tasks by a given criterion ('deadline' or 'status')
        if by == "deadline":
            self.cursor.execute('SELECT * FROM tasks ORDER BY deadline')
        elif by == "status":
            self.cursor.execute('SELECT * FROM tasks ORDER BY status')
        else:
            print("Invalid sort criterion.")
            return []

        return [Task(*row) for row in self.cursor.fetchall()]

    def get_due_soon_tasks(self):
        
        now = datetime.now()
        soon = now + timedelta(days=1)  
        soon_str = soon.strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute('''
            SELECT * FROM tasks WHERE deadline BETWEEN ? AND ?
        ''', (now.strftime("%Y-%m-%d %H:%M:%S"), soon_str))

        return [Task(*row) for row in self.cursor.fetchall()]

    def close(self):
        self.conn.close()
