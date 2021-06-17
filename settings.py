from json import load, dump

class Settings:

	def __init__(self):

		#App Conf
		self.title = 'Pajak Bumi dan Bangunan'

		#Window Conf
		base = 50
		ratio = (16,9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]
		self.screen = f'{self.width}x{self.height}+500+500'

		#PBB

		self.harga_tanah = 200000
		self.harga_bangunan = 400000
		self.tarifPBB = 1000
		self.NJOPTKP = 10000000

		#Img Conf
		self.logo = 'logo.png'
		self.image = 'image.png'

		self.data_base = None
		self.users     = None
		self.load_data_from_json()

	def load_data_from_json(self):
		with open('data/data.json', 'r') as file_json:
			self.data_base = load(file_json)

		with open('data/users.json', 'r') as user:
			self.users = load(user)

	def save_data_to_json(self):
		with open('data/data.json', 'w') as file_json:
			dump(self.data_base, file_json)

	def saveSignUp(self):
		with open('data/users.json', 'w') as user:
			dump(self.users, user)