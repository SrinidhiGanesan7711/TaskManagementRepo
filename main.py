from app.database.db import TaskManager

def main():
    db_path = "tasks.db"
    task_manager = TaskManager(db_path)
    
    while True:
        print("\nMain Menu")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Search tasks by description")
        print("8. Sort tasks")
        print("9. View due date reminders")
        print("10. Exit")

        choice = input("Enter your choice (1-10): ")

        if choice == '1':
            description = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD) or press Enter for no deadline: ")
            if not deadline:
                deadline = None
            priority = input("Enter task priority (high/medium/low): ")
            if priority not in ["high", "medium", "low"]:
                priority = "medium"  
            task_manager.add_task(description, deadline, status="pending", priority=priority)
            print("Task added successfully.")

        elif choice == '2':
            tasks = task_manager.get_all_tasks()
            if tasks:
                print("\nAll Tasks:")
                for task in tasks:
                    print(task)
            else:
                print("No tasks available.")

        elif choice == '3':
            tasks = task_manager.get_pending_tasks()
            if tasks:
                print("\nPending Tasks:")
                for task in tasks:
                    print(task)
            else:
                print("No pending tasks.")

        elif choice == '4':
            tasks = task_manager.get_completed_tasks()
            if tasks:
                print("\nCompleted Tasks:")
                for task in tasks:
                    print(task)
            else:
                print("No completed tasks.")

        elif choice == '5':
            task_id = int(input("Enter task ID to update: "))
            description = input("Enter new description (or press Enter to keep current): ")
            deadline = input("Enter new deadline (YYYY-MM-DD) or press Enter for no change: ")
            status = input("Enter new status (pending/completed) or press Enter for no change: ")
            priority = input("Enter new priority (high/medium/low) or press Enter for no change: ")

            task_manager.update_task(task_id, description, deadline, status, priority)
            print("Task updated successfully.")

        elif choice == '6':
            task_id = int(input("Enter task ID to delete: "))
            task_manager.delete_task(task_id)
            print("Task deleted successfully.")

        elif choice == '7':
            keyword = input("Enter keyword to search for in task description: ")
            tasks = task_manager.search_tasks_by_description(keyword)
            if tasks:
                print("\nSearch Results:")
                for task in tasks:
                    print(task)
            else:
                print("No tasks found with that description.")

        elif choice == '8':
            sort_by = input("Sort tasks by (deadline/status): ")
            tasks = task_manager.sort_tasks(sort_by)
            if tasks:
                print("\nSorted Tasks:")
                for task in tasks:
                    print(task)
            else:
                print("No tasks available.")

        elif choice == '9':
            tasks = task_manager.get_due_soon_tasks()
            if tasks:
                print("\nTasks due soon:")
                for task in tasks:
                    print(task)
            else:
                print("No tasks are due soon.")

        elif choice == '10':
            task_manager.close()
            print("Goodbye!")
            break



if __name__ == "__main__":
    main()
