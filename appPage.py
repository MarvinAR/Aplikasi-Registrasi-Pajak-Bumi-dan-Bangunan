import tkinter as tk
from PIL import Image, ImageTk
from time import strftime
from datetime import datetime
import requests
from json import load, dump

from tkinter import messagebox

class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_data = self.settings.data_base[0]
		self.last_current_data_index = 0
		self.update_mode = False
		self.add_mode = False
		self.data_index = []
		self.status = False

		self.bg = "#121212"
		self.fg = "#f1ec40"
		self.app_logo = self.settings.logo

		super().__init__(parent) # window.conteiner
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_right_frame()

	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg=self.bg)
		self.left_frame.grid(row=0, column=0, sticky="nsew")
		self.create_left_header()
		self.create_left_footer()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg=self.bg, width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")
		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_left_right_frame(self):
		self.grid_columnconfigure(0, weight=1) # 1/3
		self.grid_columnconfigure(1, weight=2) # 2/3
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg=self.bg)
		self.left_header.pack()

		image = Image.open(self.app_logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio),int(i_h/ratio)) #(x,y)
		image = image.resize(new_size)
		self.app_logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.app_logo, bg = self.bg)
		self.label_logo.pack()

		self.searchbox_frame = tk.Frame(self.left_header, bg="white", width=frame_w, height=frame_h//4)
		self.searchbox_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.searchbox_frame, bg="white", fg=self.bg, font=("Arial", 14), textvariable = self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.searchbox_frame, bg='white', fg='black', font=("Arial", 9), text="Find", bd = 0, width = 6, command = self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.searchbox_frame.grid_columnconfigure(0, weight=3) # 3/4
		self.searchbox_frame.grid_columnconfigure(1, weight=1) # 1/4

	def show_current_data_index_in_listbox(self):
		self.data_base_listBox.delete(0, 'end')
		data = self.settings.data_base
		for index in self.data_index:
			datum = data[index]
			for key, value in datum.items():
				full_name = f"{value['f_name']} {value['l_name']}"
				self.data_base_listBox.insert('end', full_name)

	def show_all_data_in_listbox(self):
		self.data_base_listBox.delete(0, 'end')
		data = self.settings.data_base
		self.data_index = []
		index_counter = 0
		for datum in data:
			self.data_index.append(index_counter)
			index_counter += 1

		for index in self.data_index:
			datum = data[index]
			for key, value in datum.items():
				full_name = f"{value['f_name']} {value['l_name']}"
				self.data_base_listBox.insert("end", full_name)

	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 3*self.settings.height//5

		self.left_content = tk.Frame(self.left_footer, width=frame_w, height=frame_h, bg=self.fg)
		self.left_content.pack(fill="x")

		self.data_base_listBox = tk.Listbox(self.left_content, bg=self.bg, fg=self.fg, font=("Arial", 12), height=frame_h)
		self.data_base_listBox.pack(side="left", fill="both", expand=True)

		self.data_base_scroll = tk.Scrollbar(self.left_content)
		self.data_base_scroll.pack(side="right", fill="y")

		self.show_all_data_in_listbox()

		self.data_base_listBox.configure(yscrollcommand=self.data_base_scroll.set)
		self.data_base_scroll.configure(command=self.data_base_listBox.yview)

		self.data_base_listBox.bind("<<ListboxSelect>>", self.clicked_item_in_Listbox)

	def create_left_footer(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5

		self.left_footer = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg=self.bg)
		self.left_footer.pack(fill = 'x', expand = True)
  
		self.lbl = tk.Label(self.left_footer, font = ('calibri', 20, 'bold'), background = self.bg,foreground = self.fg)
		self.lbl.pack(anchor = 'center')
		self.time()


	def time(self):
		string = strftime('%H:%M:%S')
		self.lbl.config(text = string)
		self.lbl.after(1000, self.time)

	def clicked_item_in_Listbox(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try:
				index_listbox = selection[0]
			except IndexError:
				index_listbox = self.last_current_data_index
			index = self.data_index[index_listbox]
			self.last_current_data_index = index
			self.current_data = self.settings.data_base[index]

			for phoneNumber, info in self.current_data.items():
				phone = phoneNumber
				full_name = info['f_name'] + ' ' + info['l_name']
				address = info['address']
				luas_tanah = info['luas_tanah']
				luas_bangunan = info['luas_bangunan']

			self.full_name_label.configure(text=full_name)
			self.table_info[0][1].configure(text=phone)
			self.table_info[1][1].configure(text=address)
			self.table_info[2][1].configure(text=str(luas_tanah) + ' m²')
			self.table_info[3][1].configure(text=str(luas_bangunan) + ' m²')
			self.table_info[4][1].configure(text='Rp ' + str('{:,}'.format(self.hitung_pbb(phoneNumber, info))) + ',-')
			self.table_info[5][1].configure(text='$ ' + str(f'{self.convert_idr_to_usd(self.hitung_pbb(phoneNumber, info)):.2f}'))


	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg=self.fg)
		self.right_header.pack()
		self.create_detail_right_header()

	def create_detail_right_header(self):

		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg=self.fg)
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data = list(self.current_data.values())[0]
		full_name = f"{data['f_name']} {data['l_name']}"

		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.full_name_label = tk.Label(self.detail_header, text=full_name, font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg=self.bg, fg = self.fg)
		self.full_name_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg=self.bg)
		self.right_content.pack(expand=True)
		self.create_detail_right_content()


	def create_detail_right_content(self):

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg=self.bg)
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for phoneNumber, info in self.current_data.items():		

			self.info = [
				['Telepon :', phoneNumber],
				['Alamat :', info['address']],
				['Luas Tanah :', str(info['luas_tanah']) + ' m²'],
				['Luas Bangunan :', str(info['luas_bangunan']) + ' m²'],
				['Pajak Terutang (IDR):', 'Rp ' + str('{:,}'.format(self.hitung_pbb(phoneNumber, info))) + ',-'],
				['Pajak Terutang (USD):', '$ ' + str(f'{self.convert_idr_to_usd(self.hitung_pbb(phoneNumber, info)):.2f}')]
			]

		self.table_info = []

		rows , columns = len(self.info), len(self.info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				self.label = tk.Label(self.detail_content, text=self.info[row][column], font=("Arial", 12, 'bold'), bg=self.bg, fg = self.fg)
				aRow.append(self.label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				self.label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)
			
		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg=self.bg)
		self.right_footer.pack()
		self.create_detail_right_footer()

	def create_detail_right_footer(self):

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg=self.bg)
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete']
		commands = [self.clicked_update_btn, self.clicked_delete_btn]
		self.buttons_features = []

		for feature in features:
			self.button = tk.Button(self.detail_footer, text=feature, bg=self.bg, fg=self.fg, font=("Arial", 12, "bold"), bd=0)
			self.button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(self.button)

		self.buttons_features[0].configure(command=commands[0])
		self.buttons_features[1].configure(command=commands[1])

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def recreate_right_frame_and_listbox(self):
		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()

		#ListBox
		self.data_base_listBox.delete(0, 'end')
		self.show_all_data_in_listbox()

	def clicked_update_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg=self.bg)
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for phoneNumber, info in self.current_data.items():
			info = [
				['Nama Depan :', info['f_name']],
				['Nama Belakang :', info['l_name']],
				['Telepon :', phoneNumber],
				['Alamat :', info['address']],
				['Luas Tanah :', info['luas_tanah']],
				['Luas Bangunan :', info['luas_bangunan']]
			]

		self.table_info = []
		self.entry_update_data_vars = []
		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					self.label2 = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg=self.bg, fg=self.fg)
					aRow.append(self.label2)
					sticky = "e"
					self.label2.grid(row=row, column=column, sticky=sticky)
				else:
					entryVar = tk.StringVar()
					self.entry = tk.Entry(self.detail_update_content,font=("Arial", 12), bg=self.bg, fg=self.fg, textvariable=entryVar, insertbackground=self.fg)
					self.entry.insert(0, info[row][column])
					self.entry_update_data_vars.append(entryVar)
					aRow.append(self.entry)
					sticky = "w"
					self.entry.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)


		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg=self.bg)
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_btn, self.clicked_cancel_btn]
		self.buttons_features = []

		for feature in features:
			index = features.index(feature)
			self.button2 = tk.Button(self.detail_update_footer, text=feature, bg=self.bg, fg=self.fg, font=("Arial", 12, "bold"), bd=0, command=commands[index])
			self.button2.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(self.button2)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def clicked_delete_btn(self):
		confirm = messagebox.askyesnocancel("PROPERTY TAX", "ARE YOU SURE TO DELETE THIS CLIENT'S DATA ?")

		if confirm:
			#print(self.current_contact)
			index = self.settings.data_base.index(self.current_data)
			del self.settings.data_base[index]
			self.settings.save_data_to_json()

			self.last_current_data_index = 0
			self.full_name_label.configure(text=list(self.settings.data_base[0].values())[0]['f_name'] + ' ' + list(self.settings.data_base[0].values())[0]['l_name'])
			for phoneNumber, info in self.settings.data_base[0].items():
				phone = phoneNumber
				full_name = info['f_name'] + ' ' + info['l_name']
				address = info['address']
				luas_tanah = info['luas_tanah']
				luas_bangunan = info['luas_bangunan']

			self.table_info[0][1].configure(text=phone)
			self.table_info[1][1].configure(text=address)
			self.table_info[2][1].configure(text=str(luas_tanah) + ' m²')
			self.table_info[3][1].configure(text=str(luas_bangunan) + ' m²')
			self.table_info[4][1].configure(text='Rp ' + str(self.hitung_pbb(phoneNumber, info)) + ',-')
			self.table_info[5][1].configure(text='$ ' + str(f'{self.convert_idr_to_usd(self.hitung_pbb(phoneNumber, info)):.2f}'))

		self.show_all_data_in_listbox()


	def clicked_add_new_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content.destroy()
		self.detail_footer.destroy()
		self.full_name_label.config(text = 'New Register')

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg=self.bg)
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for phoneNumber, info in self.current_data.items():
			info = [
				["Nama Depan :", info['f_name']],
				["Nama Belakang :", info["l_name"]],
				['Telepon :', phoneNumber],
				['Alamat :', info['address']],
				['Luas Tanah :', info['luas_tanah']],
				['Luas Bangunan :', info['luas_bangunan']]
			]

		self.table_info = []
		self.entry_update_data_vars = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					self.label3 = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg=self.bg, fg=self.fg)
					aRow.append(self.label3)
					sticky = "e"
					self.label3.grid(row=row, column=column, sticky=sticky)
				else:
					entryVar = tk.StringVar()
					self.entry2 = tk.Entry(self.detail_update_content, font = ("Arial", 12), bg = self.bg,fg=self.fg,  textvariable = entryVar, insertbackground = self.fg)
					self.entry_update_data_vars.append(entryVar)
					aRow.append(self.entry2)
					sticky = "w"
					self.entry2.grid(row = row, column = column, sticky = sticky)
					
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		#CONFIGURE FOOTER

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg=self.bg)
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ["Save", "Cancel"]
		commands = [self.save_add_new, self.clicked_cancel_btn]

		self.buttons_features = []

		for feature in features:
			index = features.index(feature)
			self.button3 = tk.Button(self.detail_update_footer, text=feature, bg=self.bg, fg=self.fg, font=("Arial", 12, "bold"), bd=0, command = commands[index])
			self.button3.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(self.button3)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def save_add_new(self):
		self.update_mode = False

		# ADDING TO DICT

		confirm = messagebox.askyesnocancel("PROPERTY TAX", "ARE YOU SURE TO ADD THIS CONTACT ?")

		if confirm:

			data = {
					self.entry_update_data_vars[2].get() : {
						"f_name" : self.entry_update_data_vars[0].get(),
						"l_name" : self.entry_update_data_vars[1].get(),
						"address" : self.entry_update_data_vars[3].get(),
						"luas_tanah" : int(self.entry_update_data_vars[4].get()),
						"luas_bangunan" : int(self.entry_update_data_vars[5].get())
					}
				}

			self.settings.data_base.append(data)
			self.settings.save_data_to_json()
			self.current_data = self.settings.data_base[self.last_current_data_index]

			self.recreate_right_frame_and_listbox()

	def clicked_save_btn(self):
		self.update_mode = False

		confirm = messagebox.askyesnocancel('PAJAK CONFIRMATION', 'ARE YOU SURE TO UPDATE THIS DATA ?')
		if confirm:

			f_name = self.entry_update_data_vars[0].get()
			l_name = self.entry_update_data_vars[1].get()
			phone = self.entry_update_data_vars[2].get()
			address = self.entry_update_data_vars[3].get()
			luas_tanah = int(self.entry_update_data_vars[4].get())
			luas_bangunan = int(self.entry_update_data_vars[5].get())
			self.settings.data_base[self.last_current_data_index] = {
				phone : {
					'f_name' : f_name,
					'l_name' : l_name,
					'phone' : phone,
					'address' : address,
					'luas_tanah' : luas_tanah,
					'luas_bangunan' : luas_bangunan
				}
			}
			self.settings.save_data_to_json()
			self.current_data = self.settings.data_base[self.last_current_data_index]

		self.recreate_right_frame_and_listbox()

	def clicked_cancel_btn(self):
		self.update_mode = False

		self.recreate_right_frame_and_listbox()

	def clicked_search_btn(self):
		item_search = self.entry_search_var.get()
		data = self.settings.data_base

		self.data_index = []
		index_counter = 0

		if item_search:
			for datum in data:
				for phoneNumber, info in datum.items():
					if item_search in phoneNumber:
						self.data_index.append(index_counter)
					elif item_search in info['f_name']:
						self.data_index.append(index_counter)
					elif item_search in info['l_name']:
						self.data_index.append(index_counter)
					index_counter += 1
			self.show_current_data_index_in_listbox()

		else:
			self.show_all_data_in_listbox()

	def hitung_pbb(self, phoneNumber, info):
		self.pajakTerutang = (((info['luas_tanah']*self.settings.harga_tanah) + (info['luas_bangunan']*self.settings.harga_bangunan)) - self.settings.NJOPTKP) // self.settings.tarifPBB

		return self.pajakTerutang

	def convert_idr_to_usd(self, idr):
		api_key = '349d040adbeebd3df9a997a5cf508618'
		base = 'EUR'
		symbols = 'IDR, USD'
		api_endpoint = f'http://data.fixer.io/api/latest?access_key={api_key}&base={base}&symbols={symbols}'
		#print(datetime.now().hour)
		if str(datetime.now().hour) == '12' and str(datetime.now().minute) == '00' and str(datetime.now().second) == '00':
			self.res = requests.get(api_endpoint).json()
			self.ratio = [self.res['rates']["IDR"], self.res['rates']["USD"]]
			print(self.ratio)
			self.save_ratio_to_json()
		else:
			self.load_ratio_from_json()

		rate01 = self.ratio[0]
		rate02 = self.ratio[1]
		rateResult = rate02/rate01 # askedValue / knownValue
		self.USDTotal = rateResult*idr

		return self.USDTotal

	def load_ratio_from_json(self):
		with open('data/currency.json', 'r') as f:
			self.ratio = load(f)

	def save_ratio_to_json(self):
		with open('data/currency.json', 'w') as f:
			dump(self.ratio, f)