import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        return conn, c
    except sqlite3.Error as e:
        print(f"An error occurred connecting to the database: {e}")
        return None, None

def create_table(c):
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY, task TEXT, description TEXT, priority TEXT, completed INTEGER)''')
    except sqlite3.Error as e:
        print(f"An error occurred creating the table: {e}")

def add_task(c, conn, task, description, priority):
    try:
        c.execute("INSERT INTO tasks (task, description, priority, completed) VALUES (?, ?, ?, 0)", (task, description, priority))
        conn.commit()
        print("Task added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def remove_task(c, conn, task_id):
    try:
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        print("Task removed successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def mark_completed(c, conn, task_id):
    try:
        c.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
        conn.commit()
        print("Task marked as completed!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def display_tasks(c, filter_status=None):
    try:
        if filter_status is None:
            c.execute("SELECT * FROM tasks")
        else:
            c.execute("SELECT * FROM tasks WHERE completed=?", (filter_status,))
        rows = c.fetchall()
        if rows:
            for row in rows:
                status = "Completed" if row[4] else "Pending"
                print(f"ID: {row[0]}, Task: {row[1]}, Description: {row[2]}, Priority: {row[3]}, Status: {status}")
        else:
            print("No tasks available.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def edit_task(c, conn, task_id, new_task, new_description, new_priority):
    try:
        c.execute("UPDATE tasks SET task=?, description=?, priority=? WHERE id=?", (new_task, new_description, new_priority, task_id))
        conn.commit()
        print("Task updated successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def clear_tasks(c, conn):
    try:
        c.execute("DELETE FROM tasks")
        conn.commit()
        print("All tasks cleared!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def main():
    conn, c = connect_db()
    if conn is None or c is None:
        return

    create_table(c)

    while True:
        print("\n1. Add task")
        print("2. Remove task")
        print("3. Mark task as completed")
        print("4. Display all tasks")
        print("5. Display completed tasks")
        print("6. Display pending tasks")
        print("7. Edit task description")
        print("8. Clear all tasks")
        print("9. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter task: ")
            description = input("Enter description: ")
            priority = input("Enter priority (l - normal, m - important, h - crucial): ").lower()
            priority_map = {'l': 'normal', 'm': 'important', 'h': 'crucial'}
            if priority in priority_map:
                add_task(c, conn, task, description, priority_map[priority])
            else:
                print("Invalid priority. Task not added.")
        elif choice == "2":
            try:
                task_id = int(input("Enter task ID to remove: "))
                remove_task(c, conn, task_id)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to mark as completed: "))
                mark_completed(c, conn, task_id)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        elif choice == "4":
            display_tasks(c)
        elif choice == "5":
            display_tasks(c, filter_status=1)
        elif choice == "6":
            display_tasks(c, filter_status=0)
        elif choice == "7":
            try:
                task_id = int(input("Enter task ID to edit: "))
                new_task = input("Enter new task description: ")
                new_description = input("Enter new description: ")
                new_priority = input("Enter new priority (l - normal, m - important, h - crucial): ").lower()
                priority_map = {'l': 'normal', 'm': 'important', 'h': 'crucial'}
                if new_priority in priority_map:
                    edit_task(c, conn, task_id, new_task, new_description, priority_map[new_priority])
                else:
                    print("Invalid priority. Task not updated.")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        elif choice == "8":
            clear_tasks(c, conn)
        elif choice == "9":
            print("Quitting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
