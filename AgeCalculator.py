# Author:  OMAR BIN SALAMAH
# Version: 2017-10-4

import os
import random
import sys
import tkinter as tk
import tkinter.messagebox
import webbrowser
import wikipedia
import yagmail
from datetime import *
from tkinter import ttk
from PIL import Image
from PIL import ImageGrab
from twitter import *


class AgeCalculator(tk.Tk):

	def __init__(self):
		self.age = 0
		self.day = 0
		tk.Tk.__init__(self)
		self.style = ttk.Style()
		self.title("Age calculator")
		self.label_frames = tkinter.Frame(self, bg='#c63163')

		# --------------------WINDOW ICON-------------------------#
		if "nt" == os.name:
			self.wm_iconbitmap(bitmap = "clienticon.ico")
		else:
			self.wm_iconbitmap(bitmap = "@myicon.xbm")
		# --------------------------------------------------------#

		# ---------------------Menu Items-------------------------#
		self.menu = tk.Menu(self)
		self.config(menu = self.menu)

		self.file_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label = "File", menu = self.file_menu)
		self.file_menu.add_command(label = "New...", command = AgeCalculator)
		self.file_menu.add_command(label = "Screenshot", command = self.screen_shot)
		self.file_menu.add_command(label = "Save as PDF", command = self.PDF)  # July 26
		self.file_menu.add_command(label = "Print")
		self.file_menu.add_separator()
		self.file_menu.add_command(label = "Exit", command = quit)

		self.share_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label = "Share", menu = self.share_menu)
		self.share_menu.add_command(label = 'Tweet', command = self.tweet)
		self.share_menu.add_command(label = 'Email...', command = self.gmail)
		self.share_menu.add_command(label = 'Facebook post...')  # working on it

		self.more_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label = "More", menu = self.more_menu)
		self.more_menu.add_command(label = 'year born summary', command = self.wikipedia)  # working on it
		self.more_menu.add_command(label = 'what happened that year?', command = self.what_happened)

		# ------------------- Top Border ------------------------#
		self.desc_style0 = tk.Label(self, bg = 'snow')
		self.desc_style0.place(x = 0, y = 0, height = 10, width = 1000)
		self.desc_style1 = tk.Label(self, bg = 'snow')
		self.desc_style1.place(x = 0, y = 8, height = 30, width = 1000)

		# ------------------Description Label--------------------#
		self.description = tk.Label(self, text = "Find out what day of the week you were born!", bg = 'white')
		self.description.place(x = 335, y = 11)
		self.description.config(font = ("FF Din", 15))

		# ---------------------Time Label-----------------------#
		self.date = self.date_time()

		self.date_label = tk.Label(self, text = self.date, bg = 'grey', relief = "groove",
		                           anchor = 'center')
		self.date_label.place(x = 0, y = 38, height = 25, width = 1001)
		self.date_label.config(font = ("FF Din", 12))

		# --------------------Troll Button-----------------------#
		self.style.map("C.TButton",
		               foreground = [('pressed', 'white'), ('active', 'blue')],
		               background = [('pressed', '!disabled', 'red'), ('active', 'white')])
		self.troll0 = ttk.Button(text = "Estimated time of death", style = "C.TButton", cursor='pirate',
		                         command= self.troll)
		self.troll0.place(x = 820, y = 532)

		# -------------Entry Discription Label------------------#
		self.entry_discription = tk.Label(self, text = 'DDMMYYYY')
		self.entry_discription.place(x = 265, y = 100)
		self.format_description = tk.Label(self, text = 'DDMMYYYY format')

		# -----------------Entry and Button---------------------#
		self.entry = tk.Entry(self, selectbackground = '#d8f7ee', selectforeground = '#a6c4bc')
		self.entry.place(x = 405, y = 100)
		self.button = ttk.Button(self, text = 'show me!', style = "C.TButton", cursor = 'heart',
		                         command = self.outputer)
		self.button.place(x = 610, y = 102)
		
		# --------------DIRECTING OUTPUT TO WINDOW---------------#
		self.scrollbar = ttk.Scrollbar(self, cursor = 'heart')
		self.scrollbar.config(bg = 'black')
		self.scrollbar.place(x = 800, y = 200, height = 300)
		self.text = tk.Text(self, wrap = "word", relief = "groove", yscrollcommand = self.scrollbar.set, bg = '#f0eee9',
		                    insertbackground = 'white', padx = 15, pady = 15)
		self.text.place(x = 190, y = 150)
		self.text.tag_configure('')
		self.scrollbar.config(command = self.text.yview, bg = 'black', troughcolor = 'blue')

		sys.stdout = TextRedirector(self.text, "stdout")
		sys.stderr = TextRedirector(self.text, "stderr")

	def date_time(self):
		self.current_date = datetime.now().strftime("%d%m%Y")
		self.current_day = self.current_date[0:2]
		self.current_month = self.current_date[2:4]
		self.current_year = self.current_date[-4:]
		self.current_mmdd = self.current_date[0:4]
		current_time = datetime.now().strftime("%H:%M")

		weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		today = int(self.current_date[0:2])
		day_of_week = datetime.today().weekday()

		months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
		month = int(self.current_date[2:4]) - 1

		day = weekdays[day_of_week]
		current_month = months[month]

		return day, current_month, today, current_time

	def troll(self):
		tkinter.messagebox.showinfo('shit', 'dunno man :(')

	def calculate(self):
		dob = self.entry.get()
		dd = dob[:2]
		mm = dob[2:4]
		yy = dob[-4:]
		mmdd = dob[2:4] + dob[0:2]

		if int(dd) not in range(1, 32) or int(mm) not in range(1, 13) or int(yy) not in range(1700, 2017):
			return "This date of birth doesn't seem right"

		else:

			if int(mm) == int('01'):
				mm = 'January'
			elif int(mm) == int('02'):
				mm = 'February'
			elif int(mm) == int('03'):
				mm = 'March'
			elif int(mm) == int('04'):
				mm = 'April'
			elif int(mm) == int('05'):
				mm = 'May'
			elif int(mm) == int('06'):
				mm = 'June'
			elif int(mm) == int('07'):
				mm = 'July'
			elif int(mm) == int('08'):
				mm = 'August'
			elif int(mm) == int('09'):
				mm = 'September'
			elif int(mm) == int('10'):
				mm = 'October'
			elif int(mm) == int('11'):
				mm = 'November'
			elif int(mm) == int('12'):
				mm = 'December'

			dob = ("You were born on " + mm + ' ' + dd + ', ' + yy + '\n')

			if mmdd > self.current_mmdd:
				self.age = int(self.current_year) - int(yy) - 1
			elif mmdd <= self.current_mmdd:
				self.age = int(self.current_year) - int(yy)

			self.calculate_share = ('You are ' + str(self.age) + ' years old \n')
			return 'You are ' + str(self.age) + ' years old\n' + dob

	def legalAge(self):

		if self.age > 18:
			if self.age >= 21:
				return "you can buy booze"
			elif (self.age > 18) and (self.age < 21):
				return 'you can buy cigarettes but not booze'
			elif self.age < 18:
				return 'you are not old enough to buy booze or cigarettes'

	def zeller(self):
		dob = self.entry.get()
		day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		d = int(dob[:2])
		m = int(dob[3:4])
		y = int(dob[-4:])

		if int(d) not in range(1, 32) or int(m) not in range(1, 13) or int(y) not in range(1700, 2018):
			return ''
		else:
			if m < 3:
				m += 12
				y += - 1
			self.day = (((13 * m + 3) // 5 + d + y + (y / 4) - (y // 100) + (y // 400)) % 7)
			self.zeller_share = ("Based on Zeller's algorithm, you were born on a " + day_names[int(self.day)])
			return "Based on Zeller's algorithm, you were born on a " + day_names[int(self.day)]

	def wikipedia(self):
		dob = self.entry.get()
		year_born = dob[-4:]

		try:
			intro = ('\nSummary of the year ' + year_born + ':\n')
			wiki = wikipedia.summary(year_born)
			print(intro + wiki)
		except Exception:
			tkinter.messagebox.showerror('error message', 'you did not provide any input')

	def what_happened(self):
		dob = self.entry.get()
		year = dob[-4:]

		try:
			webbrowser.get('Chrome') # specify your browser here
			webbrowser.open("https://worldhistoryproject.org/" + str(year))
		except Exception:
			tkinter.messagebox.showerror('error message', 'you did not provide any input')

	def screen_shot(self):

		# part of the screen
		img = ImageGrab.grab(bbox = (10, 55, 1150, 1200))
		name_generator = random.randrange(1, 1000)
		name = str(name_generator) + '.png'
		img.save(name)

	def PDF(self):  # take screen shot -> convert to PDF -> delete screenshot
		img = ImageGrab.grab(bbox = (10, 55, 1150, 1200))
		name_generator = random.randrange(1, 1000)
		name = str(name_generator) + '.png'
		img.save(name)

		path = name
		pdfname = 'pdf_version' + '.PDF'
		im = Image.open(path)
		if im.mode == 'RGBA':
			im = im.convert('RGB')
		im.save(pdfname, "PDF", quality = 100)
		os.remove(name)

	def outputer(self):
		try:
			print(self.calculate())
			print(self.zeller())

		except Exception:
			tkinter.messagebox.showerror('error message',
			                             "invalid input. Try typing your date of birth\n" + "DDMMYYYY format")

	def gmail(self):
		try:
			# here you can edit signature of the email to be sent
			gmail_signature = '\n\n\n\n-Omar'
			# here you put the email address of the sender and secret key
			yag = yagmail.SMTP('', '')
			# here you put email address of receiver and the message
			yag.send('', 'Facts about your DOB!',
			         (self.calculate_share + self.zeller_share + gmail_signature))
		except Exception:
			tkinter.messagebox.showerror('error', 'why email nothing? provide input...')

	def tweet(self):
		try:
			twitter_signature = '\n(This tweet was generated using Py3.6)'
			# here you put your access token from Twitter
			access_token = ''
			# here you put your access token secret from Twitter
			access_token_secret = ''
			# here you put your consumer key from Twitter
			consumer_key = ''
			# here you put your consumer secret from Twitter
			consumer_secret = ''

			t = Twitter(auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))
			t.statuses.update(status = (self.calculate_share + self.zeller_share + twitter_signature))
		except Exception:
			tkinter.messagebox.showerror('error', 'why tweet nothing? provide input..')

''' This class helps move the output from the IDE to the GUI window '''

class TextRedirector(object):
	def __init__(self, widget, tag = "stdout"):
		self.widget = widget
		self.tag = tag

	def write(self, str):
		self.widget.configure(state = "normal")
		self.widget.insert("end", str, self.tag)
		self.widget.configure(state = "disabled")


def main():
	app = AgeCalculator()
	app.geometry("1000x558") # location: +120+140
	app.resizable(width = False, height = False)
	app.mainloop()

if __name__ == "__main__":
	main()
