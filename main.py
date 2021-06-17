import tkinter as tk
import random
import string

from settings import Settings
from appPage import AppPage
from tkinter import messagebox as msg
from PIL import Image, ImageTk
from tkinter import simpledialog

class Window(tk.Tk):

	def __init__(self, App):
		self.app = App
		self.settings = App.settings

		super().__init__()
		self.title(self.settings.title)
		self.geometry(self.settings.screen)
		self.resizable(0,0)

		self.create_container()

		self.pages = {}
		self.create_appPage()
		self.create_loginPage()

	def create_menu(self):
		self.menu_bar = tk.Menu(self)
		self.config(menu=self.menu_bar)
										# ilangi ----
		label_menu_file = tk.Menu(self.menu_bar, tearoff=0)
		label_menu_file.add_command(label='Register', command=lambda:self.register("P"), accelerator="Ctrl+R")
		label_menu_file.add_command(label='Close', command=lambda:self.close("A"), accelerator="Ctrl+Q")

		self.bind_all("<Control-r>", self.register)
		self.bind_all("<Control-q>", self.close)

		#menampilkan menu bar seperti fungsi grid/pack
		self.menu_bar.add_cascade(label='File', menu=label_menu_file)

		label_about_menu = tk.Menu(self.menu_bar, tearoff=0)
		label_about_menu.add_command(label='About', command=lambda:self.about("A"), accelerator="Alt+A")

		self.bind_all("<Alt-a>", self.about)

		self.menu_bar.add_cascade(label='About', menu=label_about_menu)

		label_menu_theme = tk.Menu(self.menu_bar, tearoff=0)
		label_menu_theme.add_command(label='Dark Mode', command=lambda:self.dark("D"), accelerator="Ctrl+Shift+D")
		label_menu_theme.add_command(label='Light Mode', command=lambda:self.light("L"), accelerator="Ctrl+Shift+U")


		self.bind_all("<Control-D>", self.dark)
		self.bind_all("<Control-U>", self.light)

		self.menu_bar.add_cascade(label='Theme', menu=label_menu_theme)




	def register(self, event):
		self.pages['appPage'].clicked_add_new_btn()

	def close(self, event):
		quit()

	def about(self, event):
		msg.showinfo('About Us', 'Developed by Marvin AR and Luigi E \nAntah Berantah \nContact : -1 - 2345 - 6789 \nSince June 2021 \n©Claim 2021 Project. All rights reserved.')

	def dark(self, event):
		self.pages['appPage'].bg = "#121212"
		self.pages['appPage'].fg = "#f1ec40"
		self.pages['appPage'].app_logo = self.settings.logo

		self.recreate()

	def light(self, event):
		self.pages['appPage'].bg = "#ededed"
		self.pages['appPage'].fg = "#0e13bf"
		self.pages['appPage'].app_logo = self.settings.image

		self.recreate()

	def recreate(self):
		self.pages['appPage'].left_frame.destroy()
		self.pages['appPage'].right_frame.destroy()

		self.pages['appPage'].create_left_frame()
		self.pages['appPage'].create_right_frame()
		
	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill='both', expand=True)

	def create_appPage(self):
		self.pages['appPage'] = AppPage(self.container, self.app)

	def create_loginPage(self):
		self.pages['loginPage'] = Login(self.container, self.app)

class ContactApp:

	def __init__(self):
		self.settings = Settings()
		self.window = Window(self)

	def run(self):
		self.window.mainloop()

class Login(tk.Frame):

	def __init__(self, parent, App):

		self.app = App
		self.settings = App.settings

		background_color = "black"
		fg_color         = "yellow"
		font_page        = ("Arial", 24, "bold")
		font_content     = ("Arial", 14, "bold")

		super().__init__(parent)
		self.configure(bg="black", width=300, height=400)
		# self.pack(fill="both", expand=True)
		self.grid(row=0, column=0, sticky="nsew")

		self.frame01 = tk.Frame(self, bg=background_color,height=self.settings.height, width=self.settings.width)
		self.frame01.pack(fill="both", expand=True)

		self.textTitle = tk.Label(self.frame01, text="Application Login Page", font=font_page, bg=background_color, fg = fg_color)
		self.textTitle.pack(pady = 15)

		self.nameLabel = tk.Label(self.frame01, text="Username :", font=font_content, bg=background_color, fg = fg_color)
		self.nameLabel.pack()

		self.nameVar = tk.StringVar()
		self.nameEntry = tk.Entry(self.frame01, bg=background_color, font=font_content, textvariable=self.nameVar, fg = fg_color, insertbackground = fg_color)
		self.nameEntry.pack(pady = 15)
		

		self.passwordLabel = tk.Label(self.frame01, text="Password :", font=font_content, bg=background_color, fg = fg_color)
		self.passwordLabel.pack(pady = 15)

		self.passwordVar = tk.StringVar()
		self.passwordEntry = tk.Entry(self.frame01, bg=background_color, font=font_content, show="*", textvariable=self.passwordVar, fg = fg_color, insertbackground = fg_color)
		self.passwordEntry.pack()

		self.right_footer = tk.Frame(self, width=self.settings.width, height=self.settings.height, bg=background_color)
		self.right_footer.pack(pady = 15)

		self.detail_footer = tk.Frame(self.right_footer, width=self.settings.width, height=self.settings.height, bg=background_color)
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		self.button_login = tk.Button(self.detail_footer, text="Log In", command=self.change_to_appPage, bg=background_color, font=font_content, bd = 0, fg = fg_color)
		self.button_login.grid(row = 0, column = 0, padx = 10)

		self.button_login = tk.Button(self.detail_footer, text="Sign Up", command=self.sign_up, bg=background_color, font=font_content, bd = 0, fg = fg_color)
		self.button_login.grid(row = 0, column = 1, padx = 10)

	def change_to_appPage(self):

		username = self.nameVar.get()
		password = self.passwordVar.get()

		match = username in self.settings.users and password == self.settings.users[username] 
		if match:

			self.app.window.create_menu()

			page = self.app.window.pages['appPage']
			page.tkraise()

	def sign_up(self):
		username = self.nameVar.get()
		password = self.passwordVar.get()

		if len(username) > 2 and len(password) > 4:
			if username not in self.settings.users:

				alphabet = string.ascii_uppercase
				alpha_numeric = string.digits

				A = random.choice(alphabet)
				B = random.choice(alpha_numeric)
				C = random.choice(alphabet)
				D = random.choice(alpha_numeric)
				E = random.choice(alphabet)
				F = random.choice(alpha_numeric)

				CODE = f"{A}{B}{C}{D}{E}{F}"
				print(CODE)

				auth_code = simpledialog.askstring(title = "Authentication", prompt = "Input the code you're getting in the command prompt")
				if auth_code == CODE:
					confirm = msg.askyesnocancel("ADDING YOUR DATA", "Are You Sure To Add This User ?")

					if confirm:
						self.settings.users[username] = password
						self.settings.saveSignUp()
				else:
					msg.showwarning("FAILED ENTERING YOUR DATA", "THE CODE IS WRONG")
			else:
				msg.showwarning("FAILED ENTERING YOUR USERNAME", "Your Username is Already Taken")
		else:
			msg.showwarning("FAILED ENTERING YOUR DATA", "Username and Password should contain at least 3 and 5 letters")



if __name__ == '__main__':
	MyContactApp = ContactApp()
	MyContactApp.run()
