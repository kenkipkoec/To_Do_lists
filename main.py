import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        return conn, c
    except sqlite3.Error as e:
        print(f"An error occurred connecting to the database: {e}")
        return None, None

def create_tables(c):
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY, user_id INTEGER, task TEXT, description TEXT, priority TEXT, completed INTEGER,
                     FOREIGN KEY(user_id) REFERENCES users(id))''')
    except sqlite3.Error as e:
        print(f"An error occurred creating the tables: {e}")

def add_user(c, conn, username):
    try:
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        print("User added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def add_task(c, conn, user_id, task, description, priority):
    try:
        c.execute("INSERT INTO tasks (user_id, task, description, priority, completed) VALUES (?, ?, ?, ?, 0)",
                  (user_id, task, description, priority))
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

def display_tasks(c, user_id=None, filter_status=None):
    try:
        query = "SELECT * FROM tasks"
        params = []

        if user_id is not None:
            query += " WHERE user_id=?"
            params.append(user_id)

            if filter_status is not None:
                query += " AND completed=?"
                params.append(filter_status)
        elif filter_status is not None:
            query += " WHERE completed=?"
            params.append(filter_status)

        c.execute(query, params)
        rows = c.fetchall()
        if rows:
            for row in rows:
                status = "Completed" if row[5] else "Pending"
                print(f"ID: {row[0]}, Task: {row[2]}, Description: {row[3]}, Priority: {row[4]}, Status: {status}")
        else:
            print("No tasks available.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def edit_task(c, conn, task_id, new_task, new_description, new_priority):
    try:
        c.execute("UPDATE tasks SET task=?, description=?, priority=? WHERE id=?",
                  (new_task, new_description, new_priority, task_id))
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

    create_tables(c)

    while True:
        print("\n1. Add user")
        print("2. Add task")
        print("3. Remove task")
        print("4. Mark task as completed")
        print("5. Display all tasks")
        print("6. Display completed tasks")
        print("7. Display pending tasks")
        print("8. Edit task description")
        print("9. Clear all tasks")
        print("10. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            add_user(c, conn, username)
        elif choice == "2":
            try:
                user_id = int(input("Enter user ID: "))
                task = input("Enter task: ")
                description = input("Enter description: ")
                priority = input("Enter priority (l - normal, m - important, h - crucial): ").lower()
                priority_map = {'l': 'normal', 'm': 'important', 'h': 'crucial'}
                if priority in priority_map:
                    add_task(c, conn, user_id, task, description, priority_map[priority])
                else:
                    print("Invalid priority. Task not added.")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to remove: "))
                remove_task(c, conn, task_id)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to mark as completed: "))
                mark_completed(c, conn, task_id)
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        elif choice == "5":
            display_tasks(c)
        elif choice == "6":
            display_tasks(c, filter_status=1)
        elif choice == "7":
            display_tasks(c, filter_status=0)
        elif choice == "8":
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
        elif choice == "9":
            clear_tasks(c, conn)
        elif choice == "10":
            print("Quitting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
