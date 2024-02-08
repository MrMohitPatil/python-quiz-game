import mysql.connector
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Pass@123",
  database="PythonProject"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM Stud_data")

rows = cursor.fetchall()

root = tk.Tk()
root.title("Score Of Students")

style = ThemedStyle(root)
style.set_theme("arc")

tree = ttk.Treeview(root, columns=(1, 2, 3), show="headings")
tree.pack()

tree.heading(1, text="Name")
tree.heading(2, text="Roll No")
tree.heading(3, text="Score")

for row in rows:
    tree.insert("", "end", values=row)

root.mainloop()

cursor.close()
db.close()
