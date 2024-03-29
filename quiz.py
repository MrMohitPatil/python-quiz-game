import mysql.connector
from tkinter import *
import json
from quiz import *
from tkinter import messagebox as mb
import threading
import time


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="PythonProject"
)
def Login():

	mycursor = mydb.cursor()

	
	mycursor.execute("CREATE TABLE IF NOT EXISTS Stud_data (Name VARCHAR(30), Roll_No Int)")

	
	def insert_Stud_data():
		Name = username_entry.get()
		Roll_No = password_entry.get()

		
		sql = "INSERT INTO Stud_data (Name, Roll_No,Marks) VALUES (%s, %s,%s)"
		val = (Name, Roll_No,"0")

		
		mycursor.execute(sql, val)

		
		mydb.commit()

		
		print(mycursor.rowcount, "record inserted.")
		
		root.destroy()
		Before()
		



	
	root = Tk()
	root.geometry("300x300")

	
	root.title("Login Page")

	
	username_label = Label(root, text="Name:",font=("ariel",15,"bold"))
	username_label.place(x=50,y=20)
	username_entry = Entry(root,font=("ariel",13,"bold"))
	username_entry.place(x=50,y=50)

	
	password_label = Label(root, text="Roll No:",font=("ariel",15,"bold"))
	password_label.place(x=50,y=80)
	password_entry = Entry(root,font=("ariel",13,"bold"))
	password_entry.place(x=50,y=110)

	
	login_button = Button(root, text="Start Quiz", command=insert_Stud_data,width="10",bg="Blue",font=("ariel",16,"bold"))
	login_button.place(x=40,y=160)
	 

	root.mainloop()
	

def Before():
	
		
	class Quiz:
		
		def __init__(self):
			
			
			self.q_no=0
			
			self.display_title()
			self.display_question()
			
			self.opt_selected=IntVar()
			
			self.opts=self.radio_buttons()
			
			self.display_options()
			
			self.buttons()
			
			self.data_size=len(question)
			
			self.correct=0
			self.remaining_time = 120 # set timer to 2 minutes (120 seconds)
			self.timer_label = Label(gui, text="Time left: 2:00", width=20,
                                 font=('Arial', 16, 'bold'), anchor='w')
			self.timer_label.place(x=550, y=10)
			self.timer()
        	

        		
		def timer(self):
			def count_down():
				while self.remaining_time > 0:
					minutes = self.remaining_time // 60
					seconds = self.remaining_time % 60
					time_str = f"Time left: {minutes:02d}:{seconds:02d}"
					self.timer_label.config(text=time_str)
					time.sleep(1)
					self.remaining_time -= 1
				mb.showinfo("Time's up!", "The time is up. Click OK to see your score.")
				mycursor = mydb.cursor()
				sql = "UPDATE Stud_data SET Marks = %s ORDER BY Roll_No DESC LIMIT 1;"
				val = (self.correct,)
				mycursor.execute(sql, val)
				mydb.commit()
				self.display_result()
				gui.destroy()

			t = threading.Thread(target=count_down)
			t.start()



		def display_result(self):
			
			
			wrong_count = self.data_size - self.correct
			correct = f"Correct: {self.correct}"
			wrong = f"Wrong: {wrong_count}"
			
			score = int(self.correct / self.data_size * 100)
			result = f"Accuracy: {score}%"
			
			mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")
			


		
		def check_ans(self, q_no):
		
			
			if self.opt_selected.get() == answer[q_no]:
				return True

		
		def next_btn(self):
			
			
			if self.check_ans(self.q_no):
				
				self.correct += 1
			
			
			self.q_no += 1
			
			
			if self.q_no==self.data_size:
				
				mycursor = mydb.cursor()
				sql = "UPDATE Stud_data SET Marks = %s ORDER BY Roll_No DESC LIMIT 1;"
				val = (self.correct,)
				mycursor.execute(sql, val)
				mydb.commit()
				self.display_result()
				gui.destroy()
			else:
				
				self.display_question()
				self.display_options()


		
		def buttons(self):
			
			next_button = Button(gui, text="Next",command=self.next_btn,
			width=10,bg="blue",fg="white",font=("ariel",16,"bold"))
			
			next_button.place(x=350,y=380)
			
			quit_button = Button(gui, text="Quit", command=gui.destroy,
			width=5,bg="black", fg="white",font=("ariel",16," bold"))
		
			quit_button.place(x=700,y=50)


		def display_options(self):
			val=0
			
			
			self.opt_selected.set(0)
			
			for option in options[self.q_no]:
				self.opts[val]['text']=option
				val+=1


		def display_question(self):
			
			q_no = Label(gui, text=question[self.q_no], width=60,
			font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
			
			q_no.place(x=70, y=100)


		def display_title(self):
			
			title = Label(gui, text="QUIZ",
			width=50, bg="gray",fg="white", font=("ariel", 20, "bold"))
			
			title.place(x=0, y=2)

		def radio_buttons(self):
			
			q_list = []
			
			y_pos = 150
			
			while len(q_list) < 4:
				
				radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected,
				value = len(q_list)+1,font = ("ariel",14))
				
				q_list.append(radio_btn)
				
				radio_btn.place(x = 100, y = y_pos)
				
				y_pos += 40
			
			return q_list




	gui = Tk()

	gui.geometry("800x450")

	gui.title("MCQ Quiz")

	with open('data.json') as f:
		data = json.load(f)

	question = (data['question'])
	options = (data['options'])
	answer = (data[ 'answer'])
	quiz=Quiz()
	
	gui.mainloop()


Login()


